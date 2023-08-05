import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from distutils.version import StrictVersion
from enum import Enum, unique
from pathlib import Path
from typing import List, Optional, Tuple, Type, Union
from uuid import UUID

import click_spinner
from ereuse_utils import cli
from ereuse_utils.cli import Line
from ereuse_utils.session import DevicehubClient

from ereuse_workbench.benchmark import Benchmark, BenchmarkProcessorSysbench
from ereuse_workbench.computer import Component, Computer, DataStorage
from ereuse_workbench.erase import CannotErase, Erase, EraseType
from ereuse_workbench.install import CannotInstall
from ereuse_workbench.test import Test, TestDataStorage, TestDataStorageLength
from ereuse_workbench.utils import Dumpeable, Severity


@unique
class SnapshotSoftware(Enum):
    """The algorithm_software used to perform the Snapshot."""
    Workbench = 'Workbench'
    AndroidApp = 'AndroidApp'
    Web = 'Web'
    DesktopApp = 'DesktopApp'


class Snapshot(Dumpeable):
    """
    Generates the Snapshot report for Devicehub by obtaining the
    data from the computer, performing benchmarks and tests...

    After instantiating the class, run :meth:`.computer` before any
    other method.
    """

    def __init__(self,
                 uuid: UUID,
                 software: SnapshotSoftware,
                 version: StrictVersion,
                 session: Optional[DevicehubClient] = None) -> None:
        self.type = 'Snapshot'
        self._init_time = datetime.now(timezone.utc)
        self.uuid = uuid
        self.software = software
        self.version = version
        self.closed = False
        self.endTime = datetime.now(timezone.utc)
        self.elapsed = None
        self.device = None  # type: Computer
        self.components = None  # type: List[Component]
        self._storages = None
        self._session = session

    def computer(self):
        """Retrieves information about the computer and components."""
        print(cli.title('Retrieve computer information'), end='')
        with click_spinner.spinner():
            self.device, self.components = Computer.run()
            self._storages = tuple(c for c in self.components if isinstance(c, DataStorage))
            if self._session:
                self._session.post('/snapshots/', self, uri=self.uuid, status=204)
        # Submit
        print(self.device)

    def benchmarks(self):
        """Perform several benchmarks to the computer and its components."""
        benchmarks = []  # type: List[Tuple[Optional[int], Benchmark]]
        for i, component in enumerate(self.components):
            for benchmark in component.benchmarks():
                benchmarks.append((i, benchmark))
        for benchmark in self.device.benchmarks():
            benchmarks.append((None, benchmark))

        t = cli.title('Bennchmark')
        with Line(iterable=benchmarks, total=len(benchmarks), desc=t) as line:
            for i, benchmark in line:
                benchmark.run()
                self._submit_event(benchmark, i)

            # Print CPU Sysbench Benchmark
            try:
                b = next(b[1] for b in benchmarks if isinstance(b[1], BenchmarkProcessorSysbench))
                line.close_message(t, 'CPU {}'.format(b))
            except StopIteration:
                line.close_message(t, cli.done())

    def test_stress(self, minutes):
        """Performs a stress test."""
        test = self.device.test_stress(minutes)
        self._submit_event(test)

    def storage(self,
                smart: TestDataStorageLength = None,
                erase: EraseType = None,
                erase_steps: int = None,
                zeros: bool = None,
                install=None):
        if not self._storages:
            cli.warning('No data storage units.')
            return

        total = len(self._storages)
        lines = total * (bool(smart) + bool(erase) + bool(install))
        with Line.reserve_lines(lines), ThreadPoolExecutor() as executor:
            for storage in self._storages:
                executor.submit(self._storage, total, storage, smart, erase, erase_steps,
                                zeros, install)

    def _storage(self,
                 total: int,
                 storage: DataStorage,
                 smart: Optional[TestDataStorageLength],
                 erase: Optional[EraseType],
                 erase_steps: Optional[int],
                 zeros: Optional[bool],
                 install_path: Optional[Path]):
        i = self.components.index(storage)
        logging.info('Process storage %s (%s) with %s %s %s %s %s',
                     i, storage, smart, erase, erase_steps, zeros, install_path)
        if smart:
            t = cli.title('{} {}'.format('SMART test', storage))
            with Line(total=100, desc=t, position=i) as line:
                logging.debug('Snapshot: Install storage %s (%s)', i, storage)
                test = storage.test_smart(smart, self._progress_factory(line, i, TestDataStorage))
                if test.severity == Severity.Error:
                    line.close_message(t, cli.danger('failed; {}'.format(test.status)))
                else:
                    line.close_message(t, cli.done())
            self._submit_event(test, i)
        if erase:
            pos = total * bool(smart) + i
            t = cli.title('{} {}'.format('Erase', storage))
            with Line(total=(erase_steps + int(zeros)) * 100, desc=t, position=pos) as line:
                try:
                    erasure = storage.erase(erase, erase_steps, zeros,
                                            self._progress_factory(line, i, Erase))
                except CannotErase as e:
                    line.close_message(t, cli.danger(e))
                else:
                    line.close_message(t, cli.done())
                    self._submit_event(erasure, i)
        if install_path:
            pos = total * (bool(smart) + bool(erase)) + i
            t = cli.title('{} {}'.format('Install OS', storage))
            with Line(position=pos) as line:
                line.spin(t)
                try:
                    install = storage.install(install_path)
                except CannotInstall as e:
                    line.close_message(t, e)
                else:
                    line.close_message(t, cli.done())
                    self._submit_event(install, i)

    def _submit_event(self, event: Union[Test, Benchmark, Erase], component: int = None):
        if not self._session:
            return
        base = '/snapshots/{}/'.format(self.uuid)
        uri = 'components/{}/event/'.format(component) if component else 'device/event/'
        self._session.post(base, event, uri=uri, status=204)

    def close(self):
        self.closed = True
        self.elapsed = datetime.now(timezone.utc) - self._init_time
        if self._session:
            self._session.patch('/snapshots/', self, self.uuid, status=204)

    def _progress_factory(self, line: Line, component: int, event: Union[Type[Test], Type[Erase]]):
        def _update_line(increment):
            logging.debug('Incr c %s of %s for %s. n is %s', component, increment, event, line.n)
            line.update(increment)

        return _update_line
