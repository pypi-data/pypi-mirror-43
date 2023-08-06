# Generated from 'v1_4_0.xml' on 2019-03-14 09:42:05.973669

from typing import Tuple

from toptica.lasersdk.asyncio.client import UserLevel
from toptica.lasersdk.asyncio.client import Client

from toptica.lasersdk.asyncio.client import DecopBoolean
from toptica.lasersdk.asyncio.client import DecopInteger
from toptica.lasersdk.asyncio.client import DecopReal
from toptica.lasersdk.asyncio.client import DecopString
from toptica.lasersdk.asyncio.client import DecopBinary

from toptica.lasersdk.asyncio.client import MutableDecopBoolean
from toptica.lasersdk.asyncio.client import MutableDecopInteger
from toptica.lasersdk.asyncio.client import MutableDecopReal
from toptica.lasersdk.asyncio.client import MutableDecopString
from toptica.lasersdk.asyncio.client import MutableDecopBinary

from toptica.lasersdk.asyncio.client import Connection
from toptica.lasersdk.asyncio.client import NetworkConnection
from toptica.lasersdk.asyncio.client import SerialConnection

from toptica.lasersdk.asyncio.client import DecopError
from toptica.lasersdk.asyncio.client import DeviceNotFoundError


class FwUpdate:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name

    async def show_log(self) -> str:
        return await self.__client.exec(self.__name + ':show-log', input_stream=None, output_type=str, return_type=None)

    async def show_history(self) -> str:
        return await self.__client.exec(self.__name + ':show-history', input_stream=None, output_type=str, return_type=None)

    async def upload(self, input_stream: bytes, filename: str) -> None:
        assert isinstance(input_stream, bytes), "expected type 'bytes' for parameter 'input_stream', got '{}'".format(type(input_stream))
        assert isinstance(filename, str), "expected type 'str' for parameter 'filename', got '{}'".format(type(filename))
        await self.__client.exec(self.__name + ':upload', filename, input_stream=input_stream, output_type=None, return_type=None)


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

    async def install(self, licensekey: str) -> bool:
        assert isinstance(licensekey, str), "expected type 'str' for parameter 'licensekey', got '{}'".format(type(licensekey))
        return await self.__client.exec(self.__name + ':install', licensekey, input_stream=None, output_type=None, return_type=bool)

    async def get_key(self, key_number: int) -> str:
        assert isinstance(key_number, int), "expected type 'int' for parameter 'key_number', got '{}'".format(type(key_number))
        return await self.__client.exec(self.__name + ':get-key', key_number, input_stream=None, output_type=None, return_type=str)


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
        self._licensee = DecopString(client, name + ':licensee')
        self._valid_until = DecopString(client, name + ':valid-until')
        self._enabled = DecopBoolean(client, name + ':enabled')

    @property
    def licensee(self) -> 'DecopString':
        return self._licensee

    @property
    def valid_until(self) -> 'DecopString':
        return self._valid_until

    @property
    def enabled(self) -> 'DecopBoolean':
        return self._enabled


class SystemMessages:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._latest_message = DecopString(client, name + ':latest-message')
        self._count = DecopInteger(client, name + ':count')
        self._count_new = DecopInteger(client, name + ':count-new')

    @property
    def latest_message(self) -> 'DecopString':
        return self._latest_message

    @property
    def count(self) -> 'DecopInteger':
        return self._count

    @property
    def count_new(self) -> 'DecopInteger':
        return self._count_new

    async def show_new(self) -> str:
        return await self.__client.exec(self.__name + ':show-new', input_stream=None, output_type=str, return_type=None)

    async def show_log(self) -> str:
        return await self.__client.exec(self.__name + ':show-log', input_stream=None, output_type=str, return_type=None)

    async def mark_as_read(self, ID: int) -> None:
        assert isinstance(ID, int), "expected type 'int' for parameter 'ID', got '{}'".format(type(ID))
        await self.__client.exec(self.__name + ':mark-as-read', ID, input_stream=None, output_type=None, return_type=None)

    async def show_persistent(self) -> str:
        return await self.__client.exec(self.__name + ':show-persistent', input_stream=None, output_type=str, return_type=None)

    async def show_all(self) -> str:
        return await self.__client.exec(self.__name + ':show-all', input_stream=None, output_type=str, return_type=None)


class ServiceReport:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ready = DecopBoolean(client, name + ':ready')

    @property
    def ready(self) -> 'DecopBoolean':
        return self._ready

    async def print(self) -> bytes:
        return await self.__client.exec(self.__name + ':print', input_stream=None, output_type=bytes, return_type=None)

    async def service_report(self) -> bytes:
        return await self.__client.exec(self.__name + ':service-report', input_stream=None, output_type=bytes, return_type=None)

    async def request(self) -> None:
        await self.__client.exec(self.__name + ':request', input_stream=None, output_type=None, return_type=None)


class PcBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._channel1 = PiezoDrv2(client, name + ':channel1')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._heatsink_temp = DecopReal(client, name + ':heatsink-temp')
        self._status = DecopInteger(client, name + ':status')
        self._serial_number = DecopString(client, name + ':serial-number')
        self._revision = DecopString(client, name + ':revision')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._slot = DecopString(client, name + ':slot')

    @property
    def channel1(self) -> 'PiezoDrv2':
        return self._channel1

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def heatsink_temp(self) -> 'DecopReal':
        return self._heatsink_temp

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def slot(self) -> 'DecopString':
        return self._slot


class PiezoDrv2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._voltage_set_dithering = MutableDecopBoolean(client, name + ':voltage-set-dithering')
        self._voltage_set = MutableDecopReal(client, name + ':voltage-set')
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._path = DecopString(client, name + ':path')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._external_input = ExtInput2(client, name + ':external-input')

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def voltage_set_dithering(self) -> 'MutableDecopBoolean':
        return self._voltage_set_dithering

    @property
    def voltage_set(self) -> 'MutableDecopReal':
        return self._voltage_set

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input


class OutputFilter2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slew_rate = MutableDecopReal(client, name + ':slew-rate')
        self._slew_rate_limited = DecopBoolean(client, name + ':slew-rate-limited')
        self._slew_rate_enabled = MutableDecopBoolean(client, name + ':slew-rate-enabled')

    @property
    def slew_rate(self) -> 'MutableDecopReal':
        return self._slew_rate

    @property
    def slew_rate_limited(self) -> 'DecopBoolean':
        return self._slew_rate_limited

    @property
    def slew_rate_enabled(self) -> 'MutableDecopBoolean':
        return self._slew_rate_enabled


class ExtInput2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._factor = MutableDecopReal(client, name + ':factor')
        self._signal = MutableDecopInteger(client, name + ':signal')

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def factor(self) -> 'MutableDecopReal':
        return self._factor

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal


class TcBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._channel2 = TcChannel(client, name + ':channel2')
        self._channel1 = TcChannel(client, name + ':channel1')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._serial_number = DecopString(client, name + ':serial-number')
        self._revision = DecopString(client, name + ':revision')
        self._fpga_fw_ver = DecopString(client, name + ':fpga-fw-ver')
        self._slot = DecopString(client, name + ':slot')

    @property
    def channel2(self) -> 'TcChannel':
        return self._channel2

    @property
    def channel1(self) -> 'TcChannel':
        return self._channel1

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def fpga_fw_ver(self) -> 'DecopString':
        return self._fpga_fw_ver

    @property
    def slot(self) -> 'DecopString':
        return self._slot


class TcChannel:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._limits = TcChannelCheck(client, name + ':limits')
        self._temp_set_max = MutableDecopReal(client, name + ':temp-set-max')
        self._resistance = DecopReal(client, name + ':resistance')
        self._ntc_series_resistance = DecopReal(client, name + ':ntc-series-resistance')
        self._power_source = DecopInteger(client, name + ':power-source')
        self._fault = DecopBoolean(client, name + ':fault')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._current_set_min = MutableDecopReal(client, name + ':current-set-min')
        self._ready = DecopBoolean(client, name + ':ready')
        self._temp_set_min = MutableDecopReal(client, name + ':temp-set-min')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._temp_reset = MutableDecopBoolean(client, name + ':temp-reset')
        self._temp_roc_limit = MutableDecopReal(client, name + ':temp-roc-limit')
        self._drv_voltage = DecopReal(client, name + ':drv-voltage')
        self._temp_act = DecopReal(client, name + ':temp-act')
        self._current_act = DecopReal(client, name + ':current-act')
        self._current_set = DecopReal(client, name + ':current-set')
        self._disabled_preset = TcDisabledPreset(client, name + ':disabled-preset')
        self._status = DecopInteger(client, name + ':status')
        self._temp_roc_enabled = MutableDecopBoolean(client, name + ':temp-roc-enabled')
        self._path = DecopString(client, name + ':path')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._current_set_max = MutableDecopReal(client, name + ':current-set-max')
        self._temp_set = MutableDecopReal(client, name + ':temp-set')
        self._c_loop = TcChannelCLoop(client, name + ':c-loop')
        self._t_loop = TcChannelTLoop(client, name + ':t-loop')

    @property
    def limits(self) -> 'TcChannelCheck':
        return self._limits

    @property
    def temp_set_max(self) -> 'MutableDecopReal':
        return self._temp_set_max

    @property
    def resistance(self) -> 'DecopReal':
        return self._resistance

    @property
    def ntc_series_resistance(self) -> 'DecopReal':
        return self._ntc_series_resistance

    @property
    def power_source(self) -> 'DecopInteger':
        return self._power_source

    @property
    def fault(self) -> 'DecopBoolean':
        return self._fault

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def current_set_min(self) -> 'MutableDecopReal':
        return self._current_set_min

    @property
    def ready(self) -> 'DecopBoolean':
        return self._ready

    @property
    def temp_set_min(self) -> 'MutableDecopReal':
        return self._temp_set_min

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def temp_reset(self) -> 'MutableDecopBoolean':
        return self._temp_reset

    @property
    def temp_roc_limit(self) -> 'MutableDecopReal':
        return self._temp_roc_limit

    @property
    def drv_voltage(self) -> 'DecopReal':
        return self._drv_voltage

    @property
    def temp_act(self) -> 'DecopReal':
        return self._temp_act

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def current_set(self) -> 'DecopReal':
        return self._current_set

    @property
    def disabled_preset(self) -> 'TcDisabledPreset':
        return self._disabled_preset

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def temp_roc_enabled(self) -> 'MutableDecopBoolean':
        return self._temp_roc_enabled

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def current_set_max(self) -> 'MutableDecopReal':
        return self._current_set_max

    @property
    def temp_set(self) -> 'MutableDecopReal':
        return self._temp_set

    @property
    def c_loop(self) -> 'TcChannelCLoop':
        return self._c_loop

    @property
    def t_loop(self) -> 'TcChannelTLoop':
        return self._t_loop

    async def check_peltier(self) -> float:
        return await self.__client.exec(self.__name + ':check-peltier', input_stream=None, output_type=None, return_type=float)


class TcChannelCheck:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._timeout = MutableDecopInteger(client, name + ':timeout')
        self._temp_max = MutableDecopReal(client, name + ':temp-max')
        self._timed_out = DecopBoolean(client, name + ':timed-out')
        self._temp_min = MutableDecopReal(client, name + ':temp-min')
        self._out_of_range = DecopBoolean(client, name + ':out-of-range')

    @property
    def timeout(self) -> 'MutableDecopInteger':
        return self._timeout

    @property
    def temp_max(self) -> 'MutableDecopReal':
        return self._temp_max

    @property
    def timed_out(self) -> 'DecopBoolean':
        return self._timed_out

    @property
    def temp_min(self) -> 'MutableDecopReal':
        return self._temp_min

    @property
    def out_of_range(self) -> 'DecopBoolean':
        return self._out_of_range


class TcDisabledPreset:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name


class TcChannelCLoop:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._i_gain = MutableDecopReal(client, name + ':i-gain')
        self._on = MutableDecopBoolean(client, name + ':on')

    @property
    def i_gain(self) -> 'MutableDecopReal':
        return self._i_gain

    @property
    def on(self) -> 'MutableDecopBoolean':
        return self._on


class TcChannelTLoop:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._i_gain = MutableDecopReal(client, name + ':i-gain')
        self._ok_tolerance = MutableDecopReal(client, name + ':ok-tolerance')
        self._on = MutableDecopBoolean(client, name + ':on')
        self._ok_time = MutableDecopReal(client, name + ':ok-time')
        self._p_gain = MutableDecopReal(client, name + ':p-gain')
        self._d_gain = MutableDecopReal(client, name + ':d-gain')

    @property
    def i_gain(self) -> 'MutableDecopReal':
        return self._i_gain

    @property
    def ok_tolerance(self) -> 'MutableDecopReal':
        return self._ok_tolerance

    @property
    def on(self) -> 'MutableDecopBoolean':
        return self._on

    @property
    def ok_time(self) -> 'MutableDecopReal':
        return self._ok_time

    @property
    def p_gain(self) -> 'MutableDecopReal':
        return self._p_gain

    @property
    def d_gain(self) -> 'MutableDecopReal':
        return self._d_gain


class Cc5000Board:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._parallel_mode = DecopBoolean(client, name + ':parallel-mode')
        self._inverter_temp_fuse = DecopReal(client, name + ':inverter-temp-fuse')
        self._status = DecopInteger(client, name + ':status')
        self._variant = DecopString(client, name + ':variant')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._revision = DecopString(client, name + ':revision')
        self._inverter_temp = DecopReal(client, name + ':inverter-temp')
        self._slot = DecopString(client, name + ':slot')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._channel1 = Cc5000Drv(client, name + ':channel1')
        self._regulator_temp = DecopReal(client, name + ':regulator-temp')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._serial_number = DecopString(client, name + ':serial-number')
        self._regulator_temp_fuse = DecopReal(client, name + ':regulator-temp-fuse')
        self._power_15v = MutableDecopBoolean(client, name + ':power-15v')

    @property
    def parallel_mode(self) -> 'DecopBoolean':
        return self._parallel_mode

    @property
    def inverter_temp_fuse(self) -> 'DecopReal':
        return self._inverter_temp_fuse

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def inverter_temp(self) -> 'DecopReal':
        return self._inverter_temp

    @property
    def slot(self) -> 'DecopString':
        return self._slot

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def channel1(self) -> 'Cc5000Drv':
        return self._channel1

    @property
    def regulator_temp(self) -> 'DecopReal':
        return self._regulator_temp

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def regulator_temp_fuse(self) -> 'DecopReal':
        return self._regulator_temp_fuse

    @property
    def power_15v(self) -> 'MutableDecopBoolean':
        return self._power_15v


