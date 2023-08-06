# Generated from 'v1_6_1.xml' on 2019-03-14 09:42:04.047934

from typing import Tuple

from toptica.lasersdk.client import UserLevel
from toptica.lasersdk.client import Client

from toptica.lasersdk.client import DecopBoolean
from toptica.lasersdk.client import DecopInteger
from toptica.lasersdk.client import DecopReal
from toptica.lasersdk.client import DecopString
from toptica.lasersdk.client import DecopBinary

from toptica.lasersdk.client import MutableDecopBoolean
from toptica.lasersdk.client import MutableDecopInteger
from toptica.lasersdk.client import MutableDecopReal
from toptica.lasersdk.client import MutableDecopString
from toptica.lasersdk.client import MutableDecopBinary

from toptica.lasersdk.client import Connection
from toptica.lasersdk.client import NetworkConnection
from toptica.lasersdk.client import SerialConnection

from toptica.lasersdk.client import DecopError
from toptica.lasersdk.client import DeviceNotFoundError


class Licenses:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._options = LicenseOptions(client, name + ':options')
        self._installed_keys = DecopInteger(client, name + ':installed-keys')

    @property
    def options(self) -> 'LicenseOptions':
        return self._options

    @property
    def installed_keys(self) -> 'DecopInteger':
        return self._installed_keys

    def get_key(self, key_number: int) -> str:
        assert isinstance(key_number, int), "expected type 'int' for parameter 'key_number', got '{}'".format(type(key_number))
        return self.__client.exec(self.__name + ':get-key', key_number, input_stream=None, output_type=None, return_type=str)

    def install(self, licensekey: str) -> bool:
        assert isinstance(licensekey, str), "expected type 'str' for parameter 'licensekey', got '{}'".format(type(licensekey))
        return self.__client.exec(self.__name + ':install', licensekey, input_stream=None, output_type=None, return_type=bool)


class LicenseOptions:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._lock = LicenseOption(client, name + ':lock')

    @property
    def lock(self) -> 'LicenseOption':
        return self._lock


class LicenseOption:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._valid_until = DecopString(client, name + ':valid-until')
        self._licensee = DecopString(client, name + ':licensee')
        self._enabled = DecopBoolean(client, name + ':enabled')

    @property
    def valid_until(self) -> 'DecopString':
        return self._valid_until

    @property
    def licensee(self) -> 'DecopString':
        return self._licensee

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled


class FwUpdate:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name

    def show_log(self) -> str:
        return self.__client.exec(self.__name + ':show-log', input_stream=None, output_type=str, return_type=None)

    def upload(self, input_stream: bytes, filename: str) -> None:
        assert isinstance(input_stream, bytes), "expected type 'bytes' for parameter 'input_stream', got '{}'".format(type(input_stream))
        assert isinstance(filename, str), "expected type 'str' for parameter 'filename', got '{}'".format(type(filename))
        self.__client.exec(self.__name + ':upload', filename, input_stream=input_stream, output_type=None, return_type=None)

    def show_history(self) -> str:
        return self.__client.exec(self.__name + ':show-history', input_stream=None, output_type=str, return_type=None)


class ServiceReport:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ready = DecopBoolean(client, name + ':ready')

    @property
    def ready(self) -> 'DecopBoolean':
        return self._ready

    def print(self) -> bytes:
        return self.__client.exec(self.__name + ':print', input_stream=None, output_type=bytes, return_type=None)

    def request(self) -> None:
        self.__client.exec(self.__name + ':request', input_stream=None, output_type=None, return_type=None)

    def service_report(self) -> bytes:
        return self.__client.exec(self.__name + ':service-report', input_stream=None, output_type=bytes, return_type=None)


class SystemMessages:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._count = DecopInteger(client, name + ':count')
        self._count_new = DecopInteger(client, name + ':count-new')
        self._latest_message = DecopString(client, name + ':latest-message')

    @property
    def count(self) -> 'DecopInteger':
        return self._count

    @property
    def count_new(self) -> 'DecopInteger':
        return self._count_new

    @property
    def latest_message(self) -> 'DecopString':
        return self._latest_message

    def show_log(self) -> str:
        return self.__client.exec(self.__name + ':show-log', input_stream=None, output_type=str, return_type=None)

    def show_persistent(self) -> str:
        return self.__client.exec(self.__name + ':show-persistent', input_stream=None, output_type=str, return_type=None)

    def mark_as_read(self, ID: int) -> None:
        assert isinstance(ID, int), "expected type 'int' for parameter 'ID', got '{}'".format(type(ID))
        self.__client.exec(self.__name + ':mark-as-read', ID, input_stream=None, output_type=None, return_type=None)

    def show_new(self) -> str:
        return self.__client.exec(self.__name + ':show-new', input_stream=None, output_type=str, return_type=None)

    def show_all(self) -> str:
        return self.__client.exec(self.__name + ':show-all', input_stream=None, output_type=str, return_type=None)


class BuildInformation:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._build_tag = DecopString(client, name + ':build-tag')
        self._build_url = DecopString(client, name + ':build-url')
        self._job_name = DecopString(client, name + ':job-name')
        self._c_compiler_id = DecopString(client, name + ':c-compiler-id')
        self._cxx_compiler_id = DecopString(client, name + ':cxx-compiler-id')
        self._build_number = DecopInteger(client, name + ':build-number')
        self._build_node_name = DecopString(client, name + ':build-node-name')
        self._cxx_compiler_version = DecopString(client, name + ':cxx-compiler-version')
        self._build_id = DecopString(client, name + ':build-id')
        self._c_compiler_version = DecopString(client, name + ':c-compiler-version')

    @property
    def build_tag(self) -> 'DecopString':
        return self._build_tag

    @property
    def build_url(self) -> 'DecopString':
        return self._build_url

    @property
    def job_name(self) -> 'DecopString':
        return self._job_name

    @property
    def c_compiler_id(self) -> 'DecopString':
        return self._c_compiler_id

    @property
    def cxx_compiler_id(self) -> 'DecopString':
        return self._cxx_compiler_id

    @property
    def build_number(self) -> 'DecopInteger':
        return self._build_number

    @property
    def build_node_name(self) -> 'DecopString':
        return self._build_node_name

    @property
    def cxx_compiler_version(self) -> 'DecopString':
        return self._cxx_compiler_version

    @property
    def build_id(self) -> 'DecopString':
        return self._build_id

    @property
    def c_compiler_version(self) -> 'DecopString':
        return self._c_compiler_version


class IoBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._digital_in2 = IoDigitalInput(client, name + ':digital-in2')
        self._digital_out3 = IoDigitalOutput(client, name + ':digital-out3')
        self._revision = DecopString(client, name + ':revision')
        self._digital_out0 = IoDigitalOutput(client, name + ':digital-out0')
        self._out_b = IoOutputChannel(client, name + ':out-b')
        self._digital_out2 = IoDigitalOutput(client, name + ':digital-out2')
        self._digital_out1 = IoDigitalOutput(client, name + ':digital-out1')
        self._digital_in0 = IoDigitalInput(client, name + ':digital-in0')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._digital_in3 = IoDigitalInput(client, name + ':digital-in3')
        self._out_a = IoOutputChannel(client, name + ':out-a')
        self._digital_in1 = IoDigitalInput(client, name + ':digital-in1')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def digital_in2(self) -> 'IoDigitalInput':
        return self._digital_in2

    @property
    def digital_out3(self) -> 'IoDigitalOutput':
        return self._digital_out3

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def digital_out0(self) -> 'IoDigitalOutput':
        return self._digital_out0

    @property
    def out_b(self) -> 'IoOutputChannel':
        return self._out_b

    @property
    def digital_out2(self) -> 'IoDigitalOutput':
        return self._digital_out2

    @property
    def digital_out1(self) -> 'IoDigitalOutput':
        return self._digital_out1

    @property
    def digital_in0(self) -> 'IoDigitalInput':
        return self._digital_in0

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def digital_in3(self) -> 'IoDigitalInput':
        return self._digital_in3

    @property
    def out_a(self) -> 'IoOutputChannel':
        return self._out_a

    @property
    def digital_in1(self) -> 'IoDigitalInput':
        return self._digital_in1

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number


class IoDigitalInput:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_act = DecopBoolean(client, name + ':value-act')

    @property
    def value_act(self) -> 'DecopBoolean':
        return self._value_act


class IoDigitalOutput:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._mode = MutableDecopInteger(client, name + ':mode')
        self._value_set = MutableDecopBoolean(client, name + ':value-set')
        self._invert = MutableDecopBoolean(client, name + ':invert')
        self._value_act = DecopBoolean(client, name + ':value-act')

    @property
    def mode(self) -> 'MutableDecopInteger':
        return self._mode

    @property
    def value_set(self) -> 'MutableDecopBoolean':
        return self._value_set

    @property
    def invert(self) -> 'MutableDecopBoolean':
        return self._invert

    @property
    def value_act(self) -> 'DecopBoolean':
        return self._value_act


class IoOutputChannel:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')
        self._voltage_set = MutableDecopReal(client, name + ':voltage-set')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._voltage_offset = MutableDecopReal(client, name + ':voltage-offset')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._external_input = ExtInput2(client, name + ':external-input')
        self._linked_laser = MutableDecopInteger(client, name + ':linked-laser')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max

    @property
    def voltage_set(self) -> 'MutableDecopReal':
        return self._voltage_set

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def voltage_offset(self) -> 'MutableDecopReal':
        return self._voltage_offset

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input

    @property
    def linked_laser(self) -> 'MutableDecopInteger':
        return self._linked_laser

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled


class OutputFilter2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slew_rate_enabled = MutableDecopBoolean(client, name + ':slew-rate-enabled')
        self._slew_rate_limited = DecopBoolean(client, name + ':slew-rate-limited')
        self._slew_rate = MutableDecopReal(client, name + ':slew-rate')

    @property
    def slew_rate_enabled(self) -> 'MutableDecopBoolean':
        return self._slew_rate_enabled

    @property
    def slew_rate_limited(self) -> 'DecopBoolean':
        return self._slew_rate_limited

    @property
    def slew_rate(self) -> 'MutableDecopReal':
        return self._slew_rate


class ExtInput2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = MutableDecopInteger(client, name + ':signal')
        self._factor = MutableDecopReal(client, name + ':factor')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal

    @property
    def factor(self) -> 'MutableDecopReal':
        return self._factor

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class Laser:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._wide_scan = WideScan(client, name + ':wide-scan')
        self._emission = DecopBoolean(client, name + ':emission')
        self._uv = UvShg(client, name + ':uv')
        self._amp = LaserAmp(client, name + ':amp')
        self._ctl = CtlT(client, name + ':ctl')
        self._health = DecopInteger(client, name + ':health')
        self._scope = ScopeT(client, name + ':scope')
        self._recorder = Recorder(client, name + ':recorder')
        self._dl = LaserHead(client, name + ':dl')
        self._nlo = Nlo(client, name + ':nlo')
        self._power_stabilization = PwrStab(client, name + ':power-stabilization')
        self._scan = ScanGenerator(client, name + ':scan')
        self._product_name = DecopString(client, name + ':product-name')
        self._health_txt = DecopString(client, name + ':health-txt')
        self._pd_ext = PdExt(client, name + ':pd-ext')
        self._type_ = DecopString(client, name + ':type')
        self._dpss = Dpss2(client, name + ':dpss')

    @property
    def wide_scan(self) -> 'WideScan':
        return self._wide_scan

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def uv(self) -> 'UvShg':
        return self._uv

    @property
    def amp(self) -> 'LaserAmp':
        return self._amp

    @property
    def ctl(self) -> 'CtlT':
        return self._ctl

    @property
    def health(self) -> 'DecopInteger':
        return self._health

    @property
    def scope(self) -> 'ScopeT':
        return self._scope

    @property
    def recorder(self) -> 'Recorder':
        return self._recorder

    @property
    def dl(self) -> 'LaserHead':
        return self._dl

    @property
    def nlo(self) -> 'Nlo':
        return self._nlo

    @property
    def power_stabilization(self) -> 'PwrStab':
        return self._power_stabilization

    @property
    def scan(self) -> 'ScanGenerator':
        return self._scan

    @property
    def product_name(self) -> 'DecopString':
        return self._product_name

    @property
    def health_txt(self) -> 'DecopString':
        return self._health_txt

    @property
    def pd_ext(self) -> 'PdExt':
        return self._pd_ext

    @property
    def type_(self) -> 'DecopString':
        return self._type_

    @property
    def dpss(self) -> 'Dpss2':
        return self._dpss

    def save(self) -> None:
        self.__client.exec(self.__name + ':save', input_stream=None, output_type=None, return_type=None)

    def load(self) -> None:
        self.__client.exec(self.__name + ':load', input_stream=None, output_type=None, return_type=None)


class WideScan:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scan_begin = MutableDecopReal(client, name + ':scan-begin')
        self._remaining_time = DecopInteger(client, name + ':remaining-time')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._duration = MutableDecopReal(client, name + ':duration')
        self._speed = MutableDecopReal(client, name + ':speed')
        self._progress = DecopInteger(client, name + ':progress')
        self._state = DecopInteger(client, name + ':state')
        self._offset = MutableDecopReal(client, name + ':offset')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._scan_end = MutableDecopReal(client, name + ':scan-end')
        self._output_channel = MutableDecopInteger(client, name + ':output-channel')

    @property
    def scan_begin(self) -> 'MutableDecopReal':
        return self._scan_begin

    @property
    def remaining_time(self) -> 'DecopInteger':
        return self._remaining_time

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def duration(self) -> 'MutableDecopReal':
        return self._duration

    @property
    def speed(self) -> 'MutableDecopReal':
        return self._speed

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def offset(self) -> 'MutableDecopReal':
        return self._offset

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def scan_end(self) -> 'MutableDecopReal':
        return self._scan_end

    @property
    def output_channel(self) -> 'MutableDecopInteger':
        return self._output_channel

    def stop(self) -> None:
        self.__client.exec(self.__name + ':stop', input_stream=None, output_type=None, return_type=None)

    def start(self) -> None:
        self.__client.exec(self.__name + ':start', input_stream=None, output_type=None, return_type=None)


class UvShg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._eom = UvEom(client, name + ':eom')
        self._operation_time = DecopReal(client, name + ':operation-time')
        self._servo = NloLaserHeadUvServos(client, name + ':servo')
        self._pump = Dpss1(client, name + ':pump')
        self._error_txt = DecopString(client, name + ':error-txt')
        self._scan = NloLaserHeadSiggen1(client, name + ':scan')
        self._lock = NloLaserHeadLockShg1(client, name + ':lock')
        self._status_parameters = UvStatusParameters(client, name + ':status-parameters')
        self._cavity = UvCavity(client, name + ':cavity')
        self._pd = NloLaserHeadUvPhotoDiodes(client, name + ':pd')
        self._factory_settings = UvFactorySettings(client, name + ':factory-settings')
        self._crystal = UvCrystal(client, name + ':crystal')
        self._power_stabilization = UvShgPowerStabilization(client, name + ':power-stabilization')
        self._remaining_optics_spots = DecopInteger(client, name + ':remaining-optics-spots')
        self._power_margin = DecopReal(client, name + ':power-margin')
        self._power_optimization = UvShgPowerOptimization(client, name + ':power-optimization')
        self._scope = NloLaserHeadScopeT1(client, name + ':scope')
        self._ssw_ver = DecopString(client, name + ':ssw-ver')
        self._baseplate_temperature = DecopReal(client, name + ':baseplate-temperature')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._error = DecopInteger(client, name + ':error')

    @property
    def eom(self) -> 'UvEom':
        return self._eom

    @property
    def operation_time(self) -> 'DecopReal':
        return self._operation_time

    @property
    def servo(self) -> 'NloLaserHeadUvServos':
        return self._servo

    @property
    def pump(self) -> 'Dpss1':
        return self._pump

    @property
    def error_txt(self) -> 'DecopString':
        return self._error_txt

    @property
    def scan(self) -> 'NloLaserHeadSiggen1':
        return self._scan

    @property
    def lock(self) -> 'NloLaserHeadLockShg1':
        return self._lock

    @property
    def status_parameters(self) -> 'UvStatusParameters':
        return self._status_parameters

    @property
    def cavity(self) -> 'UvCavity':
        return self._cavity

    @property
    def pd(self) -> 'NloLaserHeadUvPhotoDiodes':
        return self._pd

    @property
    def factory_settings(self) -> 'UvFactorySettings':
        return self._factory_settings

    @property
    def crystal(self) -> 'UvCrystal':
        return self._crystal

    @property
    def power_stabilization(self) -> 'UvShgPowerStabilization':
        return self._power_stabilization

    @property
    def remaining_optics_spots(self) -> 'DecopInteger':
        return self._remaining_optics_spots

    @property
    def power_margin(self) -> 'DecopReal':
        return self._power_margin

    @property
    def power_optimization(self) -> 'UvShgPowerOptimization':
        return self._power_optimization

    @property
    def scope(self) -> 'NloLaserHeadScopeT1':
        return self._scope

    @property
    def ssw_ver(self) -> 'DecopString':
        return self._ssw_ver

    @property
    def baseplate_temperature(self) -> 'DecopReal':
        return self._baseplate_temperature

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def error(self) -> 'DecopInteger':
        return self._error

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    def perform_optimization(self) -> None:
        self.__client.exec(self.__name + ':perform-optimization', input_stream=None, output_type=None, return_type=None)

    def clear_errors(self) -> None:
        self.__client.exec(self.__name + ':clear-errors', input_stream=None, output_type=None, return_type=None)

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)


class UvEom:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcChannel1(client, name + ':tc')

    @property
    def tc(self) -> 'TcChannel1':
        return self._tc


class TcChannel1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ntc_parallel_resistance = DecopReal(client, name + ':ntc-parallel-resistance')
        self._current_act = DecopReal(client, name + ':current-act')
        self._ready = DecopBoolean(client, name + ':ready')
        self._enabled = DecopBoolean(client, name + ':enabled')
        self._current_set = DecopReal(client, name + ':current-set')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._path = DecopString(client, name + ':path')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._temp_reset = DecopBoolean(client, name + ':temp-reset')
        self._current_set_max = DecopReal(client, name + ':current-set-max')
        self._temp_roc_limit = DecopReal(client, name + ':temp-roc-limit')
        self._external_input = ExtInput1(client, name + ':external-input')
        self._c_loop = TcChannelCLoop1(client, name + ':c-loop')
        self._ntc_series_resistance = DecopReal(client, name + ':ntc-series-resistance')
        self._drv_voltage = DecopReal(client, name + ':drv-voltage')
        self._power_source = DecopInteger(client, name + ':power-source')
        self._limits = TcChannelCheck1(client, name + ':limits')
        self._current_set_min = DecopReal(client, name + ':current-set-min')
        self._temp_act = DecopReal(client, name + ':temp-act')
        self._fault = DecopBoolean(client, name + ':fault')
        self._temp_set_max = DecopReal(client, name + ':temp-set-max')
        self._resistance = DecopReal(client, name + ':resistance')
        self._temp_roc_enabled = DecopBoolean(client, name + ':temp-roc-enabled')
        self._t_loop = TcChannelTLoop1(client, name + ':t-loop')
        self._status = DecopInteger(client, name + ':status')
        self._temp_set_min = DecopReal(client, name + ':temp-set-min')
        self._temp_set = DecopReal(client, name + ':temp-set')

    @property
    def ntc_parallel_resistance(self) -> 'DecopReal':
        return self._ntc_parallel_resistance

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def ready(self) -> 'DecopBoolean':
        return self._ready

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled

    @property
    def current_set(self) -> 'DecopReal':
        return self._current_set

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def temp_reset(self) -> 'DecopBoolean':
        return self._temp_reset

    @property
    def current_set_max(self) -> 'DecopReal':
        return self._current_set_max

    @property
    def temp_roc_limit(self) -> 'DecopReal':
        return self._temp_roc_limit

    @property
    def external_input(self) -> 'ExtInput1':
        return self._external_input

    @property
    def c_loop(self) -> 'TcChannelCLoop1':
        return self._c_loop

    @property
    def ntc_series_resistance(self) -> 'DecopReal':
        return self._ntc_series_resistance

    @property
    def drv_voltage(self) -> 'DecopReal':
        return self._drv_voltage

    @property
    def power_source(self) -> 'DecopInteger':
        return self._power_source

    @property
    def limits(self) -> 'TcChannelCheck1':
        return self._limits

    @property
    def current_set_min(self) -> 'DecopReal':
        return self._current_set_min

    @property
    def temp_act(self) -> 'DecopReal':
        return self._temp_act

    @property
    def fault(self) -> 'DecopBoolean':
        return self._fault

    @property
    def temp_set_max(self) -> 'DecopReal':
        return self._temp_set_max

    @property
    def resistance(self) -> 'DecopReal':
        return self._resistance

    @property
    def temp_roc_enabled(self) -> 'DecopBoolean':
        return self._temp_roc_enabled

    @property
    def t_loop(self) -> 'TcChannelTLoop1':
        return self._t_loop

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def temp_set_min(self) -> 'DecopReal':
        return self._temp_set_min

    @property
    def temp_set(self) -> 'DecopReal':
        return self._temp_set


