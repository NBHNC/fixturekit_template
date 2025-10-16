from fixturekit.core.utils import vdiv_ratio, vdiv_unscale, ntc_r_from_v, steinhart_temp_c

def test_vdiv():
    r = vdiv_ratio(60400.0, 150000.0)
    vin = 12.3
    v = vin * r
    assert abs(vdiv_unscale(v, 60400.0, 150000.0) - vin) < 1e-6
