from smbus2 import SMBus, i2c_msg

class I2CDevice:
    def __init__(self, bus: int, addr: int):
        self.bus_no = bus
        self.addr = addr
        self.bus = SMBus(bus)

    def write_u8(self, register: int, value: int):
        self.bus.write_byte_data(self.addr, register, value & 0xFF)

    def read_u8(self, register: int) -> int:
        return self.bus.read_byte_data(self.addr, register) & 0xFF

    def write_u16(self, register: int, value: int):
        self.bus.write_word_data(self.addr, register, value & 0xFFFF)

    def read_u16(self, register: int) -> int:
        return self.bus.read_word_data(self.addr, register) & 0xFFFF

    def close(self):
        try:
            self.bus.close()
        except Exception:
            pass
