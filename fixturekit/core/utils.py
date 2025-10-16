import math

# ---------- Voltage divider helpers ----------
def vdiv_ratio(rtop: float, rbot: float) -> float:
    """Return Vout/Vin for a divider of Rtop to Vin and Rbot to GND."""
    return rbot / (rtop + rbot)

def vdiv_unscale(sample_v: float, rtop: float, rbot: float) -> float:
    """Recover Vin from ADC sample voltage using divider values."""
    return sample_v / vdiv_ratio(rtop, rbot)

# ---------- NTC Beta model helpers ----------
NTC_PULLUP_OHMS = 10000.0
NTC_REF_V       = 3.3
NTC_BETA        = 3435.0
NTC_R0          = 10000.0
NTC_T0C         = 25.0

def ntc_r_from_v(v, vref=NTC_REF_V, pullup=NTC_PULLUP_OHMS):
    v=float(v); eps=1e-6; v=max(eps, min(vref-eps, v))
    return (pullup*v)/(vref-v)

def steinhart_temp_c(r, beta=NTC_BETA, r0=NTC_R0, t0c=NTC_T0C):
    t0k = t0c + 273.15
    invT = (1.0/t0k) + (1.0/beta)*math.log(r/r0)
    return (1.0/invT) - 273.15
