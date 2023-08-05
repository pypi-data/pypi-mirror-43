from unittest.mock import MagicMock

import pytest

from ereuse_workbench.computer import Computer, DataStorage, GraphicCard, NetworkAdapter, \
    Processor, RamModule
from tests import conftest
from tests.assertions import has_ram
from tests.conftest import computer

"""
Tests computers that broke the Workbench at one point in time.

These tests use the output of LSHW from those computers.

[1]: http://eu.crucial.com/eur/en/support-memory-speeds-compatibility
"""


# todo wireless NetworkAdaptors don't have speed (ex. 54Mbps)

@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_box_xavier(lshw: MagicMock):
    computer(lshw, 'box-xavier')


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_eee_pc(lshw: MagicMock):
    pc, components = computer(lshw, 'eee-pc')
    assert len(components['Processor']) == 1
    assert has_ram(components)
    assert pc.model == '1000H', 'Model has noise enclosed between parenthesis'
    assert pc.serial_number == '8BOAAQ191999'
    assert pc.chassis == 'Netbook'
    assert isinstance(pc, Computer)
    assert len(components['GraphicCard']) == 1
    eth, wifi = components[NetworkAdapter.__name__]
    assert not eth.wireless
    assert wifi.wireless
    # todo assert components == jsonf('eee-pc-components-output')


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_lenovo(lshw: MagicMock):
    pc, components = computer(lshw, 'lenovo')
    assert len(components['Processor']) == 1
    assert has_ram(components), 'Computer without RAM'


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_pc_laudem(lshw: MagicMock):
    # todo fix
    pc, components = computer(lshw, 'pc-laudem')
    assert len(components['Processor']) == 1
    assert has_ram(components), 'Computer without RAM'
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_virtualbox_client(lshw: MagicMock):
    """
    Tests a virtualized computer.

    Virtualized computers return much lesser information as they cannot
    directly access directly the hardware of the host machine.
    """
    pc, components = computer(lshw, 'virtualbox-client')


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_xeon(lshw: MagicMock):
    pc, components = computer(lshw, 'xeon')
    assert 'HardDrive' not in components
    assert has_ram(components), 'Computer without RAM'
    assert len(components['GraphicCard']) == 2
    ram0, ram1 = components['GraphicCard']
    assert ram0.serial_number is ram1.serial_number is None
    assert ram0.model == 'GT200GL Quadro FX 3800'
    assert ram1.model == 'GF100GL Quadro 4000'
    assert ram0.manufacturer == ram1.manufacturer == 'NVIDIA Corporation'


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_xiaomi(lshw: MagicMock):
    pc, components = computer(lshw, 'xiaomi')
    assert len(components['Processor']) == 1
    assert has_ram(components), 'Computer without RAM'
    assert len(components['GraphicCard']) == 2
    ram0, ram1 = components['GraphicCard']
    assert ram0.model == 'Sky Lake Integrated Graphics'
    assert ram0.serial_number is None
    assert ram0.manufacturer == 'Intel Corporation'
    assert ram1.model == 'NVIDIA Corporation'
    assert ram1.serial_number is None
    assert ram1.manufacturer == 'NVIDIA Corporation'
    # todo pc has ethernet capabilities through USB3 type C
    # how do we reflect this?
    wifi = components[NetworkAdapter.__name__][0]
    assert wifi.wireless
    # todo data storage is not detected! (Pci express data storage)


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_dell(lshw: MagicMock):
    pc, components = computer(lshw, 'dell-logicalname-network')
    assert len(components['Processor']) == 1
    assert has_ram(components), 'Computer without RAM'
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_hp_dc7900(lshw: MagicMock):
    """Tests an HP DC 7900 with an erased HDD following HMG IS5."""
    # todo check totalSlots and usedSlots
    pc, components = computer(lshw, 'erased-i5.lshw')
    assert len(components['Processor']) == 1
    assert pc.type == 'Desktop'
    assert has_ram(components), 'Computer without RAM'
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_virtualbox_without_hdd_and_with_usb(lshw: MagicMock):
    """
    Tests that a Virtualbox with an USB plugged-in doesn't provide
    more information (like the USB or an extra hard-drive),
    and tests a system without hard-drive.

    In some computers it was detected that this behaviour it was
    triggered if there was no hard-drive.
    """
    _, components = computer(lshw, 'virtualbox-no-hdd')
    assert 'HardDrive' not in components and 'SolidStateDrive' not in components
    _, components = computer(lshw, 'virtualbox-no-hdd-yes-usb')
    assert 'HardDrive' not in components and 'SolidStateDrive' not in components


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_nec(lshw: MagicMock):
    """
    Tests a NEC computer.

    See `issue
    <https://tree.taiga.io/project/ereuseorg-workbench/issue/55>`_ for
    computer information.
    """
    pc, components = computer(lshw, 'nec.lshw')
    assert len(components['Processor']) == 1
    # todo fails: assert pc.serial_number == '210623170008'
    # todo fails: assert pc.model == 'DAK-BLU'
    assert len(components['HardDrive']) == 1
    hdd = components['HardDrive'][0]
    assert hdd.serial_number == 'STA2L7MV39LL6D'
    # todo fails: assert hdd.model == 'HDT721032SLA380'
    assert hdd.manufacturer == 'Hitachi'
    assert hdd.size == 305245
    assert len(components['RamModule']) == 2
    # todo the printed model is M378T2863QZS-CE6 or M378T2863QZS (easy to mislead the last part)
    for ram in components['RamModule']:
        assert ram.model == 'M3 78T2863QZS-CE6'
        assert ram.size == 1024
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_hp_compaq_8100(lshw: MagicMock):
    """
    Tests an HP Compaq 8100.

    See `issue
    <https://tree.taiga.io/project/ereuseorg-workbench/issue/54>`_ for
    more info.
    """
    pc, components = computer(lshw, 'hp-compaq-8100.lshw')
    assert pc.serial_number == 'CZC0408YPV'
    assert pc.model == 'HP Compaq 8100 Elite SFF'
    assert pc.manufacturer == 'Hewlett-Packard'
    assert len(components['Processor']) == 1
    assert len(components['HardDrive']) == 1
    hdd = components['HardDrive'][0]
    # todo in picture serialNumber is exactly ``WCAV2U856544``
    assert hdd.serial_number == 'WD-WCAV2U856544'
    assert hdd.size == 305245
    # todo in picture model is exactly ``WD3200AAJS``
    assert hdd.model == 'WDC WD3200AAJS-6'
    assert hdd.manufacturer == 'Western Digital'
    assert len(components['RamModule']) == 4
    for ram in components['RamModule']:
        assert ram.serial_number in {'92072F30', 'A4482E29', '939E2E29', '48FD2E30'}
        assert ram.speed == 1333.0
        assert ram.size == 2048
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_lenovo_7220w3t(lshw: MagicMock):
    pc, components = computer(lshw, 'lenovo-7220w3t.lshw')
    assert pc.manufacturer == 'LENOVO'
    assert pc.serial_number == 'S4R6062'
    assert pc.model == '7220W3T'
    assert len(components['Processor']) == 1
    assert len(components['HardDrive']) == 1
    motherboard = components['Motherboard'][0]
    assert motherboard.serial_number is None
    assert len(components['RamModule']) == 2
    for ram in components['RamModule']:
        assert ram.serial_number is None
        assert ram.model is None
        assert ram.manufacturer is None
        assert ram.size == 2048
        assert ram.speed == 1067.0
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_lenovo_type_as_intel(lshw: MagicMock):
    """
    Tests a lenovo computer whose LSHW output was wrongly taken
    as an Intel and without S/N.
    """
    pc, components = computer(lshw, 'lenovo-as-intel.lshw')
    assert pc.manufacturer == 'LENOVO'
    assert pc.serial_number == 'S4R6460'
    assert pc.model == '7220W3T'
    hdd = components['HardDrive'][0]
    assert hdd.serial_number == 'S1L6J9BZ103714'
    assert hdd.model == 'SAMSUNG HD251HJ'
    # todo model should be HD251HJ and manufacturer Samsung
    # assert hdd.model == 'HD251HJ'
    # assert hdd.manufacturer == 'Samsung'
    assert len(components['RamModule']) == 2
    for ram in components['RamModule']:
        assert ram.serial_number is None
        assert ram.model is None
        # todo why when ram who as empty has a vendor of "48spaces"?
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_asus_all_series(lshw: MagicMock):
    pc, components = computer(lshw, 'asus-all-series.lshw')
    # todo it doesn't work assert pc.serial_number == '104094'
    ram = components['RamModule'][0]
    assert ram.manufacturer == 'Kingston'
    assert ram.model == '9905584-017.A00LF'
    assert ram.serial_number == '9D341297'
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_custom_pc(lshw: MagicMock):
    pc, components = computer(lshw, 'custom.lshw')
    ram = components['RamModule'][0]
    assert ram.manufacturer == 'Kingston'
    assert ram.model == '9905584-017.A00LF'
    assert ram.serial_number == '9D341297'
    assert ram.size == 4096
    assert ram.speed == 1600
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_all_series(lshw: MagicMock):
    pc, components = computer(lshw, 'all-series.lshw')
    assert 'RamModule' in components
    ram = components['RamModule'][0]
    assert ram.manufacturer == 'Kingston'
    assert ram.serial_number == '290E5155'
    assert ram.model == '99U5584-003.A00LF'
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_vostro_260(lshw: MagicMock):
    pc, components = computer(lshw, 'vostro-260.lshw')
    processor = components['Processor'][0]
    assert processor.serial_number is None
    assert processor.model == 'Intel Core i3-2120 CPU @ 3.30GHz'
    assert processor.manufacturer == 'Intel Corp.'
    graphic_card = components['GraphicCard'][0]
    assert graphic_card.serial_number is None
    assert graphic_card.model == '2nd Generation Core Processor Family ' \
                                 'Integrated Graphics Controller'
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_ecs_computers(lshw: MagicMock):
    # Visually checked
    pc, components = computer(lshw, 'ecs-computers.lshw')
    assert len(components['HardDrive']) == 1
    hdd = components['HardDrive'][0]
    assert hdd.serial_number == 'WD-WCC2ETY84203'  # printed sn is 'WCC2ETY84203'
    assert hdd.model == 'WDC WD5000AAKX-6'  # printed sn is 'WD5000AAKX'
    assert hdd.manufacturer == 'Western Digital'  # printed is the logo: 'WD'
    assert len(components['RamModule'])
    ram = components['RamModule'][0]
    assert ram.manufacturer == 'Kingston'
    assert ram.serial_number == '8618F309'  # This is not present in the module
    assert ram.size == 4096
    assert ram.speed == 1600.0
    assert ram.model == '99U5584-003.A00LF'  # Exactly as printed
    assert len(components['SoundCard']) == 1
    sound_card = components['SoundCard'][0]
    assert sound_card.model == '8 Series/C220 Series Chipset ' \
                               'High Definition Audio Controller'
    assert sound_card.serial_number is None
    assert sound_card.manufacturer == 'Intel Corporation'
    assert len(components['Processor']) == 1
    cpu = components['Processor'][0]
    assert cpu.address == 64
    assert cpu.manufacturer == 'Intel Corp.'
    assert cpu.model == 'Intel Core i5-4440 CPU @ 3.10GHz'
    assert cpu.cores == 4
    assert cpu.serial_number is None
    assert cpu.speed == 2.200311
    assert len(components['NetworkAdapter']) == 1
    net = components['NetworkAdapter'][0]
    assert net.manufacturer == 'Realtek Semiconductor Co., Ltd.'
    assert net.model == 'RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller'
    assert net.serial_number == 'e0:3f:49:1a:d0:44'
    assert net.speed == 1000
    assert len(components['Motherboard']) == 1
    mother = components['Motherboard'][0]
    assert mother.serial_number == '131219772601195'  # Found in printed barcode but the
    # text is different
    assert mother.model == 'H81M-K'  # found exactly like this
    assert mother.manufacturer == 'ASUSTeK COMPUTER INC.'  # found as ASUS
    assert mother.slots == 1  # Verified
    # todo assert net['connectors']['usb'] == 6 but only 3 recognized
    assert len(components['GraphicCard']) == 1
    assert components['GraphicCard'][0].manufacturer == 'Intel Corporation'


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_core2(lshw: MagicMock):
    pc, components = computer(lshw, 'core2.lshw')
    assert len(components) == 7
    ram = components['RamModule'][0]
    assert ram.manufacturer is None
    assert ram.serial_number is None
    assert ram.model is None
    assert ram.size == 1024
    assert ram.speed == 667.0
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_ecs2(lshw: MagicMock):
    pc, components = computer(lshw, 'ecs-2.lshw')
    assert len(components['RamModule']) == 3
    for ram in components['RamModule']:
        assert ram.manufacturer is None
        assert ram.serial_number is None
        assert ram.model is None
        assert ram.speed == 533.0
        assert ram.size == 1024
    assert len(components['GraphicCard']) == 1


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_optiplex_745(lshw: MagicMock):
    # Visually checked
    pc, components = computer(lshw, 'optiplex-745.lshw')
    assert pc.model == 'OptiPlex 745'
    assert pc.manufacturer == 'Dell Inc.'
    assert pc.serial_number == 'HQ5583J'  # Checked
    assert len(components['RamModule']) == 2
    ram0, ram1 = components['RamModule']
    # The printed code is HYS64T128020HU-3S-B
    assert ram0.model == ram1.model == '64T128020HU3SB'
    # It doesn't appear printer
    assert ram0.manufacturer == ram1.manufacturer == 'Infineon'
    assert ram0.serial_number == '07129114'
    assert ram1.serial_number == '07127E11'
    assert len(components['HardDrive']) == 1
    hdd = components['HardDrive'][0]
    assert hdd.manufacturer == 'Western Digital'
    assert hdd.model == 'WDC WD3200AAKS-7'  # Printed is WD3200AAKS-75L9A0 (text and barcode)
    assert hdd.serial_number == 'WD-WMAV2W580992'  # As printed (text and barcode)
    assert len(components['GraphicCard']) == 1
    gc = components['GraphicCard'][0]
    assert gc.manufacturer == 'Intel Corporation'
    assert gc.model == '82Q963/Q965 Integrated Graphics Controller'
    assert gc.serial_number is None
    assert len(components['Motherboard']) == 1
    mb = components['Motherboard'][0]
    assert mb.manufacturer == 'Dell Inc.'
    assert mb.serial_number == '..CN137407AJ02SW.'  # Printed is CN-0HP962-13740-7AJ-02SW
    assert mb.model == '0HP962'  # As above


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_optiplex_gx520(lshw: MagicMock):
    pc, components = computer(lshw, 'optiplex-gx520.lshw')
    assert len(components['RamModule']) == 2
    ram0, ram1 = components['RamModule']
    assert ram0.serial_number == '197312A4'  # not printed
    assert ram0.manufacturer == 'Nanya Technology'
    assert ram0.model == 'NT512T64U88A0BY-37'  # Written as NT512T64U88A0BY-37B
    assert ram1.size == ram0.size == 512
    assert ram1.speed == ram0.speed == 533.0
    # This ram1 is exactly the same as ram0...
    assert ram1.serial_number is None
    assert ram1.manufacturer is None
    assert ram1.model is None  # printed is Nanya
    assert len(components['GraphicCard']) == 1
    gc = components['GraphicCard'][0]
    assert gc.manufacturer == 'Intel Corporation'
    assert gc.model == '82945G/GZ Integrated Graphics Controller'
    assert gc.serial_number is None
    assert len(components['HardDrive']) == 1
    hdd = components['HardDrive'][0]
    assert hdd.serial_number == '5LR30DTZ'  # checked on print ok
    assert hdd.model == 'ST3808110AS'  # checked on print ok
    assert hdd.manufacturer == 'Seagate'  # checked on print ok


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_hp_pavilion_dv4000(lshw: MagicMock):
    pc, components = computer(lshw, 'hp-pavilion-dv4000.lshw')
    assert pc.type == 'Laptop'
    wifi, ethernet = components[NetworkAdapter.__name__]
    assert wifi.wireless
    assert not ethernet.wireless


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_nox(lshw: MagicMock):
    pc, components = computer(lshw, 'nox.lshw')
    ram = components['RamModule'][0]
    assert ram.model == '9905403-038.A00LF'
    assert ram.serial_number == '8F17943'
    assert ram.size == 4096
    assert ram.speed == 1333.0  # checked
    assert ram.manufacturer == 'Kingston'  # checked
    assert ram.interface == 'DDR3'  # checked
    assert ram.format == 'DIMM'  # checked
    hdd = components['HardDrive'][0]
    assert hdd.model == 'ST3500413AS'  # checked
    assert hdd.serial_number == 'Z2A3HR7N'  # checked
    assert hdd.manufacturer == 'Seagate'  # checked
    assert hdd.size == 476940  # print shows 500GB
    motherboard = components['Motherboard'][0]
    assert motherboard.serial_number == '109192430003459'
    assert motherboard.model == 'P8H61-M LE'  # checked
    assert motherboard.manufacturer == 'ASUSTeK Computer INC.'  # print shows asus


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_lenovo_thinkcentre_edge(lshw: MagicMock):
    # serial number motherboard that doesnt recognize: 11S0B39930ZVQ27W2AT2VS 210
    pc, components = computer(lshw, 'lenovo-thinkcentre-edge.lshw')
    motherboard = components['Motherboard'][0]
    ram = components['RamModule'][0]  # type: RamModule
    assert ram.size == 2048
    assert ram.serial_number == '292E48DA'  # no printed
    assert ram.model == '16JTF25664AZ-1G4F1'  # printed one starts with 'MT'...
    assert ram.manufacturer == 'Micron'  # checked on print ok
    assert ram.interface == 'DDR3'
    assert ram.speed == 1333.0  # printed pc3-1600 (check [1] at the beginning of file)
    hdd = components['HardDrive'][0]
    assert isinstance(hdd, DataStorage)
    assert hdd.serial_number == 'Z2AYPLNP'  # checked on print ok
    assert hdd.model == 'ST250DM000-1BD14'  # printed one doesn't have the '-1BD14'
    assert hdd.size == 238475  # disk capacity is 250GB
    assert components['GraphicCard'][0].model == '2nd Generation Core Processor ' \
                                                 'Family Integrated Graphics Controller'
    assert len(components['GraphicCard']) == 1
    assert len(components['Processor']) == 1
    assert len(components['Processor']) == 1
    cpu = components['Processor'][0]
    assert isinstance(cpu, Processor)
    assert cpu.address == 64
    assert cpu.cores == 2
    assert cpu.threads == 2
    assert cpu.manufacturer == 'Intel Corp.'
    assert cpu.serial_number is None
    assert cpu.speed == 1.674792


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_toshiba(lshw: MagicMock):
    pc, components = computer(lshw, 'toshiba.lshw')


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_acer_aspire_5737z(lshw: MagicMock):
    pc, components = computer(lshw, 'acer-aspire-5737z.lshw')


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_david(lshw: MagicMock):
    # todo check on hardware the ids, etc
    pc, components = computer(lshw, 'david.lshw')
    assert pc.model == 'Latitude E6440'
    assert pc.serial_number == 'FJBQVZ1'
    assert pc.manufacturer == 'Dell Inc.'
    assert pc.type == 'Laptop'
    cpu = components['Processor'][0]
    assert len(components['Processor']) == 1
    assert cpu.model == 'Intel Core i7-4600M CPU @ 2.90GHz'
    assert len(components['RamModule']) == 2
    for ram in components['RamModule']:
        assert isinstance(ram, RamModule)
        assert ram.format == 'SODIMM'
        assert ram.interface == 'DDR3'
        assert ram.model == 'M471B5173DB0-YK0'
        assert ram.serial_number in {'152DD498', '732CD498'}
        assert ram.size == 4096
    hdd = components['HardDrive'][0]
    assert len(components['HardDrive']) == 1
    assert isinstance(hdd, DataStorage)
    assert hdd.model == 'Crucial_CT525MX3'
    assert hdd.serial_number == '164014297BCC'
    assert hdd.size == 500786
    # todo is hdd an ssd?
    assert len(components['GraphicCard']) == 1
    gpu = components['GraphicCard'][0]
    assert isinstance(gpu, GraphicCard)
    assert gpu.manufacturer == 'Intel Corporation'
    assert gpu.model == '4th Gen Core Processor Integrated Graphics Controller'
    assert gpu.serial_number is None
    assert gpu.memory is None
    assert len(components['NetworkAdapter']) == 3  # todo why 3?
    eth = components['NetworkAdapter'][0]
    assert isinstance(eth, NetworkAdapter)
    assert eth.speed == 1000
    assert eth.serial_number == 'ec:f4:bb:0b:18:90'
    assert not eth.wireless
    wifi = components['NetworkAdapter'][1]
    assert isinstance(wifi, NetworkAdapter)
    assert wifi.model == 'Centrino Advanced-N 6235'
    assert wifi.serial_number == 'c4:d9:87:47:90:e1'
    assert wifi.manufacturer == 'Intel Corporation'
    assert wifi.wireless
    # todo check the third net adapter
    # todo check sound cards
    assert len(components['Motherboard']) == 1
    mother = components['Motherboard'][0]
    assert mother.manufacturer == 'Dell Inc.'
    assert mother.serial_number == '/FJBQVZ1/CN1296342I009B/'
    assert mother.model == '0159N7'
    # todo check USB ports and slots


