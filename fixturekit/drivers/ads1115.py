from __future__ import annotations
import time
from ..core.base import ADC
from ..core.i2c import I2CDevice

# ADS1115 registers & bits
REG_CONV = 0x00
REG_CFG  = 0x01
REG_LOTH = 0x02
REG_HITH = 0x03

# config bits
OS_SINGLE = 0x8000
MUX = {
    0: 0x4000,  # AIN0-GND
    1: 0x5000,  # AIN1-GND
    2: 0x6000,  # AIN2-GND
    3: 0x7000,  # AIN3-GND
}
PGA_4_096 = 0x0200  # +/-4.096V -> 125uV/LSB
MODE_SINGLE = 0x0100
DR_128SPS = 0x0080  # good default
COMP_DISABLE = 0x0003

LSB_uV = 125.0  # for PGA +/-4.096V

class ADS1115(ADC):
    def __init__(self, i2c_bus: int, addr: int, name: str = "ADS1115"):
        super().__init__(name)
        self.dev = I2CDevice(i2c_bus, addr)

    def read_voltage(self, channel: int) -> float:
        assert channel in (0,1,2,3)
        cfg = (OS_SINGLE | MUX[channel] | PGA_4_096 | MODE_SINGLE | DR_128SPS | COMP_DISABLE)
        # write config
        self.dev.write_u16(REG_CFG, ((cfg >> 8) & 0xFF) | ((cfg & 0xFF) << 8))  # ADS expects big-endian
        # wait for conversion (>=8ms @128SPS)
        time.sleep(0.009)
        raw = self.dev.read_u16(REG_CONV)
        raw = ((raw << 8) & 0xFF00) | (raw >> 8)  # swap endian
        if raw & 0x8000:  # negative -> two's complement
            raw = -((~raw & 0xFFFF) + 1)
        volts = (raw * LSB_uV) / 1e6
        return volts

    def close(self):
        self.dev.close()
