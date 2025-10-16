from __future__ import annotations
from typing import Dict
from ..core.base import PowerSupply
from ..core.scpi import SCPIInstrument

class KoradKD3005P(PowerSupply):
    """Korad KD3005P SCPI-over-USB driver.
    Notes:
      - Common command set used in the wild:
          *IDN?
          VSET1:12.30
          ISET1:2.000
          OUT1 / OUT0
          VOUT1?
          IOUT1?
    """
    def __init__(self, port: str, baud: int = 9600, name: str = "KoradKD3005P"):
        super().__init__(name)
        self.ins = SCPIInstrument(port=port, baud=baud, timeout=1.0, write_timeout=1.0)

    def idn(self) -> str:
        try:
            return self.ins.query("*IDN?")
        except Exception:
            return "KORAD?"

    def preset(self, volts: float, current_limit: float) -> None:
        self.ins.write(f"VSET1:{volts:0.2f}")
        self.ins.write(f"ISET1:{current_limit:0.3f}")

    def output(self, enable: bool) -> None:
        self.ins.write("OUT1" if enable else "OUT0")

    def measure(self) -> Dict[str, float]:
        try:
            v = float(self.ins.query("VOUT1?"))
        except Exception:
            v = float('nan')
        try:
            i = float(self.ins.query("IOUT1?"))
        except Exception:
            i = float('nan')
        return {"volts": v, "amps": i}

    def close(self):
        self.ins.close()