class ExtInput1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = DecopInteger(client, name + ':signal')
        self._factor = DecopReal(client, name + ':factor')
        self._enabled = DecopBoolean(client, name + ':enabled')

    @property
    def signal(self) -> 'DecopInteger':
        return self._signal

    @property
    def factor(self) -> 'DecopReal':
        return self._factor

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled


class TcChannelCLoop1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._on = DecopBoolean(client, name + ':on')
        self._i_gain = DecopReal(client, name + ':i-gain')

    @property
    def on(self) -> 'DecopBoolean':
        return self._on

    @property
    def i_gain(self) -> 'DecopReal':
        return self._i_gain


class TcChannelCheck1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._timeout = DecopInteger(client, name + ':timeout')
        self._out_of_range = DecopBoolean(client, name + ':out-of-range')
        self._temp_max = DecopReal(client, name + ':temp-max')
        self._timed_out = DecopBoolean(client, name + ':timed-out')
        self._temp_min = DecopReal(client, name + ':temp-min')

    @property
    def timeout(self) -> 'DecopInteger':
        return self._timeout

    @property
    def out_of_range(self) -> 'DecopBoolean':
        return self._out_of_range

    @property
    def temp_max(self) -> 'DecopReal':
        return self._temp_max

    @property
    def timed_out(self) -> 'DecopBoolean':
        return self._timed_out

    @property
    def temp_min(self) -> 'DecopReal':
        return self._temp_min


class TcChannelTLoop1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._on = DecopBoolean(client, name + ':on')
        self._ok_tolerance = DecopReal(client, name + ':ok-tolerance')
        self._d_gain = DecopReal(client, name + ':d-gain')
        self._ok_time = DecopReal(client, name + ':ok-time')
        self._p_gain = DecopReal(client, name + ':p-gain')
        self._i_gain = DecopReal(client, name + ':i-gain')

    @property
    def on(self) -> 'DecopBoolean':
        return self._on

    @property
    def ok_tolerance(self) -> 'DecopReal':
        return self._ok_tolerance

    @property
    def d_gain(self) -> 'DecopReal':
        return self._d_gain

    @property
    def ok_time(self) -> 'DecopReal':
        return self._ok_time

    @property
    def p_gain(self) -> 'DecopReal':
        return self._p_gain

    @property
    def i_gain(self) -> 'DecopReal':
        return self._i_gain


class NloLaserHeadUvServos:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._comp_vert = NloLaserHeadServoPwm1(client, name + ':comp-vert')
        self._shg2_hor = NloLaserHeadServoPwm1(client, name + ':shg2-hor')
        self._shg2_vert = NloLaserHeadServoPwm1(client, name + ':shg2-vert')
        self._shg1_vert = NloLaserHeadServoPwm1(client, name + ':shg1-vert')
        self._lens = NloLaserHeadServoPwm1(client, name + ':lens')
        self._shg1_hor = NloLaserHeadServoPwm1(client, name + ':shg1-hor')
        self._comp_hor = NloLaserHeadServoPwm1(client, name + ':comp-hor')
        self._outcpl = NloLaserHeadServoPwm1(client, name + ':outcpl')
        self._hwp = NloLaserHeadServoPwm1(client, name + ':hwp')
        self._cryst = NloLaserHeadServoPwm1(client, name + ':cryst')

    @property
    def comp_vert(self) -> 'NloLaserHeadServoPwm1':
        return self._comp_vert

    @property
    def shg2_hor(self) -> 'NloLaserHeadServoPwm1':
        return self._shg2_hor

    @property
    def shg2_vert(self) -> 'NloLaserHeadServoPwm1':
        return self._shg2_vert

    @property
    def shg1_vert(self) -> 'NloLaserHeadServoPwm1':
        return self._shg1_vert

    @property
    def lens(self) -> 'NloLaserHeadServoPwm1':
        return self._lens

    @property
    def shg1_hor(self) -> 'NloLaserHeadServoPwm1':
        return self._shg1_hor

    @property
    def comp_hor(self) -> 'NloLaserHeadServoPwm1':
        return self._comp_hor

    @property
    def outcpl(self) -> 'NloLaserHeadServoPwm1':
        return self._outcpl

    @property
    def hwp(self) -> 'NloLaserHeadServoPwm1':
        return self._hwp

    @property
    def cryst(self) -> 'NloLaserHeadServoPwm1':
        return self._cryst


class NloLaserHeadServoPwm1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = DecopBoolean(client, name + ':enabled')
        self._value = DecopInteger(client, name + ':value')
        self._display_name = DecopString(client, name + ':display-name')

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled

    @property
    def value(self) -> 'DecopInteger':
        return self._value

    @property
    def display_name(self) -> 'DecopString':
        return self._display_name


class Dpss1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._operation_time = DecopReal(client, name + ':operation-time')
        self._power_act = DecopReal(client, name + ':power-act')
        self._enabled = DecopBoolean(client, name + ':enabled')
        self._error_txt = DecopString(client, name + ':error-txt')
        self._tc_status_txt = DecopString(client, name + ':tc-status-txt')
        self._power_margin = DecopReal(client, name + ':power-margin')
        self._error_code = DecopInteger(client, name + ':error-code')
        self._current_act = DecopReal(client, name + ':current-act')
        self._tc_status = DecopInteger(client, name + ':tc-status')
        self._current_max = DecopReal(client, name + ':current-max')
        self._power_set = DecopReal(client, name + ':power-set')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._power_max = DecopReal(client, name + ':power-max')

    @property
    def operation_time(self) -> 'DecopReal':
        return self._operation_time

    @property
    def power_act(self) -> 'DecopReal':
        return self._power_act

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled

    @property
    def error_txt(self) -> 'DecopString':
        return self._error_txt

    @property
    def tc_status_txt(self) -> 'DecopString':
        return self._tc_status_txt

    @property
    def power_margin(self) -> 'DecopReal':
        return self._power_margin

    @property
    def error_code(self) -> 'DecopInteger':
        return self._error_code

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def tc_status(self) -> 'DecopInteger':
        return self._tc_status

    @property
    def current_max(self) -> 'DecopReal':
        return self._current_max

    @property
    def power_set(self) -> 'DecopReal':
        return self._power_set

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def power_max(self) -> 'DecopReal':
        return self._power_max


class NloLaserHeadSiggen1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._amplitude = DecopReal(client, name + ':amplitude')
        self._enabled = DecopBoolean(client, name + ':enabled')
        self._frequency = DecopReal(client, name + ':frequency')
        self._offset = DecopReal(client, name + ':offset')

    @property
    def amplitude(self) -> 'DecopReal':
        return self._amplitude

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled

    @property
    def frequency(self) -> 'DecopReal':
        return self._frequency

    @property
    def offset(self) -> 'DecopReal':
        return self._offset


class NloLaserHeadLockShg1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid_selection = DecopInteger(client, name + ':pid-selection')
        self._cavity_fast_pzt_voltage = DecopReal(client, name + ':cavity-fast-pzt-voltage')
        self._local_oscillator = NloLaserHeadLocalOscillatorShg1(client, name + ':local-oscillator')
        self._pid1 = NloLaserHeadPid1(client, name + ':pid1')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._cavity_slow_pzt_voltage = DecopReal(client, name + ':cavity-slow-pzt-voltage')
        self._analog_dl_gain = NloLaserHeadMinifalc1(client, name + ':analog-dl-gain')
        self._background_trace = DecopBinary(client, name + ':background-trace')
        self._state = DecopInteger(client, name + ':state')
        self._setpoint = DecopReal(client, name + ':setpoint')
        self._lock_enabled = DecopBoolean(client, name + ':lock-enabled')
        self._pid2 = NloLaserHeadPid1(client, name + ':pid2')
        self._window = NloLaserHeadWindow1(client, name + ':window')
        self._relock = NloLaserHeadRelock1(client, name + ':relock')

    @property
    def pid_selection(self) -> 'DecopInteger':
        return self._pid_selection

    @property
    def cavity_fast_pzt_voltage(self) -> 'DecopReal':
        return self._cavity_fast_pzt_voltage

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorShg1':
        return self._local_oscillator

    @property
    def pid1(self) -> 'NloLaserHeadPid1':
        return self._pid1

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def cavity_slow_pzt_voltage(self) -> 'DecopReal':
        return self._cavity_slow_pzt_voltage

    @property
    def analog_dl_gain(self) -> 'NloLaserHeadMinifalc1':
        return self._analog_dl_gain

    @property
    def background_trace(self) -> 'DecopBinary':
        return self._background_trace

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def setpoint(self) -> 'DecopReal':
        return self._setpoint

    @property
    def lock_enabled(self) -> 'DecopBoolean':
        return self._lock_enabled

    @property
    def pid2(self) -> 'NloLaserHeadPid1':
        return self._pid2

    @property
    def window(self) -> 'NloLaserHeadWindow1':
        return self._window

    @property
    def relock(self) -> 'NloLaserHeadRelock1':
        return self._relock


class NloLaserHeadLocalOscillatorShg1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._phase_shift = DecopReal(client, name + ':phase-shift')
        self._coupled_modulation = DecopBoolean(client, name + ':coupled-modulation')
        self._amplitude = DecopReal(client, name + ':amplitude')
        self._use_external_oscillator = DecopBoolean(client, name + ':use-external-oscillator')
        self._enabled = DecopBoolean(client, name + ':enabled')
        self._use_fast_oscillator = DecopBoolean(client, name + ':use-fast-oscillator')
        self._attenuation_raw = DecopInteger(client, name + ':attenuation-raw')

    @property
    def phase_shift(self) -> 'DecopReal':
        return self._phase_shift

    @property
    def coupled_modulation(self) -> 'DecopBoolean':
        return self._coupled_modulation

    @property
    def amplitude(self) -> 'DecopReal':
        return self._amplitude

    @property
    def use_external_oscillator(self) -> 'DecopBoolean':
        return self._use_external_oscillator

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled

    @property
    def use_fast_oscillator(self) -> 'DecopBoolean':
        return self._use_fast_oscillator

    @property
    def attenuation_raw(self) -> 'DecopInteger':
        return self._attenuation_raw


class NloLaserHeadPid1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._gain = NloLaserHeadGain1(client, name + ':gain')

    @property
    def gain(self) -> 'NloLaserHeadGain1':
        return self._gain


class NloLaserHeadGain1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._p = DecopReal(client, name + ':p')
        self._i = DecopReal(client, name + ':i')
        self._d = DecopReal(client, name + ':d')
        self._all = DecopReal(client, name + ':all')
        self._i_cutoff = DecopReal(client, name + ':i-cutoff')
        self._i_cutoff_enabled = DecopBoolean(client, name + ':i-cutoff-enabled')

    @property
    def p(self) -> 'DecopReal':
        return self._p

    @property
    def i(self) -> 'DecopReal':
        return self._i

    @property
    def d(self) -> 'DecopReal':
        return self._d

    @property
    def all(self) -> 'DecopReal':
        return self._all

    @property
    def i_cutoff(self) -> 'DecopReal':
        return self._i_cutoff

    @property
    def i_cutoff_enabled(self) -> 'DecopBoolean':
        return self._i_cutoff_enabled


class NloLaserHeadMinifalc1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._p_gain = DecopReal(client, name + ':p-gain')

    @property
    def p_gain(self) -> 'DecopReal':
        return self._p_gain


class NloLaserHeadWindow1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._level_hysteresis = DecopReal(client, name + ':level-hysteresis')
        self._input_channel = DecopInteger(client, name + ':input-channel')
        self._threshold = DecopReal(client, name + ':threshold')

    @property
    def level_hysteresis(self) -> 'DecopReal':
        return self._level_hysteresis

    @property
    def input_channel(self) -> 'DecopInteger':
        return self._input_channel

    @property
    def threshold(self) -> 'DecopReal':
        return self._threshold


class NloLaserHeadRelock1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._amplitude = DecopReal(client, name + ':amplitude')
        self._enabled = DecopBoolean(client, name + ':enabled')
        self._frequency = DecopReal(client, name + ':frequency')
        self._delay = DecopReal(client, name + ':delay')

    @property
    def amplitude(self) -> 'DecopReal':
        return self._amplitude

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled

    @property
    def frequency(self) -> 'DecopReal':
        return self._frequency

    @property
    def delay(self) -> 'DecopReal':
        return self._delay


class UvStatusParameters:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cavity_lock_settle_time = DecopInteger(client, name + ':cavity-lock-settle-time')
        self._baseplate_temperature_limit = DecopReal(client, name + ':baseplate-temperature-limit')
        self._power_lock_settle_time = DecopInteger(client, name + ':power-lock-settle-time')
        self._cavity_lock_tolerance_factor = DecopInteger(client, name + ':cavity-lock-tolerance-factor')
        self._power_output_relative_error_max = DecopReal(client, name + ':power-output-relative-error-max')
        self._operational_pump_power = DecopReal(client, name + ':operational-pump-power')
        self._power_stabilization_strategy = DecopInteger(client, name + ':power-stabilization-strategy')
        self._cavity_scan_duration = DecopInteger(client, name + ':cavity-scan-duration')
        self._settle_down_delay = DecopInteger(client, name + ':settle-down-delay')
        self._temperature_settle_time = DecopInteger(client, name + ':temperature-settle-time')
        self._power_output_relative_deviation_max = DecopReal(client, name + ':power-output-relative-deviation-max')
        self._pump_lock_settle_time = DecopInteger(client, name + ':pump-lock-settle-time')
        self._power_margin_tolerance_time = DecopInteger(client, name + ':power-margin-tolerance-time')
        self._power_margin_threshold = DecopReal(client, name + ':power-margin-threshold')

    @property
    def cavity_lock_settle_time(self) -> 'DecopInteger':
        return self._cavity_lock_settle_time

    @property
    def baseplate_temperature_limit(self) -> 'DecopReal':
        return self._baseplate_temperature_limit

    @property
    def power_lock_settle_time(self) -> 'DecopInteger':
        return self._power_lock_settle_time

    @property
    def cavity_lock_tolerance_factor(self) -> 'DecopInteger':
        return self._cavity_lock_tolerance_factor

    @property
    def power_output_relative_error_max(self) -> 'DecopReal':
        return self._power_output_relative_error_max

    @property
    def operational_pump_power(self) -> 'DecopReal':
        return self._operational_pump_power

    @property
    def power_stabilization_strategy(self) -> 'DecopInteger':
        return self._power_stabilization_strategy

    @property
    def cavity_scan_duration(self) -> 'DecopInteger':
        return self._cavity_scan_duration

    @property
    def settle_down_delay(self) -> 'DecopInteger':
        return self._settle_down_delay

    @property
    def temperature_settle_time(self) -> 'DecopInteger':
        return self._temperature_settle_time

    @property
    def power_output_relative_deviation_max(self) -> 'DecopReal':
        return self._power_output_relative_deviation_max

    @property
    def pump_lock_settle_time(self) -> 'DecopInteger':
        return self._pump_lock_settle_time

    @property
    def power_margin_tolerance_time(self) -> 'DecopInteger':
        return self._power_margin_tolerance_time

    @property
    def power_margin_threshold(self) -> 'DecopReal':
        return self._power_margin_threshold


class UvCavity:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcChannel1(client, name + ':tc')
        self._pc = PiezoDrv1(client, name + ':pc')

    @property
    def tc(self) -> 'TcChannel1':
        return self._tc

    @property
    def pc(self) -> 'PiezoDrv1':
        return self._pc


class PiezoDrv1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_min = DecopReal(client, name + ':voltage-min')
        self._voltage_set = DecopReal(client, name + ':voltage-set')
        self._heatsink_temp = DecopReal(client, name + ':heatsink-temp')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._external_input = ExtInput1(client, name + ':external-input')
        self._voltage_set_dithering = DecopBoolean(client, name + ':voltage-set-dithering')
        self._voltage_max = DecopReal(client, name + ':voltage-max')
        self._enabled = DecopBoolean(client, name + ':enabled')
        self._output_filter = OutputFilter1(client, name + ':output-filter')
        self._feedforward_factor = DecopReal(client, name + ':feedforward-factor')
        self._path = DecopString(client, name + ':path')
        self._feedforward_master = DecopInteger(client, name + ':feedforward-master')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._feedforward_enabled = DecopBoolean(client, name + ':feedforward-enabled')

    @property
    def voltage_min(self) -> 'DecopReal':
        return self._voltage_min

    @property
    def voltage_set(self) -> 'DecopReal':
        return self._voltage_set

    @property
    def heatsink_temp(self) -> 'DecopReal':
        return self._heatsink_temp

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def external_input(self) -> 'ExtInput1':
        return self._external_input

    @property
    def voltage_set_dithering(self) -> 'DecopBoolean':
        return self._voltage_set_dithering

    @property
    def voltage_max(self) -> 'DecopReal':
        return self._voltage_max

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled

    @property
    def output_filter(self) -> 'OutputFilter1':
        return self._output_filter

    @property
    def feedforward_factor(self) -> 'DecopReal':
        return self._feedforward_factor

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def feedforward_master(self) -> 'DecopInteger':
        return self._feedforward_master

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def feedforward_enabled(self) -> 'DecopBoolean':
        return self._feedforward_enabled


class OutputFilter1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slew_rate_enabled = DecopBoolean(client, name + ':slew-rate-enabled')
        self._slew_rate_limited = DecopBoolean(client, name + ':slew-rate-limited')
        self._slew_rate = DecopReal(client, name + ':slew-rate')

    @property
    def slew_rate_enabled(self) -> 'DecopBoolean':
        return self._slew_rate_enabled

    @property
    def slew_rate_limited(self) -> 'DecopBoolean':
        return self._slew_rate_limited

    @property
    def slew_rate(self) -> 'DecopReal':
        return self._slew_rate


class NloLaserHeadUvPhotoDiodes:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._shg = NloLaserHeadNloPhotodiode1(client, name + ':shg')
        self._pdh_dc = NloLaserHeadNloDigilockPhotodiode1(client, name + ':pdh-dc')
        self._pdh_rf = NloLaserHeadNloPdhPhotodiode1(client, name + ':pdh-rf')

    @property
    def shg(self) -> 'NloLaserHeadNloPhotodiode1':
        return self._shg

    @property
    def pdh_dc(self) -> 'NloLaserHeadNloDigilockPhotodiode1':
        return self._pdh_dc

    @property
    def pdh_rf(self) -> 'NloLaserHeadNloPdhPhotodiode1':
        return self._pdh_rf


class NloLaserHeadNloPhotodiode1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._cal_factor = DecopReal(client, name + ':cal-factor')
        self._power = DecopReal(client, name + ':power')
        self._cal_offset = DecopReal(client, name + ':cal-offset')

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def cal_factor(self) -> 'DecopReal':
        return self._cal_factor

    @property
    def power(self) -> 'DecopReal':
        return self._power

    @property
    def cal_offset(self) -> 'DecopReal':
        return self._cal_offset


class NloLaserHeadNloDigilockPhotodiode1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._cal_offset = DecopReal(client, name + ':cal-offset')

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def cal_offset(self) -> 'DecopReal':
        return self._cal_offset


class NloLaserHeadNloPdhPhotodiode1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._gain = DecopReal(client, name + ':gain')

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def gain(self) -> 'DecopReal':
        return self._gain


class UvFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cavity_tc = NloLaserHeadTcFactorySettings(client, name + ':cavity-tc')
        self._crystal_tc = NloLaserHeadTcFactorySettings(client, name + ':crystal-tc')
        self._lock = NloLaserHeadLockFactorySettings(client, name + ':lock')
        self._pd = NloLaserHeadUvPhotodiodesFactorySettings(client, name + ':pd')
        self._pc = NloLaserHeadPcFactorySettings(client, name + ':pc')
        self._eom_tc = NloLaserHeadTcFactorySettings(client, name + ':eom-tc')
        self._modified = DecopBoolean(client, name + ':modified')

    @property
    def cavity_tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._cavity_tc

    @property
    def crystal_tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._crystal_tc

    @property
    def lock(self) -> 'NloLaserHeadLockFactorySettings':
        return self._lock

    @property
    def pd(self) -> 'NloLaserHeadUvPhotodiodesFactorySettings':
        return self._pd

    @property
    def pc(self) -> 'NloLaserHeadPcFactorySettings':
        return self._pc

    @property
    def eom_tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._eom_tc

    @property
    def modified(self) -> 'DecopBoolean':
        return self._modified

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadTcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_source = MutableDecopInteger(client, name + ':power-source')
        self._current_max = MutableDecopReal(client, name + ':current-max')
        self._current_min = MutableDecopReal(client, name + ':current-min')
        self._p_gain = MutableDecopReal(client, name + ':p-gain')
        self._temp_min = MutableDecopReal(client, name + ':temp-min')
        self._ntc_series_resistance = MutableDecopReal(client, name + ':ntc-series-resistance')
        self._timeout = MutableDecopInteger(client, name + ':timeout')
        self._ok_time = MutableDecopReal(client, name + ':ok-time')
        self._temp_max = MutableDecopReal(client, name + ':temp-max')
        self._ok_tolerance = MutableDecopReal(client, name + ':ok-tolerance')
        self._d_gain = MutableDecopReal(client, name + ':d-gain')
        self._temp_roc_enabled = MutableDecopBoolean(client, name + ':temp-roc-enabled')
        self._temp_roc_limit = MutableDecopReal(client, name + ':temp-roc-limit')
        self._i_gain = MutableDecopReal(client, name + ':i-gain')
        self._c_gain = MutableDecopReal(client, name + ':c-gain')
        self._temp_set = MutableDecopReal(client, name + ':temp-set')

    @property
    def power_source(self) -> 'MutableDecopInteger':
        return self._power_source

    @property
    def current_max(self) -> 'MutableDecopReal':
        return self._current_max

    @property
    def current_min(self) -> 'MutableDecopReal':
        return self._current_min

    @property
    def p_gain(self) -> 'MutableDecopReal':
        return self._p_gain

    @property
    def temp_min(self) -> 'MutableDecopReal':
        return self._temp_min

    @property
    def ntc_series_resistance(self) -> 'MutableDecopReal':
        return self._ntc_series_resistance

    @property
    def timeout(self) -> 'MutableDecopInteger':
        return self._timeout

    @property
    def ok_time(self) -> 'MutableDecopReal':
        return self._ok_time

    @property
    def temp_max(self) -> 'MutableDecopReal':
        return self._temp_max

    @property
    def ok_tolerance(self) -> 'MutableDecopReal':
        return self._ok_tolerance

    @property
    def d_gain(self) -> 'MutableDecopReal':
        return self._d_gain

    @property
    def temp_roc_enabled(self) -> 'MutableDecopBoolean':
        return self._temp_roc_enabled

    @property
    def temp_roc_limit(self) -> 'MutableDecopReal':
        return self._temp_roc_limit

    @property
    def i_gain(self) -> 'MutableDecopReal':
        return self._i_gain

    @property
    def c_gain(self) -> 'MutableDecopReal':
        return self._c_gain

    @property
    def temp_set(self) -> 'MutableDecopReal':
        return self._temp_set


class NloLaserHeadLockFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid2_gain = NloLaserHeadPidGainFactorySettings(client, name + ':pid2-gain')
        self._pid_selection = MutableDecopInteger(client, name + ':pid-selection')
        self._local_oscillator = NloLaserHeadLocalOscillatorFactorySettings(client, name + ':local-oscillator')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._analog_p_gain = MutableDecopReal(client, name + ':analog-p-gain')
        self._relock = NloLaserHeadRelockFactorySettings(client, name + ':relock')
        self._pid1_gain = NloLaserHeadPidGainFactorySettings(client, name + ':pid1-gain')
        self._window = NloLaserHeadLockWindowFactorySettings(client, name + ':window')

    @property
    def pid2_gain(self) -> 'NloLaserHeadPidGainFactorySettings':
        return self._pid2_gain

    @property
    def pid_selection(self) -> 'MutableDecopInteger':
        return self._pid_selection

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorFactorySettings':
        return self._local_oscillator

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def analog_p_gain(self) -> 'MutableDecopReal':
        return self._analog_p_gain

    @property
    def relock(self) -> 'NloLaserHeadRelockFactorySettings':
        return self._relock

    @property
    def pid1_gain(self) -> 'NloLaserHeadPidGainFactorySettings':
        return self._pid1_gain

    @property
    def window(self) -> 'NloLaserHeadLockWindowFactorySettings':
        return self._window


class NloLaserHeadPidGainFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._d = MutableDecopReal(client, name + ':d')
        self._p = MutableDecopReal(client, name + ':p')
        self._i = MutableDecopReal(client, name + ':i')
        self._all = MutableDecopReal(client, name + ':all')
        self._i_cutoff = MutableDecopReal(client, name + ':i-cutoff')
        self._i_cutoff_enabled = MutableDecopBoolean(client, name + ':i-cutoff-enabled')

    @property
    def d(self) -> 'MutableDecopReal':
        return self._d

    @property
    def p(self) -> 'MutableDecopReal':
        return self._p

    @property
    def i(self) -> 'MutableDecopReal':
        return self._i

    @property
    def all(self) -> 'MutableDecopReal':
        return self._all

    @property
    def i_cutoff(self) -> 'MutableDecopReal':
        return self._i_cutoff

    @property
    def i_cutoff_enabled(self) -> 'MutableDecopBoolean':
        return self._i_cutoff_enabled


class NloLaserHeadLocalOscillatorFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._phase_shift_fhg = MutableDecopReal(client, name + ':phase-shift-fhg')
        self._coupled_modulation = MutableDecopBoolean(client, name + ':coupled-modulation')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._attenuation_fhg_raw = MutableDecopInteger(client, name + ':attenuation-fhg-raw')
        self._use_fast_oscillator = MutableDecopBoolean(client, name + ':use-fast-oscillator')
        self._attenuation_shg_raw = MutableDecopInteger(client, name + ':attenuation-shg-raw')
        self._phase_shift_shg = MutableDecopReal(client, name + ':phase-shift-shg')

    @property
    def phase_shift_fhg(self) -> 'MutableDecopReal':
        return self._phase_shift_fhg

    @property
    def coupled_modulation(self) -> 'MutableDecopBoolean':
        return self._coupled_modulation

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def attenuation_fhg_raw(self) -> 'MutableDecopInteger':
        return self._attenuation_fhg_raw

    @property
    def use_fast_oscillator(self) -> 'MutableDecopBoolean':
        return self._use_fast_oscillator

    @property
    def attenuation_shg_raw(self) -> 'MutableDecopInteger':
        return self._attenuation_shg_raw

    @property
    def phase_shift_shg(self) -> 'MutableDecopReal':
        return self._phase_shift_shg


class NloLaserHeadRelockFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._delay = MutableDecopReal(client, name + ':delay')

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def delay(self) -> 'MutableDecopReal':
        return self._delay


class NloLaserHeadLockWindowFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._threshold = MutableDecopReal(client, name + ':threshold')
        self._level_hysteresis = MutableDecopReal(client, name + ':level-hysteresis')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')

    @property
    def threshold(self) -> 'MutableDecopReal':
        return self._threshold

    @property
    def level_hysteresis(self) -> 'MutableDecopReal':
        return self._level_hysteresis

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel


class NloLaserHeadUvPhotodiodesFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._shg = NloLaserHeadPdFactorySettings(client, name + ':shg')
        self._pdh_dc = NloLaserHeadPdDigilockFactorySettings(client, name + ':pdh-dc')
        self._pdh_rf = NloLaserHeadPdPdhFactorySettings(client, name + ':pdh-rf')

    @property
    def shg(self) -> 'NloLaserHeadPdFactorySettings':
        return self._shg

    @property
    def pdh_dc(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._pdh_dc

    @property
    def pdh_rf(self) -> 'NloLaserHeadPdPdhFactorySettings':
        return self._pdh_rf


class NloLaserHeadPdFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset


class NloLaserHeadPdDigilockFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset


class NloLaserHeadPdPdhFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._gain = MutableDecopReal(client, name + ':gain')

    @property
    def gain(self) -> 'MutableDecopReal':
        return self._gain


class NloLaserHeadPcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')
        self._scan_offset = MutableDecopReal(client, name + ':scan-offset')
        self._capacitance = MutableDecopReal(client, name + ':capacitance')
        self._scan_amplitude = MutableDecopReal(client, name + ':scan-amplitude')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._scan_frequency = MutableDecopReal(client, name + ':scan-frequency')

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max

    @property
    def scan_offset(self) -> 'MutableDecopReal':
        return self._scan_offset

    @property
    def capacitance(self) -> 'MutableDecopReal':
        return self._capacitance

    @property
    def scan_amplitude(self) -> 'MutableDecopReal':
        return self._scan_amplitude

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def scan_frequency(self) -> 'MutableDecopReal':
        return self._scan_frequency


class UvCrystal:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcChannel1(client, name + ':tc')
        self._optics_shifters = NloLaserHeadUvCrystalSpots(client, name + ':optics-shifters')

    @property
    def tc(self) -> 'TcChannel1':
        return self._tc

    @property
    def optics_shifters(self) -> 'NloLaserHeadUvCrystalSpots':
        return self._optics_shifters


class NloLaserHeadUvCrystalSpots:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._current_spot = DecopInteger(client, name + ':current-spot')
        self._remaining_spots = DecopInteger(client, name + ':remaining-spots')

    @property
    def current_spot(self) -> 'DecopInteger':
        return self._current_spot

    @property
    def remaining_spots(self) -> 'DecopInteger':
        return self._remaining_spots


class UvShgPowerStabilization:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_min = DecopReal(client, name + ':power-min')
        self._power_act = DecopReal(client, name + ':power-act')
        self._gain = PwrStabGain1(client, name + ':gain')
        self._enabled = DecopBoolean(client, name + ':enabled')
        self._power_set = DecopReal(client, name + ':power-set')
        self._state = DecopInteger(client, name + ':state')
        self._power_max = DecopReal(client, name + ':power-max')

    @property
    def power_min(self) -> 'DecopReal':
        return self._power_min

    @property
    def power_act(self) -> 'DecopReal':
        return self._power_act

    @property
    def gain(self) -> 'PwrStabGain1':
        return self._gain

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled

    @property
    def power_set(self) -> 'DecopReal':
        return self._power_set

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def power_max(self) -> 'DecopReal':
        return self._power_max


class PwrStabGain1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._d = DecopReal(client, name + ':d')
        self._p = DecopReal(client, name + ':p')
        self._i = DecopReal(client, name + ':i')
        self._all = DecopReal(client, name + ':all')

    @property
    def d(self) -> 'DecopReal':
        return self._d

    @property
    def p(self) -> 'DecopReal':
        return self._p

    @property
    def i(self) -> 'DecopReal':
        return self._i

    @property
    def all(self) -> 'DecopReal':
        return self._all


class UvShgPowerOptimization:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._status_string = DecopString(client, name + ':status-string')
        self._abort = DecopBoolean(client, name + ':abort')
        self._status = DecopInteger(client, name + ':status')
        self._ongoing = DecopBoolean(client, name + ':ongoing')
        self._cavity = NloLaserHeadStage1(client, name + ':cavity')
        self._progress_data = DecopBinary(client, name + ':progress-data')

    @property
    def status_string(self) -> 'DecopString':
        return self._status_string

    @property
    def abort(self) -> 'DecopBoolean':
        return self._abort

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def ongoing(self) -> 'DecopBoolean':
        return self._ongoing

    @property
    def cavity(self) -> 'NloLaserHeadStage1':
        return self._cavity

    @property
    def progress_data(self) -> 'DecopBinary':
        return self._progress_data


class NloLaserHeadStage1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._restore_on_abort = DecopBoolean(client, name + ':restore-on-abort')
        self._input = NloLaserHeadOptInput1(client, name + ':input')
        self._progress = DecopInteger(client, name + ':progress')
        self._optimization_in_progress = DecopBoolean(client, name + ':optimization-in-progress')
        self._regress_tolerance = DecopInteger(client, name + ':regress-tolerance')
        self._restore_on_regress = DecopBoolean(client, name + ':restore-on-regress')

    @property
    def restore_on_abort(self) -> 'DecopBoolean':
        return self._restore_on_abort

    @property
    def input(self) -> 'NloLaserHeadOptInput1':
        return self._input

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    @property
    def optimization_in_progress(self) -> 'DecopBoolean':
        return self._optimization_in_progress

    @property
    def regress_tolerance(self) -> 'DecopInteger':
        return self._regress_tolerance

    @property
    def restore_on_regress(self) -> 'DecopBoolean':
        return self._restore_on_regress


class NloLaserHeadOptInput1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_calibrated = DecopReal(client, name + ':value-calibrated')

    @property
    def value_calibrated(self) -> 'DecopReal':
        return self._value_calibrated


class NloLaserHeadScopeT1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._variant = DecopInteger(client, name + ':variant')
        self._channelx = NloLaserHeadScopeXAxisT1(client, name + ':channelx')
        self._channel1 = NloLaserHeadScopeChannelT1(client, name + ':channel1')
        self._timescale = DecopReal(client, name + ':timescale')
        self._data = DecopBinary(client, name + ':data')
        self._update_rate = DecopInteger(client, name + ':update-rate')
        self._channel2 = NloLaserHeadScopeChannelT1(client, name + ':channel2')

    @property
    def variant(self) -> 'DecopInteger':
        return self._variant

    @property
    def channelx(self) -> 'NloLaserHeadScopeXAxisT1':
        return self._channelx

    @property
    def channel1(self) -> 'NloLaserHeadScopeChannelT1':
        return self._channel1

    @property
    def timescale(self) -> 'DecopReal':
        return self._timescale

    @property
    def data(self) -> 'DecopBinary':
        return self._data

    @property
    def update_rate(self) -> 'DecopInteger':
        return self._update_rate

    @property
    def channel2(self) -> 'NloLaserHeadScopeChannelT1':
        return self._channel2


class NloLaserHeadScopeXAxisT1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scope_timescale = DecopReal(client, name + ':scope-timescale')
        self._spectrum_range = DecopReal(client, name + ':spectrum-range')
        self._xy_signal = DecopInteger(client, name + ':xy-signal')
        self._name = DecopString(client, name + ':name')
        self._unit = DecopString(client, name + ':unit')
        self._spectrum_omit_dc = DecopBoolean(client, name + ':spectrum-omit-dc')

    @property
    def scope_timescale(self) -> 'DecopReal':
        return self._scope_timescale

    @property
    def spectrum_range(self) -> 'DecopReal':
        return self._spectrum_range

    @property
    def xy_signal(self) -> 'DecopInteger':
        return self._xy_signal

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def spectrum_omit_dc(self) -> 'DecopBoolean':
        return self._spectrum_omit_dc


class NloLaserHeadScopeChannelT1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = DecopInteger(client, name + ':signal')
        self._name = DecopString(client, name + ':name')
        self._unit = DecopString(client, name + ':unit')
        self._enabled = DecopBoolean(client, name + ':enabled')

    @property
    def signal(self) -> 'DecopInteger':
        return self._signal

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled


class LaserAmp:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._seedonly_check = AmpSeedonlyCheck(client, name + ':seedonly-check')
        self._seed_limits = AmpPower(client, name + ':seed-limits')
        self._output_limits = AmpPower(client, name + ':output-limits')
        self._version = DecopString(client, name + ':version')
        self._legacy = DecopBoolean(client, name + ':legacy')
        self._ontime = DecopInteger(client, name + ':ontime')
        self._cc = Cc5000Drv(client, name + ':cc')
        self._tc = TcChannel2(client, name + ':tc')
        self._type_ = DecopString(client, name + ':type')
        self._factory_settings = AmpFactory(client, name + ':factory-settings')
        self._ontime_txt = DecopString(client, name + ':ontime-txt')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def seedonly_check(self) -> 'AmpSeedonlyCheck':
        return self._seedonly_check

    @property
    def seed_limits(self) -> 'AmpPower':
        return self._seed_limits

    @property
    def output_limits(self) -> 'AmpPower':
        return self._output_limits

    @property
    def version(self) -> 'DecopString':
        return self._version

    @property
    def legacy(self) -> 'DecopBoolean':
        return self._legacy

    @property
    def ontime(self) -> 'DecopInteger':
        return self._ontime

    @property
    def cc(self) -> 'Cc5000Drv':
        return self._cc

    @property
    def tc(self) -> 'TcChannel2':
        return self._tc

    @property
    def type_(self) -> 'DecopString':
        return self._type_

    @property
    def factory_settings(self) -> 'AmpFactory':
        return self._factory_settings

    @property
    def ontime_txt(self) -> 'DecopString':
        return self._ontime_txt

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)


class AmpSeedonlyCheck:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pump = DecopBoolean(client, name + ':pump')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._seed = DecopBoolean(client, name + ':seed')
        self._warning_delay = MutableDecopReal(client, name + ':warning-delay')
        self._status = DecopInteger(client, name + ':status')
        self._shutdown_delay = MutableDecopReal(client, name + ':shutdown-delay')

    @property
    def pump(self) -> 'DecopBoolean':
        return self._pump

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def seed(self) -> 'DecopBoolean':
        return self._seed

    @property
    def warning_delay(self) -> 'MutableDecopReal':
        return self._warning_delay

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def shutdown_delay(self) -> 'MutableDecopReal':
        return self._shutdown_delay


class AmpPower:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_min = MutableDecopReal(client, name + ':power-min')
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._power_max = MutableDecopReal(client, name + ':power-max')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._power_max_shutdown_delay = MutableDecopReal(client, name + ':power-max-shutdown-delay')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._power_min_shutdown_delay = MutableDecopReal(client, name + ':power-min-shutdown-delay')
        self._power_min_warning_delay = MutableDecopReal(client, name + ':power-min-warning-delay')
        self._status = DecopInteger(client, name + ':status')
        self._power_max_warning_delay = MutableDecopReal(client, name + ':power-max-warning-delay')
        self._power = DecopReal(client, name + ':power')

    @property
    def power_min(self) -> 'MutableDecopReal':
        return self._power_min

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def power_max(self) -> 'MutableDecopReal':
        return self._power_max

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def power_max_shutdown_delay(self) -> 'MutableDecopReal':
        return self._power_max_shutdown_delay

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def power_min_shutdown_delay(self) -> 'MutableDecopReal':
        return self._power_min_shutdown_delay

    @property
    def power_min_warning_delay(self) -> 'MutableDecopReal':
        return self._power_min_warning_delay

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def power_max_warning_delay(self) -> 'MutableDecopReal':
        return self._power_max_warning_delay

    @property
    def power(self) -> 'DecopReal':
        return self._power


class Cc5000Drv:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._emission = DecopBoolean(client, name + ':emission')
        self._current_act = DecopReal(client, name + ':current-act')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._current_set = MutableDecopReal(client, name + ':current-set')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._current_clip_limit = DecopReal(client, name + ':current-clip-limit')
        self._variant = DecopString(client, name + ':variant')
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._voltage_out = DecopReal(client, name + ':voltage-out')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._aux = DecopReal(client, name + ':aux')
        self._current_offset = MutableDecopReal(client, name + ':current-offset')
        self._forced_off = MutableDecopBoolean(client, name + ':forced-off')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._path = DecopString(client, name + ':path')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._status = DecopInteger(client, name + ':status')

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def current_clip_limit(self) -> 'DecopReal':
        return self._current_clip_limit

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def voltage_out(self) -> 'DecopReal':
        return self._voltage_out

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def aux(self) -> 'DecopReal':
        return self._aux

    @property
    def current_offset(self) -> 'MutableDecopReal':
        return self._current_offset

    @property
    def forced_off(self) -> 'MutableDecopBoolean':
        return self._forced_off

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def status(self) -> 'DecopInteger':
        return self._status


