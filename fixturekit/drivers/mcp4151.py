from __future__ import annotations
from ..core.base import Potentiometer
from ..core.spi import SPIDevice

# MCP41xxx/42xxx 256-tap digipot
CMD_WRITE = 0x11  # 0001 0001 -> write to pot0 wiper
CMD_SHDN  = 0x21  # shutdown

class MCP4151(Potentiometer):
    def __init__(self, spi_bus: int = 0, spi_dev: int = 0, name: str = "MCP4151"):
        super().__init__(name)
        self.spi = SPIDevice(bus=spi_bus, device=spi_dev, max_hz=1000000, mode=0)

    def set_wiper(self, value: int) -> None:
        value = max(0, min(255, int(value)))
        self.spi.xfer2([CMD_WRITE, value])

    def shutdown(self, enable: bool = True) -> None:
        if enable:
            self.spi.xfer2([CMD_SHDN, 0x00])

    def close(self):
        self.spi.close()