@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_isard_probook(lshw: MagicMock):
    # todo check on hardware the ids, etc
    pc, components = computer(lshw, 'test_isard_probook.lshw')
    assert 'ProBook 430 G4'== pc.model #found
    assert '5CD7314HDY'== pc.serial_number #found
    assert 'HP' == pc.manufacturer #found
    assert 'Laptop' ==  pc.type #found
    cpu = components['Processor'][0]
    assert len(components['Processor']) == 1
    assert 'Intel Core i5-7200U CPU @ 2.50GHz' ==  cpu.model #found
    assert len(components['RamModule']) == 1 #found
    for ram in components['RamModule']:
        assert isinstance(ram, RamModule)
        assert 'SODIMM' == ram.format #found
        assert 'DDR4' == ram.interface #found
        assert 'M471A1K43CB1-CRC' == ram.model #found
        assert ram.serial_number in {'362E4E84'} #found
        assert 8192 == ram.size
#    hdd = components['HardDrive'][0]
#    assert len(components['HardDrive']) == 1
#    assert isinstance(hdd, DataStorage)
#    assert hdd.model == 'Crucial_CT525MX3'
#    assert hdd.serial_number == '164014297BCC'
#    assert hdd.size == 500786
    # todo is hdd an ssd?
    assert len(components['GraphicCard']) == 1 #found
    gpu = components['GraphicCard'][0]
    assert isinstance(gpu, GraphicCard)
    assert 'Intel Corporation'== gpu.manufacturer #found
    assert 'Intel Corporation'== gpu.model #found
    assert gpu.serial_number is None
    assert None == gpu.memory #found (no es none, és 256.0)
    assert len(components['NetworkAdapter']) == 2  # todo why 3?
    eth = components['NetworkAdapter'][0]
    assert isinstance(eth, NetworkAdapter)
    assert  1000 == eth.speed #found
    assert 'f4:30:b9:a8:6d:15' == eth.serial_number #found
    assert not eth.wireless #found
    wifi = components['NetworkAdapter'][1]
    assert isinstance(wifi, NetworkAdapter)
    assert  'Wireless 7265' == wifi.model #found (Centrino Advanced-N 6235)
    assert  '16:7b:5f:33:d2:3d' == wifi.serial_number #found
    assert  'Intel Corporation' == wifi.manufacturer #found
    assert wifi.wireless #found
    # todo check the third net adapter
    # todo check sound cards
    assert len(components['Motherboard']) == 1
    mother = components['Motherboard'][0]
    assert 'HP' == mother.manufacturer
    assert 'PGDZN018J887YS'== mother.serial_number
    assert  '822C'==  mother.model
    # todo check USB ports and slots

