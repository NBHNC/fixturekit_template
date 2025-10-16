#!/usr/bin/env python3
import argparse, time, yaml
from fixturekit.core.registry import build_from_yaml
from fixturekit.core.utils import vdiv_unscale

def read_indicators(devs, cfg):
    results = []
    ind_cfg = cfg.get("indicators", [])
    for it in ind_cfg:
        adc = devs[it["adc"]]
        ch = int(it["channel"])
        th = float(it.get("threshold_v", 0.8))
        v = adc.read_voltage(ch)
        results.append({ "name": it["name"], "volts": v, "is_on": v >= th })
    return results

def read_measurements(devs, cfg):
    results = []
    meas_cfg = cfg.get("measurements", [])
    for m in meas_cfg:
        adc = devs[m["adc"]]
        ch = int(m["channel"])
        v = adc.read_voltage(ch)
        vin = v
        div = m.get("divider")
        if div:
            vin = vdiv_unscale(v, float(div["rtop"]), float(div["rbot"]))
        results.append({ "name": m["name"], "sample_v": v, "value_v": vin })
    return results

def main():
    ap = argparse.ArgumentParser(description="Generic fixture smoke test")
    ap.add_argument("--config", default="configs/generic_example.yaml")
    ap.add_argument("--psu-volts", type=float, default=12.30)
    ap.add_argument("--psu-ilim", type=float, default=2.00)
    ap.add_argument("--relay-mask", type=lambda x: int(x, 0), default=0x00)
    args = ap.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    devs = build_from_yaml(args.config)
    psu = devs.get("psu")
    rel = devs.get("relays")

    if psu:
        print("[PSU]", psu.idn())
        psu.preset(args.psu_volts, args.psu_ilim)
        psu.output(True)
        print(f"[PSU] Output ON -> {args.psu_volts:.2f} V, ILIM {args.psu_ilim:.2f} A")

    if rel:
        print(f"[REL] set mask = {hex(args.relay_mask)}")
        rel.set_mask(args.relay_mask)

    # Indicators (generic names from YAML)
    inds = read_indicators(devs, cfg)
    for r in inds:
        print(f"[IND] {r['name']}: {r['volts']:.3f} V  ->  {'ON' if r['is_on'] else 'off'}")

    # Measurements (with optional divider recovery)
    meas = read_measurements(devs, cfg)
    for r in meas:
        print(f"[MEAS] {r['name']}: sample={r['sample_v']:.3f} V  value={r['value_v']:.3f} V")

    if psu:
        state = psu.measure()
        print("[PSU] measure:", state)
        psu.output(False)
        print("[PSU] Output OFF")

if __name__ == "__main__":
    main()