class TcChannel2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ntc_parallel_resistance = DecopReal(client, name + ':ntc-parallel-resistance')
        self._current_act = DecopReal(client, name + ':current-act')
        self._ready = DecopBoolean(client, name + ':ready')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._current_set = DecopReal(client, name + ':current-set')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._path = DecopString(client, name + ':path')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._temp_reset = MutableDecopBoolean(client, name + ':temp-reset')
        self._current_set_max = MutableDecopReal(client, name + ':current-set-max')
        self._temp_roc_limit = MutableDecopReal(client, name + ':temp-roc-limit')
        self._external_input = ExtInput2(client, name + ':external-input')
        self._c_loop = TcChannelCLoop2(client, name + ':c-loop')
        self._ntc_series_resistance = DecopReal(client, name + ':ntc-series-resistance')
        self._drv_voltage = DecopReal(client, name + ':drv-voltage')
        self._power_source = DecopInteger(client, name + ':power-source')
        self._limits = TcChannelCheck2(client, name + ':limits')
        self._current_set_min = MutableDecopReal(client, name + ':current-set-min')
        self._temp_act = DecopReal(client, name + ':temp-act')
        self._fault = DecopBoolean(client, name + ':fault')
        self._temp_set_max = MutableDecopReal(client, name + ':temp-set-max')
        self._resistance = DecopReal(client, name + ':resistance')
        self._temp_roc_enabled = MutableDecopBoolean(client, name + ':temp-roc-enabled')
        self._t_loop = TcChannelTLoop2(client, name + ':t-loop')
        self._status = DecopInteger(client, name + ':status')
        self._temp_set_min = MutableDecopReal(client, name + ':temp-set-min')
        self._temp_set = MutableDecopReal(client, name + ':temp-set')

    @property
    def ntc_parallel_resistance(self) -> 'DecopReal':
        return self._ntc_parallel_resistance

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def ready(self) -> 'DecopBoolean':
        return self._ready

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def current_set(self) -> 'DecopReal':
        return self._current_set

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def temp_reset(self) -> 'MutableDecopBoolean':
        return self._temp_reset

    @property
    def current_set_max(self) -> 'MutableDecopReal':
        return self._current_set_max

    @property
    def temp_roc_limit(self) -> 'MutableDecopReal':
        return self._temp_roc_limit

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input

    @property
    def c_loop(self) -> 'TcChannelCLoop2':
        return self._c_loop

    @property
    def ntc_series_resistance(self) -> 'DecopReal':
        return self._ntc_series_resistance

    @property
    def drv_voltage(self) -> 'DecopReal':
        return self._drv_voltage

    @property
    def power_source(self) -> 'DecopInteger':
        return self._power_source

    @property
    def limits(self) -> 'TcChannelCheck2':
        return self._limits

    @property
    def current_set_min(self) -> 'MutableDecopReal':
        return self._current_set_min

    @property
    def temp_act(self) -> 'DecopReal':
        return self._temp_act

    @property
    def fault(self) -> 'DecopBoolean':
        return self._fault

    @property
    def temp_set_max(self) -> 'MutableDecopReal':
        return self._temp_set_max

    @property
    def resistance(self) -> 'DecopReal':
        return self._resistance

    @property
    def temp_roc_enabled(self) -> 'MutableDecopBoolean':
        return self._temp_roc_enabled

    @property
    def t_loop(self) -> 'TcChannelTLoop2':
        return self._t_loop

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def temp_set_min(self) -> 'MutableDecopReal':
        return self._temp_set_min

    @property
    def temp_set(self) -> 'MutableDecopReal':
        return self._temp_set

    def check_peltier(self) -> float:
        return self.__client.exec(self.__name + ':check-peltier', input_stream=None, output_type=None, return_type=float)


class TcChannelCLoop2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._on = MutableDecopBoolean(client, name + ':on')
        self._i_gain = MutableDecopReal(client, name + ':i-gain')

    @property
    def on(self) -> 'MutableDecopBoolean':
        return self._on

    @property
    def i_gain(self) -> 'MutableDecopReal':
        return self._i_gain


class TcChannelCheck2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._timeout = MutableDecopInteger(client, name + ':timeout')
        self._out_of_range = DecopBoolean(client, name + ':out-of-range')
        self._temp_max = MutableDecopReal(client, name + ':temp-max')
        self._timed_out = DecopBoolean(client, name + ':timed-out')
        self._temp_min = MutableDecopReal(client, name + ':temp-min')

    @property
    def timeout(self) -> 'MutableDecopInteger':
        return self._timeout

    @property
    def out_of_range(self) -> 'DecopBoolean':
        return self._out_of_range

    @property
    def temp_max(self) -> 'MutableDecopReal':
        return self._temp_max

    @property
    def timed_out(self) -> 'DecopBoolean':
        return self._timed_out

    @property
    def temp_min(self) -> 'MutableDecopReal':
        return self._temp_min


class TcChannelTLoop2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._on = MutableDecopBoolean(client, name + ':on')
        self._ok_tolerance = MutableDecopReal(client, name + ':ok-tolerance')
        self._d_gain = MutableDecopReal(client, name + ':d-gain')
        self._ok_time = MutableDecopReal(client, name + ':ok-time')
        self._p_gain = MutableDecopReal(client, name + ':p-gain')
        self._i_gain = MutableDecopReal(client, name + ':i-gain')

    @property
    def on(self) -> 'MutableDecopBoolean':
        return self._on

    @property
    def ok_tolerance(self) -> 'MutableDecopReal':
        return self._ok_tolerance

    @property
    def d_gain(self) -> 'MutableDecopReal':
        return self._d_gain

    @property
    def ok_time(self) -> 'MutableDecopReal':
        return self._ok_time

    @property
    def p_gain(self) -> 'MutableDecopReal':
        return self._p_gain

    @property
    def i_gain(self) -> 'MutableDecopReal':
        return self._i_gain


class AmpFactory:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._seed_limits = AmpFactoryPower(client, name + ':seed-limits')
        self._cc = AmpFactoryCc(client, name + ':cc')
        self._tc = TcFactorySettings(client, name + ':tc')
        self._wavelength = MutableDecopReal(client, name + ':wavelength')
        self._seedonly_check = AmpFactorySeedonly(client, name + ':seedonly-check')
        self._last_modified = DecopString(client, name + ':last-modified')
        self._modified = DecopBoolean(client, name + ':modified')
        self._power = MutableDecopReal(client, name + ':power')
        self._output_limits = AmpFactoryPower(client, name + ':output-limits')

    @property
    def seed_limits(self) -> 'AmpFactoryPower':
        return self._seed_limits

    @property
    def cc(self) -> 'AmpFactoryCc':
        return self._cc

    @property
    def tc(self) -> 'TcFactorySettings':
        return self._tc

    @property
    def wavelength(self) -> 'MutableDecopReal':
        return self._wavelength

    @property
    def seedonly_check(self) -> 'AmpFactorySeedonly':
        return self._seedonly_check

    @property
    def last_modified(self) -> 'DecopString':
        return self._last_modified

    @property
    def modified(self) -> 'DecopBoolean':
        return self._modified

    @property
    def power(self) -> 'MutableDecopReal':
        return self._power

    @property
    def output_limits(self) -> 'AmpFactoryPower':
        return self._output_limits

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class AmpFactoryPower:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_min = MutableDecopReal(client, name + ':power-min')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')
        self._power_min_shutdown_delay = MutableDecopReal(client, name + ':power-min-shutdown-delay')
        self._power_max_warning_delay = MutableDecopReal(client, name + ':power-max-warning-delay')
        self._power_min_warning_delay = MutableDecopReal(client, name + ':power-min-warning-delay')
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._power_max_shutdown_delay = MutableDecopReal(client, name + ':power-max-shutdown-delay')
        self._power_max = MutableDecopReal(client, name + ':power-max')

    @property
    def power_min(self) -> 'MutableDecopReal':
        return self._power_min

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset

    @property
    def power_min_shutdown_delay(self) -> 'MutableDecopReal':
        return self._power_min_shutdown_delay

    @property
    def power_max_warning_delay(self) -> 'MutableDecopReal':
        return self._power_max_warning_delay

    @property
    def power_min_warning_delay(self) -> 'MutableDecopReal':
        return self._power_min_warning_delay

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def power_max_shutdown_delay(self) -> 'MutableDecopReal':
        return self._power_max_shutdown_delay

    @property
    def power_max(self) -> 'MutableDecopReal':
        return self._power_max


class AmpFactoryCc:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._current_clip_modified = DecopBoolean(client, name + ':current-clip-modified')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')
        self._current_clip_last_modified = DecopString(client, name + ':current-clip-last-modified')
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._current_set = MutableDecopReal(client, name + ':current-set')

    @property
    def current_clip_modified(self) -> 'DecopBoolean':
        return self._current_clip_modified

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip

    @property
    def current_clip_last_modified(self) -> 'DecopString':
        return self._current_clip_last_modified

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set


class TcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_source = MutableDecopInteger(client, name + ':power-source')
        self._ntc_parallel_resistance = MutableDecopReal(client, name + ':ntc-parallel-resistance')
        self._current_max = MutableDecopReal(client, name + ':current-max')
        self._current_min = MutableDecopReal(client, name + ':current-min')
        self._p_gain = MutableDecopReal(client, name + ':p-gain')
        self._temp_min = MutableDecopReal(client, name + ':temp-min')
        self._ntc_series_resistance = MutableDecopReal(client, name + ':ntc-series-resistance')
        self._timeout = MutableDecopInteger(client, name + ':timeout')
        self._ok_time = MutableDecopReal(client, name + ':ok-time')
        self._temp_max = MutableDecopReal(client, name + ':temp-max')
        self._ok_tolerance = MutableDecopReal(client, name + ':ok-tolerance')
        self._d_gain = MutableDecopReal(client, name + ':d-gain')
        self._temp_roc_enabled = MutableDecopBoolean(client, name + ':temp-roc-enabled')
        self._temp_roc_limit = MutableDecopReal(client, name + ':temp-roc-limit')
        self._i_gain = MutableDecopReal(client, name + ':i-gain')
        self._c_gain = MutableDecopReal(client, name + ':c-gain')
        self._temp_set = MutableDecopReal(client, name + ':temp-set')

    @property
    def power_source(self) -> 'MutableDecopInteger':
        return self._power_source

    @property
    def ntc_parallel_resistance(self) -> 'MutableDecopReal':
        return self._ntc_parallel_resistance

    @property
    def current_max(self) -> 'MutableDecopReal':
        return self._current_max

    @property
    def current_min(self) -> 'MutableDecopReal':
        return self._current_min

    @property
    def p_gain(self) -> 'MutableDecopReal':
        return self._p_gain

    @property
    def temp_min(self) -> 'MutableDecopReal':
        return self._temp_min

    @property
    def ntc_series_resistance(self) -> 'MutableDecopReal':
        return self._ntc_series_resistance

    @property
    def timeout(self) -> 'MutableDecopInteger':
        return self._timeout

    @property
    def ok_time(self) -> 'MutableDecopReal':
        return self._ok_time

    @property
    def temp_max(self) -> 'MutableDecopReal':
        return self._temp_max

    @property
    def ok_tolerance(self) -> 'MutableDecopReal':
        return self._ok_tolerance

    @property
    def d_gain(self) -> 'MutableDecopReal':
        return self._d_gain

    @property
    def temp_roc_enabled(self) -> 'MutableDecopBoolean':
        return self._temp_roc_enabled

    @property
    def temp_roc_limit(self) -> 'MutableDecopReal':
        return self._temp_roc_limit

    @property
    def i_gain(self) -> 'MutableDecopReal':
        return self._i_gain

    @property
    def c_gain(self) -> 'MutableDecopReal':
        return self._c_gain

    @property
    def temp_set(self) -> 'MutableDecopReal':
        return self._temp_set


class AmpFactorySeedonly:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._warning_delay = MutableDecopReal(client, name + ':warning-delay')
        self._shutdown_delay = MutableDecopReal(client, name + ':shutdown-delay')

    @property
    def warning_delay(self) -> 'MutableDecopReal':
        return self._warning_delay

    @property
    def shutdown_delay(self) -> 'MutableDecopReal':
        return self._shutdown_delay


class CtlT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._mode_control = CtlModeControl(client, name + ':mode-control')
        self._wavelength_max = DecopReal(client, name + ':wavelength-max')
        self._wavelength_set = MutableDecopReal(client, name + ':wavelength-set')
        self._head_temperature = DecopReal(client, name + ':head-temperature')
        self._wavelength_min = DecopReal(client, name + ':wavelength-min')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._tuning_power_min = DecopReal(client, name + ':tuning-power-min')
        self._power = CtlPower(client, name + ':power')
        self._scan = CtlScanT(client, name + ':scan')
        self._motor = CtlMotor(client, name + ':motor')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._tuning_current_min = DecopReal(client, name + ':tuning-current-min')
        self._state = DecopInteger(client, name + ':state')
        self._optimization = CtlOptimizationT(client, name + ':optimization')
        self._wavelength_act = DecopReal(client, name + ':wavelength-act')
        self._factory_settings = CtlFactory(client, name + ':factory-settings')
        self._remote_control = CtlRemoteControl(client, name + ':remote-control')

    @property
    def mode_control(self) -> 'CtlModeControl':
        return self._mode_control

    @property
    def wavelength_max(self) -> 'DecopReal':
        return self._wavelength_max

    @property
    def wavelength_set(self) -> 'MutableDecopReal':
        return self._wavelength_set

    @property
    def head_temperature(self) -> 'DecopReal':
        return self._head_temperature

    @property
    def wavelength_min(self) -> 'DecopReal':
        return self._wavelength_min

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def tuning_power_min(self) -> 'DecopReal':
        return self._tuning_power_min

    @property
    def power(self) -> 'CtlPower':
        return self._power

    @property
    def scan(self) -> 'CtlScanT':
        return self._scan

    @property
    def motor(self) -> 'CtlMotor':
        return self._motor

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def tuning_current_min(self) -> 'DecopReal':
        return self._tuning_current_min

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def optimization(self) -> 'CtlOptimizationT':
        return self._optimization

    @property
    def wavelength_act(self) -> 'DecopReal':
        return self._wavelength_act

    @property
    def factory_settings(self) -> 'CtlFactory':
        return self._factory_settings

    @property
    def remote_control(self) -> 'CtlRemoteControl':
        return self._remote_control


class CtlModeControl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._loop_enabled = MutableDecopBoolean(client, name + ':loop-enabled')

    @property
    def loop_enabled(self) -> 'MutableDecopBoolean':
        return self._loop_enabled


class CtlPower:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_act = DecopReal(client, name + ':power-act')

    @property
    def power_act(self) -> 'DecopReal':
        return self._power_act


class CtlScanT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._shape = MutableDecopInteger(client, name + ':shape')
        self._wavelength_end = MutableDecopReal(client, name + ':wavelength-end')
        self._microsteps = MutableDecopBoolean(client, name + ':microsteps')
        self._trigger = CtlTriggerT(client, name + ':trigger')
        self._speed = MutableDecopReal(client, name + ':speed')
        self._speed_min = DecopReal(client, name + ':speed-min')
        self._remaining_time = DecopInteger(client, name + ':remaining-time')
        self._wavelength_begin = MutableDecopReal(client, name + ':wavelength-begin')
        self._progress = DecopInteger(client, name + ':progress')
        self._speed_max = DecopReal(client, name + ':speed-max')
        self._continuous_mode = MutableDecopBoolean(client, name + ':continuous-mode')

    @property
    def shape(self) -> 'MutableDecopInteger':
        return self._shape

    @property
    def wavelength_end(self) -> 'MutableDecopReal':
        return self._wavelength_end

    @property
    def microsteps(self) -> 'MutableDecopBoolean':
        return self._microsteps

    @property
    def trigger(self) -> 'CtlTriggerT':
        return self._trigger

    @property
    def speed(self) -> 'MutableDecopReal':
        return self._speed

    @property
    def speed_min(self) -> 'DecopReal':
        return self._speed_min

    @property
    def remaining_time(self) -> 'DecopInteger':
        return self._remaining_time

    @property
    def wavelength_begin(self) -> 'MutableDecopReal':
        return self._wavelength_begin

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    @property
    def speed_max(self) -> 'DecopReal':
        return self._speed_max

    @property
    def continuous_mode(self) -> 'MutableDecopBoolean':
        return self._continuous_mode

    def stop(self) -> None:
        self.__client.exec(self.__name + ':stop', input_stream=None, output_type=None, return_type=None)

    def start(self) -> None:
        self.__client.exec(self.__name + ':start', input_stream=None, output_type=None, return_type=None)

    def pause(self) -> None:
        self.__client.exec(self.__name + ':pause', input_stream=None, output_type=None, return_type=None)

    def continue_(self) -> None:
        self.__client.exec(self.__name + ':continue', input_stream=None, output_type=None, return_type=None)


class CtlTriggerT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._output_threshold = MutableDecopReal(client, name + ':output-threshold')
        self._input_enabled = MutableDecopBoolean(client, name + ':input-enabled')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._output_enabled = MutableDecopBoolean(client, name + ':output-enabled')

    @property
    def output_threshold(self) -> 'MutableDecopReal':
        return self._output_threshold

    @property
    def input_enabled(self) -> 'MutableDecopBoolean':
        return self._input_enabled

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def output_enabled(self) -> 'MutableDecopBoolean':
        return self._output_enabled


class CtlMotor:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._position_accuracy_microstep = MutableDecopInteger(client, name + ':position-accuracy-microstep')
        self._position_hysteresis_microstep = MutableDecopInteger(client, name + ':position-hysteresis-microstep')
        self._position_accuracy_fullstep = MutableDecopInteger(client, name + ':position-accuracy-fullstep')
        self._power_save_disabled = MutableDecopBoolean(client, name + ':power-save-disabled')
        self._position_hysteresis_fullstep = MutableDecopInteger(client, name + ':position-hysteresis-fullstep')

    @property
    def position_accuracy_microstep(self) -> 'MutableDecopInteger':
        return self._position_accuracy_microstep

    @property
    def position_hysteresis_microstep(self) -> 'MutableDecopInteger':
        return self._position_hysteresis_microstep

    @property
    def position_accuracy_fullstep(self) -> 'MutableDecopInteger':
        return self._position_accuracy_fullstep

    @property
    def power_save_disabled(self) -> 'MutableDecopBoolean':
        return self._power_save_disabled

    @property
    def position_hysteresis_fullstep(self) -> 'MutableDecopInteger':
        return self._position_hysteresis_fullstep


class CtlOptimizationT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._progress = DecopInteger(client, name + ':progress')

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    def abort(self) -> None:
        self.__client.exec(self.__name + ':abort', input_stream=None, output_type=None, return_type=None)

    def smile(self) -> None:
        self.__client.exec(self.__name + ':smile', input_stream=None, output_type=None, return_type=None)

    def flow(self) -> None:
        self.__client.exec(self.__name + ':flow', input_stream=None, output_type=None, return_type=None)


class CtlFactory:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tuning_current_min = DecopReal(client, name + ':tuning-current-min')
        self._wavelength_min = DecopReal(client, name + ':wavelength-min')
        self._tuning_power_min = DecopReal(client, name + ':tuning-power-min')
        self._wavelength_max = DecopReal(client, name + ':wavelength-max')

    @property
    def tuning_current_min(self) -> 'DecopReal':
        return self._tuning_current_min

    @property
    def wavelength_min(self) -> 'DecopReal':
        return self._wavelength_min

    @property
    def tuning_power_min(self) -> 'DecopReal':
        return self._tuning_power_min

    @property
    def wavelength_max(self) -> 'DecopReal':
        return self._wavelength_max

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)