@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_pc_hpCompaq8100(lshw: MagicMock):
    # todo check on hardware the ids, etc
    pc, components = computer(lshw, 'test_pc_hpCompaq8100.lshw')
    assert 'HP Compaq 8100 Elite SFF'== pc.model #found
    assert 'CZC0408YPV'== pc.serial_number #found
    #assert '' == pc.manufacturer
    assert 'Desktop' ==  pc.type #found
    cpu = components['Processor'][0]
    assert len(components['Processor']) == 1 #found
    assert 'Intel Core i3 CPU 530 @ 2.93GHz' ==  cpu.model #found
    assert len(components['RamModule']) == 4
    for ram in components['RamModule']: #found
        assert isinstance(ram, RamModule) 
        assert 'DIMM' == ram.format #found
        assert 'DDR3' == ram.interface #found
        assert '16JTF25664AZ-1G4F' == ram.model #found (principi amb 'MT' i al final hi ha un 1)
        assert ram.serial_number in {'92072F30','A4482E29','939E2E29', '48FD2E30'} #found
        assert 2048 == ram.size #found
#No detecta la SSD
    #ssd = components['SolidStateDrive'][0]
    #assert len(components['SolidStateDrive']) == 1 #found
    #assert isinstance(ssd, DataStorage)
    #assert 'KINGSTON SA400S3' == ssd.model #found (falta un 7 al final: SA400S37)
    #assert '50026B7782018EE6' == sdd.serial_number #found
    #assert 114473 == sdd.size #found
    assert len(components['GraphicCard']) == 1 #found
    gpu = components['GraphicCard'][0]
    assert isinstance(gpu, GraphicCard)
    assert 'Intel Corporation'== gpu.manufacturer #found
    assert 'Core Processor Integrated Graphics Controller'== gpu.model #found
    assert gpu.serial_number is None
    assert None == gpu.memory #found ( és 256.0)
    assert len(components['NetworkAdapter']) == 1  #found
    eth = components['NetworkAdapter'][0]
    assert isinstance(eth, NetworkAdapter)
    assert  1000 == eth.speed #found
    assert '6c:62:6d:81:4d:ae' == eth.serial_number #found
    assert not eth.wireless #found
    # todo check the third net adapter
    # todo check sound cards
    assert len(components['Motherboard']) == 1 #found
    mother = components['Motherboard'][0]
    assert 'Hewlett-Packard' == mother.manufacturer #found
    assert 'CZC0408YPV'== mother.serial_number #found
    assert  '304Ah'==  mother.model #found
    # todo check USB ports and slots

