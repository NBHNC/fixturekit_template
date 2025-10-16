#!/usr/bin/env python3
import time, argparse
from fixturekit.core.registry import build_from_yaml
from fixturekit.core.utils import ntc_r_from_v, steinhart_temp_c, vdiv_unscale

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/sg313_example.yaml")
    ap.add_argument("--volts", type=float, default=12.30)
    ap.add_argument("--ilim", type=float, default=2.0)
    ap.add_argument("--relay-mask", type=lambda x: int(x,0), default=0x00)
    ap.add_argument("--stat-th", type=float, default=0.8, help="LED on-threshold (V)")
    ap.add_argument("--vout-rtop", type=float, default=60400.0)
    ap.add_argument("--vout-rbot", type=float, default=150000.0)
    args = ap.parse_args()

    devs = build_from_yaml(args.config)
    psu = devs["psu"]
    adc1 = devs["adc1"]
    rel = devs["relays"]

    print("[PSU]", psu.idn())
    psu.preset(args.volts, args.ilim)
    psu.output(True)
    print("[PSU] Output ON")

    print("[REL] mask ->", hex(args.relay_mask))
    rel.set_mask(args.relay_mask)

    # Example: read PG/STAT pins on adc1 channels 0..2 (voltage in V)
    pg = adc1.read_voltage(0)
    stat1 = adc1.read_voltage(1)
    stat2 = adc1.read_voltage(2)
    print(f"[ADC] PG={pg:0.3f}V  STAT1={stat1:0.3f}V  STAT2={stat2:0.3f}V")

    # Example: recover VIN/VOUT via known divider (edit resistors to match)
    vout_sense = adc1.read_voltage(3)
    vout = vdiv_unscale(vout_sense, args.vout_rtop, args.vout_rbot)
    print(f"[ADC] VOUT_sense={vout_sense:0.3f}V  ->  VOUT={vout:0.3f}V")

    psu_state = psu.measure()
    print("[PSU]", psu_state)
    psu.output(False)
    print("[PSU] Output OFF")

if __name__ == "__main__":
    main()