class CtlRemoteControl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = MutableDecopInteger(client, name + ':signal')
        self._factor = MutableDecopReal(client, name + ':factor')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._speed = MutableDecopReal(client, name + ':speed')

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal

    @property
    def factor(self) -> 'MutableDecopReal':
        return self._factor

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def speed(self) -> 'MutableDecopReal':
        return self._speed


class ScopeT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._variant = MutableDecopInteger(client, name + ':variant')
        self._channelx = ScopeXAxisT(client, name + ':channelx')
        self._channel1 = ScopeChannelT(client, name + ':channel1')
        self._timescale = MutableDecopReal(client, name + ':timescale')
        self._data = DecopBinary(client, name + ':data')
        self._update_rate = MutableDecopInteger(client, name + ':update-rate')
        self._channel2 = ScopeChannelT(client, name + ':channel2')

    @property
    def variant(self) -> 'MutableDecopInteger':
        return self._variant

    @property
    def channelx(self) -> 'ScopeXAxisT':
        return self._channelx

    @property
    def channel1(self) -> 'ScopeChannelT':
        return self._channel1

    @property
    def timescale(self) -> 'MutableDecopReal':
        return self._timescale

    @property
    def data(self) -> 'DecopBinary':
        return self._data

    @property
    def update_rate(self) -> 'MutableDecopInteger':
        return self._update_rate

    @property
    def channel2(self) -> 'ScopeChannelT':
        return self._channel2


class ScopeXAxisT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scope_timescale = MutableDecopReal(client, name + ':scope-timescale')
        self._unit = DecopString(client, name + ':unit')
        self._spectrum_range = MutableDecopReal(client, name + ':spectrum-range')
        self._xy_signal = MutableDecopInteger(client, name + ':xy-signal')
        self._name = DecopString(client, name + ':name')
        self._spectrum_omit_dc = MutableDecopBoolean(client, name + ':spectrum-omit-dc')

    @property
    def scope_timescale(self) -> 'MutableDecopReal':
        return self._scope_timescale

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def spectrum_range(self) -> 'MutableDecopReal':
        return self._spectrum_range

    @property
    def xy_signal(self) -> 'MutableDecopInteger':
        return self._xy_signal

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def spectrum_omit_dc(self) -> 'MutableDecopBoolean':
        return self._spectrum_omit_dc


class ScopeChannelT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = MutableDecopInteger(client, name + ':signal')
        self._name = DecopString(client, name + ':name')
        self._unit = DecopString(client, name + ':unit')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class Recorder:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._sample_count_set = MutableDecopInteger(client, name + ':sample-count-set')
        self._sampling_interval = DecopReal(client, name + ':sampling-interval')
        self._state = DecopInteger(client, name + ':state')
        self._sample_count = DecopInteger(client, name + ':sample-count')
        self._data = RecorderData(client, name + ':data')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._recording_time = MutableDecopReal(client, name + ':recording-time')
        self._signals = RecorderInputs(client, name + ':signals')

    @property
    def sample_count_set(self) -> 'MutableDecopInteger':
        return self._sample_count_set

    @property
    def sampling_interval(self) -> 'DecopReal':
        return self._sampling_interval

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def sample_count(self) -> 'DecopInteger':
        return self._sample_count

    @property
    def data(self) -> 'RecorderData':
        return self._data

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def recording_time(self) -> 'MutableDecopReal':
        return self._recording_time

    @property
    def signals(self) -> 'RecorderInputs':
        return self._signals


class RecorderData:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._zoom_data = DecopBinary(client, name + ':zoom-data')
        self._channel2 = RecorderChannel(client, name + ':channel2')
        self._channelx = RecorderChannel(client, name + ':channelx')
        self._recorded_sample_count = DecopInteger(client, name + ':recorded-sample-count')
        self._channel1 = RecorderChannel(client, name + ':channel1')
        self._zoom_offset = MutableDecopReal(client, name + ':zoom-offset')
        self._zoom_amplitude = MutableDecopReal(client, name + ':zoom-amplitude')

    @property
    def zoom_data(self) -> 'DecopBinary':
        return self._zoom_data

    @property
    def channel2(self) -> 'RecorderChannel':
        return self._channel2

    @property
    def channelx(self) -> 'RecorderChannel':
        return self._channelx

    @property
    def recorded_sample_count(self) -> 'DecopInteger':
        return self._recorded_sample_count

    @property
    def channel1(self) -> 'RecorderChannel':
        return self._channel1

    @property
    def zoom_offset(self) -> 'MutableDecopReal':
        return self._zoom_offset

    @property
    def zoom_amplitude(self) -> 'MutableDecopReal':
        return self._zoom_amplitude

    def get_data(self, start_index: int, count: int) -> bytes:
        assert isinstance(start_index, int), "expected type 'int' for parameter 'start_index', got '{}'".format(type(start_index))
        assert isinstance(count, int), "expected type 'int' for parameter 'count', got '{}'".format(type(count))
        return self.__client.exec(self.__name + ':get-data', start_index, count, input_stream=None, output_type=None, return_type=bytes)

    def show_data(self, start_index: int, count: int) -> None:
        assert isinstance(start_index, int), "expected type 'int' for parameter 'start_index', got '{}'".format(type(start_index))
        assert isinstance(count, int), "expected type 'int' for parameter 'count', got '{}'".format(type(count))
        self.__client.exec(self.__name + ':show-data', start_index, count, input_stream=None, output_type=None, return_type=None)

    def zoom_out(self) -> None:
        self.__client.exec(self.__name + ':zoom-out', input_stream=None, output_type=None, return_type=None)


class RecorderChannel:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = DecopInteger(client, name + ':signal')
        self._name = DecopString(client, name + ':name')
        self._unit = DecopString(client, name + ':unit')

    @property
    def signal(self) -> 'DecopInteger':
        return self._signal

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def unit(self) -> 'DecopString':
        return self._unit


class RecorderInputs:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._channel2 = MutableDecopInteger(client, name + ':channel2')
        self._channelx = MutableDecopInteger(client, name + ':channelx')
        self._channel1 = MutableDecopInteger(client, name + ':channel1')

    @property
    def channel2(self) -> 'MutableDecopInteger':
        return self._channel2

    @property
    def channelx(self) -> 'MutableDecopInteger':
        return self._channelx

    @property
    def channel1(self) -> 'MutableDecopInteger':
        return self._channel1


class LaserHead:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pressure_compensation = PressureCompensation(client, name + ':pressure-compensation')
        self._model = DecopString(client, name + ':model')
        self._version = DecopString(client, name + ':version')
        self._legacy = DecopBoolean(client, name + ':legacy')
        self._ontime = DecopInteger(client, name + ':ontime')
        self._pd = PdCal(client, name + ':pd')
        self._cc = CurrDrv1(client, name + ':cc')
        self._lock = Lock(client, name + ':lock')
        self._tc = TcChannel2(client, name + ':tc')
        self._pc = PiezoDrv2(client, name + ':pc')
        self._type_ = DecopString(client, name + ':type')
        self._factory_settings = LhFactory(client, name + ':factory-settings')
        self._ontime_txt = DecopString(client, name + ':ontime-txt')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def pressure_compensation(self) -> 'PressureCompensation':
        return self._pressure_compensation

    @property
    def model(self) -> 'DecopString':
        return self._model

    @property
    def version(self) -> 'DecopString':
        return self._version

    @property
    def legacy(self) -> 'DecopBoolean':
        return self._legacy

    @property
    def ontime(self) -> 'DecopInteger':
        return self._ontime

    @property
    def pd(self) -> 'PdCal':
        return self._pd

    @property
    def cc(self) -> 'CurrDrv1':
        return self._cc

    @property
    def lock(self) -> 'Lock':
        return self._lock

    @property
    def tc(self) -> 'TcChannel2':
        return self._tc

    @property
    def pc(self) -> 'PiezoDrv2':
        return self._pc

    @property
    def type_(self) -> 'DecopString':
        return self._type_

    @property
    def factory_settings(self) -> 'LhFactory':
        return self._factory_settings

    @property
    def ontime_txt(self) -> 'DecopString':
        return self._ontime_txt

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)


class PressureCompensation:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._offset = DecopReal(client, name + ':offset')
        self._air_pressure = DecopReal(client, name + ':air-pressure')
        self._factor = MutableDecopReal(client, name + ':factor')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._compensation_voltage = DecopReal(client, name + ':compensation-voltage')

    @property
    def offset(self) -> 'DecopReal':
        return self._offset

    @property
    def air_pressure(self) -> 'DecopReal':
        return self._air_pressure

    @property
    def factor(self) -> 'MutableDecopReal':
        return self._factor

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def compensation_voltage(self) -> 'DecopReal':
        return self._compensation_voltage


class PdCal:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._power = DecopReal(client, name + ':power')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def power(self) -> 'DecopReal':
        return self._power

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset


class CurrDrv1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._emission = DecopBoolean(client, name + ':emission')
        self._current_act = DecopReal(client, name + ':current-act')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._current_set = MutableDecopReal(client, name + ':current-set')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._positive_polarity = MutableDecopBoolean(client, name + ':positive-polarity')
        self._current_clip_limit = DecopReal(client, name + ':current-clip-limit')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._variant = DecopString(client, name + ':variant')
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._external_input = ExtInput2(client, name + ':external-input')
        self._aux = DecopReal(client, name + ':aux')
        self._current_offset = MutableDecopReal(client, name + ':current-offset')
        self._forced_off = MutableDecopBoolean(client, name + ':forced-off')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')
        self._snubber = MutableDecopBoolean(client, name + ':snubber')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._path = DecopString(client, name + ':path')
        self._current_set_dithering = MutableDecopBoolean(client, name + ':current-set-dithering')
        self._pd = DecopReal(client, name + ':pd')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._status = DecopInteger(client, name + ':status')

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def positive_polarity(self) -> 'MutableDecopBoolean':
        return self._positive_polarity

    @property
    def current_clip_limit(self) -> 'DecopReal':
        return self._current_clip_limit

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input

    @property
    def aux(self) -> 'DecopReal':
        return self._aux

    @property
    def current_offset(self) -> 'MutableDecopReal':
        return self._current_offset

    @property
    def forced_off(self) -> 'MutableDecopBoolean':
        return self._forced_off

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip

    @property
    def snubber(self) -> 'MutableDecopBoolean':
        return self._snubber

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def current_set_dithering(self) -> 'MutableDecopBoolean':
        return self._current_set_dithering

    @property
    def pd(self) -> 'DecopReal':
        return self._pd

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def status(self) -> 'DecopInteger':
        return self._status


class Lock:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid2 = Pid(client, name + ':pid2')
        self._pid_selection = MutableDecopInteger(client, name + ':pid-selection')
        self._hold = MutableDecopBoolean(client, name + ':hold')
        self._lock_tracking = Coordinate(client, name + ':lock-tracking')
        self._lock_without_lockpoint = MutableDecopBoolean(client, name + ':lock-without-lockpoint')
        self._pid1 = Pid(client, name + ':pid1')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._candidates = DecopBinary(client, name + ':candidates')
        self._spectrum_input_channel = MutableDecopInteger(client, name + ':spectrum-input-channel')
        self._locking_delay = MutableDecopInteger(client, name + ':locking-delay')
        self._candidate_filter = AlCandidateFilter(client, name + ':candidate-filter')
        self._lockpoint = AlLockpoint(client, name + ':lockpoint')
        self._background_trace = DecopBinary(client, name + ':background-trace')
        self._state = DecopInteger(client, name + ':state')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._lock_enabled = MutableDecopBoolean(client, name + ':lock-enabled')
        self._type_ = MutableDecopInteger(client, name + ':type')
        self._reset = AlReset(client, name + ':reset')
        self._window = AlWindow(client, name + ':window')
        self._lockin = Lockin(client, name + ':lockin')
        self._relock = AlRelock(client, name + ':relock')

    @property
    def pid2(self) -> 'Pid':
        return self._pid2

    @property
    def pid_selection(self) -> 'MutableDecopInteger':
        return self._pid_selection

    @property
    def hold(self) -> 'MutableDecopBoolean':
        return self._hold

    @property
    def lock_tracking(self) -> 'Coordinate':
        return self._lock_tracking

    @property
    def lock_without_lockpoint(self) -> 'MutableDecopBoolean':
        return self._lock_without_lockpoint

    @property
    def pid1(self) -> 'Pid':
        return self._pid1

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def candidates(self) -> 'DecopBinary':
        return self._candidates

    @property
    def spectrum_input_channel(self) -> 'MutableDecopInteger':
        return self._spectrum_input_channel

    @property
    def locking_delay(self) -> 'MutableDecopInteger':
        return self._locking_delay

    @property
    def candidate_filter(self) -> 'AlCandidateFilter':
        return self._candidate_filter

    @property
    def lockpoint(self) -> 'AlLockpoint':
        return self._lockpoint

    @property
    def background_trace(self) -> 'DecopBinary':
        return self._background_trace

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def lock_enabled(self) -> 'MutableDecopBoolean':
        return self._lock_enabled

    @property
    def type_(self) -> 'MutableDecopInteger':
        return self._type_

    @property
    def reset(self) -> 'AlReset':
        return self._reset

    @property
    def window(self) -> 'AlWindow':
        return self._window

    @property
    def lockin(self) -> 'Lockin':
        return self._lockin

    @property
    def relock(self) -> 'AlRelock':
        return self._relock

    def close(self) -> None:
        self.__client.exec(self.__name + ':close', input_stream=None, output_type=None, return_type=None)

    def open(self) -> None:
        self.__client.exec(self.__name + ':open', input_stream=None, output_type=None, return_type=None)

    def select_lockpoint(self, x: float, y: float, type_: int) -> None:
        assert isinstance(x, float), "expected type 'float' for parameter 'x', got '{}'".format(type(x))
        assert isinstance(y, float), "expected type 'float' for parameter 'y', got '{}'".format(type(y))
        assert isinstance(type_, int), "expected type 'int' for parameter 'type_', got '{}'".format(type(type_))
        self.__client.exec(self.__name + ':select-lockpoint', x, y, type_, input_stream=None, output_type=None, return_type=None)

    def show_candidates(self) -> Tuple[str, int]:
        return self.__client.exec(self.__name + ':show-candidates', input_stream=None, output_type=str, return_type=int)

    def find_candidates(self) -> None:
        self.__client.exec(self.__name + ':find-candidates', input_stream=None, output_type=None, return_type=None)


class Pid:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._hold_state = DecopBoolean(client, name + ':hold-state')
        self._hold = MutableDecopBoolean(client, name + ':hold')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._regulating_state = DecopBoolean(client, name + ':regulating-state')
        self._slope = MutableDecopBoolean(client, name + ':slope')
        self._gain = Gain(client, name + ':gain')
        self._sign = MutableDecopBoolean(client, name + ':sign')
        self._lock_state = DecopBoolean(client, name + ':lock-state')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._hold_output_on_unlock = MutableDecopBoolean(client, name + ':hold-output-on-unlock')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._output_channel = MutableDecopInteger(client, name + ':output-channel')
        self._outputlimit = Outputlimit(client, name + ':outputlimit')

    @property
    def hold_state(self) -> 'DecopBoolean':
        return self._hold_state

    @property
    def hold(self) -> 'MutableDecopBoolean':
        return self._hold

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def regulating_state(self) -> 'DecopBoolean':
        return self._regulating_state

    @property
    def slope(self) -> 'MutableDecopBoolean':
        return self._slope

    @property
    def gain(self) -> 'Gain':
        return self._gain

    @property
    def sign(self) -> 'MutableDecopBoolean':
        return self._sign

    @property
    def lock_state(self) -> 'DecopBoolean':
        return self._lock_state

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def hold_output_on_unlock(self) -> 'MutableDecopBoolean':
        return self._hold_output_on_unlock

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def output_channel(self) -> 'MutableDecopInteger':
        return self._output_channel

    @property
    def outputlimit(self) -> 'Outputlimit':
        return self._outputlimit


class Gain:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fc_ip = DecopReal(client, name + ':fc-ip')
        self._fc_pd = DecopReal(client, name + ':fc-pd')
        self._d = MutableDecopReal(client, name + ':d')
        self._p = MutableDecopReal(client, name + ':p')
        self._i = MutableDecopReal(client, name + ':i')
        self._all = MutableDecopReal(client, name + ':all')
        self._i_cutoff = MutableDecopReal(client, name + ':i-cutoff')
        self._i_cutoff_enabled = MutableDecopBoolean(client, name + ':i-cutoff-enabled')

    @property
    def fc_ip(self) -> 'DecopReal':
        return self._fc_ip

    @property
    def fc_pd(self) -> 'DecopReal':
        return self._fc_pd

    @property
    def d(self) -> 'MutableDecopReal':
        return self._d

    @property
    def p(self) -> 'MutableDecopReal':
        return self._p

    @property
    def i(self) -> 'MutableDecopReal':
        return self._i

    @property
    def all(self) -> 'MutableDecopReal':
        return self._all

    @property
    def i_cutoff(self) -> 'MutableDecopReal':
        return self._i_cutoff

    @property
    def i_cutoff_enabled(self) -> 'MutableDecopBoolean':
        return self._i_cutoff_enabled


class Outputlimit:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._max = MutableDecopReal(client, name + ':max')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def max(self) -> 'MutableDecopReal':
        return self._max

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class Coordinate:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name

    def get(self) -> Tuple[float, float]:
        return self.__client.get(self.__name)

    def set(self, x: float, y: float) -> None:
        assert isinstance(x, float), "expected type 'float' for 'x', got '{}'".format(type(x))
        assert isinstance(y, float), "expected type 'float' for 'y', got '{}'".format(type(y))
        self.__client.set(self.__name, x, y)


class AlCandidateFilter:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._peak_noise_tolerance = MutableDecopReal(client, name + ':peak-noise-tolerance')
        self._negative_edge = MutableDecopBoolean(client, name + ':negative-edge')
        self._positive_edge = MutableDecopBoolean(client, name + ':positive-edge')
        self._top = MutableDecopBoolean(client, name + ':top')
        self._edge_min_distance = MutableDecopInteger(client, name + ':edge-min-distance')
        self._bottom = MutableDecopBoolean(client, name + ':bottom')
        self._edge_level = MutableDecopReal(client, name + ':edge-level')

    @property
    def peak_noise_tolerance(self) -> 'MutableDecopReal':
        return self._peak_noise_tolerance

    @property
    def negative_edge(self) -> 'MutableDecopBoolean':
        return self._negative_edge

    @property
    def positive_edge(self) -> 'MutableDecopBoolean':
        return self._positive_edge

    @property
    def top(self) -> 'MutableDecopBoolean':
        return self._top

    @property
    def edge_min_distance(self) -> 'MutableDecopInteger':
        return self._edge_min_distance

    @property
    def bottom(self) -> 'MutableDecopBoolean':
        return self._bottom

    @property
    def edge_level(self) -> 'MutableDecopReal':
        return self._edge_level


class AlLockpoint:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._position = Coordinate(client, name + ':position')
        self._type_ = DecopString(client, name + ':type')

    @property
    def position(self) -> 'Coordinate':
        return self._position

    @property
    def type_(self) -> 'DecopString':
        return self._type_


class AlReset:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class AlWindow:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._level_high = MutableDecopReal(client, name + ':level-high')
        self._level_hysteresis = MutableDecopReal(client, name + ':level-hysteresis')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._level_low = MutableDecopReal(client, name + ':level-low')

    @property
    def level_high(self) -> 'MutableDecopReal':
        return self._level_high

    @property
    def level_hysteresis(self) -> 'MutableDecopReal':
        return self._level_hysteresis

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def level_low(self) -> 'MutableDecopReal':
        return self._level_low


class Lockin:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._phase_shift = MutableDecopReal(client, name + ':phase-shift')
        self._modulation_output_channel = MutableDecopInteger(client, name + ':modulation-output-channel')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._lock_level = MutableDecopReal(client, name + ':lock-level')
        self._auto_lir = AutoLir(client, name + ':auto-lir')
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._modulation_enabled = MutableDecopBoolean(client, name + ':modulation-enabled')

    @property
    def phase_shift(self) -> 'MutableDecopReal':
        return self._phase_shift

    @property
    def modulation_output_channel(self) -> 'MutableDecopInteger':
        return self._modulation_output_channel

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def lock_level(self) -> 'MutableDecopReal':
        return self._lock_level

    @property
    def auto_lir(self) -> 'AutoLir':
        return self._auto_lir

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def modulation_enabled(self) -> 'MutableDecopBoolean':
        return self._modulation_enabled


