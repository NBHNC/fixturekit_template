from __future__ import annotations
from ..core.base import RelayBoard
from ..core.i2c import I2CDevice

# MCP23008 registers
IODIR = 0x00
GPIO  = 0x09
OLAT  = 0x0A
GPPU  = 0x06

class RL40002(RelayBoard):
    """RL40002-style 4-channel I2C relay board using MCP23008.
    We expose an 8-bit mask even if only 4 relays exist.
    """
    def __init__(self, i2c_bus: int, addr: int, name: str = "RL40002"):
        super().__init__(name)
        self.dev = I2CDevice(i2c_bus, addr)
        # all outputs, no pullups
        self.dev.write_u8(IODIR, 0x00)
        self.dev.write_u8(GPPU,  0x00)
        self._mask = 0x00
        self.dev.write_u8(OLAT, self._mask)

    def set_mask(self, mask: int) -> None:
        self._mask = mask & 0xFF
        self.dev.write_u8(OLAT, self._mask)

    def get_mask(self) -> int:
        return self._mask

    def close(self):
        self.dev.close()
