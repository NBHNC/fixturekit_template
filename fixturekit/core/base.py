from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Device(ABC):
    name: str
    def __init__(self, name: str):
        self.name = name

class PowerSupply(Device):
    @abstractmethod
    def idn(self) -> str: ...
    @abstractmethod
    def preset(self, volts: float, current_limit: float) -> None: ...
    @abstractmethod
    def output(self, enable: bool) -> None: ...
    @abstractmethod
    def measure(self) -> Dict[str, float]: ...

class ElectronicLoad(Device):
    @abstractmethod
    def idn(self) -> str: ...
    @abstractmethod
    def set_cc(self, amps: float) -> None: ...
    @abstractmethod
    def set_cv(self, volts: float) -> None: ...
    @abstractmethod
    def input(self, enable: bool) -> None: ...
    @abstractmethod
    def measure(self) -> Dict[str, float]: ...

class ADC(Device):
    @abstractmethod
    def read_voltage(self, channel: int) -> float: ...

class CurrentMonitor(Device):
    @abstractmethod
    def read(self) -> Dict[str, float]: ...

class Potentiometer(Device):
    @abstractmethod
    def set_wiper(self, value: int) -> None: ...

class RelayBoard(Device):
    @abstractmethod
    def set_mask(self, mask: int) -> None: ...
    @abstractmethod
    def get_mask(self) -> int: ...