class AutoLir:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._progress = DecopInteger(client, name + ':progress')

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    def auto_lir(self) -> None:
        self.__client.exec(self.__name + ':auto-lir', input_stream=None, output_type=None, return_type=None)


class AlRelock:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._output_channel = MutableDecopInteger(client, name + ':output-channel')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._delay = MutableDecopReal(client, name + ':delay')

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def output_channel(self) -> 'MutableDecopInteger':
        return self._output_channel

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def delay(self) -> 'MutableDecopReal':
        return self._delay


class PiezoDrv2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._voltage_set = MutableDecopReal(client, name + ':voltage-set')
        self._heatsink_temp = DecopReal(client, name + ':heatsink-temp')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._external_input = ExtInput2(client, name + ':external-input')
        self._voltage_set_dithering = MutableDecopBoolean(client, name + ':voltage-set-dithering')
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._path = DecopString(client, name + ':path')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def voltage_set(self) -> 'MutableDecopReal':
        return self._voltage_set

    @property
    def heatsink_temp(self) -> 'DecopReal':
        return self._heatsink_temp

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input

    @property
    def voltage_set_dithering(self) -> 'MutableDecopBoolean':
        return self._voltage_set_dithering

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled


class LhFactory:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._threshold_current = MutableDecopReal(client, name + ':threshold-current')
        self._wavelength = MutableDecopReal(client, name + ':wavelength')
        self._pc = PcFactorySettings(client, name + ':pc')
        self._tc = TcFactorySettings(client, name + ':tc')
        self._cc = LhFactoryCc(client, name + ':cc')
        self._pd = LhFactoryPd(client, name + ':pd')
        self._modified = DecopBoolean(client, name + ':modified')
        self._power = MutableDecopReal(client, name + ':power')
        self._last_modified = DecopString(client, name + ':last-modified')

    @property
    def threshold_current(self) -> 'MutableDecopReal':
        return self._threshold_current

    @property
    def wavelength(self) -> 'MutableDecopReal':
        return self._wavelength

    @property
    def pc(self) -> 'PcFactorySettings':
        return self._pc

    @property
    def tc(self) -> 'TcFactorySettings':
        return self._tc

    @property
    def cc(self) -> 'LhFactoryCc':
        return self._cc

    @property
    def pd(self) -> 'LhFactoryPd':
        return self._pd

    @property
    def modified(self) -> 'DecopBoolean':
        return self._modified

    @property
    def power(self) -> 'MutableDecopReal':
        return self._power

    @property
    def last_modified(self) -> 'DecopString':
        return self._last_modified

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class PcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._pressure_compensation_factor = MutableDecopReal(client, name + ':pressure-compensation-factor')
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')
        self._scan_offset = MutableDecopReal(client, name + ':scan-offset')
        self._capacitance = MutableDecopReal(client, name + ':capacitance')
        self._scan_amplitude = MutableDecopReal(client, name + ':scan-amplitude')
        self._slew_rate_enabled = MutableDecopBoolean(client, name + ':slew-rate-enabled')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._slew_rate = MutableDecopReal(client, name + ':slew-rate')

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def pressure_compensation_factor(self) -> 'MutableDecopReal':
        return self._pressure_compensation_factor

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max

    @property
    def scan_offset(self) -> 'MutableDecopReal':
        return self._scan_offset

    @property
    def capacitance(self) -> 'MutableDecopReal':
        return self._capacitance

    @property
    def scan_amplitude(self) -> 'MutableDecopReal':
        return self._scan_amplitude

    @property
    def slew_rate_enabled(self) -> 'MutableDecopBoolean':
        return self._slew_rate_enabled

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def slew_rate(self) -> 'MutableDecopReal':
        return self._slew_rate


class LhFactoryCc:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._current_clip_modified = DecopBoolean(client, name + ':current-clip-modified')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')
        self._current_clip_last_modified = DecopString(client, name + ':current-clip-last-modified')
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._current_set = MutableDecopReal(client, name + ':current-set')
        self._snubber = MutableDecopBoolean(client, name + ':snubber')
        self._positive_polarity = MutableDecopBoolean(client, name + ':positive-polarity')

    @property
    def current_clip_modified(self) -> 'DecopBoolean':
        return self._current_clip_modified

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip

    @property
    def current_clip_last_modified(self) -> 'DecopString':
        return self._current_clip_last_modified

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set

    @property
    def snubber(self) -> 'MutableDecopBoolean':
        return self._snubber

    @property
    def positive_polarity(self) -> 'MutableDecopBoolean':
        return self._positive_polarity


class LhFactoryPd:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset


class Nlo:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pd = NloLaserHeadPhotoDiodes(client, name + ':pd')
        self._fhg = Fhg(client, name + ':fhg')
        self._ssw_ver = DecopString(client, name + ':ssw-ver')
        self._power_optimization = NloLaserHeadPowerOptimization(client, name + ':power-optimization')
        self._shg = Shg(client, name + ':shg')
        self._servo = NloLaserHeadServos(client, name + ':servo')

    @property
    def pd(self) -> 'NloLaserHeadPhotoDiodes':
        return self._pd

    @property
    def fhg(self) -> 'Fhg':
        return self._fhg

    @property
    def ssw_ver(self) -> 'DecopString':
        return self._ssw_ver

    @property
    def power_optimization(self) -> 'NloLaserHeadPowerOptimization':
        return self._power_optimization

    @property
    def shg(self) -> 'Shg':
        return self._shg

    @property
    def servo(self) -> 'NloLaserHeadServos':
        return self._servo


