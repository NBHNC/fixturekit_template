import spidev

class SPIDevice:
    def __init__(self, bus: int = 0, device: int = 0, max_hz: int = 1000000, mode: int = 0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_hz
        self.spi.mode = mode

    def xfer2(self, data: bytes | list[int]) -> list[int]:
        if isinstance(data, bytes):
            data = list(data)
        return self.spi.xfer2(data)

    def close(self):
        try:
            self.spi.close()
        except Exception:
            pass
