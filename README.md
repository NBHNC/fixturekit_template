# FixtureKit — device repository for test fixtures

A small, class-based Python package that standardizes drivers and configs for your common peripherals
(Korad KD3005P, ADS1115, INA219, MCP4151, MCP23008/RL40002, etc.).

## Quick start (Raspberry Pi)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
sudo apt-get install -y python3-smbus i2c-tools  # if needed
python scripts/discover_i2c.py --bus 1
python examples/sg313_smoke_test.py --config configs/sg313_example.yaml
```

Edit `configs/sg313_example.yaml` to match your port names and I2C addresses.

## What’s inside
- `fixturekit/core/*`: abstract base classes, SCPI/I2C/SPI helpers, math utils
- `fixturekit/drivers/*`: concrete drivers
- `configs/`: YAML device sets you can reuse across fixtures
- `examples/`: minimal smoke test showing composition
- `scripts/`: handy utilities (I2C scanner)

## Extending
Add a Python file in `fixturekit/drivers/`, implement the abstract class, and reference it from YAML:
```yaml
- name: myload
  driver: { module: fixturekit.drivers.it8211, class: IT8211 }
  init:   { port: /dev/ttyUSB0, baud: 115200 }
```

## Notes
- Korad KD3005P commands reflect the common `VSET1/ISET1/OUT1` style used in many builds.
  Adjust if your firmware variant differs.
- ADS1115 uses +/-4.096 V PGA; scale external dividers with `vdiv_unscale()`.
- INA219 requires your actual shunt value and chosen current_LSB for best accuracy.
- MCP4151 assumes 256-tap variant.
- MCP23008 relay board exposes an 8-bit mask (even if you only have 4 relays).

## Generic example
Use `configs/generic_example.yaml` and `examples/generic_smoke_test.py` for a fully generic template.
Indicators are defined in YAML (no SG313-specific names). Measurements can define optional dividers.
