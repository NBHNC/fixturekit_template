from __future__ import annotations
import yaml
from typing import Any, Dict
from importlib import import_module

def build_from_yaml(path: str) -> Dict[str, Any]:
    """Load devices from a YAML config. Example schema in configs/sg313_example.yaml"""
    with open(path, 'r') as f:
        cfg = yaml.safe_load(f)
    devices: Dict[str, Any] = {}
    for item in cfg.get('devices', []):
        mname = item['driver']['module']
        cname = item['driver']['class']
        params = item.get('init', {})
        mod = import_module(mname)
        cls = getattr(mod, cname)
        dev = cls(**params)
        devices[item['name']] = dev
    return devices
