#!/usr/bin/env python3
from smbus2 import SMBus
import argparse

def scan(busno: int):
    bus = SMBus(busno)
    found = []
    for addr in range(0x03, 0x78):
        try:
            bus.write_quick(addr)
            found.append(addr)
        except Exception:
            pass
    bus.close()
    return found

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bus", type=int, default=1)
    a = ap.parse_args()
    addrs = scan(a.bus)
    print("I2C bus", a.bus, "found:", [hex(x) for x in addrs])