class NloLaserHeadPhotoDiodes:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._shg_pdh_dc = NloLaserHeadNloDigilockPhotodiode2(client, name + ':shg-pdh-dc')
        self._shg_pdh_rf = NloLaserHeadNloPdhPhotodiode2(client, name + ':shg-pdh-rf')
        self._dl = NloLaserHeadNloPhotodiode2(client, name + ':dl')
        self._fiber = NloLaserHeadNloPhotodiode2(client, name + ':fiber')
        self._fhg = NloLaserHeadNloPhotodiode2(client, name + ':fhg')
        self._fhg_pdh_dc = NloLaserHeadNloDigilockPhotodiode2(client, name + ':fhg-pdh-dc')
        self._fhg_pdh_rf = NloLaserHeadNloPdhPhotodiode2(client, name + ':fhg-pdh-rf')
        self._shg = NloLaserHeadNloPhotodiode2(client, name + ':shg')
        self._fhg_int = NloLaserHeadNloDigilockPhotodiode2(client, name + ':fhg-int')
        self._amp = NloLaserHeadNloPhotodiode2(client, name + ':amp')
        self._shg_int = NloLaserHeadNloDigilockPhotodiode2(client, name + ':shg-int')

    @property
    def shg_pdh_dc(self) -> 'NloLaserHeadNloDigilockPhotodiode2':
        return self._shg_pdh_dc

    @property
    def shg_pdh_rf(self) -> 'NloLaserHeadNloPdhPhotodiode2':
        return self._shg_pdh_rf

    @property
    def dl(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._dl

    @property
    def fiber(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._fiber

    @property
    def fhg(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._fhg

    @property
    def fhg_pdh_dc(self) -> 'NloLaserHeadNloDigilockPhotodiode2':
        return self._fhg_pdh_dc

    @property
    def fhg_pdh_rf(self) -> 'NloLaserHeadNloPdhPhotodiode2':
        return self._fhg_pdh_rf

    @property
    def shg(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._shg

    @property
    def fhg_int(self) -> 'NloLaserHeadNloDigilockPhotodiode2':
        return self._fhg_int

    @property
    def amp(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._amp

    @property
    def shg_int(self) -> 'NloLaserHeadNloDigilockPhotodiode2':
        return self._shg_int


class NloLaserHeadNloDigilockPhotodiode2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset


class NloLaserHeadNloPdhPhotodiode2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._gain = MutableDecopReal(client, name + ':gain')

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def gain(self) -> 'MutableDecopReal':
        return self._gain


class NloLaserHeadNloPhotodiode2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._power = DecopReal(client, name + ':power')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def power(self) -> 'DecopReal':
        return self._power

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset


class Fhg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scope = NloLaserHeadScopeT2(client, name + ':scope')
        self._scan = NloLaserHeadSiggen2(client, name + ':scan')
        self._lock = NloLaserHeadLockFhg(client, name + ':lock')
        self._tc = TcChannel2(client, name + ':tc')
        self._pc = PiezoDrv2(client, name + ':pc')
        self._factory_settings = FhgFactorySettings(client, name + ':factory-settings')

    @property
    def scope(self) -> 'NloLaserHeadScopeT2':
        return self._scope

    @property
    def scan(self) -> 'NloLaserHeadSiggen2':
        return self._scan

    @property
    def lock(self) -> 'NloLaserHeadLockFhg':
        return self._lock

    @property
    def tc(self) -> 'TcChannel2':
        return self._tc

    @property
    def pc(self) -> 'PiezoDrv2':
        return self._pc

    @property
    def factory_settings(self) -> 'FhgFactorySettings':
        return self._factory_settings

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadScopeT2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._variant = MutableDecopInteger(client, name + ':variant')
        self._channelx = NloLaserHeadScopeXAxisT2(client, name + ':channelx')
        self._channel1 = NloLaserHeadScopeChannelT2(client, name + ':channel1')
        self._timescale = MutableDecopReal(client, name + ':timescale')
        self._data = DecopBinary(client, name + ':data')
        self._update_rate = MutableDecopInteger(client, name + ':update-rate')
        self._channel2 = NloLaserHeadScopeChannelT2(client, name + ':channel2')

    @property
    def variant(self) -> 'MutableDecopInteger':
        return self._variant

    @property
    def channelx(self) -> 'NloLaserHeadScopeXAxisT2':
        return self._channelx

    @property
    def channel1(self) -> 'NloLaserHeadScopeChannelT2':
        return self._channel1

    @property
    def timescale(self) -> 'MutableDecopReal':
        return self._timescale

    @property
    def data(self) -> 'DecopBinary':
        return self._data

    @property
    def update_rate(self) -> 'MutableDecopInteger':
        return self._update_rate

    @property
    def channel2(self) -> 'NloLaserHeadScopeChannelT2':
        return self._channel2


class NloLaserHeadScopeXAxisT2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scope_timescale = MutableDecopReal(client, name + ':scope-timescale')
        self._spectrum_range = MutableDecopReal(client, name + ':spectrum-range')
        self._xy_signal = MutableDecopInteger(client, name + ':xy-signal')
        self._name = DecopString(client, name + ':name')
        self._unit = DecopString(client, name + ':unit')
        self._spectrum_omit_dc = MutableDecopBoolean(client, name + ':spectrum-omit-dc')

    @property
    def scope_timescale(self) -> 'MutableDecopReal':
        return self._scope_timescale

    @property
    def spectrum_range(self) -> 'MutableDecopReal':
        return self._spectrum_range

    @property
    def xy_signal(self) -> 'MutableDecopInteger':
        return self._xy_signal

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def spectrum_omit_dc(self) -> 'MutableDecopBoolean':
        return self._spectrum_omit_dc


class NloLaserHeadScopeChannelT2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = MutableDecopInteger(client, name + ':signal')
        self._name = DecopString(client, name + ':name')
        self._unit = DecopString(client, name + ':unit')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class NloLaserHeadSiggen2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._offset = MutableDecopReal(client, name + ':offset')

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def offset(self) -> 'MutableDecopReal':
        return self._offset


class NloLaserHeadLockFhg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid_selection = MutableDecopInteger(client, name + ':pid-selection')
        self._cavity_fast_pzt_voltage = MutableDecopReal(client, name + ':cavity-fast-pzt-voltage')
        self._local_oscillator = NloLaserHeadLocalOscillatorFhg(client, name + ':local-oscillator')
        self._pid1 = NloLaserHeadPid2(client, name + ':pid1')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._cavity_slow_pzt_voltage = MutableDecopReal(client, name + ':cavity-slow-pzt-voltage')
        self._background_trace = DecopBinary(client, name + ':background-trace')
        self._state = DecopInteger(client, name + ':state')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._lock_enabled = MutableDecopBoolean(client, name + ':lock-enabled')
        self._pid2 = NloLaserHeadPid2(client, name + ':pid2')
        self._window = NloLaserHeadWindow2(client, name + ':window')
        self._relock = NloLaserHeadRelock2(client, name + ':relock')

    @property
    def pid_selection(self) -> 'MutableDecopInteger':
        return self._pid_selection

    @property
    def cavity_fast_pzt_voltage(self) -> 'MutableDecopReal':
        return self._cavity_fast_pzt_voltage

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorFhg':
        return self._local_oscillator

    @property
    def pid1(self) -> 'NloLaserHeadPid2':
        return self._pid1

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def cavity_slow_pzt_voltage(self) -> 'MutableDecopReal':
        return self._cavity_slow_pzt_voltage

    @property
    def background_trace(self) -> 'DecopBinary':
        return self._background_trace

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def lock_enabled(self) -> 'MutableDecopBoolean':
        return self._lock_enabled

    @property
    def pid2(self) -> 'NloLaserHeadPid2':
        return self._pid2

    @property
    def window(self) -> 'NloLaserHeadWindow2':
        return self._window

    @property
    def relock(self) -> 'NloLaserHeadRelock2':
        return self._relock


class NloLaserHeadLocalOscillatorFhg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._phase_shift = MutableDecopReal(client, name + ':phase-shift')
        self._coupled_modulation = MutableDecopBoolean(client, name + ':coupled-modulation')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._use_fast_oscillator = MutableDecopBoolean(client, name + ':use-fast-oscillator')
        self._attenuation_raw = MutableDecopInteger(client, name + ':attenuation-raw')

    @property
    def phase_shift(self) -> 'MutableDecopReal':
        return self._phase_shift

    @property
    def coupled_modulation(self) -> 'MutableDecopBoolean':
        return self._coupled_modulation

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def use_fast_oscillator(self) -> 'MutableDecopBoolean':
        return self._use_fast_oscillator

    @property
    def attenuation_raw(self) -> 'MutableDecopInteger':
        return self._attenuation_raw

    def auto_pdh(self) -> None:
        self.__client.exec(self.__name + ':auto-pdh', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadPid2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._gain = NloLaserHeadGain2(client, name + ':gain')

    @property
    def gain(self) -> 'NloLaserHeadGain2':
        return self._gain


class NloLaserHeadGain2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._p = MutableDecopReal(client, name + ':p')
        self._i = MutableDecopReal(client, name + ':i')
        self._d = MutableDecopReal(client, name + ':d')
        self._all = MutableDecopReal(client, name + ':all')
        self._i_cutoff = MutableDecopReal(client, name + ':i-cutoff')
        self._i_cutoff_enabled = MutableDecopBoolean(client, name + ':i-cutoff-enabled')

    @property
    def p(self) -> 'MutableDecopReal':
        return self._p

    @property
    def i(self) -> 'MutableDecopReal':
        return self._i

    @property
    def d(self) -> 'MutableDecopReal':
        return self._d

    @property
    def all(self) -> 'MutableDecopReal':
        return self._all

    @property
    def i_cutoff(self) -> 'MutableDecopReal':
        return self._i_cutoff

    @property
    def i_cutoff_enabled(self) -> 'MutableDecopBoolean':
        return self._i_cutoff_enabled


class NloLaserHeadWindow2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._level_hysteresis = MutableDecopReal(client, name + ':level-hysteresis')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._threshold = MutableDecopReal(client, name + ':threshold')

    @property
    def level_hysteresis(self) -> 'MutableDecopReal':
        return self._level_hysteresis

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def threshold(self) -> 'MutableDecopReal':
        return self._threshold


class NloLaserHeadRelock2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._delay = MutableDecopReal(client, name + ':delay')

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def delay(self) -> 'MutableDecopReal':
        return self._delay


class FhgFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = NloLaserHeadTcFactorySettings(client, name + ':tc')
        self._pc = NloLaserHeadPcFactorySettings(client, name + ':pc')
        self._lock = NloLaserHeadLockFactorySettings(client, name + ':lock')
        self._modified = DecopBoolean(client, name + ':modified')
        self._pd = NloLaserHeadFhgPhotodiodesFactorySettings(client, name + ':pd')

    @property
    def tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._tc

    @property
    def pc(self) -> 'NloLaserHeadPcFactorySettings':
        return self._pc

    @property
    def lock(self) -> 'NloLaserHeadLockFactorySettings':
        return self._lock

    @property
    def modified(self) -> 'DecopBoolean':
        return self._modified

    @property
    def pd(self) -> 'NloLaserHeadFhgPhotodiodesFactorySettings':
        return self._pd

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadFhgPhotodiodesFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fhg = NloLaserHeadPdFactorySettings(client, name + ':fhg')
        self._pdh_rf = NloLaserHeadPdPdhFactorySettings(client, name + ':pdh-rf')
        self._pdh_dc = NloLaserHeadPdDigilockFactorySettings(client, name + ':pdh-dc')
        self._int = NloLaserHeadPdDigilockFactorySettings(client, name + ':int')

    @property
    def fhg(self) -> 'NloLaserHeadPdFactorySettings':
        return self._fhg

    @property
    def pdh_rf(self) -> 'NloLaserHeadPdPdhFactorySettings':
        return self._pdh_rf

    @property
    def pdh_dc(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._pdh_dc

    @property
    def int(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._int


class NloLaserHeadPowerOptimization:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._progress_data_fhg = DecopBinary(client, name + ':progress-data-fhg')
        self._status_string = DecopString(client, name + ':status-string')
        self._abort = MutableDecopBoolean(client, name + ':abort')
        self._stage3 = NloLaserHeadStage2(client, name + ':stage3')
        self._progress_data_amp = DecopBinary(client, name + ':progress-data-amp')
        self._stage5 = NloLaserHeadStage2(client, name + ':stage5')
        self._stage2 = NloLaserHeadStage2(client, name + ':stage2')
        self._stage4 = NloLaserHeadStage2(client, name + ':stage4')
        self._progress_data_shg = DecopBinary(client, name + ':progress-data-shg')
        self._shg_advanced = MutableDecopBoolean(client, name + ':shg-advanced')
        self._progress = DecopInteger(client, name + ':progress')
        self._stage1 = NloLaserHeadStage2(client, name + ':stage1')
        self._status = DecopInteger(client, name + ':status')
        self._ongoing = DecopBoolean(client, name + ':ongoing')
        self._progress_data_fiber = DecopBinary(client, name + ':progress-data-fiber')

    @property
    def progress_data_fhg(self) -> 'DecopBinary':
        return self._progress_data_fhg

    @property
    def status_string(self) -> 'DecopString':
        return self._status_string

    @property
    def abort(self) -> 'MutableDecopBoolean':
        return self._abort

    @property
    def stage3(self) -> 'NloLaserHeadStage2':
        return self._stage3

    @property
    def progress_data_amp(self) -> 'DecopBinary':
        return self._progress_data_amp

    @property
    def stage5(self) -> 'NloLaserHeadStage2':
        return self._stage5

    @property
    def stage2(self) -> 'NloLaserHeadStage2':
        return self._stage2

    @property
    def stage4(self) -> 'NloLaserHeadStage2':
        return self._stage4

    @property
    def progress_data_shg(self) -> 'DecopBinary':
        return self._progress_data_shg

    @property
    def shg_advanced(self) -> 'MutableDecopBoolean':
        return self._shg_advanced

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    @property
    def stage1(self) -> 'NloLaserHeadStage2':
        return self._stage1

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def ongoing(self) -> 'DecopBoolean':
        return self._ongoing

    @property
    def progress_data_fiber(self) -> 'DecopBinary':
        return self._progress_data_fiber

    def start_optimization_all(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-all', input_stream=None, output_type=None, return_type=int)

    def start_optimization_fhg(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-fhg', input_stream=None, output_type=None, return_type=int)

    def start_optimization_shg(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-shg', input_stream=None, output_type=None, return_type=int)

    def start_optimization_fiber(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-fiber', input_stream=None, output_type=None, return_type=int)

    def start_optimization_amp(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-amp', input_stream=None, output_type=None, return_type=int)


class NloLaserHeadStage2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._restore_on_abort = MutableDecopBoolean(client, name + ':restore-on-abort')
        self._input = NloLaserHeadOptInput2(client, name + ':input')
        self._progress = DecopInteger(client, name + ':progress')
        self._optimization_in_progress = DecopBoolean(client, name + ':optimization-in-progress')
        self._regress_tolerance = MutableDecopInteger(client, name + ':regress-tolerance')
        self._restore_on_regress = MutableDecopBoolean(client, name + ':restore-on-regress')

    @property
    def restore_on_abort(self) -> 'MutableDecopBoolean':
        return self._restore_on_abort

    @property
    def input(self) -> 'NloLaserHeadOptInput2':
        return self._input

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    @property
    def optimization_in_progress(self) -> 'DecopBoolean':
        return self._optimization_in_progress

    @property
    def regress_tolerance(self) -> 'MutableDecopInteger':
        return self._regress_tolerance

    @property
    def restore_on_regress(self) -> 'MutableDecopBoolean':
        return self._restore_on_regress

    def start_optimization(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization', input_stream=None, output_type=None, return_type=int)


class NloLaserHeadOptInput2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_calibrated = DecopReal(client, name + ':value-calibrated')

    @property
    def value_calibrated(self) -> 'DecopReal':
        return self._value_calibrated


class Shg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scope = NloLaserHeadScopeT2(client, name + ':scope')
        self._scan = NloLaserHeadSiggen2(client, name + ':scan')
        self._lock = NloLaserHeadLockShg2(client, name + ':lock')
        self._tc = TcChannel2(client, name + ':tc')
        self._pc = PiezoDrv2(client, name + ':pc')
        self._factory_settings = ShgFactorySettings(client, name + ':factory-settings')

    @property
    def scope(self) -> 'NloLaserHeadScopeT2':
        return self._scope

    @property
    def scan(self) -> 'NloLaserHeadSiggen2':
        return self._scan

    @property
    def lock(self) -> 'NloLaserHeadLockShg2':
        return self._lock

    @property
    def tc(self) -> 'TcChannel2':
        return self._tc

    @property
    def pc(self) -> 'PiezoDrv2':
        return self._pc

    @property
    def factory_settings(self) -> 'ShgFactorySettings':
        return self._factory_settings

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadLockShg2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid_selection = MutableDecopInteger(client, name + ':pid-selection')
        self._cavity_fast_pzt_voltage = MutableDecopReal(client, name + ':cavity-fast-pzt-voltage')
        self._local_oscillator = NloLaserHeadLocalOscillatorShg2(client, name + ':local-oscillator')
        self._pid1 = NloLaserHeadPid2(client, name + ':pid1')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._cavity_slow_pzt_voltage = MutableDecopReal(client, name + ':cavity-slow-pzt-voltage')
        self._analog_dl_gain = NloLaserHeadMinifalc2(client, name + ':analog-dl-gain')
        self._background_trace = DecopBinary(client, name + ':background-trace')
        self._state = DecopInteger(client, name + ':state')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._lock_enabled = MutableDecopBoolean(client, name + ':lock-enabled')
        self._pid2 = NloLaserHeadPid2(client, name + ':pid2')
        self._window = NloLaserHeadWindow2(client, name + ':window')
        self._relock = NloLaserHeadRelock2(client, name + ':relock')

    @property
    def pid_selection(self) -> 'MutableDecopInteger':
        return self._pid_selection

    @property
    def cavity_fast_pzt_voltage(self) -> 'MutableDecopReal':
        return self._cavity_fast_pzt_voltage

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorShg2':
        return self._local_oscillator

    @property
    def pid1(self) -> 'NloLaserHeadPid2':
        return self._pid1

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def cavity_slow_pzt_voltage(self) -> 'MutableDecopReal':
        return self._cavity_slow_pzt_voltage

    @property
    def analog_dl_gain(self) -> 'NloLaserHeadMinifalc2':
        return self._analog_dl_gain

    @property
    def background_trace(self) -> 'DecopBinary':
        return self._background_trace

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def lock_enabled(self) -> 'MutableDecopBoolean':
        return self._lock_enabled

    @property
    def pid2(self) -> 'NloLaserHeadPid2':
        return self._pid2

    @property
    def window(self) -> 'NloLaserHeadWindow2':
        return self._window

    @property
    def relock(self) -> 'NloLaserHeadRelock2':
        return self._relock


class NloLaserHeadLocalOscillatorShg2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._phase_shift = MutableDecopReal(client, name + ':phase-shift')
        self._coupled_modulation = MutableDecopBoolean(client, name + ':coupled-modulation')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._use_external_oscillator = MutableDecopBoolean(client, name + ':use-external-oscillator')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._use_fast_oscillator = MutableDecopBoolean(client, name + ':use-fast-oscillator')
        self._attenuation_raw = MutableDecopInteger(client, name + ':attenuation-raw')

    @property
    def phase_shift(self) -> 'MutableDecopReal':
        return self._phase_shift

    @property
    def coupled_modulation(self) -> 'MutableDecopBoolean':
        return self._coupled_modulation

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def use_external_oscillator(self) -> 'MutableDecopBoolean':
        return self._use_external_oscillator

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def use_fast_oscillator(self) -> 'MutableDecopBoolean':
        return self._use_fast_oscillator

    @property
    def attenuation_raw(self) -> 'MutableDecopInteger':
        return self._attenuation_raw

    def auto_pdh(self) -> None:
        self.__client.exec(self.__name + ':auto-pdh', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadMinifalc2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._p_gain = MutableDecopReal(client, name + ':p-gain')

    @property
    def p_gain(self) -> 'MutableDecopReal':
        return self._p_gain


class ShgFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = NloLaserHeadTcFactorySettings(client, name + ':tc')
        self._pc = NloLaserHeadPcFactorySettings(client, name + ':pc')
        self._lock = NloLaserHeadLockFactorySettings(client, name + ':lock')
        self._modified = DecopBoolean(client, name + ':modified')
        self._pd = NloLaserHeadShgPhotodiodesFactorySettings(client, name + ':pd')

    @property
    def tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._tc

    @property
    def pc(self) -> 'NloLaserHeadPcFactorySettings':
        return self._pc

    @property
    def lock(self) -> 'NloLaserHeadLockFactorySettings':
        return self._lock

    @property
    def modified(self) -> 'DecopBoolean':
        return self._modified

    @property
    def pd(self) -> 'NloLaserHeadShgPhotodiodesFactorySettings':
        return self._pd

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadShgPhotodiodesFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fiber = NloLaserHeadPdFactorySettings(client, name + ':fiber')
        self._shg = NloLaserHeadPdFactorySettings(client, name + ':shg')
        self._pdh_dc = NloLaserHeadPdDigilockFactorySettings(client, name + ':pdh-dc')
        self._int = NloLaserHeadPdDigilockFactorySettings(client, name + ':int')
        self._pdh_rf = NloLaserHeadPdPdhFactorySettings(client, name + ':pdh-rf')

    @property
    def fiber(self) -> 'NloLaserHeadPdFactorySettings':
        return self._fiber

    @property
    def shg(self) -> 'NloLaserHeadPdFactorySettings':
        return self._shg

    @property
    def pdh_dc(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._pdh_dc

    @property
    def int(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._int

    @property
    def pdh_rf(self) -> 'NloLaserHeadPdPdhFactorySettings':
        return self._pdh_rf


class NloLaserHeadServos:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ta1_vert = NloLaserHeadServoPwm2(client, name + ':ta1-vert')
        self._ta2_hor = NloLaserHeadServoPwm2(client, name + ':ta2-hor')
        self._shg1_vert = NloLaserHeadServoPwm2(client, name + ':shg1-vert')
        self._uv_outcpl = NloLaserHeadServoPwm2(client, name + ':uv-outcpl')
        self._shg1_hor = NloLaserHeadServoPwm2(client, name + ':shg1-hor')
        self._fhg1_hor = NloLaserHeadServoPwm2(client, name + ':fhg1-hor')
        self._fiber1_hor = NloLaserHeadServoPwm2(client, name + ':fiber1-hor')
        self._fiber2_vert = NloLaserHeadServoPwm2(client, name + ':fiber2-vert')
        self._fiber2_hor = NloLaserHeadServoPwm2(client, name + ':fiber2-hor')
        self._ta1_hor = NloLaserHeadServoPwm2(client, name + ':ta1-hor')
        self._ta2_vert = NloLaserHeadServoPwm2(client, name + ':ta2-vert')
        self._fiber1_vert = NloLaserHeadServoPwm2(client, name + ':fiber1-vert')
        self._uv_cryst = NloLaserHeadServoPwm2(client, name + ':uv-cryst')
        self._shg2_hor = NloLaserHeadServoPwm2(client, name + ':shg2-hor')
        self._fhg2_hor = NloLaserHeadServoPwm2(client, name + ':fhg2-hor')
        self._fhg1_vert = NloLaserHeadServoPwm2(client, name + ':fhg1-vert')
        self._fhg2_vert = NloLaserHeadServoPwm2(client, name + ':fhg2-vert')
        self._shg2_vert = NloLaserHeadServoPwm2(client, name + ':shg2-vert')

    @property
    def ta1_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._ta1_vert

    @property
    def ta2_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._ta2_hor

    @property
    def shg1_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._shg1_vert

    @property
    def uv_outcpl(self) -> 'NloLaserHeadServoPwm2':
        return self._uv_outcpl

    @property
    def shg1_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._shg1_hor

    @property
    def fhg1_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._fhg1_hor

    @property
    def fiber1_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._fiber1_hor

    @property
    def fiber2_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._fiber2_vert

    @property
    def fiber2_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._fiber2_hor

    @property
    def ta1_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._ta1_hor

    @property
    def ta2_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._ta2_vert

    @property
    def fiber1_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._fiber1_vert

    @property
    def uv_cryst(self) -> 'NloLaserHeadServoPwm2':
        return self._uv_cryst

    @property
    def shg2_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._shg2_hor

    @property
    def fhg2_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._fhg2_hor

    @property
    def fhg1_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._fhg1_vert

    @property
    def fhg2_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._fhg2_vert

    @property
    def shg2_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._shg2_vert

    def center_fiber_servos(self) -> None:
        self.__client.exec(self.__name + ':center-fiber-servos', input_stream=None, output_type=None, return_type=None)

    def center_fhg_servos(self) -> None:
        self.__client.exec(self.__name + ':center-fhg-servos', input_stream=None, output_type=None, return_type=None)

    def center_shg_servos(self) -> None:
        self.__client.exec(self.__name + ':center-shg-servos', input_stream=None, output_type=None, return_type=None)

    def center_ta_servos(self) -> None:
        self.__client.exec(self.__name + ':center-ta-servos', input_stream=None, output_type=None, return_type=None)

    def center_all_servos(self) -> None:
        self.__client.exec(self.__name + ':center-all-servos', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadServoPwm2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._value = MutableDecopInteger(client, name + ':value')
        self._display_name = DecopString(client, name + ':display-name')

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def value(self) -> 'MutableDecopInteger':
        return self._value

    @property
    def display_name(self) -> 'DecopString':
        return self._display_name

    def center_servo(self) -> None:
        self.__client.exec(self.__name + ':center-servo', input_stream=None, output_type=None, return_type=None)


class PwrStab:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._input_channel_value_act = DecopReal(client, name + ':input-channel-value-act')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._gain = PwrStabGain2(client, name + ':gain')
        self._sign = MutableDecopBoolean(client, name + ':sign')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._hold_output_on_unlock = MutableDecopBoolean(client, name + ':hold-output-on-unlock')
        self._state = DecopInteger(client, name + ':state')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._window = PwrStabWindow(client, name + ':window')
        self._output_channel = DecopInteger(client, name + ':output-channel')

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def input_channel_value_act(self) -> 'DecopReal':
        return self._input_channel_value_act

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def gain(self) -> 'PwrStabGain2':
        return self._gain

    @property
    def sign(self) -> 'MutableDecopBoolean':
        return self._sign

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def hold_output_on_unlock(self) -> 'MutableDecopBoolean':
        return self._hold_output_on_unlock

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def window(self) -> 'PwrStabWindow':
        return self._window

    @property
    def output_channel(self) -> 'DecopInteger':
        return self._output_channel


class PwrStabGain2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._d = MutableDecopReal(client, name + ':d')
        self._p = MutableDecopReal(client, name + ':p')
        self._i = MutableDecopReal(client, name + ':i')
        self._all = MutableDecopReal(client, name + ':all')

    @property
    def d(self) -> 'MutableDecopReal':
        return self._d

    @property
    def p(self) -> 'MutableDecopReal':
        return self._p

    @property
    def i(self) -> 'MutableDecopReal':
        return self._i

    @property
    def all(self) -> 'MutableDecopReal':
        return self._all


class PwrStabWindow:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._level_hysteresis = MutableDecopReal(client, name + ':level-hysteresis')
        self._level_low = MutableDecopReal(client, name + ':level-low')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def level_hysteresis(self) -> 'MutableDecopReal':
        return self._level_hysteresis

    @property
    def level_low(self) -> 'MutableDecopReal':
        return self._level_low

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class ScanGenerator:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._phase_shift = MutableDecopReal(client, name + ':phase-shift')
        self._end = MutableDecopReal(client, name + ':end')
        self._unit = DecopString(client, name + ':unit')
        self._hold = MutableDecopBoolean(client, name + ':hold')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._offset = MutableDecopReal(client, name + ':offset')
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._start = MutableDecopReal(client, name + ':start')
        self._signal_type = MutableDecopInteger(client, name + ':signal-type')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._output_channel = MutableDecopInteger(client, name + ':output-channel')

    @property
    def phase_shift(self) -> 'MutableDecopReal':
        return self._phase_shift

    @property
    def end(self) -> 'MutableDecopReal':
        return self._end

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def hold(self) -> 'MutableDecopBoolean':
        return self._hold

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def offset(self) -> 'MutableDecopReal':
        return self._offset

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def start(self) -> 'MutableDecopReal':
        return self._start

    @property
    def signal_type(self) -> 'MutableDecopInteger':
        return self._signal_type

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def output_channel(self) -> 'MutableDecopInteger':
        return self._output_channel


class PdExt:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._power = DecopReal(client, name + ':power')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def power(self) -> 'DecopReal':
        return self._power

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset


class Dpss2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._operation_time = DecopReal(client, name + ':operation-time')
        self._power_act = DecopReal(client, name + ':power-act')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._error_txt = DecopString(client, name + ':error-txt')
        self._tc_status_txt = DecopString(client, name + ':tc-status-txt')
        self._power_margin = DecopReal(client, name + ':power-margin')
        self._error_code = DecopInteger(client, name + ':error-code')
        self._current_act = DecopReal(client, name + ':current-act')
        self._tc_status = DecopInteger(client, name + ':tc-status')
        self._current_max = DecopReal(client, name + ':current-max')
        self._power_set = MutableDecopReal(client, name + ':power-set')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._power_max = DecopReal(client, name + ':power-max')

    @property
    def operation_time(self) -> 'DecopReal':
        return self._operation_time

    @property
    def power_act(self) -> 'DecopReal':
        return self._power_act

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def error_txt(self) -> 'DecopString':
        return self._error_txt

    @property
    def tc_status_txt(self) -> 'DecopString':
        return self._tc_status_txt

    @property
    def power_margin(self) -> 'DecopReal':
        return self._power_margin

    @property
    def error_code(self) -> 'DecopInteger':
        return self._error_code

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def tc_status(self) -> 'DecopInteger':
        return self._tc_status

    @property
    def current_max(self) -> 'DecopReal':
        return self._current_max

    @property
    def power_set(self) -> 'MutableDecopReal':
        return self._power_set

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def power_max(self) -> 'DecopReal':
        return self._power_max


class UvShgLaser:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._emission = DecopBoolean(client, name + ':emission')
        self._power_set = MutableDecopReal(client, name + ':power-set')
        self._power_act = DecopReal(client, name + ':power-act')
        self._operation_time_uv = DecopReal(client, name + ':operation-time-uv')
        self._remaining_optics_spots = DecopInteger(client, name + ':remaining-optics-spots')
        self._error_txt = DecopString(client, name + ':error-txt')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._operation_time_pump = DecopReal(client, name + ':operation-time-pump')
        self._pump_power_margin = DecopReal(client, name + ':pump-power-margin')
        self._error = DecopInteger(client, name + ':error')

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def power_set(self) -> 'MutableDecopReal':
        return self._power_set

    @property
    def power_act(self) -> 'DecopReal':
        return self._power_act

    @property
    def operation_time_uv(self) -> 'DecopReal':
        return self._operation_time_uv

    @property
    def remaining_optics_spots(self) -> 'DecopInteger':
        return self._remaining_optics_spots

    @property
    def error_txt(self) -> 'DecopString':
        return self._error_txt

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def operation_time_pump(self) -> 'DecopReal':
        return self._operation_time_pump

    @property
    def pump_power_margin(self) -> 'DecopReal':
        return self._pump_power_margin

    @property
    def error(self) -> 'DecopInteger':
        return self._error

    def perform_optimization(self) -> None:
        self.__client.exec(self.__name + ':perform-optimization', input_stream=None, output_type=None, return_type=None)

    def clear_errors(self) -> None:
        self.__client.exec(self.__name + ':clear-errors', input_stream=None, output_type=None, return_type=None)


class Display:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._state = DecopInteger(client, name + ':state')
        self._auto_dark = MutableDecopBoolean(client, name + ':auto-dark')
        self._brightness = MutableDecopReal(client, name + ':brightness')
        self._idle_timeout = MutableDecopInteger(client, name + ':idle-timeout')

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def auto_dark(self) -> 'MutableDecopBoolean':
        return self._auto_dark

    @property
    def brightness(self) -> 'MutableDecopReal':
        return self._brightness

    @property
    def idle_timeout(self) -> 'MutableDecopInteger':
        return self._idle_timeout

    def update_state(self, active: bool) -> None:
        assert isinstance(active, bool), "expected type 'bool' for parameter 'active', got '{}'".format(type(active))
        self.__client.exec(self.__name + ':update-state', active, input_stream=None, output_type=None, return_type=None)


class PowerSupply:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_15V = DecopReal(client, name + ':voltage-15V')
        self._voltage_3V3 = DecopReal(client, name + ':voltage-3V3')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._revision = DecopString(client, name + ':revision')
        self._heatsink_temp = DecopReal(client, name + ':heatsink-temp')
        self._current_15Vn = DecopReal(client, name + ':current-15Vn')
        self._serial_number = DecopString(client, name + ':serial-number')
        self._load = DecopReal(client, name + ':load')
        self._voltage_15Vn = DecopReal(client, name + ':voltage-15Vn')
        self._voltage_5V = DecopReal(client, name + ':voltage-5V')
        self._current_5V = DecopReal(client, name + ':current-5V')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._status = DecopInteger(client, name + ':status')
        self._current_15V = DecopReal(client, name + ':current-15V')
        self._type_ = DecopString(client, name + ':type')

    @property
    def voltage_15V(self) -> 'DecopReal':
        return self._voltage_15V

    @property
    def voltage_3V3(self) -> 'DecopReal':
        return self._voltage_3V3

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def heatsink_temp(self) -> 'DecopReal':
        return self._heatsink_temp

    @property
    def current_15Vn(self) -> 'DecopReal':
        return self._current_15Vn

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def load(self) -> 'DecopReal':
        return self._load

    @property
    def voltage_15Vn(self) -> 'DecopReal':
        return self._voltage_15Vn

    @property
    def voltage_5V(self) -> 'DecopReal':
        return self._voltage_5V

    @property
    def current_5V(self) -> 'DecopReal':
        return self._current_5V

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def current_15V(self) -> 'DecopReal':
        return self._current_15V

    @property
    def type_(self) -> 'DecopString':
        return self._type_


class CcBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._channel1 = CurrDrv2(client, name + ':channel1')
        self._revision = DecopString(client, name + ':revision')
        self._channel2 = CurrDrv2(client, name + ':channel2')
        self._slot = DecopString(client, name + ':slot')
        self._variant = DecopString(client, name + ':variant')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._status = DecopInteger(client, name + ':status')
        self._parallel_mode = DecopBoolean(client, name + ':parallel-mode')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def channel1(self) -> 'CurrDrv2':
        return self._channel1

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def channel2(self) -> 'CurrDrv2':
        return self._channel2

    @property
    def slot(self) -> 'DecopString':
        return self._slot

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def parallel_mode(self) -> 'DecopBoolean':
        return self._parallel_mode

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number


class CurrDrv2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._emission = DecopBoolean(client, name + ':emission')
        self._current_act = DecopReal(client, name + ':current-act')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._current_set = MutableDecopReal(client, name + ':current-set')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._positive_polarity = MutableDecopBoolean(client, name + ':positive-polarity')
        self._current_clip_limit = DecopReal(client, name + ':current-clip-limit')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._variant = DecopString(client, name + ':variant')
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._external_input = ExtInput3(client, name + ':external-input')
        self._aux = DecopReal(client, name + ':aux')
        self._current_offset = MutableDecopReal(client, name + ':current-offset')
        self._forced_off = MutableDecopBoolean(client, name + ':forced-off')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')
        self._snubber = MutableDecopBoolean(client, name + ':snubber')
        self._output_filter = OutputFilter3(client, name + ':output-filter')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._path = DecopString(client, name + ':path')
        self._current_set_dithering = MutableDecopBoolean(client, name + ':current-set-dithering')
        self._pd = DecopReal(client, name + ':pd')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._status = DecopInteger(client, name + ':status')

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def positive_polarity(self) -> 'MutableDecopBoolean':
        return self._positive_polarity

    @property
    def current_clip_limit(self) -> 'DecopReal':
        return self._current_clip_limit

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def external_input(self) -> 'ExtInput3':
        return self._external_input

    @property
    def aux(self) -> 'DecopReal':
        return self._aux

    @property
    def current_offset(self) -> 'MutableDecopReal':
        return self._current_offset

    @property
    def forced_off(self) -> 'MutableDecopBoolean':
        return self._forced_off

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip

    @property
    def snubber(self) -> 'MutableDecopBoolean':
        return self._snubber

    @property
    def output_filter(self) -> 'OutputFilter3':
        return self._output_filter

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def current_set_dithering(self) -> 'MutableDecopBoolean':
        return self._current_set_dithering

    @property
    def pd(self) -> 'DecopReal':
        return self._pd

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def status(self) -> 'DecopInteger':
        return self._status


class ExtInput3:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = MutableDecopInteger(client, name + ':signal')
        self._factor = MutableDecopReal(client, name + ':factor')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal

    @property
    def factor(self) -> 'MutableDecopReal':
        return self._factor

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class OutputFilter3:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slew_rate_enabled = MutableDecopBoolean(client, name + ':slew-rate-enabled')
        self._slew_rate_limited = DecopBoolean(client, name + ':slew-rate-limited')
        self._slew_rate = MutableDecopReal(client, name + ':slew-rate')

    @property
    def slew_rate_enabled(self) -> 'MutableDecopBoolean':
        return self._slew_rate_enabled

    @property
    def slew_rate_limited(self) -> 'DecopBoolean':
        return self._slew_rate_limited

    @property
    def slew_rate(self) -> 'MutableDecopReal':
        return self._slew_rate


class Cc5000Board:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._channel1 = Cc5000Drv(client, name + ':channel1')
        self._revision = DecopString(client, name + ':revision')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._regulator_temp = DecopReal(client, name + ':regulator-temp')
        self._slot = DecopString(client, name + ':slot')
        self._variant = DecopString(client, name + ':variant')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._power_15v = MutableDecopBoolean(client, name + ':power-15v')
        self._inverter_temp_fuse = DecopReal(client, name + ':inverter-temp-fuse')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._status = DecopInteger(client, name + ':status')
        self._parallel_mode = DecopBoolean(client, name + ':parallel-mode')
        self._inverter_temp = DecopReal(client, name + ':inverter-temp')
        self._regulator_temp_fuse = DecopReal(client, name + ':regulator-temp-fuse')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def channel1(self) -> 'Cc5000Drv':
        return self._channel1

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def regulator_temp(self) -> 'DecopReal':
        return self._regulator_temp

    @property
    def slot(self) -> 'DecopString':
        return self._slot

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def power_15v(self) -> 'MutableDecopBoolean':
        return self._power_15v

    @property
    def inverter_temp_fuse(self) -> 'DecopReal':
        return self._inverter_temp_fuse

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def parallel_mode(self) -> 'DecopBoolean':
        return self._parallel_mode

    @property
    def inverter_temp(self) -> 'DecopReal':
        return self._inverter_temp

    @property
    def regulator_temp_fuse(self) -> 'DecopReal':
        return self._regulator_temp_fuse

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number


class PcBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slot = DecopString(client, name + ':slot')
        self._variant = DecopString(client, name + ':variant')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._channel1 = PiezoDrv3(client, name + ':channel1')
        self._revision = DecopString(client, name + ':revision')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._channel_count = DecopInteger(client, name + ':channel-count')
        self._channel2 = PiezoDrv3(client, name + ':channel2')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def slot(self) -> 'DecopString':
        return self._slot

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def channel1(self) -> 'PiezoDrv3':
        return self._channel1

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def channel_count(self) -> 'DecopInteger':
        return self._channel_count

    @property
    def channel2(self) -> 'PiezoDrv3':
        return self._channel2

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number


class PiezoDrv3:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._voltage_set = MutableDecopReal(client, name + ':voltage-set')
        self._heatsink_temp = DecopReal(client, name + ':heatsink-temp')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._external_input = ExtInput3(client, name + ':external-input')
        self._voltage_set_dithering = MutableDecopBoolean(client, name + ':voltage-set-dithering')
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._output_filter = OutputFilter3(client, name + ':output-filter')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._path = DecopString(client, name + ':path')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def voltage_set(self) -> 'MutableDecopReal':
        return self._voltage_set

    @property
    def heatsink_temp(self) -> 'DecopReal':
        return self._heatsink_temp

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def external_input(self) -> 'ExtInput3':
        return self._external_input

    @property
    def voltage_set_dithering(self) -> 'MutableDecopBoolean':
        return self._voltage_set_dithering

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def output_filter(self) -> 'OutputFilter3':
        return self._output_filter

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled


class Standby:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._state = DecopInteger(client, name + ':state')
        self._laser1 = StandbyLaser(client, name + ':laser1')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def laser1(self) -> 'StandbyLaser':
        return self._laser1

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class StandbyLaser:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._dl = StandbyDl(client, name + ':dl')
        self._amp = StandbyAmp(client, name + ':amp')
        self._nlo = StandbyShg(client, name + ':nlo')

    @property
    def dl(self) -> 'StandbyDl':
        return self._dl

    @property
    def amp(self) -> 'StandbyAmp':
        return self._amp

    @property
    def nlo(self) -> 'StandbyShg':
        return self._nlo


class StandbyDl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._disable_pc = MutableDecopBoolean(client, name + ':disable-pc')
        self._disable_tc = MutableDecopBoolean(client, name + ':disable-tc')
        self._disable_cc = MutableDecopBoolean(client, name + ':disable-cc')

    @property
    def disable_pc(self) -> 'MutableDecopBoolean':
        return self._disable_pc

    @property
    def disable_tc(self) -> 'MutableDecopBoolean':
        return self._disable_tc

    @property
    def disable_cc(self) -> 'MutableDecopBoolean':
        return self._disable_cc


class StandbyAmp:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._disable_tc = MutableDecopBoolean(client, name + ':disable-tc')
        self._disable_cc = MutableDecopBoolean(client, name + ':disable-cc')

    @property
    def disable_tc(self) -> 'MutableDecopBoolean':
        return self._disable_tc

    @property
    def disable_cc(self) -> 'MutableDecopBoolean':
        return self._disable_cc


class StandbyShg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._disable_pc = MutableDecopBoolean(client, name + ':disable-pc')
        self._disable_power_stabilization = MutableDecopBoolean(client, name + ':disable-power-stabilization')
        self._disable_tc = MutableDecopBoolean(client, name + ':disable-tc')
        self._disable_cavity_lock = MutableDecopBoolean(client, name + ':disable-cavity-lock')
        self._disable_servo_subsystem = MutableDecopBoolean(client, name + ':disable-servo-subsystem')

    @property
    def disable_pc(self) -> 'MutableDecopBoolean':
        return self._disable_pc

    @property
    def disable_power_stabilization(self) -> 'MutableDecopBoolean':
        return self._disable_power_stabilization

    @property
    def disable_tc(self) -> 'MutableDecopBoolean':
        return self._disable_tc

    @property
    def disable_cavity_lock(self) -> 'MutableDecopBoolean':
        return self._disable_cavity_lock

    @property
    def disable_servo_subsystem(self) -> 'MutableDecopBoolean':
        return self._disable_servo_subsystem


class Buzzer:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._welcome = MutableDecopString(client, name + ':welcome')

    @property
    def welcome(self) -> 'MutableDecopString':
        return self._welcome

    def play_welcome(self) -> None:
        self.__client.exec(self.__name + ':play-welcome', input_stream=None, output_type=None, return_type=None)

    def play(self, melody: str) -> None:
        assert isinstance(melody, str), "expected type 'str' for parameter 'melody', got '{}'".format(type(melody))
        self.__client.exec(self.__name + ':play', melody, input_stream=None, output_type=None, return_type=None)


class TcBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slot = DecopString(client, name + ':slot')
        self._channel2 = TcChannel2(client, name + ':channel2')
        self._fpga_fw_ver = DecopString(client, name + ':fpga-fw-ver')
        self._channel1 = TcChannel2(client, name + ':channel1')
        self._revision = DecopString(client, name + ':revision')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def slot(self) -> 'DecopString':
        return self._slot

    @property
    def channel2(self) -> 'TcChannel2':
        return self._channel2

    @property
    def fpga_fw_ver(self) -> 'DecopString':
        return self._fpga_fw_ver

    @property
    def channel1(self) -> 'TcChannel2':
        return self._channel1

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number


class McBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fpga_fw_ver = DecopString(client, name + ':fpga-fw-ver')
        self._revision = DecopString(client, name + ':revision')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._air_pressure = DecopReal(client, name + ':air-pressure')
        self._relative_humidity = DecopReal(client, name + ':relative-humidity')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def fpga_fw_ver(self) -> 'DecopString':
        return self._fpga_fw_ver

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def air_pressure(self) -> 'DecopReal':
        return self._air_pressure

    @property
    def relative_humidity(self) -> 'DecopReal':
        return self._relative_humidity

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number


class Ipconfig:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._dhcp = DecopBoolean(client, name + ':dhcp')
        self._mac_addr = DecopString(client, name + ':mac-addr')
        self._cmd_port = DecopInteger(client, name + ':cmd-port')
        self._net_mask = DecopString(client, name + ':net-mask')
        self._mon_port = DecopInteger(client, name + ':mon-port')
        self._ip_addr = DecopString(client, name + ':ip-addr')

    @property
    def dhcp(self) -> 'DecopBoolean':
        return self._dhcp

    @property
    def mac_addr(self) -> 'DecopString':
        return self._mac_addr

    @property
    def cmd_port(self) -> 'DecopInteger':
        return self._cmd_port

    @property
    def net_mask(self) -> 'DecopString':
        return self._net_mask

    @property
    def mon_port(self) -> 'DecopInteger':
        return self._mon_port

    @property
    def ip_addr(self) -> 'DecopString':
        return self._ip_addr

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def set_ip(self, ip_addr: str, net_mask: str) -> None:
        assert isinstance(ip_addr, str), "expected type 'str' for parameter 'ip_addr', got '{}'".format(type(ip_addr))
        assert isinstance(net_mask, str), "expected type 'str' for parameter 'net_mask', got '{}'".format(type(net_mask))
        self.__client.exec(self.__name + ':set-ip', ip_addr, net_mask, input_stream=None, output_type=None, return_type=None)

    def set_dhcp(self) -> None:
        self.__client.exec(self.__name + ':set-dhcp', input_stream=None, output_type=None, return_type=None)


class DLCpro:
    def __init__(self, connection: Connection) -> None:
        self.__client = Client(connection)
        self._tan = DecopInteger(self.__client, 'tan')
        self._licenses = Licenses(self.__client, 'licenses')
        self._fw_update = FwUpdate(self.__client, 'fw-update')
        self._system_service_report = ServiceReport(self.__client, 'system-service-report')
        self._time = MutableDecopString(self.__client, 'time')
        self._system_messages = SystemMessages(self.__client, 'system-messages')
        self._decof_svn_revision = DecopString(self.__client, 'decof-svn-revision')
        self._fw_ver = DecopString(self.__client, 'fw-ver')
        self._system_type = DecopString(self.__client, 'system-type')
        self._uptime = DecopInteger(self.__client, 'uptime')
        self._ssw_ver = DecopString(self.__client, 'ssw-ver')
        self._decof_ver = DecopString(self.__client, 'decof-ver')
        self._build_information = BuildInformation(self.__client, 'build-information')
        self._uptime_txt = DecopString(self.__client, 'uptime-txt')
        self._system_label = MutableDecopString(self.__client, 'system-label')
        self._echo = MutableDecopBoolean(self.__client, 'echo')
        self._system_model = DecopString(self.__client, 'system-model')
        self._svn_revision = DecopString(self.__client, 'svn-revision')
        self._ssw_svn_revision = DecopString(self.__client, 'ssw-svn-revision')
        self._serial_number = DecopString(self.__client, 'serial-number')
        self._io = IoBoard(self.__client, 'io')
        self._emission = DecopBoolean(self.__client, 'emission')
        self._laser1 = Laser(self.__client, 'laser1')
        self._uv = UvShgLaser(self.__client, 'uv')
        self._display = Display(self.__client, 'display')
        self._system_health = DecopInteger(self.__client, 'system-health')
        self._power_supply = PowerSupply(self.__client, 'power-supply')
        self._interlock_open = DecopBoolean(self.__client, 'interlock-open')
        self._cc2 = CcBoard(self.__client, 'cc2')
        self._ampcc2 = Cc5000Board(self.__client, 'ampcc2')
        self._pc1 = PcBoard(self.__client, 'pc1')
        self._pc2 = PcBoard(self.__client, 'pc2')
        self._standby = Standby(self.__client, 'standby')
        self._frontkey_locked = DecopBoolean(self.__client, 'frontkey-locked')
        self._buzzer = Buzzer(self.__client, 'buzzer')
        self._tc1 = TcBoard(self.__client, 'tc1')
        self._cc1 = CcBoard(self.__client, 'cc1')
        self._ampcc1 = Cc5000Board(self.__client, 'ampcc1')
        self._tc2 = TcBoard(self.__client, 'tc2')
        self._mc = McBoard(self.__client, 'mc')
        self._pc3 = PcBoard(self.__client, 'pc3')
        self._system_health_txt = DecopString(self.__client, 'system-health-txt')
        self._ul = MutableDecopInteger(self.__client, 'ul')
        self._net_conf = Ipconfig(self.__client, 'net-conf')

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def open(self) -> None:
        self.__client.open()

    def close(self) -> None:
        self.__client.close()

    def run(self, timeout: int = None) -> None:
        self.__client.run(timeout)

    def stop(self) -> None:
        self.__client.stop()

    def poll(self) -> None:
        self.__client.poll()

    @property
    def tan(self) -> 'DecopInteger':
        return self._tan

    @property
    def licenses(self) -> 'Licenses':
        return self._licenses

    @property
    def fw_update(self) -> 'FwUpdate':
        return self._fw_update

    @property
    def system_service_report(self) -> 'ServiceReport':
        return self._system_service_report

    @property
    def time(self) -> 'MutableDecopString':
        return self._time

    @property
    def system_messages(self) -> 'SystemMessages':
        return self._system_messages

    @property
    def decof_svn_revision(self) -> 'DecopString':
        return self._decof_svn_revision

    @property
    def fw_ver(self) -> 'DecopString':
        return self._fw_ver

    @property
    def system_type(self) -> 'DecopString':
        return self._system_type

    @property
    def uptime(self) -> 'DecopInteger':
        return self._uptime

    @property
    def ssw_ver(self) -> 'DecopString':
        return self._ssw_ver

    @property
    def decof_ver(self) -> 'DecopString':
        return self._decof_ver

    @property
    def build_information(self) -> 'BuildInformation':
        return self._build_information

    @property
    def uptime_txt(self) -> 'DecopString':
        return self._uptime_txt

    @property
    def system_label(self) -> 'MutableDecopString':
        return self._system_label

    @property
    def echo(self) -> 'MutableDecopBoolean':
        return self._echo

    @property
    def system_model(self) -> 'DecopString':
        return self._system_model

    @property
    def svn_revision(self) -> 'DecopString':
        return self._svn_revision

    @property
    def ssw_svn_revision(self) -> 'DecopString':
        return self._ssw_svn_revision

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def io(self) -> 'IoBoard':
        return self._io

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def laser1(self) -> 'Laser':
        return self._laser1

    @property
    def uv(self) -> 'UvShgLaser':
        return self._uv

    @property
    def display(self) -> 'Display':
        return self._display

    @property
    def system_health(self) -> 'DecopInteger':
        return self._system_health

    @property
    def power_supply(self) -> 'PowerSupply':
        return self._power_supply

    @property
    def interlock_open(self) -> 'DecopBoolean':
        return self._interlock_open

    @property
    def cc2(self) -> 'CcBoard':
        return self._cc2

    @property
    def ampcc2(self) -> 'Cc5000Board':
        return self._ampcc2

    @property
    def pc1(self) -> 'PcBoard':
        return self._pc1

    @property
    def pc2(self) -> 'PcBoard':
        return self._pc2

    @property
    def standby(self) -> 'Standby':
        return self._standby

    @property
    def frontkey_locked(self) -> 'DecopBoolean':
        return self._frontkey_locked

    @property
    def buzzer(self) -> 'Buzzer':
        return self._buzzer

    @property
    def tc1(self) -> 'TcBoard':
        return self._tc1

    @property
    def cc1(self) -> 'CcBoard':
        return self._cc1

    @property
    def ampcc1(self) -> 'Cc5000Board':
        return self._ampcc1

    @property
    def tc2(self) -> 'TcBoard':
        return self._tc2

    @property
    def mc(self) -> 'McBoard':
        return self._mc

    @property
    def pc3(self) -> 'PcBoard':
        return self._pc3

    @property
    def system_health_txt(self) -> 'DecopString':
        return self._system_health_txt

    @property
    def ul(self) -> 'MutableDecopInteger':
        return self._ul

    @property
    def net_conf(self) -> 'Ipconfig':
        return self._net_conf

    def error_log(self) -> str:
        return self.__client.exec('error-log', input_stream=None, output_type=str, return_type=None)

    def service_log(self) -> str:
        return self.__client.exec('service-log', input_stream=None, output_type=str, return_type=None)

    def service_report(self) -> bytes:
        return self.__client.exec('service-report', input_stream=None, output_type=bytes, return_type=None)

    def service_script(self, input_stream: bytes) -> None:
        assert isinstance(input_stream, bytes), "expected type 'bytes' for parameter 'input_stream', got '{}'".format(type(input_stream))
        self.__client.exec('service-script', input_stream=input_stream, output_type=None, return_type=None)

    def debug_log(self) -> str:
        return self.__client.exec('debug-log', input_stream=None, output_type=str, return_type=None)

    def system_connections(self) -> Tuple[str, int]:
        return self.__client.exec('system-connections', input_stream=None, output_type=str, return_type=int)

    def system_summary(self) -> str:
        return self.__client.exec('system-summary', input_stream=None, output_type=str, return_type=None)

    def change_ul(self, ul: UserLevel, passwd: str) -> int:
        assert isinstance(ul, UserLevel), "expected type 'UserLevel' for parameter 'ul', got '{}'".format(type(ul))
        assert isinstance(passwd, str), "expected type 'str' for parameter 'passwd', got '{}'".format(type(passwd))
        return self.__client.change_ul(ul, passwd)

    def change_password(self, password: str) -> None:
        assert isinstance(password, str), "expected type 'str' for parameter 'password', got '{}'".format(type(password))
        self.__client.exec('change-password', password, input_stream=None, output_type=None, return_type=None)

