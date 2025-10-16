import time
import serial

class SCPIInstrument:
    """Minimal SCPI-over-serial wrapper.
    - newline terminated writes
    - reads until newline
    """
    def __init__(self, port: str, baud: int = 9600, timeout: float = 1.0, write_timeout: float = 1.0):
        self.ser = serial.Serial(port=port, baudrate=baud, timeout=timeout, write_timeout=write_timeout)

    def write(self, cmd: str) -> None:
        if not cmd.endswith('\n'):
            cmd += '\n'
        self.ser.write(cmd.encode('ascii'))

    def query(self, cmd: str) -> str:
        self.write(cmd)
        resp = self.ser.readline().decode('ascii', errors='ignore').strip()
        return resp

    def close(self):
        try:
            self.ser.close()
        except Exception:
            pass
