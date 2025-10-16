from __future__ import annotations
from ..core.base import CurrentMonitor
from ..core.i2c import I2CDevice

# Registers
REG_CONFIG   = 0x00
REG_SHUNT_V  = 0x01
REG_BUS_V    = 0x02
REG_POWER    = 0x03
REG_CURRENT  = 0x04
REG_CALIB    = 0x05

class INA219(CurrentMonitor):
    """Minimal INA219 driver.
    Provide shunt_ohms and current_lsb (A/bit) to set CAL.
    """
    def __init__(self, i2c_bus: int, addr: int, shunt_ohms: float = 0.1, current_lsb: float = 0.0001, name: str = "INA219"):
        super().__init__(name)
        self.dev = I2CDevice(i2c_bus, addr)
        self.shunt = shunt_ohms
        self.current_lsb = current_lsb  # A/bit
        # Calculate calibration per datasheet: CAL = 0.04096 / (current_lsb * shunt_ohms)
        cal = int(0.04096 / (self.current_lsb * self.shunt))
        self.dev.write_u16(REG_CALIB, ((cal >> 8) & 0xFF) | ((cal & 0xFF) << 8))
        # Config: 32V range, 320mV shunt, 12-bit, 128x samples (could be tuned); using default here.
        self.dev.write_u16(REG_CONFIG, 0x019F)  # typical safe default

    def _read_u16_be(self, reg: int) -> int:
        v = self.dev.read_u16(reg)
        return ((v << 8) & 0xFF00) | (v >> 8)

    def read(self):
        shunt_mV = self._read_u16_be(REG_SHUNT_V) * 0.01   # 10uV/LSB -> mV
        bus_V    = (self._read_u16_be(REG_BUS_V) >> 3) * 0.004  # 4mV/LSB
        curr_A   = self._read_u16_be(REG_CURRENT) * self.current_lsb
        power_W  = self._read_u16_be(REG_POWER) * (20 * self.current_lsb)  # per datasheet
        return {"bus_v": bus_V, "shunt_mv": shunt_mV, "amps": curr_A, "watts": power_W}

    def close(self):
        self.dev.close()