class Cc5000Drv:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._status_txt = DecopString(client, name + ':status-txt')
        self._current_clip_limit = DecopReal(client, name + ':current-clip-limit')
        self._output_filter = OutputFilter1(client, name + ':output-filter')
        self._aux = DecopReal(client, name + ':aux')
        self._voltage_out = DecopReal(client, name + ':voltage-out')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._current_offset = MutableDecopReal(client, name + ':current-offset')
        self._emission = DecopBoolean(client, name + ':emission')
        self._current_act = DecopReal(client, name + ':current-act')
        self._variant = DecopString(client, name + ':variant')
        self._status = DecopInteger(client, name + ':status')
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._forced_off = MutableDecopBoolean(client, name + ':forced-off')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._path = DecopString(client, name + ':path')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._current_set = MutableDecopReal(client, name + ':current-set')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def current_clip_limit(self) -> 'DecopReal':
        return self._current_clip_limit

    @property
    def output_filter(self) -> 'OutputFilter1':
        return self._output_filter

    @property
    def aux(self) -> 'DecopReal':
        return self._aux

    @property
    def voltage_out(self) -> 'DecopReal':
        return self._voltage_out

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def current_offset(self) -> 'MutableDecopReal':
        return self._current_offset

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def forced_off(self) -> 'MutableDecopBoolean':
        return self._forced_off

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip


class OutputFilter1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slew_rate = MutableDecopReal(client, name + ':slew-rate')
        self._slew_rate_limited = DecopBoolean(client, name + ':slew-rate-limited')
        self._slew_rate_enabled = MutableDecopBoolean(client, name + ':slew-rate-enabled')

    @property
    def slew_rate(self) -> 'MutableDecopReal':
        return self._slew_rate

    @property
    def slew_rate_limited(self) -> 'DecopBoolean':
        return self._slew_rate_limited

    @property
    def slew_rate_enabled(self) -> 'MutableDecopBoolean':
        return self._slew_rate_enabled


class Standby:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._laser1 = StandbyLaser(client, name + ':laser1')
        self._state = DecopInteger(client, name + ':state')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def laser1(self) -> 'StandbyLaser':
        return self._laser1

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class StandbyLaser:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._nlo = StandbyShg(client, name + ':nlo')
        self._amp = StandbyAmp(client, name + ':amp')
        self._dl = StandbyDl(client, name + ':dl')

    @property
    def nlo(self) -> 'StandbyShg':
        return self._nlo

    @property
    def amp(self) -> 'StandbyAmp':
        return self._amp

    @property
    def dl(self) -> 'StandbyDl':
        return self._dl


class StandbyShg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._disable_tc = MutableDecopBoolean(client, name + ':disable-tc')
        self._disable_pc = MutableDecopBoolean(client, name + ':disable-pc')
        self._disable_servo_subsystem = MutableDecopBoolean(client, name + ':disable-servo-subsystem')
        self._disable_power_stabilization = MutableDecopBoolean(client, name + ':disable-power-stabilization')
        self._disable_cavity_lock = MutableDecopBoolean(client, name + ':disable-cavity-lock')

    @property
    def disable_tc(self) -> 'MutableDecopBoolean':
        return self._disable_tc

    @property
    def disable_pc(self) -> 'MutableDecopBoolean':
        return self._disable_pc

    @property
    def disable_servo_subsystem(self) -> 'MutableDecopBoolean':
        return self._disable_servo_subsystem

    @property
    def disable_power_stabilization(self) -> 'MutableDecopBoolean':
        return self._disable_power_stabilization

    @property
    def disable_cavity_lock(self) -> 'MutableDecopBoolean':
        return self._disable_cavity_lock


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


class StandbyDl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._disable_tc = MutableDecopBoolean(client, name + ':disable-tc')
        self._disable_pc = MutableDecopBoolean(client, name + ':disable-pc')
        self._disable_cc = MutableDecopBoolean(client, name + ':disable-cc')

    @property
    def disable_tc(self) -> 'MutableDecopBoolean':
        return self._disable_tc

    @property
    def disable_pc(self) -> 'MutableDecopBoolean':
        return self._disable_pc

    @property
    def disable_cc(self) -> 'MutableDecopBoolean':
        return self._disable_cc


class PowerSupply:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_3V3 = DecopReal(client, name + ':voltage-3V3')
        self._load = DecopReal(client, name + ':load')
        self._current_15Vn = DecopReal(client, name + ':current-15Vn')
        self._heatsink_temp = DecopReal(client, name + ':heatsink-temp')
        self._status = DecopInteger(client, name + ':status')
        self._current_15V = DecopReal(client, name + ':current-15V')
        self._revision = DecopString(client, name + ':revision')
        self._voltage_15V = DecopReal(client, name + ':voltage-15V')
        self._voltage_5V = DecopReal(client, name + ':voltage-5V')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._current_5V = DecopReal(client, name + ':current-5V')
        self._voltage_15Vn = DecopReal(client, name + ':voltage-15Vn')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def voltage_3V3(self) -> 'DecopReal':
        return self._voltage_3V3

    @property
    def load(self) -> 'DecopReal':
        return self._load

    @property
    def current_15Vn(self) -> 'DecopReal':
        return self._current_15Vn

    @property
    def heatsink_temp(self) -> 'DecopReal':
        return self._heatsink_temp

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def current_15V(self) -> 'DecopReal':
        return self._current_15V

    @property
    def revision(self) -> 'DecopString':
        return self._revision

    @property
    def voltage_15V(self) -> 'DecopReal':
        return self._voltage_15V

    @property
    def voltage_5V(self) -> 'DecopReal':
        return self._voltage_5V

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def current_5V(self) -> 'DecopReal':
        return self._current_5V

    @property
    def voltage_15Vn(self) -> 'DecopReal':
        return self._voltage_15Vn

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number


class Laser:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pd_ext = PdExt(client, name + ':pd-ext')
        self._emission = DecopBoolean(client, name + ':emission')
        self._nlo = Nlo(client, name + ':nlo')
        self._ctl = CtlT(client, name + ':ctl')
        self._scope = ScopeT(client, name + ':scope')
        self._type_ = DecopString(client, name + ':type')
        self._health_txt = DecopString(client, name + ':health-txt')
        self._product_name = DecopString(client, name + ':product-name')
        self._health = DecopInteger(client, name + ':health')
        self._amp = LaserAmp(client, name + ':amp')
        self._power_stabilization = PwrStab(client, name + ':power-stabilization')
        self._dl = LaserHead(client, name + ':dl')
        self._scan = Siggen(client, name + ':scan')

    @property
    def pd_ext(self) -> 'PdExt':
        return self._pd_ext

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def nlo(self) -> 'Nlo':
        return self._nlo

    @property
    def ctl(self) -> 'CtlT':
        return self._ctl

    @property
    def scope(self) -> 'ScopeT':
        return self._scope

    @property
    def type_(self) -> 'DecopString':
        return self._type_

    @property
    def health_txt(self) -> 'DecopString':
        return self._health_txt

    @property
    def product_name(self) -> 'DecopString':
        return self._product_name

    @property
    def health(self) -> 'DecopInteger':
        return self._health

    @property
    def amp(self) -> 'LaserAmp':
        return self._amp

    @property
    def power_stabilization(self) -> 'PwrStab':
        return self._power_stabilization

    @property
    def dl(self) -> 'LaserHead':
        return self._dl

    @property
    def scan(self) -> 'Siggen':
        return self._scan

    async def save(self) -> None:
        await self.__client.exec(self.__name + ':save', input_stream=None, output_type=None, return_type=None)

    async def detect(self) -> None:
        await self.__client.exec(self.__name + ':detect', input_stream=None, output_type=None, return_type=None)

    async def load(self) -> None:
        await self.__client.exec(self.__name + ':load', input_stream=None, output_type=None, return_type=None)


class PdExt:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._power = DecopReal(client, name + ':power')
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def power(self) -> 'DecopReal':
        return self._power

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset


class Nlo:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._servo = NloLaserHeadServos(client, name + ':servo')
        self._shg = Shg(client, name + ':shg')
        self._power_optimization = NloLaserHeadPowerOptimization(client, name + ':power-optimization')
        self._pd = NloLaserHeadPhotoDiodes(client, name + ':pd')
        self._ssw_ver = DecopString(client, name + ':ssw-ver')
        self._fhg = Fhg(client, name + ':fhg')

    @property
    def servo(self) -> 'NloLaserHeadServos':
        return self._servo

    @property
    def shg(self) -> 'Shg':
        return self._shg

    @property
    def power_optimization(self) -> 'NloLaserHeadPowerOptimization':
        return self._power_optimization

    @property
    def pd(self) -> 'NloLaserHeadPhotoDiodes':
        return self._pd

    @property
    def ssw_ver(self) -> 'DecopString':
        return self._ssw_ver

    @property
    def fhg(self) -> 'Fhg':
        return self._fhg


class NloLaserHeadServos:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._uv_outcpl = NloLaserHeadServoPwm(client, name + ':uv-outcpl')
        self._fiber1_vert = NloLaserHeadServoPwm(client, name + ':fiber1-vert')
        self._fhg1_vert = NloLaserHeadServoPwm(client, name + ':fhg1-vert')
        self._ta1_vert = NloLaserHeadServoPwm(client, name + ':ta1-vert')
        self._fhg2_vert = NloLaserHeadServoPwm(client, name + ':fhg2-vert')
        self._fiber2_hor = NloLaserHeadServoPwm(client, name + ':fiber2-hor')
        self._shg2_vert = NloLaserHeadServoPwm(client, name + ':shg2-vert')
        self._uv_cryst = NloLaserHeadServoPwm(client, name + ':uv-cryst')
        self._ta1_hor = NloLaserHeadServoPwm(client, name + ':ta1-hor')
        self._shg1_vert = NloLaserHeadServoPwm(client, name + ':shg1-vert')
        self._ta2_hor = NloLaserHeadServoPwm(client, name + ':ta2-hor')
        self._shg2_hor = NloLaserHeadServoPwm(client, name + ':shg2-hor')
        self._shg1_hor = NloLaserHeadServoPwm(client, name + ':shg1-hor')
        self._fiber1_hor = NloLaserHeadServoPwm(client, name + ':fiber1-hor')
        self._ta2_vert = NloLaserHeadServoPwm(client, name + ':ta2-vert')
        self._fiber2_vert = NloLaserHeadServoPwm(client, name + ':fiber2-vert')
        self._fhg2_hor = NloLaserHeadServoPwm(client, name + ':fhg2-hor')
        self._fhg1_hor = NloLaserHeadServoPwm(client, name + ':fhg1-hor')

    @property
    def uv_outcpl(self) -> 'NloLaserHeadServoPwm':
        return self._uv_outcpl

    @property
    def fiber1_vert(self) -> 'NloLaserHeadServoPwm':
        return self._fiber1_vert

    @property
    def fhg1_vert(self) -> 'NloLaserHeadServoPwm':
        return self._fhg1_vert

    @property
    def ta1_vert(self) -> 'NloLaserHeadServoPwm':
        return self._ta1_vert

    @property
    def fhg2_vert(self) -> 'NloLaserHeadServoPwm':
        return self._fhg2_vert

    @property
    def fiber2_hor(self) -> 'NloLaserHeadServoPwm':
        return self._fiber2_hor

    @property
    def shg2_vert(self) -> 'NloLaserHeadServoPwm':
        return self._shg2_vert

    @property
    def uv_cryst(self) -> 'NloLaserHeadServoPwm':
        return self._uv_cryst

    @property
    def ta1_hor(self) -> 'NloLaserHeadServoPwm':
        return self._ta1_hor

    @property
    def shg1_vert(self) -> 'NloLaserHeadServoPwm':
        return self._shg1_vert

    @property
    def ta2_hor(self) -> 'NloLaserHeadServoPwm':
        return self._ta2_hor

    @property
    def shg2_hor(self) -> 'NloLaserHeadServoPwm':
        return self._shg2_hor

    @property
    def shg1_hor(self) -> 'NloLaserHeadServoPwm':
        return self._shg1_hor

    @property
    def fiber1_hor(self) -> 'NloLaserHeadServoPwm':
        return self._fiber1_hor

    @property
    def ta2_vert(self) -> 'NloLaserHeadServoPwm':
        return self._ta2_vert

    @property
    def fiber2_vert(self) -> 'NloLaserHeadServoPwm':
        return self._fiber2_vert

    @property
    def fhg2_hor(self) -> 'NloLaserHeadServoPwm':
        return self._fhg2_hor

    @property
    def fhg1_hor(self) -> 'NloLaserHeadServoPwm':
        return self._fhg1_hor

    async def center_fhg_servos(self) -> None:
        await self.__client.exec(self.__name + ':center-fhg-servos', input_stream=None, output_type=None, return_type=None)

    async def center_ta_servos(self) -> None:
        await self.__client.exec(self.__name + ':center-ta-servos', input_stream=None, output_type=None, return_type=None)

    async def center_fiber_servos(self) -> None:
        await self.__client.exec(self.__name + ':center-fiber-servos', input_stream=None, output_type=None, return_type=None)

    async def center_shg_servos(self) -> None:
        await self.__client.exec(self.__name + ':center-shg-servos', input_stream=None, output_type=None, return_type=None)

    async def center_all_servos(self) -> None:
        await self.__client.exec(self.__name + ':center-all-servos', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadServoPwm:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._display_name = DecopString(client, name + ':display-name')
        self._value = MutableDecopInteger(client, name + ':value')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def display_name(self) -> 'DecopString':
        return self._display_name

    @property
    def value(self) -> 'MutableDecopInteger':
        return self._value

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    async def center_servo(self) -> None:
        await self.__client.exec(self.__name + ':center-servo', input_stream=None, output_type=None, return_type=None)


class Shg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcChannel(client, name + ':tc')
        self._factory_settings = ShgFactorySettings(client, name + ':factory-settings')
        self._lock = NloLaserHeadLockShg(client, name + ':lock')
        self._pc = PiezoDrv1(client, name + ':pc')
        self._scope = NloLaserHeadScopeT(client, name + ':scope')
        self._scan = NloLaserHeadSiggen(client, name + ':scan')

    @property
    def tc(self) -> 'TcChannel':
        return self._tc

    @property
    def factory_settings(self) -> 'ShgFactorySettings':
        return self._factory_settings

    @property
    def lock(self) -> 'NloLaserHeadLockShg':
        return self._lock

    @property
    def pc(self) -> 'PiezoDrv1':
        return self._pc

    @property
    def scope(self) -> 'NloLaserHeadScopeT':
        return self._scope

    @property
    def scan(self) -> 'NloLaserHeadSiggen':
        return self._scan

    async def store(self) -> None:
        await self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    async def restore(self) -> None:
        await self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)


class ShgFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = NloLaserHeadTcFactorySettings(client, name + ':tc')
        self._pd = NloLaserHeadShgPhotodiodesFactorySettings(client, name + ':pd')
        self._pc = NloLaserHeadPcFactorySettings(client, name + ':pc')
        self._modified = DecopBoolean(client, name + ':modified')
        self._lock = NloLaserHeadLockFactorySettings(client, name + ':lock')

    @property
    def tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._tc

    @property
    def pd(self) -> 'NloLaserHeadShgPhotodiodesFactorySettings':
        return self._pd

    @property
    def pc(self) -> 'NloLaserHeadPcFactorySettings':
        return self._pc

    @property
    def modified(self) -> 'DecopBoolean':
        return self._modified

    @property
    def lock(self) -> 'NloLaserHeadLockFactorySettings':
        return self._lock

    async def apply(self) -> None:
        await self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    async def retrieve_now(self) -> None:
        await self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadTcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._temp_roc_limit = MutableDecopReal(client, name + ':temp-roc-limit')
        self._timeout = MutableDecopInteger(client, name + ':timeout')
        self._power_source = MutableDecopInteger(client, name + ':power-source')
        self._temp_min = MutableDecopReal(client, name + ':temp-min')
        self._ok_tolerance = MutableDecopReal(client, name + ':ok-tolerance')
        self._current_max = MutableDecopReal(client, name + ':current-max')
        self._current_min = MutableDecopReal(client, name + ':current-min')
        self._p_gain = MutableDecopReal(client, name + ':p-gain')
        self._ok_time = MutableDecopReal(client, name + ':ok-time')
        self._i_gain = MutableDecopReal(client, name + ':i-gain')
        self._temp_max = MutableDecopReal(client, name + ':temp-max')
        self._temp_roc_enabled = MutableDecopBoolean(client, name + ':temp-roc-enabled')
        self._temp_set = MutableDecopReal(client, name + ':temp-set')
        self._c_gain = MutableDecopReal(client, name + ':c-gain')
        self._ntc_series_resistance = MutableDecopReal(client, name + ':ntc-series-resistance')
        self._d_gain = MutableDecopReal(client, name + ':d-gain')

    @property
    def temp_roc_limit(self) -> 'MutableDecopReal':
        return self._temp_roc_limit

    @property
    def timeout(self) -> 'MutableDecopInteger':
        return self._timeout

    @property
    def power_source(self) -> 'MutableDecopInteger':
        return self._power_source

    @property
    def temp_min(self) -> 'MutableDecopReal':
        return self._temp_min

    @property
    def ok_tolerance(self) -> 'MutableDecopReal':
        return self._ok_tolerance

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
    def ok_time(self) -> 'MutableDecopReal':
        return self._ok_time

    @property
    def i_gain(self) -> 'MutableDecopReal':
        return self._i_gain

    @property
    def temp_max(self) -> 'MutableDecopReal':
        return self._temp_max

    @property
    def temp_roc_enabled(self) -> 'MutableDecopBoolean':
        return self._temp_roc_enabled

    @property
    def temp_set(self) -> 'MutableDecopReal':
        return self._temp_set

    @property
    def c_gain(self) -> 'MutableDecopReal':
        return self._c_gain

    @property
    def ntc_series_resistance(self) -> 'MutableDecopReal':
        return self._ntc_series_resistance

    @property
    def d_gain(self) -> 'MutableDecopReal':
        return self._d_gain


class NloLaserHeadShgPhotodiodesFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fiber = NloLaserHeadPdFactorySettings(client, name + ':fiber')
        self._shg = NloLaserHeadPdFactorySettings(client, name + ':shg')
        self._amp = NloLaserHeadPdFactorySettings(client, name + ':amp')
        self._pdh_rf = NloLaserHeadPdPdhFactorySettings(client, name + ':pdh-rf')
        self._pdh_dc = NloLaserHeadPdDigilockFactorySettings(client, name + ':pdh-dc')
        self._dl = NloLaserHeadPdFactorySettings(client, name + ':dl')
        self._int = NloLaserHeadPdDigilockFactorySettings(client, name + ':int')

    @property
    def fiber(self) -> 'NloLaserHeadPdFactorySettings':
        return self._fiber

    @property
    def shg(self) -> 'NloLaserHeadPdFactorySettings':
        return self._shg

    @property
    def amp(self) -> 'NloLaserHeadPdFactorySettings':
        return self._amp

    @property
    def pdh_rf(self) -> 'NloLaserHeadPdPdhFactorySettings':
        return self._pdh_rf

    @property
    def pdh_dc(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._pdh_dc

    @property
    def dl(self) -> 'NloLaserHeadPdFactorySettings':
        return self._dl

    @property
    def int(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._int


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


class NloLaserHeadPdPdhFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._gain = MutableDecopReal(client, name + ':gain')

    @property
    def gain(self) -> 'MutableDecopReal':
        return self._gain


class NloLaserHeadPdDigilockFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset


class NloLaserHeadPcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scan_amplitude = MutableDecopReal(client, name + ':scan-amplitude')
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._scan_offset = MutableDecopReal(client, name + ':scan-offset')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._scan_frequency = MutableDecopReal(client, name + ':scan-frequency')
        self._capacitance = MutableDecopReal(client, name + ':capacitance')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')

    @property
    def scan_amplitude(self) -> 'MutableDecopReal':
        return self._scan_amplitude

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def scan_offset(self) -> 'MutableDecopReal':
        return self._scan_offset

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def scan_frequency(self) -> 'MutableDecopReal':
        return self._scan_frequency

    @property
    def capacitance(self) -> 'MutableDecopReal':
        return self._capacitance

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max


class NloLaserHeadLockFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._window = NloLaserHeadLockWindowFactorySettings(client, name + ':window')
        self._pid2_gain = NloLaserHeadPidGainFactorySettings(client, name + ':pid2-gain')
        self._pid_selection = MutableDecopInteger(client, name + ':pid-selection')
        self._pid1_gain = NloLaserHeadPidGainFactorySettings(client, name + ':pid1-gain')
        self._analog_p_gain = MutableDecopReal(client, name + ':analog-p-gain')
        self._relock = NloLaserHeadRelockFactorySettings(client, name + ':relock')
        self._local_oscillator = NloLaserHeadLocalOscillatorFactorySettings(client, name + ':local-oscillator')

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def window(self) -> 'NloLaserHeadLockWindowFactorySettings':
        return self._window

    @property
    def pid2_gain(self) -> 'NloLaserHeadPidGainFactorySettings':
        return self._pid2_gain

    @property
    def pid_selection(self) -> 'MutableDecopInteger':
        return self._pid_selection

    @property
    def pid1_gain(self) -> 'NloLaserHeadPidGainFactorySettings':
        return self._pid1_gain

    @property
    def analog_p_gain(self) -> 'MutableDecopReal':
        return self._analog_p_gain

    @property
    def relock(self) -> 'NloLaserHeadRelockFactorySettings':
        return self._relock

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorFactorySettings':
        return self._local_oscillator


class NloLaserHeadLockWindowFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._level_hysteresis = MutableDecopReal(client, name + ':level-hysteresis')
        self._threshold = MutableDecopReal(client, name + ':threshold')

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def level_hysteresis(self) -> 'MutableDecopReal':
        return self._level_hysteresis

    @property
    def threshold(self) -> 'MutableDecopReal':
        return self._threshold


class NloLaserHeadPidGainFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._i = MutableDecopReal(client, name + ':i')
        self._i_cutoff = MutableDecopReal(client, name + ':i-cutoff')
        self._d = MutableDecopReal(client, name + ':d')
        self._i_cutoff_enabled = MutableDecopBoolean(client, name + ':i-cutoff-enabled')
        self._p = MutableDecopReal(client, name + ':p')
        self._all = MutableDecopReal(client, name + ':all')

    @property
    def i(self) -> 'MutableDecopReal':
        return self._i

    @property
    def i_cutoff(self) -> 'MutableDecopReal':
        return self._i_cutoff

    @property
    def d(self) -> 'MutableDecopReal':
        return self._d

    @property
    def i_cutoff_enabled(self) -> 'MutableDecopBoolean':
        return self._i_cutoff_enabled

    @property
    def p(self) -> 'MutableDecopReal':
        return self._p

    @property
    def all(self) -> 'MutableDecopReal':
        return self._all


class NloLaserHeadRelockFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._delay = MutableDecopReal(client, name + ':delay')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def delay(self) -> 'MutableDecopReal':
        return self._delay

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class NloLaserHeadLocalOscillatorFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._phase_shift_fhg = MutableDecopReal(client, name + ':phase-shift-fhg')
        self._attenuation_shg_raw = MutableDecopInteger(client, name + ':attenuation-shg-raw')
        self._phase_shift_shg = MutableDecopReal(client, name + ':phase-shift-shg')
        self._attenuation_fhg_raw = MutableDecopInteger(client, name + ':attenuation-fhg-raw')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def phase_shift_fhg(self) -> 'MutableDecopReal':
        return self._phase_shift_fhg

    @property
    def attenuation_shg_raw(self) -> 'MutableDecopInteger':
        return self._attenuation_shg_raw

    @property
    def phase_shift_shg(self) -> 'MutableDecopReal':
        return self._phase_shift_shg

    @property
    def attenuation_fhg_raw(self) -> 'MutableDecopInteger':
        return self._attenuation_fhg_raw

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class NloLaserHeadLockShg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._window = NloLaserHeadWindow(client, name + ':window')
        self._state = MutableDecopInteger(client, name + ':state')
        self._pid_selection = MutableDecopInteger(client, name + ':pid-selection')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._background_trace = DecopBinary(client, name + ':background-trace')
        self._relock = NloLaserHeadRelock(client, name + ':relock')
        self._lock_enabled = MutableDecopBoolean(client, name + ':lock-enabled')
        self._analog_dl_gain = NloLaserHeadMinifalc(client, name + ':analog-dl-gain')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._local_oscillator = NloLaserHeadLocalOscillatorShg(client, name + ':local-oscillator')
        self._cavity_fast_pzt_voltage = MutableDecopReal(client, name + ':cavity-fast-pzt-voltage')
        self._pid2 = NloLaserHeadPid(client, name + ':pid2')
        self._cavity_slow_pzt_voltage = MutableDecopReal(client, name + ':cavity-slow-pzt-voltage')
        self._pid1 = NloLaserHeadPid(client, name + ':pid1')

    @property
    def window(self) -> 'NloLaserHeadWindow':
        return self._window

    @property
    def state(self) -> 'MutableDecopInteger':
        return self._state

    @property
    def pid_selection(self) -> 'MutableDecopInteger':
        return self._pid_selection

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def background_trace(self) -> 'DecopBinary':
        return self._background_trace

    @property
    def relock(self) -> 'NloLaserHeadRelock':
        return self._relock

    @property
    def lock_enabled(self) -> 'MutableDecopBoolean':
        return self._lock_enabled

    @property
    def analog_dl_gain(self) -> 'NloLaserHeadMinifalc':
        return self._analog_dl_gain

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorShg':
        return self._local_oscillator

    @property
    def cavity_fast_pzt_voltage(self) -> 'MutableDecopReal':
        return self._cavity_fast_pzt_voltage

    @property
    def pid2(self) -> 'NloLaserHeadPid':
        return self._pid2

    @property
    def cavity_slow_pzt_voltage(self) -> 'MutableDecopReal':
        return self._cavity_slow_pzt_voltage

    @property
    def pid1(self) -> 'NloLaserHeadPid':
        return self._pid1


class NloLaserHeadWindow:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._threshold = MutableDecopReal(client, name + ':threshold')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._level_hysteresis = MutableDecopReal(client, name + ':level-hysteresis')

    @property
    def threshold(self) -> 'MutableDecopReal':
        return self._threshold

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def level_hysteresis(self) -> 'MutableDecopReal':
        return self._level_hysteresis


class NloLaserHeadRelock:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._delay = MutableDecopReal(client, name + ':delay')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def delay(self) -> 'MutableDecopReal':
        return self._delay

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class NloLaserHeadMinifalc:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._p_gain = MutableDecopReal(client, name + ':p-gain')

    @property
    def p_gain(self) -> 'MutableDecopReal':
        return self._p_gain


class NloLaserHeadLocalOscillatorShg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._use_fast_oscillator = MutableDecopBoolean(client, name + ':use-fast-oscillator')
        self._coupled_modulation = MutableDecopBoolean(client, name + ':coupled-modulation')
        self._use_external_oscillator = MutableDecopBoolean(client, name + ':use-external-oscillator')
        self._phase_shift = MutableDecopReal(client, name + ':phase-shift')
        self._attenuation_raw = MutableDecopInteger(client, name + ':attenuation-raw')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def use_fast_oscillator(self) -> 'MutableDecopBoolean':
        return self._use_fast_oscillator

    @property
    def coupled_modulation(self) -> 'MutableDecopBoolean':
        return self._coupled_modulation

    @property
    def use_external_oscillator(self) -> 'MutableDecopBoolean':
        return self._use_external_oscillator

    @property
    def phase_shift(self) -> 'MutableDecopReal':
        return self._phase_shift

    @property
    def attenuation_raw(self) -> 'MutableDecopInteger':
        return self._attenuation_raw

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    async def auto_pdh(self) -> None:
        await self.__client.exec(self.__name + ':auto-pdh', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadPid:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._gain = NloLaserHeadGain(client, name + ':gain')

    @property
    def gain(self) -> 'NloLaserHeadGain':
        return self._gain


class NloLaserHeadGain:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._i_cutoff_enabled = MutableDecopBoolean(client, name + ':i-cutoff-enabled')
        self._d = MutableDecopReal(client, name + ':d')
        self._all = MutableDecopReal(client, name + ':all')
        self._i = MutableDecopReal(client, name + ':i')
        self._i_cutoff = MutableDecopReal(client, name + ':i-cutoff')
        self._p = MutableDecopReal(client, name + ':p')

    @property
    def i_cutoff_enabled(self) -> 'MutableDecopBoolean':
        return self._i_cutoff_enabled

    @property
    def d(self) -> 'MutableDecopReal':
        return self._d

    @property
    def all(self) -> 'MutableDecopReal':
        return self._all

    @property
    def i(self) -> 'MutableDecopReal':
        return self._i

    @property
    def i_cutoff(self) -> 'MutableDecopReal':
        return self._i_cutoff

    @property
    def p(self) -> 'MutableDecopReal':
        return self._p


class PiezoDrv1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')
        self._output_filter = OutputFilter1(client, name + ':output-filter')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._voltage_set_dithering = MutableDecopBoolean(client, name + ':voltage-set-dithering')
        self._voltage_set = MutableDecopReal(client, name + ':voltage-set')
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._path = DecopString(client, name + ':path')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._external_input = ExtInput1(client, name + ':external-input')

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max

    @property
    def output_filter(self) -> 'OutputFilter1':
        return self._output_filter

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def voltage_set_dithering(self) -> 'MutableDecopBoolean':
        return self._voltage_set_dithering

    @property
    def voltage_set(self) -> 'MutableDecopReal':
        return self._voltage_set

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def external_input(self) -> 'ExtInput1':
        return self._external_input


class ExtInput1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._factor = MutableDecopReal(client, name + ':factor')
        self._signal = MutableDecopInteger(client, name + ':signal')

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def factor(self) -> 'MutableDecopReal':
        return self._factor

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal


class NloLaserHeadScopeT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._update_rate = MutableDecopInteger(client, name + ':update-rate')
        self._data = DecopBinary(client, name + ':data')
        self._channelx = NloLaserHeadScopeXAxisT(client, name + ':channelx')
        self._channel1 = NloLaserHeadScopeChannelT(client, name + ':channel1')
        self._variant = MutableDecopInteger(client, name + ':variant')
        self._timescale = MutableDecopReal(client, name + ':timescale')
        self._channel2 = NloLaserHeadScopeChannelT(client, name + ':channel2')

    @property
    def update_rate(self) -> 'MutableDecopInteger':
        return self._update_rate

    @property
    def data(self) -> 'DecopBinary':
        return self._data

    @property
    def channelx(self) -> 'NloLaserHeadScopeXAxisT':
        return self._channelx

    @property
    def channel1(self) -> 'NloLaserHeadScopeChannelT':
        return self._channel1

    @property
    def variant(self) -> 'MutableDecopInteger':
        return self._variant

    @property
    def timescale(self) -> 'MutableDecopReal':
        return self._timescale

    @property
    def channel2(self) -> 'NloLaserHeadScopeChannelT':
        return self._channel2


class NloLaserHeadScopeXAxisT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scope_timescale = MutableDecopReal(client, name + ':scope-timescale')
        self._xy_signal = MutableDecopInteger(client, name + ':xy-signal')
        self._unit = DecopString(client, name + ':unit')
        self._name = DecopString(client, name + ':name')
        self._spectrum_range = MutableDecopReal(client, name + ':spectrum-range')
        self._spectrum_omit_dc = MutableDecopBoolean(client, name + ':spectrum-omit-dc')

    @property
    def scope_timescale(self) -> 'MutableDecopReal':
        return self._scope_timescale

    @property
    def xy_signal(self) -> 'MutableDecopInteger':
        return self._xy_signal

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def spectrum_range(self) -> 'MutableDecopReal':
        return self._spectrum_range

    @property
    def spectrum_omit_dc(self) -> 'MutableDecopBoolean':
        return self._spectrum_omit_dc


class NloLaserHeadScopeChannelT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._unit = DecopString(client, name + ':unit')
        self._name = DecopString(client, name + ':name')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._signal = MutableDecopInteger(client, name + ':signal')

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal


class NloLaserHeadSiggen:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._offset = MutableDecopReal(client, name + ':offset')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def offset(self) -> 'MutableDecopReal':
        return self._offset

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class NloLaserHeadPowerOptimization:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._stage3 = NloLaserHeadStage(client, name + ':stage3')
        self._progress_data_amp = DecopBinary(client, name + ':progress-data-amp')
        self._progress_data_shg = DecopBinary(client, name + ':progress-data-shg')
        self._progress_data_fiber = DecopBinary(client, name + ':progress-data-fiber')
        self._abort = MutableDecopBoolean(client, name + ':abort')
        self._status_string = DecopString(client, name + ':status-string')
        self._status = DecopInteger(client, name + ':status')
        self._ongoing = DecopBoolean(client, name + ':ongoing')
        self._stage4 = NloLaserHeadStage(client, name + ':stage4')
        self._stage1 = NloLaserHeadStage(client, name + ':stage1')
        self._progress = DecopInteger(client, name + ':progress')
        self._shg_advanced = MutableDecopBoolean(client, name + ':shg-advanced')
        self._stage5 = NloLaserHeadStage(client, name + ':stage5')
        self._progress_data_fhg = DecopBinary(client, name + ':progress-data-fhg')
        self._stage2 = NloLaserHeadStage(client, name + ':stage2')

    @property
    def stage3(self) -> 'NloLaserHeadStage':
        return self._stage3

    @property
    def progress_data_amp(self) -> 'DecopBinary':
        return self._progress_data_amp

    @property
    def progress_data_shg(self) -> 'DecopBinary':
        return self._progress_data_shg

    @property
    def progress_data_fiber(self) -> 'DecopBinary':
        return self._progress_data_fiber

    @property
    def abort(self) -> 'MutableDecopBoolean':
        return self._abort

    @property
    def status_string(self) -> 'DecopString':
        return self._status_string

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def ongoing(self) -> 'DecopBoolean':
        return self._ongoing

    @property
    def stage4(self) -> 'NloLaserHeadStage':
        return self._stage4

    @property
    def stage1(self) -> 'NloLaserHeadStage':
        return self._stage1

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    @property
    def shg_advanced(self) -> 'MutableDecopBoolean':
        return self._shg_advanced

    @property
    def stage5(self) -> 'NloLaserHeadStage':
        return self._stage5

    @property
    def progress_data_fhg(self) -> 'DecopBinary':
        return self._progress_data_fhg

    @property
    def stage2(self) -> 'NloLaserHeadStage':
        return self._stage2

    async def start_optimization_amp(self) -> int:
        return await self.__client.exec(self.__name + ':start-optimization-amp', input_stream=None, output_type=None, return_type=int)

    async def start_optimization_fhg(self) -> int:
        return await self.__client.exec(self.__name + ':start-optimization-fhg', input_stream=None, output_type=None, return_type=int)

    async def start_optimization_fiber(self) -> int:
        return await self.__client.exec(self.__name + ':start-optimization-fiber', input_stream=None, output_type=None, return_type=int)

    async def start_optimization_all(self) -> int:
        return await self.__client.exec(self.__name + ':start-optimization-all', input_stream=None, output_type=None, return_type=int)

    async def start_optimization_shg(self) -> int:
        return await self.__client.exec(self.__name + ':start-optimization-shg', input_stream=None, output_type=None, return_type=int)


class NloLaserHeadStage:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._progress = DecopInteger(client, name + ':progress')
        self._restore_on_regress = MutableDecopBoolean(client, name + ':restore-on-regress')
        self._optimization_in_progress = DecopBoolean(client, name + ':optimization-in-progress')
        self._regress_tolerance = MutableDecopInteger(client, name + ':regress-tolerance')
        self._input = NloLaserHeadOptInput(client, name + ':input')
        self._restore_on_abort = MutableDecopBoolean(client, name + ':restore-on-abort')

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    @property
    def restore_on_regress(self) -> 'MutableDecopBoolean':
        return self._restore_on_regress

    @property
    def optimization_in_progress(self) -> 'DecopBoolean':
        return self._optimization_in_progress

    @property
    def regress_tolerance(self) -> 'MutableDecopInteger':
        return self._regress_tolerance

    @property
    def input(self) -> 'NloLaserHeadOptInput':
        return self._input

    @property
    def restore_on_abort(self) -> 'MutableDecopBoolean':
        return self._restore_on_abort

    async def start_optimization(self) -> int:
        return await self.__client.exec(self.__name + ':start-optimization', input_stream=None, output_type=None, return_type=int)


class NloLaserHeadOptInput:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_calibrated = DecopReal(client, name + ':value-calibrated')

    @property
    def value_calibrated(self) -> 'DecopReal':
        return self._value_calibrated


class NloLaserHeadPhotoDiodes:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fiber = NloLaserHeadNloPhotodiode(client, name + ':fiber')
        self._fhg_pdh_dc = NloLaserHeadNloDigilockPhotodiode(client, name + ':fhg-pdh-dc')
        self._fhg = NloLaserHeadNloPhotodiode(client, name + ':fhg')
        self._shg = NloLaserHeadNloPhotodiode(client, name + ':shg')
        self._fhg_pdh_rf = NloLaserHeadNloPdhPhotodiode(client, name + ':fhg-pdh-rf')
        self._shg_int = NloLaserHeadNloDigilockPhotodiode(client, name + ':shg-int')
        self._amp = NloLaserHeadNloPhotodiode(client, name + ':amp')
        self._shg_pdh_rf = NloLaserHeadNloPdhPhotodiode(client, name + ':shg-pdh-rf')
        self._shg_pdh_dc = NloLaserHeadNloDigilockPhotodiode(client, name + ':shg-pdh-dc')
        self._dl = NloLaserHeadNloPhotodiode(client, name + ':dl')
        self._fhg_int = NloLaserHeadNloDigilockPhotodiode(client, name + ':fhg-int')

    @property
    def fiber(self) -> 'NloLaserHeadNloPhotodiode':
        return self._fiber

    @property
    def fhg_pdh_dc(self) -> 'NloLaserHeadNloDigilockPhotodiode':
        return self._fhg_pdh_dc

    @property
    def fhg(self) -> 'NloLaserHeadNloPhotodiode':
        return self._fhg

    @property
    def shg(self) -> 'NloLaserHeadNloPhotodiode':
        return self._shg

    @property
    def fhg_pdh_rf(self) -> 'NloLaserHeadNloPdhPhotodiode':
        return self._fhg_pdh_rf

    @property
    def shg_int(self) -> 'NloLaserHeadNloDigilockPhotodiode':
        return self._shg_int

    @property
    def amp(self) -> 'NloLaserHeadNloPhotodiode':
        return self._amp

    @property
    def shg_pdh_rf(self) -> 'NloLaserHeadNloPdhPhotodiode':
        return self._shg_pdh_rf

    @property
    def shg_pdh_dc(self) -> 'NloLaserHeadNloDigilockPhotodiode':
        return self._shg_pdh_dc

    @property
    def dl(self) -> 'NloLaserHeadNloPhotodiode':
        return self._dl

    @property
    def fhg_int(self) -> 'NloLaserHeadNloDigilockPhotodiode':
        return self._fhg_int


class NloLaserHeadNloPhotodiode:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._power = DecopReal(client, name + ':power')

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def power(self) -> 'DecopReal':
        return self._power


class NloLaserHeadNloDigilockPhotodiode:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')
        self._photodiode = DecopReal(client, name + ':photodiode')

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode


class NloLaserHeadNloPdhPhotodiode:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._gain = MutableDecopReal(client, name + ':gain')
        self._photodiode = DecopReal(client, name + ':photodiode')

    @property
    def gain(self) -> 'MutableDecopReal':
        return self._gain

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode


class Fhg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcChannel(client, name + ':tc')
        self._factory_settings = FhgFactorySettings(client, name + ':factory-settings')
        self._lock = NloLaserHeadLockFhg(client, name + ':lock')
        self._pc = PiezoDrv1(client, name + ':pc')
        self._scope = NloLaserHeadScopeT(client, name + ':scope')
        self._scan = NloLaserHeadSiggen(client, name + ':scan')

    @property
    def tc(self) -> 'TcChannel':
        return self._tc

    @property
    def factory_settings(self) -> 'FhgFactorySettings':
        return self._factory_settings

    @property
    def lock(self) -> 'NloLaserHeadLockFhg':
        return self._lock

    @property
    def pc(self) -> 'PiezoDrv1':
        return self._pc

    @property
    def scope(self) -> 'NloLaserHeadScopeT':
        return self._scope

    @property
    def scan(self) -> 'NloLaserHeadSiggen':
        return self._scan

    async def store(self) -> None:
        await self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    async def restore(self) -> None:
        await self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)


class FhgFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = NloLaserHeadTcFactorySettings(client, name + ':tc')
        self._pd = NloLaserHeadFhgPhotodiodesFactorySettings(client, name + ':pd')
        self._pc = NloLaserHeadPcFactorySettings(client, name + ':pc')
        self._modified = DecopBoolean(client, name + ':modified')
        self._lock = NloLaserHeadLockFactorySettings(client, name + ':lock')

    @property
    def tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._tc

    @property
    def pd(self) -> 'NloLaserHeadFhgPhotodiodesFactorySettings':
        return self._pd

    @property
    def pc(self) -> 'NloLaserHeadPcFactorySettings':
        return self._pc

    @property
    def modified(self) -> 'DecopBoolean':
        return self._modified

    @property
    def lock(self) -> 'NloLaserHeadLockFactorySettings':
        return self._lock

    async def apply(self) -> None:
        await self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    async def retrieve_now(self) -> None:
        await self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadFhgPhotodiodesFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pdh_rf = NloLaserHeadPdPdhFactorySettings(client, name + ':pdh-rf')
        self._pdh_dc = NloLaserHeadPdDigilockFactorySettings(client, name + ':pdh-dc')
        self._fhg = NloLaserHeadPdFactorySettings(client, name + ':fhg')
        self._int = NloLaserHeadPdDigilockFactorySettings(client, name + ':int')

    @property
    def pdh_rf(self) -> 'NloLaserHeadPdPdhFactorySettings':
        return self._pdh_rf

    @property
    def pdh_dc(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._pdh_dc

    @property
    def fhg(self) -> 'NloLaserHeadPdFactorySettings':
        return self._fhg

    @property
    def int(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._int


class NloLaserHeadLockFhg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._window = NloLaserHeadWindow(client, name + ':window')
        self._state = MutableDecopInteger(client, name + ':state')
        self._pid_selection = MutableDecopInteger(client, name + ':pid-selection')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._background_trace = DecopBinary(client, name + ':background-trace')
        self._relock = NloLaserHeadRelock(client, name + ':relock')
        self._lock_enabled = MutableDecopBoolean(client, name + ':lock-enabled')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._local_oscillator = NloLaserHeadLocalOscillatorFhg(client, name + ':local-oscillator')
        self._cavity_fast_pzt_voltage = MutableDecopReal(client, name + ':cavity-fast-pzt-voltage')
        self._pid2 = NloLaserHeadPid(client, name + ':pid2')
        self._cavity_slow_pzt_voltage = MutableDecopReal(client, name + ':cavity-slow-pzt-voltage')
        self._pid1 = NloLaserHeadPid(client, name + ':pid1')

    @property
    def window(self) -> 'NloLaserHeadWindow':
        return self._window

    @property
    def state(self) -> 'MutableDecopInteger':
        return self._state

    @property
    def pid_selection(self) -> 'MutableDecopInteger':
        return self._pid_selection

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def background_trace(self) -> 'DecopBinary':
        return self._background_trace

    @property
    def relock(self) -> 'NloLaserHeadRelock':
        return self._relock

    @property
    def lock_enabled(self) -> 'MutableDecopBoolean':
        return self._lock_enabled

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorFhg':
        return self._local_oscillator

    @property
    def cavity_fast_pzt_voltage(self) -> 'MutableDecopReal':
        return self._cavity_fast_pzt_voltage

    @property
    def pid2(self) -> 'NloLaserHeadPid':
        return self._pid2

    @property
    def cavity_slow_pzt_voltage(self) -> 'MutableDecopReal':
        return self._cavity_slow_pzt_voltage

    @property
    def pid1(self) -> 'NloLaserHeadPid':
        return self._pid1


class NloLaserHeadLocalOscillatorFhg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._use_fast_oscillator = MutableDecopBoolean(client, name + ':use-fast-oscillator')
        self._coupled_modulation = MutableDecopBoolean(client, name + ':coupled-modulation')
        self._use_external_oscillator = MutableDecopBoolean(client, name + ':use-external-oscillator')
        self._phase_shift = MutableDecopReal(client, name + ':phase-shift')
        self._attenuation_raw = MutableDecopInteger(client, name + ':attenuation-raw')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def use_fast_oscillator(self) -> 'MutableDecopBoolean':
        return self._use_fast_oscillator

    @property
    def coupled_modulation(self) -> 'MutableDecopBoolean':
        return self._coupled_modulation

    @property
    def use_external_oscillator(self) -> 'MutableDecopBoolean':
        return self._use_external_oscillator

    @property
    def phase_shift(self) -> 'MutableDecopReal':
        return self._phase_shift

    @property
    def attenuation_raw(self) -> 'MutableDecopInteger':
        return self._attenuation_raw

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    async def auto_pdh(self) -> None:
        await self.__client.exec(self.__name + ':auto-pdh', input_stream=None, output_type=None, return_type=None)


class CtlT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._wavelength_act = DecopReal(client, name + ':wavelength-act')
        self._state = DecopInteger(client, name + ':state')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._motor = CtlMotor(client, name + ':motor')
        self._tuning_current_min = DecopReal(client, name + ':tuning-current-min')
        self._power = CtlPower(client, name + ':power')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._optimization = CtlOptimizationT(client, name + ':optimization')
        self._wavelength_set = MutableDecopReal(client, name + ':wavelength-set')
        self._tuning_power_min = DecopReal(client, name + ':tuning-power-min')
        self._head_temperature = DecopReal(client, name + ':head-temperature')
        self._factory_settings = CtlFactory(client, name + ':factory-settings')
        self._wavelength_max = DecopReal(client, name + ':wavelength-max')
        self._remote_control = CtlRemoteControl(client, name + ':remote-control')
        self._mode_control = CtlModeControl(client, name + ':mode-control')
        self._wavelength_min = DecopReal(client, name + ':wavelength-min')
        self._scan = CtlScanT(client, name + ':scan')

    @property
    def wavelength_act(self) -> 'DecopReal':
        return self._wavelength_act

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def motor(self) -> 'CtlMotor':
        return self._motor

    @property
    def tuning_current_min(self) -> 'DecopReal':
        return self._tuning_current_min

    @property
    def power(self) -> 'CtlPower':
        return self._power

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def optimization(self) -> 'CtlOptimizationT':
        return self._optimization

    @property
    def wavelength_set(self) -> 'MutableDecopReal':
        return self._wavelength_set

    @property
    def tuning_power_min(self) -> 'DecopReal':
        return self._tuning_power_min

    @property
    def head_temperature(self) -> 'DecopReal':
        return self._head_temperature

    @property
    def factory_settings(self) -> 'CtlFactory':
        return self._factory_settings

    @property
    def wavelength_max(self) -> 'DecopReal':
        return self._wavelength_max

    @property
    def remote_control(self) -> 'CtlRemoteControl':
        return self._remote_control

    @property
    def mode_control(self) -> 'CtlModeControl':
        return self._mode_control

    @property
    def wavelength_min(self) -> 'DecopReal':
        return self._wavelength_min

    @property
    def scan(self) -> 'CtlScanT':
        return self._scan


class CtlMotor:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_save_disabled = MutableDecopBoolean(client, name + ':power-save-disabled')
        self._position_hysteresis = MutableDecopInteger(client, name + ':position-hysteresis')
        self._position_accuracy = MutableDecopInteger(client, name + ':position-accuracy')

    @property
    def power_save_disabled(self) -> 'MutableDecopBoolean':
        return self._power_save_disabled

    @property
    def position_hysteresis(self) -> 'MutableDecopInteger':
        return self._position_hysteresis

    @property
    def position_accuracy(self) -> 'MutableDecopInteger':
        return self._position_accuracy


class CtlPower:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_act = DecopReal(client, name + ':power-act')

    @property
    def power_act(self) -> 'DecopReal':
        return self._power_act


class CtlOptimizationT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._progress = DecopInteger(client, name + ':progress')

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    async def flow(self) -> None:
        await self.__client.exec(self.__name + ':flow', input_stream=None, output_type=None, return_type=None)

    async def abort(self) -> None:
        await self.__client.exec(self.__name + ':abort', input_stream=None, output_type=None, return_type=None)

    async def smile(self) -> None:
        await self.__client.exec(self.__name + ':smile', input_stream=None, output_type=None, return_type=None)


class CtlFactory:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tuning_power_min = DecopReal(client, name + ':tuning-power-min')
        self._wavelength_max = DecopReal(client, name + ':wavelength-max')
        self._tuning_current_min = DecopReal(client, name + ':tuning-current-min')
        self._wavelength_min = DecopReal(client, name + ':wavelength-min')

    @property
    def tuning_power_min(self) -> 'DecopReal':
        return self._tuning_power_min

    @property
    def wavelength_max(self) -> 'DecopReal':
        return self._wavelength_max

    @property
    def tuning_current_min(self) -> 'DecopReal':
        return self._tuning_current_min

    @property
    def wavelength_min(self) -> 'DecopReal':
        return self._wavelength_min

    async def apply(self) -> None:
        await self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)


class CtlRemoteControl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._speed = MutableDecopReal(client, name + ':speed')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._factor = MutableDecopReal(client, name + ':factor')
        self._signal = MutableDecopInteger(client, name + ':signal')

    @property
    def speed(self) -> 'MutableDecopReal':
        return self._speed

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def factor(self) -> 'MutableDecopReal':
        return self._factor

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal


class CtlModeControl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._loop_enabled = MutableDecopBoolean(client, name + ':loop-enabled')

    @property
    def loop_enabled(self) -> 'MutableDecopBoolean':
        return self._loop_enabled


class CtlScanT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._wavelength_begin = MutableDecopReal(client, name + ':wavelength-begin')
        self._trigger = CtlTriggerT(client, name + ':trigger')
        self._microsteps = MutableDecopBoolean(client, name + ':microsteps')
        self._remaining_time = DecopInteger(client, name + ':remaining-time')
        self._progress = DecopInteger(client, name + ':progress')
        self._continuous_mode = MutableDecopBoolean(client, name + ':continuous-mode')
        self._speed = MutableDecopReal(client, name + ':speed')
        self._wavelength_end = MutableDecopReal(client, name + ':wavelength-end')
        self._speed_min = DecopReal(client, name + ':speed-min')
        self._shape = MutableDecopInteger(client, name + ':shape')
        self._speed_max = DecopReal(client, name + ':speed-max')

    @property
    def wavelength_begin(self) -> 'MutableDecopReal':
        return self._wavelength_begin

    @property
    def trigger(self) -> 'CtlTriggerT':
        return self._trigger

    @property
    def microsteps(self) -> 'MutableDecopBoolean':
        return self._microsteps

    @property
    def remaining_time(self) -> 'DecopInteger':
        return self._remaining_time

    @property
    def progress(self) -> 'DecopInteger':
        return self._progress

    @property
    def continuous_mode(self) -> 'MutableDecopBoolean':
        return self._continuous_mode

    @property
    def speed(self) -> 'MutableDecopReal':
        return self._speed

    @property
    def wavelength_end(self) -> 'MutableDecopReal':
        return self._wavelength_end

    @property
    def speed_min(self) -> 'DecopReal':
        return self._speed_min

    @property
    def shape(self) -> 'MutableDecopInteger':
        return self._shape

    @property
    def speed_max(self) -> 'DecopReal':
        return self._speed_max

    async def stop(self) -> None:
        await self.__client.exec(self.__name + ':stop', input_stream=None, output_type=None, return_type=None)

    async def start(self) -> None:
        await self.__client.exec(self.__name + ':start', input_stream=None, output_type=None, return_type=None)

    async def pause(self) -> None:
        await self.__client.exec(self.__name + ':pause', input_stream=None, output_type=None, return_type=None)

    async def continue_(self) -> None:
        await self.__client.exec(self.__name + ':continue', input_stream=None, output_type=None, return_type=None)


class CtlTriggerT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._output_threshold = MutableDecopReal(client, name + ':output-threshold')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._output_enabled = MutableDecopBoolean(client, name + ':output-enabled')
        self._input_enabled = MutableDecopBoolean(client, name + ':input-enabled')

    @property
    def output_threshold(self) -> 'MutableDecopReal':
        return self._output_threshold

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def output_enabled(self) -> 'MutableDecopBoolean':
        return self._output_enabled

    @property
    def input_enabled(self) -> 'MutableDecopBoolean':
        return self._input_enabled


class ScopeT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._update_rate = MutableDecopInteger(client, name + ':update-rate')
        self._data = DecopBinary(client, name + ':data')
        self._channelx = ScopeXAxisT(client, name + ':channelx')
        self._channel1 = ScopeChannelT(client, name + ':channel1')
        self._variant = MutableDecopInteger(client, name + ':variant')
        self._timescale = MutableDecopReal(client, name + ':timescale')
        self._channel2 = ScopeChannelT(client, name + ':channel2')

    @property
    def update_rate(self) -> 'MutableDecopInteger':
        return self._update_rate

    @property
    def data(self) -> 'DecopBinary':
        return self._data

    @property
    def channelx(self) -> 'ScopeXAxisT':
        return self._channelx

    @property
    def channel1(self) -> 'ScopeChannelT':
        return self._channel1

    @property
    def variant(self) -> 'MutableDecopInteger':
        return self._variant

    @property
    def timescale(self) -> 'MutableDecopReal':
        return self._timescale

    @property
    def channel2(self) -> 'ScopeChannelT':
        return self._channel2


class ScopeXAxisT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scope_timescale = MutableDecopReal(client, name + ':scope-timescale')
        self._xy_signal = MutableDecopInteger(client, name + ':xy-signal')
        self._unit = DecopString(client, name + ':unit')
        self._name = DecopString(client, name + ':name')
        self._spectrum_range = MutableDecopReal(client, name + ':spectrum-range')
        self._spectrum_omit_dc = MutableDecopBoolean(client, name + ':spectrum-omit-dc')

    @property
    def scope_timescale(self) -> 'MutableDecopReal':
        return self._scope_timescale

    @property
    def xy_signal(self) -> 'MutableDecopInteger':
        return self._xy_signal

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def spectrum_range(self) -> 'MutableDecopReal':
        return self._spectrum_range

    @property
    def spectrum_omit_dc(self) -> 'MutableDecopBoolean':
        return self._spectrum_omit_dc


class ScopeChannelT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._unit = DecopString(client, name + ':unit')
        self._name = DecopString(client, name + ':name')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._signal = MutableDecopInteger(client, name + ':signal')

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def name(self) -> 'DecopString':
        return self._name

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def signal(self) -> 'MutableDecopInteger':
        return self._signal


class LaserAmp:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcChannel(client, name + ':tc')
        self._seed_limits = AmpPower(client, name + ':seed-limits')
        self._ontime_txt = DecopString(client, name + ':ontime-txt')
        self._legacy = DecopBoolean(client, name + ':legacy')
        self._output_limits = AmpPower(client, name + ':output-limits')
        self._cc = Cc5000Drv(client, name + ':cc')
        self._seedonly_check = AmpSeedonlyCheck(client, name + ':seedonly-check')
        self._type_ = DecopString(client, name + ':type')
        self._ontime = DecopInteger(client, name + ':ontime')
        self._factory_settings = AmpFactory(client, name + ':factory-settings')
        self._version = DecopString(client, name + ':version')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def tc(self) -> 'TcChannel':
        return self._tc

    @property
    def seed_limits(self) -> 'AmpPower':
        return self._seed_limits

    @property
    def ontime_txt(self) -> 'DecopString':
        return self._ontime_txt

    @property
    def legacy(self) -> 'DecopBoolean':
        return self._legacy

    @property
    def output_limits(self) -> 'AmpPower':
        return self._output_limits

    @property
    def cc(self) -> 'Cc5000Drv':
        return self._cc

    @property
    def seedonly_check(self) -> 'AmpSeedonlyCheck':
        return self._seedonly_check

    @property
    def type_(self) -> 'DecopString':
        return self._type_

    @property
    def ontime(self) -> 'DecopInteger':
        return self._ontime

    @property
    def factory_settings(self) -> 'AmpFactory':
        return self._factory_settings

    @property
    def version(self) -> 'DecopString':
        return self._version

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    async def store(self) -> None:
        await self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    async def restore(self) -> None:
        await self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)


class AmpPower:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_max_shutdown_delay = MutableDecopReal(client, name + ':power-max-shutdown-delay')
        self._power_min_warning_delay = MutableDecopReal(client, name + ':power-min-warning-delay')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._power = DecopReal(client, name + ':power')
        self._photodiode = DecopReal(client, name + ':photodiode')
        self._power_min_shutdown_delay = MutableDecopReal(client, name + ':power-min-shutdown-delay')
        self._power_max = MutableDecopReal(client, name + ':power-max')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._status = DecopInteger(client, name + ':status')
        self._power_min = MutableDecopReal(client, name + ':power-min')
        self._power_max_warning_delay = MutableDecopReal(client, name + ':power-max-warning-delay')

    @property
    def power_max_shutdown_delay(self) -> 'MutableDecopReal':
        return self._power_max_shutdown_delay

    @property
    def power_min_warning_delay(self) -> 'MutableDecopReal':
        return self._power_min_warning_delay

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def power(self) -> 'DecopReal':
        return self._power

    @property
    def photodiode(self) -> 'DecopReal':
        return self._photodiode

    @property
    def power_min_shutdown_delay(self) -> 'MutableDecopReal':
        return self._power_min_shutdown_delay

    @property
    def power_max(self) -> 'MutableDecopReal':
        return self._power_max

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def power_min(self) -> 'MutableDecopReal':
        return self._power_min

    @property
    def power_max_warning_delay(self) -> 'MutableDecopReal':
        return self._power_max_warning_delay


class AmpSeedonlyCheck:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pump = DecopBoolean(client, name + ':pump')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._seed = DecopBoolean(client, name + ':seed')
        self._shutdown_delay = MutableDecopReal(client, name + ':shutdown-delay')
        self._warning_delay = MutableDecopReal(client, name + ':warning-delay')
        self._status = DecopInteger(client, name + ':status')

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
    def shutdown_delay(self) -> 'MutableDecopReal':
        return self._shutdown_delay

    @property
    def warning_delay(self) -> 'MutableDecopReal':
        return self._warning_delay

    @property
    def status(self) -> 'DecopInteger':
        return self._status


class AmpFactory:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcFactorySettings(client, name + ':tc')
        self._seed_limits = AmpFactoryPower(client, name + ':seed-limits')
        self._wavelength = MutableDecopReal(client, name + ':wavelength')
        self._modified = DecopBoolean(client, name + ':modified')
        self._last_modified = DecopString(client, name + ':last-modified')
        self._output_limits = AmpFactoryPower(client, name + ':output-limits')
        self._power = MutableDecopReal(client, name + ':power')
        self._seedonly_check = AmpFactorySeedonly(client, name + ':seedonly-check')
        self._cc = AmpFactoryCc(client, name + ':cc')

    @property
    def tc(self) -> 'TcFactorySettings':
        return self._tc

    @property
    def seed_limits(self) -> 'AmpFactoryPower':
        return self._seed_limits

    @property
    def wavelength(self) -> 'MutableDecopReal':
        return self._wavelength

    @property
    def modified(self) -> 'DecopBoolean':
        return self._modified

    @property
    def last_modified(self) -> 'DecopString':
        return self._last_modified

    @property
    def output_limits(self) -> 'AmpFactoryPower':
        return self._output_limits

    @property
    def power(self) -> 'MutableDecopReal':
        return self._power

    @property
    def seedonly_check(self) -> 'AmpFactorySeedonly':
        return self._seedonly_check

    @property
    def cc(self) -> 'AmpFactoryCc':
        return self._cc

    async def apply(self) -> None:
        await self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    async def retrieve_now(self) -> None:
        await self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class TcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._temp_roc_limit = MutableDecopReal(client, name + ':temp-roc-limit')
        self._timeout = MutableDecopInteger(client, name + ':timeout')
        self._power_source = MutableDecopInteger(client, name + ':power-source')
        self._temp_min = MutableDecopReal(client, name + ':temp-min')
        self._ok_tolerance = MutableDecopReal(client, name + ':ok-tolerance')
        self._current_max = MutableDecopReal(client, name + ':current-max')
        self._current_min = MutableDecopReal(client, name + ':current-min')
        self._p_gain = MutableDecopReal(client, name + ':p-gain')
        self._ok_time = MutableDecopReal(client, name + ':ok-time')
        self._i_gain = MutableDecopReal(client, name + ':i-gain')
        self._temp_max = MutableDecopReal(client, name + ':temp-max')
        self._temp_roc_enabled = MutableDecopBoolean(client, name + ':temp-roc-enabled')
        self._temp_set = MutableDecopReal(client, name + ':temp-set')
        self._c_gain = MutableDecopReal(client, name + ':c-gain')
        self._ntc_series_resistance = MutableDecopReal(client, name + ':ntc-series-resistance')
        self._d_gain = MutableDecopReal(client, name + ':d-gain')

    @property
    def temp_roc_limit(self) -> 'MutableDecopReal':
        return self._temp_roc_limit

    @property
    def timeout(self) -> 'MutableDecopInteger':
        return self._timeout

    @property
    def power_source(self) -> 'MutableDecopInteger':
        return self._power_source

    @property
    def temp_min(self) -> 'MutableDecopReal':
        return self._temp_min

    @property
    def ok_tolerance(self) -> 'MutableDecopReal':
        return self._ok_tolerance

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
    def ok_time(self) -> 'MutableDecopReal':
        return self._ok_time

    @property
    def i_gain(self) -> 'MutableDecopReal':
        return self._i_gain

    @property
    def temp_max(self) -> 'MutableDecopReal':
        return self._temp_max

    @property
    def temp_roc_enabled(self) -> 'MutableDecopBoolean':
        return self._temp_roc_enabled

    @property
    def temp_set(self) -> 'MutableDecopReal':
        return self._temp_set

    @property
    def c_gain(self) -> 'MutableDecopReal':
        return self._c_gain

    @property
    def ntc_series_resistance(self) -> 'MutableDecopReal':
        return self._ntc_series_resistance

    @property
    def d_gain(self) -> 'MutableDecopReal':
        return self._d_gain


class AmpFactoryPower:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_max_shutdown_delay = MutableDecopReal(client, name + ':power-max-shutdown-delay')
        self._power_max = MutableDecopReal(client, name + ':power-max')
        self._power_min_warning_delay = MutableDecopReal(client, name + ':power-min-warning-delay')
        self._power_max_warning_delay = MutableDecopReal(client, name + ':power-max-warning-delay')
        self._power_min = MutableDecopReal(client, name + ':power-min')
        self._cal_factor = MutableDecopReal(client, name + ':cal-factor')
        self._cal_offset = MutableDecopReal(client, name + ':cal-offset')
        self._power_min_shutdown_delay = MutableDecopReal(client, name + ':power-min-shutdown-delay')

    @property
    def power_max_shutdown_delay(self) -> 'MutableDecopReal':
        return self._power_max_shutdown_delay

    @property
    def power_max(self) -> 'MutableDecopReal':
        return self._power_max

    @property
    def power_min_warning_delay(self) -> 'MutableDecopReal':
        return self._power_min_warning_delay

    @property
    def power_max_warning_delay(self) -> 'MutableDecopReal':
        return self._power_max_warning_delay

    @property
    def power_min(self) -> 'MutableDecopReal':
        return self._power_min

    @property
    def cal_factor(self) -> 'MutableDecopReal':
        return self._cal_factor

    @property
    def cal_offset(self) -> 'MutableDecopReal':
        return self._cal_offset

    @property
    def power_min_shutdown_delay(self) -> 'MutableDecopReal':
        return self._power_min_shutdown_delay


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


class AmpFactoryCc:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._current_clip_modified = DecopBoolean(client, name + ':current-clip-modified')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')
        self._current_set = MutableDecopReal(client, name + ':current-set')
        self._current_clip_last_modified = DecopString(client, name + ':current-clip-last-modified')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def current_clip_modified(self) -> 'DecopBoolean':
        return self._current_clip_modified

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set

    @property
    def current_clip_last_modified(self) -> 'DecopString':
        return self._current_clip_last_modified

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor


class PwrStab:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._window = PwrStabWindow(client, name + ':window')
        self._state = DecopInteger(client, name + ':state')
        self._hold_output_on_unlock = MutableDecopBoolean(client, name + ':hold-output-on-unlock')
        self._output_channel = DecopInteger(client, name + ':output-channel')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._input_channel_value_act = DecopReal(client, name + ':input-channel-value-act')
        self._gain = PwrStabGain(client, name + ':gain')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._sign = MutableDecopBoolean(client, name + ':sign')

    @property
    def window(self) -> 'PwrStabWindow':
        return self._window

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def hold_output_on_unlock(self) -> 'MutableDecopBoolean':
        return self._hold_output_on_unlock

    @property
    def output_channel(self) -> 'DecopInteger':
        return self._output_channel

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def input_channel_value_act(self) -> 'DecopReal':
        return self._input_channel_value_act

    @property
    def gain(self) -> 'PwrStabGain':
        return self._gain

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def sign(self) -> 'MutableDecopBoolean':
        return self._sign


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


class PwrStabGain:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._d = MutableDecopReal(client, name + ':d')
        self._i = MutableDecopReal(client, name + ':i')
        self._p = MutableDecopReal(client, name + ':p')
        self._all = MutableDecopReal(client, name + ':all')

    @property
    def d(self) -> 'MutableDecopReal':
        return self._d

    @property
    def i(self) -> 'MutableDecopReal':
        return self._i

    @property
    def p(self) -> 'MutableDecopReal':
        return self._p

    @property
    def all(self) -> 'MutableDecopReal':
        return self._all


class LaserHead:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcChannel(client, name + ':tc')
        self._ontime_txt = DecopString(client, name + ':ontime-txt')
        self._legacy = DecopBoolean(client, name + ':legacy')
        self._lock = Lock(client, name + ':lock')
        self._pc = PiezoDrv1(client, name + ':pc')
        self._cc = CurrDrv1(client, name + ':cc')
        self._type_ = DecopString(client, name + ':type')
        self._ontime = DecopInteger(client, name + ':ontime')
        self._factory_settings = LhFactory(client, name + ':factory-settings')
        self._version = DecopString(client, name + ':version')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def tc(self) -> 'TcChannel':
        return self._tc

    @property
    def ontime_txt(self) -> 'DecopString':
        return self._ontime_txt

    @property
    def legacy(self) -> 'DecopBoolean':
        return self._legacy

    @property
    def lock(self) -> 'Lock':
        return self._lock

    @property
    def pc(self) -> 'PiezoDrv1':
        return self._pc

    @property
    def cc(self) -> 'CurrDrv1':
        return self._cc

    @property
    def type_(self) -> 'DecopString':
        return self._type_

    @property
    def ontime(self) -> 'DecopInteger':
        return self._ontime

    @property
    def factory_settings(self) -> 'LhFactory':
        return self._factory_settings

    @property
    def version(self) -> 'DecopString':
        return self._version

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    async def store(self) -> None:
        await self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    async def restore(self) -> None:
        await self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)


class Lock:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._reset = AlReset(client, name + ':reset')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._candidate_filter = AlCandidateFilter(client, name + ':candidate-filter')
        self._locking_delay = MutableDecopInteger(client, name + ':locking-delay')
        self._state = DecopInteger(client, name + ':state')
        self._pid_selection = MutableDecopInteger(client, name + ':pid-selection')
        self._relock = AlRelock(client, name + ':relock')
        self._spectrum_input_channel = MutableDecopInteger(client, name + ':spectrum-input-channel')
        self._window = AlWindow(client, name + ':window')
        self._state_txt = DecopString(client, name + ':state-txt')
        self._lock_enabled = MutableDecopBoolean(client, name + ':lock-enabled')
        self._type_ = MutableDecopInteger(client, name + ':type')
        self._lockin = Lockin(client, name + ':lockin')
        self._candidates = DecopBinary(client, name + ':candidates')
        self._pid2 = Pid(client, name + ':pid2')
        self._lockpoint = AlLockpoint(client, name + ':lockpoint')
        self._background_trace = DecopBinary(client, name + ':background-trace')
        self._hold = MutableDecopBoolean(client, name + ':hold')
        self._pid1 = Pid(client, name + ':pid1')

    @property
    def reset(self) -> 'AlReset':
        return self._reset

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def candidate_filter(self) -> 'AlCandidateFilter':
        return self._candidate_filter

    @property
    def locking_delay(self) -> 'MutableDecopInteger':
        return self._locking_delay

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    @property
    def pid_selection(self) -> 'MutableDecopInteger':
        return self._pid_selection

    @property
    def relock(self) -> 'AlRelock':
        return self._relock

    @property
    def spectrum_input_channel(self) -> 'MutableDecopInteger':
        return self._spectrum_input_channel

    @property
    def window(self) -> 'AlWindow':
        return self._window

    @property
    def state_txt(self) -> 'DecopString':
        return self._state_txt

    @property
    def lock_enabled(self) -> 'MutableDecopBoolean':
        return self._lock_enabled

    @property
    def type_(self) -> 'MutableDecopInteger':
        return self._type_

    @property
    def lockin(self) -> 'Lockin':
        return self._lockin

    @property
    def candidates(self) -> 'DecopBinary':
        return self._candidates

    @property
    def pid2(self) -> 'Pid':
        return self._pid2

    @property
    def lockpoint(self) -> 'AlLockpoint':
        return self._lockpoint

    @property
    def background_trace(self) -> 'DecopBinary':
        return self._background_trace

    @property
    def hold(self) -> 'MutableDecopBoolean':
        return self._hold

    @property
    def pid1(self) -> 'Pid':
        return self._pid1

    async def select_lockpoint(self, x: float, y: float, type_: int) -> None:
        assert isinstance(x, float), "expected type 'float' for parameter 'x', got '{}'".format(type(x))
        assert isinstance(y, float), "expected type 'float' for parameter 'y', got '{}'".format(type(y))
        assert isinstance(type_, int), "expected type 'int' for parameter 'type_', got '{}'".format(type(type_))
        await self.__client.exec(self.__name + ':select-lockpoint', x, y, type_, input_stream=None, output_type=None, return_type=None)

    async def open(self) -> None:
        await self.__client.exec(self.__name + ':open', input_stream=None, output_type=None, return_type=None)

    async def find_candidates(self) -> None:
        await self.__client.exec(self.__name + ':find-candidates', input_stream=None, output_type=None, return_type=None)

    async def stop_scan(self) -> None:
        await self.__client.exec(self.__name + ':stop-scan', input_stream=None, output_type=None, return_type=None)

    async def show_candidates(self) -> Tuple[str, int]:
        return await self.__client.exec(self.__name + ':show-candidates', input_stream=None, output_type=str, return_type=int)

    async def close(self) -> None:
        await self.__client.exec(self.__name + ':close', input_stream=None, output_type=None, return_type=None)

    async def start_scan(self) -> None:
        await self.__client.exec(self.__name + ':start-scan', input_stream=None, output_type=None, return_type=None)


class AlReset:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class AlCandidateFilter:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._edge_level = MutableDecopReal(client, name + ':edge-level')
        self._edge_min_distance = MutableDecopInteger(client, name + ':edge-min-distance')
        self._peak_noise_tolerance = MutableDecopReal(client, name + ':peak-noise-tolerance')
        self._negative_edge = MutableDecopBoolean(client, name + ':negative-edge')
        self._positive_edge = MutableDecopBoolean(client, name + ':positive-edge')
        self._top = MutableDecopBoolean(client, name + ':top')
        self._bottom = MutableDecopBoolean(client, name + ':bottom')

    @property
    def edge_level(self) -> 'MutableDecopReal':
        return self._edge_level

    @property
    def edge_min_distance(self) -> 'MutableDecopInteger':
        return self._edge_min_distance

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
    def bottom(self) -> 'MutableDecopBoolean':
        return self._bottom


class AlRelock:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._output_channel = MutableDecopInteger(client, name + ':output-channel')
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._delay = MutableDecopReal(client, name + ':delay')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def output_channel(self) -> 'MutableDecopInteger':
        return self._output_channel

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def delay(self) -> 'MutableDecopReal':
        return self._delay

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class AlWindow:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._level_hysteresis = MutableDecopReal(client, name + ':level-hysteresis')
        self._level_low = MutableDecopReal(client, name + ':level-low')
        self._level_high = MutableDecopReal(client, name + ':level-high')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def level_hysteresis(self) -> 'MutableDecopReal':
        return self._level_hysteresis

    @property
    def level_low(self) -> 'MutableDecopReal':
        return self._level_low

    @property
    def level_high(self) -> 'MutableDecopReal':
        return self._level_high

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class Lockin:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._modulation_output_channel = MutableDecopInteger(client, name + ':modulation-output-channel')
        self._modulation_enabled = MutableDecopBoolean(client, name + ':modulation-enabled')
        self._phase_shift = MutableDecopReal(client, name + ':phase-shift')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._lock_level = MutableDecopReal(client, name + ':lock-level')

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def modulation_output_channel(self) -> 'MutableDecopInteger':
        return self._modulation_output_channel

    @property
    def modulation_enabled(self) -> 'MutableDecopBoolean':
        return self._modulation_enabled

    @property
    def phase_shift(self) -> 'MutableDecopReal':
        return self._phase_shift

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def lock_level(self) -> 'MutableDecopReal':
        return self._lock_level


class Pid:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._lock_state = DecopBoolean(client, name + ':lock-state')
        self._output_channel = MutableDecopInteger(client, name + ':output-channel')
        self._outputlimit = Outputlimit(client, name + ':outputlimit')
        self._hold_state = DecopBoolean(client, name + ':hold-state')
        self._input_channel = MutableDecopInteger(client, name + ':input-channel')
        self._setpoint = MutableDecopReal(client, name + ':setpoint')
        self._gain = Gain(client, name + ':gain')
        self._slope = MutableDecopBoolean(client, name + ':slope')
        self._hold_output_on_unlock = MutableDecopBoolean(client, name + ':hold-output-on-unlock')
        self._hold = MutableDecopBoolean(client, name + ':hold')
        self._regulating_state = DecopBoolean(client, name + ':regulating-state')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._sign = MutableDecopBoolean(client, name + ':sign')

    @property
    def lock_state(self) -> 'DecopBoolean':
        return self._lock_state

    @property
    def output_channel(self) -> 'MutableDecopInteger':
        return self._output_channel

    @property
    def outputlimit(self) -> 'Outputlimit':
        return self._outputlimit

    @property
    def hold_state(self) -> 'DecopBoolean':
        return self._hold_state

    @property
    def input_channel(self) -> 'MutableDecopInteger':
        return self._input_channel

    @property
    def setpoint(self) -> 'MutableDecopReal':
        return self._setpoint

    @property
    def gain(self) -> 'Gain':
        return self._gain

    @property
    def slope(self) -> 'MutableDecopBoolean':
        return self._slope

    @property
    def hold_output_on_unlock(self) -> 'MutableDecopBoolean':
        return self._hold_output_on_unlock

    @property
    def hold(self) -> 'MutableDecopBoolean':
        return self._hold

    @property
    def regulating_state(self) -> 'DecopBoolean':
        return self._regulating_state

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def sign(self) -> 'MutableDecopBoolean':
        return self._sign


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


class Gain:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fc_pd = DecopReal(client, name + ':fc-pd')
        self._i = MutableDecopReal(client, name + ':i')
        self._fc_ip = DecopReal(client, name + ':fc-ip')
        self._i_cutoff = MutableDecopReal(client, name + ':i-cutoff')
        self._d = MutableDecopReal(client, name + ':d')
        self._i_cutoff_enabled = MutableDecopBoolean(client, name + ':i-cutoff-enabled')
        self._p = MutableDecopReal(client, name + ':p')
        self._all = MutableDecopReal(client, name + ':all')

    @property
    def fc_pd(self) -> 'DecopReal':
        return self._fc_pd

    @property
    def i(self) -> 'MutableDecopReal':
        return self._i

    @property
    def fc_ip(self) -> 'DecopReal':
        return self._fc_ip

    @property
    def i_cutoff(self) -> 'MutableDecopReal':
        return self._i_cutoff

    @property
    def d(self) -> 'MutableDecopReal':
        return self._d

    @property
    def i_cutoff_enabled(self) -> 'MutableDecopBoolean':
        return self._i_cutoff_enabled

    @property
    def p(self) -> 'MutableDecopReal':
        return self._p

    @property
    def all(self) -> 'MutableDecopReal':
        return self._all


class AlLockpoint:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._type_ = DecopString(client, name + ':type')
        self._position = Coordinate(client, name + ':position')

    @property
    def type_(self) -> 'DecopString':
        return self._type_

    @property
    def position(self) -> 'Coordinate':
        return self._position


class Coordinate:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name

    async def get(self) -> Tuple[float, float]:
        return await self.__client.get(self.__name)

    async def set(self, y: float, x: float) -> None:
        assert isinstance(y, float), "expected type 'float' for 'y', got '{}'".format(type(y))
        assert isinstance(x, float), "expected type 'float' for 'x', got '{}'".format(type(x))
        await self.__client.set(self.__name, y, x)


class CurrDrv1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._forced_off = MutableDecopBoolean(client, name + ':forced-off')
        self._current_clip_limit = DecopReal(client, name + ':current-clip-limit')
        self._current_set_dithering = MutableDecopBoolean(client, name + ':current-set-dithering')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')
        self._output_filter = OutputFilter1(client, name + ':output-filter')
        self._aux = DecopReal(client, name + ':aux')
        self._pd = DecopReal(client, name + ':pd')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._positive_polarity = MutableDecopBoolean(client, name + ':positive-polarity')
        self._current_offset = MutableDecopReal(client, name + ':current-offset')
        self._emission = DecopBoolean(client, name + ':emission')
        self._status = DecopInteger(client, name + ':status')
        self._external_input = ExtInput1(client, name + ':external-input')
        self._current_act = DecopReal(client, name + ':current-act')
        self._variant = DecopString(client, name + ':variant')
        self._snubber = MutableDecopBoolean(client, name + ':snubber')
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._path = DecopString(client, name + ':path')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._current_set = MutableDecopReal(client, name + ':current-set')
        self._status_txt = DecopString(client, name + ':status-txt')

    @property
    def forced_off(self) -> 'MutableDecopBoolean':
        return self._forced_off

    @property
    def current_clip_limit(self) -> 'DecopReal':
        return self._current_clip_limit

    @property
    def current_set_dithering(self) -> 'MutableDecopBoolean':
        return self._current_set_dithering

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip

    @property
    def output_filter(self) -> 'OutputFilter1':
        return self._output_filter

    @property
    def aux(self) -> 'DecopReal':
        return self._aux

    @property
    def pd(self) -> 'DecopReal':
        return self._pd

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def positive_polarity(self) -> 'MutableDecopBoolean':
        return self._positive_polarity

    @property
    def current_offset(self) -> 'MutableDecopReal':
        return self._current_offset

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def external_input(self) -> 'ExtInput1':
        return self._external_input

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def snubber(self) -> 'MutableDecopBoolean':
        return self._snubber

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt


class LhFactory:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcFactorySettings(client, name + ':tc')
        self._wavelength = MutableDecopReal(client, name + ':wavelength')
        self._modified = DecopBoolean(client, name + ':modified')
        self._last_modified = DecopString(client, name + ':last-modified')
        self._threshold_current = MutableDecopReal(client, name + ':threshold-current')
        self._pc = PcFactorySettings(client, name + ':pc')
        self._cc = LhFactoryCc(client, name + ':cc')
        self._power = MutableDecopReal(client, name + ':power')

    @property
    def tc(self) -> 'TcFactorySettings':
        return self._tc

    @property
    def wavelength(self) -> 'MutableDecopReal':
        return self._wavelength

    @property
    def modified(self) -> 'DecopBoolean':
        return self._modified

    @property
    def last_modified(self) -> 'DecopString':
        return self._last_modified

    @property
    def threshold_current(self) -> 'MutableDecopReal':
        return self._threshold_current

    @property
    def pc(self) -> 'PcFactorySettings':
        return self._pc

    @property
    def cc(self) -> 'LhFactoryCc':
        return self._cc

    @property
    def power(self) -> 'MutableDecopReal':
        return self._power

    async def apply(self) -> None:
        await self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    async def retrieve_now(self) -> None:
        await self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class PcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scan_amplitude = MutableDecopReal(client, name + ':scan-amplitude')
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._scan_offset = MutableDecopReal(client, name + ':scan-offset')
        self._slew_rate_enabled = MutableDecopBoolean(client, name + ':slew-rate-enabled')
        self._slew_rate = MutableDecopReal(client, name + ':slew-rate')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._capacitance = MutableDecopReal(client, name + ':capacitance')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')

    @property
    def scan_amplitude(self) -> 'MutableDecopReal':
        return self._scan_amplitude

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def scan_offset(self) -> 'MutableDecopReal':
        return self._scan_offset

    @property
    def slew_rate_enabled(self) -> 'MutableDecopBoolean':
        return self._slew_rate_enabled

    @property
    def slew_rate(self) -> 'MutableDecopReal':
        return self._slew_rate

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def capacitance(self) -> 'MutableDecopReal':
        return self._capacitance

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max


class LhFactoryCc:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._snubber = MutableDecopBoolean(client, name + ':snubber')
        self._current_clip_modified = DecopBoolean(client, name + ':current-clip-modified')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')
        self._current_set = MutableDecopReal(client, name + ':current-set')
        self._current_clip_last_modified = DecopString(client, name + ':current-clip-last-modified')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._positive_polarity = MutableDecopBoolean(client, name + ':positive-polarity')

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def snubber(self) -> 'MutableDecopBoolean':
        return self._snubber

    @property
    def current_clip_modified(self) -> 'DecopBoolean':
        return self._current_clip_modified

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set

    @property
    def current_clip_last_modified(self) -> 'DecopString':
        return self._current_clip_last_modified

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def positive_polarity(self) -> 'MutableDecopBoolean':
        return self._positive_polarity


class Siggen:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecopReal(client, name + ':frequency')
        self._output_channel = MutableDecopInteger(client, name + ':output-channel')
        self._amplitude = MutableDecopReal(client, name + ':amplitude')
        self._offset = MutableDecopReal(client, name + ':offset')
        self._unit = DecopString(client, name + ':unit')
        self._end = MutableDecopReal(client, name + ':end')
        self._signal_type = MutableDecopInteger(client, name + ':signal-type')
        self._start = MutableDecopReal(client, name + ':start')
        self._hold = MutableDecopBoolean(client, name + ':hold')
        self._phase_shift = MutableDecopReal(client, name + ':phase-shift')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')

    @property
    def frequency(self) -> 'MutableDecopReal':
        return self._frequency

    @property
    def output_channel(self) -> 'MutableDecopInteger':
        return self._output_channel

    @property
    def amplitude(self) -> 'MutableDecopReal':
        return self._amplitude

    @property
    def offset(self) -> 'MutableDecopReal':
        return self._offset

    @property
    def unit(self) -> 'DecopString':
        return self._unit

    @property
    def end(self) -> 'MutableDecopReal':
        return self._end

    @property
    def signal_type(self) -> 'MutableDecopInteger':
        return self._signal_type

    @property
    def start(self) -> 'MutableDecopReal':
        return self._start

    @property
    def hold(self) -> 'MutableDecopBoolean':
        return self._hold

    @property
    def phase_shift(self) -> 'MutableDecopReal':
        return self._phase_shift

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled


class McBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._air_pressure = DecopReal(client, name + ':air-pressure')
        self._relative_humidity = DecopReal(client, name + ':relative-humidity')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._serial_number = DecopString(client, name + ':serial-number')
        self._fpga_fw_ver = DecopString(client, name + ':fpga-fw-ver')
        self._revision = DecopString(client, name + ':revision')

    @property
    def air_pressure(self) -> 'DecopReal':
        return self._air_pressure

    @property
    def relative_humidity(self) -> 'DecopReal':
        return self._relative_humidity

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def fpga_fw_ver(self) -> 'DecopString':
        return self._fpga_fw_ver

    @property
    def revision(self) -> 'DecopString':
        return self._revision


class Display:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._brightness = MutableDecopReal(client, name + ':brightness')
        self._auto_dark = MutableDecopBoolean(client, name + ':auto-dark')
        self._idle_timeout = MutableDecopInteger(client, name + ':idle-timeout')
        self._state = DecopInteger(client, name + ':state')

    @property
    def brightness(self) -> 'MutableDecopReal':
        return self._brightness

    @property
    def auto_dark(self) -> 'MutableDecopBoolean':
        return self._auto_dark

    @property
    def idle_timeout(self) -> 'MutableDecopInteger':
        return self._idle_timeout

    @property
    def state(self) -> 'DecopInteger':
        return self._state

    async def update_state(self, active: bool) -> None:
        assert isinstance(active, bool), "expected type 'bool' for parameter 'active', got '{}'".format(type(active))
        await self.__client.exec(self.__name + ':update-state', active, input_stream=None, output_type=None, return_type=None)


class IoBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._digital_in1 = IoDigitalInput(client, name + ':digital-in1')
        self._out_a = IoOutputChannel(client, name + ':out-a')
        self._digital_out1 = IoDigitalOutput(client, name + ':digital-out1')
        self._digital_in3 = IoDigitalInput(client, name + ':digital-in3')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._digital_out0 = IoDigitalOutput(client, name + ':digital-out0')
        self._digital_out2 = IoDigitalOutput(client, name + ':digital-out2')
        self._digital_out3 = IoDigitalOutput(client, name + ':digital-out3')
        self._digital_in2 = IoDigitalInput(client, name + ':digital-in2')
        self._digital_in0 = IoDigitalInput(client, name + ':digital-in0')
        self._serial_number = DecopString(client, name + ':serial-number')
        self._out_b = IoOutputChannel(client, name + ':out-b')
        self._revision = DecopString(client, name + ':revision')

    @property
    def digital_in1(self) -> 'IoDigitalInput':
        return self._digital_in1

    @property
    def out_a(self) -> 'IoOutputChannel':
        return self._out_a

    @property
    def digital_out1(self) -> 'IoDigitalOutput':
        return self._digital_out1

    @property
    def digital_in3(self) -> 'IoDigitalInput':
        return self._digital_in3

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def digital_out0(self) -> 'IoDigitalOutput':
        return self._digital_out0

    @property
    def digital_out2(self) -> 'IoDigitalOutput':
        return self._digital_out2

    @property
    def digital_out3(self) -> 'IoDigitalOutput':
        return self._digital_out3

    @property
    def digital_in2(self) -> 'IoDigitalInput':
        return self._digital_in2

    @property
    def digital_in0(self) -> 'IoDigitalInput':
        return self._digital_in0

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def out_b(self) -> 'IoOutputChannel':
        return self._out_b

    @property
    def revision(self) -> 'DecopString':
        return self._revision


class IoDigitalInput:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_act = DecopBoolean(client, name + ':value-act')

    @property
    def value_act(self) -> 'DecopBoolean':
        return self._value_act


class IoOutputChannel:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_offset = MutableDecopReal(client, name + ':voltage-offset')
        self._output_filter = OutputFilter1(client, name + ':output-filter')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._voltage_set = MutableDecopReal(client, name + ':voltage-set')
        self._voltage_min = MutableDecopReal(client, name + ':voltage-min')
        self._external_input = ExtInput1(client, name + ':external-input')
        self._voltage_max = MutableDecopReal(client, name + ':voltage-max')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')

    @property
    def voltage_offset(self) -> 'MutableDecopReal':
        return self._voltage_offset

    @property
    def output_filter(self) -> 'OutputFilter1':
        return self._output_filter

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def voltage_set(self) -> 'MutableDecopReal':
        return self._voltage_set

    @property
    def voltage_min(self) -> 'MutableDecopReal':
        return self._voltage_min

    @property
    def external_input(self) -> 'ExtInput1':
        return self._external_input

    @property
    def voltage_max(self) -> 'MutableDecopReal':
        return self._voltage_max

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled


class IoDigitalOutput:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_act = DecopBoolean(client, name + ':value-act')
        self._value_set = MutableDecopBoolean(client, name + ':value-set')
        self._mode = MutableDecopInteger(client, name + ':mode')
        self._invert = MutableDecopBoolean(client, name + ':invert')

    @property
    def value_act(self) -> 'DecopBoolean':
        return self._value_act

    @property
    def value_set(self) -> 'MutableDecopBoolean':
        return self._value_set

    @property
    def mode(self) -> 'MutableDecopInteger':
        return self._mode

    @property
    def invert(self) -> 'MutableDecopBoolean':
        return self._invert


class CcBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._channel2 = CurrDrv2(client, name + ':channel2')
        self._parallel_mode = DecopBoolean(client, name + ':parallel-mode')
        self._variant = DecopString(client, name + ':variant')
        self._fpga_fw_ver = DecopInteger(client, name + ':fpga-fw-ver')
        self._status = DecopInteger(client, name + ':status')
        self._slot = DecopString(client, name + ':slot')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._channel1 = CurrDrv2(client, name + ':channel1')
        self._board_temp = DecopReal(client, name + ':board-temp')
        self._serial_number = DecopString(client, name + ':serial-number')
        self._revision = DecopString(client, name + ':revision')

    @property
    def channel2(self) -> 'CurrDrv2':
        return self._channel2

    @property
    def parallel_mode(self) -> 'DecopBoolean':
        return self._parallel_mode

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def fpga_fw_ver(self) -> 'DecopInteger':
        return self._fpga_fw_ver

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def slot(self) -> 'DecopString':
        return self._slot

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def channel1(self) -> 'CurrDrv2':
        return self._channel1

    @property
    def board_temp(self) -> 'DecopReal':
        return self._board_temp

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def revision(self) -> 'DecopString':
        return self._revision


class CurrDrv2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._forced_off = MutableDecopBoolean(client, name + ':forced-off')
        self._current_clip_limit = DecopReal(client, name + ':current-clip-limit')
        self._current_set_dithering = MutableDecopBoolean(client, name + ':current-set-dithering')
        self._voltage_clip = MutableDecopReal(client, name + ':voltage-clip')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._aux = DecopReal(client, name + ':aux')
        self._pd = DecopReal(client, name + ':pd')
        self._feedforward_enabled = MutableDecopBoolean(client, name + ':feedforward-enabled')
        self._enabled = MutableDecopBoolean(client, name + ':enabled')
        self._positive_polarity = MutableDecopBoolean(client, name + ':positive-polarity')
        self._current_offset = MutableDecopReal(client, name + ':current-offset')
        self._emission = DecopBoolean(client, name + ':emission')
        self._status = DecopInteger(client, name + ':status')
        self._external_input = ExtInput2(client, name + ':external-input')
        self._current_act = DecopReal(client, name + ':current-act')
        self._variant = DecopString(client, name + ':variant')
        self._snubber = MutableDecopBoolean(client, name + ':snubber')
        self._current_clip = MutableDecopReal(client, name + ':current-clip')
        self._feedforward_factor = MutableDecopReal(client, name + ':feedforward-factor')
        self._path = DecopString(client, name + ':path')
        self._voltage_act = DecopReal(client, name + ':voltage-act')
        self._feedforward_master = MutableDecopInteger(client, name + ':feedforward-master')
        self._current_set = MutableDecopReal(client, name + ':current-set')
        self._status_txt = DecopString(client, name + ':status-txt')

    @property
    def forced_off(self) -> 'MutableDecopBoolean':
        return self._forced_off

    @property
    def current_clip_limit(self) -> 'DecopReal':
        return self._current_clip_limit

    @property
    def current_set_dithering(self) -> 'MutableDecopBoolean':
        return self._current_set_dithering

    @property
    def voltage_clip(self) -> 'MutableDecopReal':
        return self._voltage_clip

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def aux(self) -> 'DecopReal':
        return self._aux

    @property
    def pd(self) -> 'DecopReal':
        return self._pd

    @property
    def feedforward_enabled(self) -> 'MutableDecopBoolean':
        return self._feedforward_enabled

    @property
    def enabled(self) -> 'MutableDecopBoolean':
        return self._enabled

    @property
    def positive_polarity(self) -> 'MutableDecopBoolean':
        return self._positive_polarity

    @property
    def current_offset(self) -> 'MutableDecopReal':
        return self._current_offset

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input

    @property
    def current_act(self) -> 'DecopReal':
        return self._current_act

    @property
    def variant(self) -> 'DecopString':
        return self._variant

    @property
    def snubber(self) -> 'MutableDecopBoolean':
        return self._snubber

    @property
    def current_clip(self) -> 'MutableDecopReal':
        return self._current_clip

    @property
    def feedforward_factor(self) -> 'MutableDecopReal':
        return self._feedforward_factor

    @property
    def path(self) -> 'DecopString':
        return self._path

    @property
    def voltage_act(self) -> 'DecopReal':
        return self._voltage_act

    @property
    def feedforward_master(self) -> 'MutableDecopInteger':
        return self._feedforward_master

    @property
    def current_set(self) -> 'MutableDecopReal':
        return self._current_set

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt


class Buzzer:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._welcome = MutableDecopString(client, name + ':welcome')

    @property
    def welcome(self) -> 'MutableDecopString':
        return self._welcome

    async def play_welcome(self) -> None:
        await self.__client.exec(self.__name + ':play-welcome', input_stream=None, output_type=None, return_type=None)

    async def play(self, melody: str) -> None:
        assert isinstance(melody, str), "expected type 'str' for parameter 'melody', got '{}'".format(type(melody))
        await self.__client.exec(self.__name + ':play', melody, input_stream=None, output_type=None, return_type=None)


class BuildInformation:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._c_compiler_id = DecopString(client, name + ':c-compiler-id')
        self._cxx_compiler_id = DecopString(client, name + ':cxx-compiler-id')
        self._build_url = DecopString(client, name + ':build-url')
        self._build_node_name = DecopString(client, name + ':build-node-name')
        self._c_compiler_version = DecopString(client, name + ':c-compiler-version')
        self._cxx_compiler_version = DecopString(client, name + ':cxx-compiler-version')
        self._job_name = DecopString(client, name + ':job-name')
        self._build_tag = DecopString(client, name + ':build-tag')
        self._build_number = DecopInteger(client, name + ':build-number')
        self._build_id = DecopString(client, name + ':build-id')

    @property
    def c_compiler_id(self) -> 'DecopString':
        return self._c_compiler_id

    @property
    def cxx_compiler_id(self) -> 'DecopString':
        return self._cxx_compiler_id

    @property
    def build_url(self) -> 'DecopString':
        return self._build_url

    @property
    def build_node_name(self) -> 'DecopString':
        return self._build_node_name

    @property
    def c_compiler_version(self) -> 'DecopString':
        return self._c_compiler_version

    @property
    def cxx_compiler_version(self) -> 'DecopString':
        return self._cxx_compiler_version

    @property
    def job_name(self) -> 'DecopString':
        return self._job_name

    @property
    def build_tag(self) -> 'DecopString':
        return self._build_tag

    @property
    def build_number(self) -> 'DecopInteger':
        return self._build_number

    @property
    def build_id(self) -> 'DecopString':
        return self._build_id


class Ipconfig:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ip_addr = DecopString(client, name + ':ip-addr')
        self._mac_addr = DecopString(client, name + ':mac-addr')
        self._cmd_port = DecopInteger(client, name + ':cmd-port')
        self._net_mask = DecopString(client, name + ':net-mask')
        self._dhcp = DecopBoolean(client, name + ':dhcp')
        self._mon_port = DecopInteger(client, name + ':mon-port')

    @property
    def ip_addr(self) -> 'DecopString':
        return self._ip_addr

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
    def dhcp(self) -> 'DecopBoolean':
        return self._dhcp

    @property
    def mon_port(self) -> 'DecopInteger':
        return self._mon_port

    async def apply(self) -> None:
        await self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    async def set_dhcp(self) -> None:
        await self.__client.exec(self.__name + ':set-dhcp', input_stream=None, output_type=None, return_type=None)

    async def set_ip(self, ip_addr: str, net_mask: str) -> None:
        assert isinstance(ip_addr, str), "expected type 'str' for parameter 'ip_addr', got '{}'".format(type(ip_addr))
        assert isinstance(net_mask, str), "expected type 'str' for parameter 'net_mask', got '{}'".format(type(net_mask))
        await self.__client.exec(self.__name + ':set-ip', ip_addr, net_mask, input_stream=None, output_type=None, return_type=None)


class DLCpro:
    def __init__(self, connection: Connection) -> None:
        self.__client = Client(connection)
        self._fw_update = FwUpdate(self.__client, 'fw-update')
        self._licenses = Licenses(self.__client, 'licenses')
        self._system_messages = SystemMessages(self.__client, 'system-messages')
        self._time = MutableDecopString(self.__client, 'time')
        self._tan = DecopInteger(self.__client, 'tan')
        self._system_service_report = ServiceReport(self.__client, 'system-service-report')
        self._pc1 = PcBoard(self.__client, 'pc1')
        self._tc2 = TcBoard(self.__client, 'tc2')
        self._ampcc1 = Cc5000Board(self.__client, 'ampcc1')
        self._tc1 = TcBoard(self.__client, 'tc1')
        self._interlock_open = DecopBoolean(self.__client, 'interlock-open')
        self._system_health = DecopInteger(self.__client, 'system-health')
        self._pc2 = PcBoard(self.__client, 'pc2')
        self._pc3 = PcBoard(self.__client, 'pc3')
        self._standby = Standby(self.__client, 'standby')
        self._power_supply = PowerSupply(self.__client, 'power-supply')
        self._laser1 = Laser(self.__client, 'laser1')
        self._frontkey_locked = DecopBoolean(self.__client, 'frontkey-locked')
        self._mc = McBoard(self.__client, 'mc')
        self._emission = DecopBoolean(self.__client, 'emission')
        self._display = Display(self.__client, 'display')
        self._io = IoBoard(self.__client, 'io')
        self._cc1 = CcBoard(self.__client, 'cc1')
        self._system_health_txt = DecopString(self.__client, 'system-health-txt')
        self._buzzer = Buzzer(self.__client, 'buzzer')
        self._ampcc2 = Cc5000Board(self.__client, 'ampcc2')
        self._build_information = BuildInformation(self.__client, 'build-information')
        self._system_label = MutableDecopString(self.__client, 'system-label')
        self._echo = MutableDecopBoolean(self.__client, 'echo')
        self._svn_revision = DecopString(self.__client, 'svn-revision')
        self._fw_ver = DecopString(self.__client, 'fw-ver')
        self._decof_ver = DecopString(self.__client, 'decof-ver')
        self._uptime = DecopInteger(self.__client, 'uptime')
        self._decof_svn_revision = DecopString(self.__client, 'decof-svn-revision')
        self._system_type = DecopString(self.__client, 'system-type')
        self._system_model = DecopString(self.__client, 'system-model')
        self._ssw_ver = DecopString(self.__client, 'ssw-ver')
        self._ssw_svn_revision = DecopString(self.__client, 'ssw-svn-revision')
        self._serial_number = DecopString(self.__client, 'serial-number')
        self._uptime_txt = DecopString(self.__client, 'uptime-txt')
        self._ul = MutableDecopInteger(self.__client, 'ul')
        self._net_conf = Ipconfig(self.__client, 'net-conf')

    def __enter__(self):
        return self

    def __exit__(self):
        raise RuntimeError()

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, *args):
        await self.close()

    def __await__(self):
        return self.__aenter__().__await__()

    async def open(self) -> None:
        await self.__client.open()

    async def close(self) -> None:
        await self.__client.close()

    @property
    def fw_update(self) -> 'FwUpdate':
        return self._fw_update

    @property
    def licenses(self) -> 'Licenses':
        return self._licenses

    @property
    def system_messages(self) -> 'SystemMessages':
        return self._system_messages

    @property
    def time(self) -> 'MutableDecopString':
        return self._time

    @property
    def tan(self) -> 'DecopInteger':
        return self._tan

    @property
    def system_service_report(self) -> 'ServiceReport':
        return self._system_service_report

    @property
    def pc1(self) -> 'PcBoard':
        return self._pc1

    @property
    def tc2(self) -> 'TcBoard':
        return self._tc2

    @property
    def ampcc1(self) -> 'Cc5000Board':
        return self._ampcc1

    @property
    def tc1(self) -> 'TcBoard':
        return self._tc1

    @property
    def interlock_open(self) -> 'DecopBoolean':
        return self._interlock_open

    @property
    def system_health(self) -> 'DecopInteger':
        return self._system_health

    @property
    def pc2(self) -> 'PcBoard':
        return self._pc2

    @property
    def pc3(self) -> 'PcBoard':
        return self._pc3

    @property
    def standby(self) -> 'Standby':
        return self._standby

    @property
    def power_supply(self) -> 'PowerSupply':
        return self._power_supply

    @property
    def laser1(self) -> 'Laser':
        return self._laser1

    @property
    def frontkey_locked(self) -> 'DecopBoolean':
        return self._frontkey_locked

    @property
    def mc(self) -> 'McBoard':
        return self._mc

    @property
    def emission(self) -> 'DecopBoolean':
        return self._emission

    @property
    def display(self) -> 'Display':
        return self._display

    @property
    def io(self) -> 'IoBoard':
        return self._io

    @property
    def cc1(self) -> 'CcBoard':
        return self._cc1

    @property
    def system_health_txt(self) -> 'DecopString':
        return self._system_health_txt

    @property
    def buzzer(self) -> 'Buzzer':
        return self._buzzer

    @property
    def ampcc2(self) -> 'Cc5000Board':
        return self._ampcc2

    @property
    def build_information(self) -> 'BuildInformation':
        return self._build_information

    @property
    def system_label(self) -> 'MutableDecopString':
        return self._system_label

    @property
    def echo(self) -> 'MutableDecopBoolean':
        return self._echo

    @property
    def svn_revision(self) -> 'DecopString':
        return self._svn_revision

    @property
    def fw_ver(self) -> 'DecopString':
        return self._fw_ver

    @property
    def decof_ver(self) -> 'DecopString':
        return self._decof_ver

    @property
    def uptime(self) -> 'DecopInteger':
        return self._uptime

    @property
    def decof_svn_revision(self) -> 'DecopString':
        return self._decof_svn_revision

    @property
    def system_type(self) -> 'DecopString':
        return self._system_type

    @property
    def system_model(self) -> 'DecopString':
        return self._system_model

    @property
    def ssw_ver(self) -> 'DecopString':
        return self._ssw_ver

    @property
    def ssw_svn_revision(self) -> 'DecopString':
        return self._ssw_svn_revision

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def uptime_txt(self) -> 'DecopString':
        return self._uptime_txt

    @property
    def ul(self) -> 'MutableDecopInteger':
        return self._ul

    @property
    def net_conf(self) -> 'Ipconfig':
        return self._net_conf

    async def service_log(self) -> str:
        return await self.__client.exec('service-log', input_stream=None, output_type=str, return_type=None)

    async def service_script(self, input_stream: bytes) -> None:
        assert isinstance(input_stream, bytes), "expected type 'bytes' for parameter 'input_stream', got '{}'".format(type(input_stream))
        await self.__client.exec('service-script', input_stream=input_stream, output_type=None, return_type=None)

    async def error_log(self) -> str:
        return await self.__client.exec('error-log', input_stream=None, output_type=str, return_type=None)

    async def debug_log(self) -> str:
        return await self.__client.exec('debug-log', input_stream=None, output_type=str, return_type=None)

    async def service_report(self) -> bytes:
        return await self.__client.exec('service-report', input_stream=None, output_type=bytes, return_type=None)

    async def system_connections(self) -> Tuple[str, int]:
        return await self.__client.exec('system-connections', input_stream=None, output_type=str, return_type=int)

    async def system_summary(self) -> str:
        return await self.__client.exec('system-summary', input_stream=None, output_type=str, return_type=None)

    async def change_ul(self, ul: UserLevel, passwd: str) -> int:
        assert isinstance(ul, UserLevel), "expected type 'UserLevel' for parameter 'ul', got '{}'".format(type(ul))
        assert isinstance(passwd, str), "expected type 'str' for parameter 'passwd', got '{}'".format(type(passwd))
        return await self.__client.change_ul(ul, passwd)

    async def change_password(self, password: str) -> None:
        assert isinstance(password, str), "expected type 'str' for parameter 'password', got '{}'".format(type(password))
        await self.__client.exec('change-password', password, input_stream=None, output_type=None, return_type=None)

