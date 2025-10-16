from __future__ import annotations
from typing import Dict
from ..core.base import ADC

class LEDProbe:
    """Simple helper to interpret phototransistor voltage into ON/OFF/BLINK.
    Use a sampling window in your application for blink detection.
    """
    def __init__(self, adc: ADC, channel: int, on_threshold_v: float = 0.8):
        self.adc = adc
        self.ch = channel
        self.th = on_threshold_v

    def sample(self) -> Dict[str, float | bool]:
        v = self.adc.read_voltage(self.ch)
        return {"volts": v, "is_on": v >= self.th}