@pytest.mark.usefixtures(conftest.pysmart_device.__name__)
def test_pc_hpCompaq7900(lshw: MagicMock):
    # todo check on hardware the ids, etc
    pc, components = computer(lshw, 'test_pc_hpCompaq7900.lshw')
    assert 'HP Compaq dc7900 Small Form Factor'== pc.model #found
    assert 'CZC901381R'== pc.serial_number #found
    #assert '' == pc.manufacturer
    assert 'Desktop' ==  pc.type #found
    cpu = components['Processor'][0]
    assert len(components['Processor']) == 1
    assert 'Intel Core2 Duo CPU E8400 @ 3.00GHz' ==  cpu.model
    assert len(components['RamModule']) == 1
    for ram in components['RamModule']: #found
        assert isinstance(ram, RamModule) 
        assert 'DIMM' == ram.format #found
        assert 'DDR2' == ram.interface #found
        assert 'HYMP125U64CP8-S6' == ram.model #found 
        assert ram.serial_number in {None} #found (811X6W8)
        assert 2048 == ram.size #found
    #ssd = components['SolidStateDrive'][0]
    #assert len(components['SolidStateDrive']) == 1 #found
    #assert isinstance(ssd, DataStorage)
    #assert 'KINGSTON SA400S3' == ssd.model #found (falta un 7 al final: SA400S37)
    #assert '50026B7782018EE6' == sdd.serial_number #found
    #assert '114473' == sdd.size #found
    hdd = components['HardDrive'][0]
    assert len(components['HardDrive']) == 1
    assert isinstance(hdd, DataStorage)
    assert 'ST3160815AS'== hdd.model #found
    assert '6RX7AWEZ'== hdd.serial_number #found
    assert  152627 == hdd.size #found
    # todo is hdd an ssd?
    assert len(components['GraphicCard']) == 1 #found
    gpu = components['GraphicCard'][0]
    assert isinstance(gpu, GraphicCard)
    assert 'Intel Corporation'== gpu.manufacturer #found
    assert '4 Series Chipset Integrated Graphics Controller'== gpu.model #found
    assert gpu.serial_number is None
    assert None == gpu.memory #found (256.0)
    assert len(components['NetworkAdapter']) == 1  #found
    eth = components['NetworkAdapter'][0]
    assert isinstance(eth, NetworkAdapter)
    assert  1000 == eth.speed #found
    assert '00:23:7d:49:5e:31' == eth.serial_number #found
    assert not eth.wireless #found
    # todo check the third net adapter
    # todo check sound cards
    assert len(components['Motherboard']) == 1 #found
    mother = components['Motherboard'][0]
    assert 'Hewlett-Packard' == mother.manufacturer #found
    assert 'CZC901381R'== mother.serial_number #found
    assert  '3031h'==  mother.model #found
    # todo check USB ports and slots
