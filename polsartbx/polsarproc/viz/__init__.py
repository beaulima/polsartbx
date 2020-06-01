import logging
import polsartbx.polsarproc.definitions as defs

logger = logging.getLogger("pyatcortbx.viz")

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def linear_transform(x0, y0, x1, y1):
    m = (y1 - y0) / float(x1 - x0)
    b = y1 - m * x1
    return m, b


def linear_q_stretching(raster_bands, min_q=0.05, max_q=0.95, min_v=0.0, max_v=1.0):
    min_q = min_q
    max_q = max_q
    min_y = min_v
    max_y = max_v
    raster_bands0 = []
    for k in range(raster_bands.shape[0]):
        min_x = np.quantile(raster_bands[k], min_q)
        max_x = np.quantile(raster_bands[k], max_q)
        m, b = linear_transform(min_x, min_y, max_x, max_y)
        raster_bands0.append(m * raster_bands[k] + b)
    raster_bands0 = np.dstack(raster_bands0).transpose(2, 0, 1)
    np.clip(raster_bands0, min_y, max_y)
    return raster_bands0


def linear_sigma_stretching(raster_bands, sigma=1.5, min_v=0.0, max_v=1.0):
    min_y = min_v
    max_y = max_v
    raster_bands0 = []
    for k in range(raster_bands.shape[2]):
        avg = np.mean(raster_bands[k])
        stdev = np.std(raster_bands[k])
        min_x = avg - sigma * stdev
        max_x = avg + sigma * stdev
        m, b = linear_transform(min_x, min_y, max_x, max_y)
        raster_bands0.append(m * raster_bands[k] + b)
    raster_bands0 = np.dstack(raster_bands0)
    np.clip(raster_bands0, min_y, max_y)
    return raster_bands0


def rgb_pauli_from_s2_polsar(raster_bands, min_q=0.05, max_q=0.95, min_v=0.0, max_v=1.0):
    i_HH = raster_bands[defs.HH].real
    i_VV = raster_bands[defs.VV].real
    i_HV = raster_bands[defs.HV].real
    i_VH = raster_bands[defs.VH].real
    q_HH = raster_bands[defs.HH].imag
    q_VV = raster_bands[defs.VV].imag
    q_HV = raster_bands[defs.HV].imag
    q_VH = raster_bands[defs.VH].imag
    r = ((i_HH - i_VV) * (i_HH - i_VV) + (q_HH - q_VV) * (q_HH - q_VV)) / 2
    g = ((i_HV + i_VH) * (i_HV + i_VH) + (q_HV + q_VH) * (q_HV + q_VH)) / 2
    b = ((i_HV + i_VH) * (i_HV + i_VH) + (q_HV + q_VH) * (q_HV + q_VH)) / 2
    rgb = np.dstack([r, g, b]).transpose(2, 0, 1)
    rgb = linear_q_stretching(rgb, min_q, max_q, min_v, max_v)
    return rgb


def lrgb_pauli_from_s2_polsar(raster_bands, min_vi, max_vi, min_vf=0.0, max_vf=1.0):
    i_HH = raster_bands[defs.HH].real
    i_VV = raster_bands[defs.VV].real
    i_HV = raster_bands[defs.HV].real
    i_VH = raster_bands[defs.VH].real
    q_HH = raster_bands[defs.HH].imag
    q_VV = raster_bands[defs.VV].imag
    q_HV = raster_bands[defs.HV].imag
    q_VH = raster_bands[defs.VH].imag
    r = ((i_HH - i_VV) * (i_HH - i_VV) + (q_HH - q_VV) * (q_HH - q_VV)) / 2
    g = ((i_HV + i_VH) * (i_HV + i_VH) + (q_HV + q_VH) * (q_HV + q_VH)) / 2
    b = ((i_HV + i_VH) * (i_HV + i_VH) + (q_HV + q_VH) * (q_HV + q_VH)) / 2
    rgb = np.dstack([r, g, b])
    rgb = linear_q_stretching(rgb, min_vi, max_vi, min_vf, max_vf)
    return rgb


def rgb_pauli_from_t3_polsar(raster_bands, min_q=0.05, max_q=0.95, min_v=0.0, max_v=1.0):
    rgb = raster_bands[[defs.PAULI_T3_VIZ_IDX["R"], defs.PAULI_T3_VIZ_IDX["G"], defs.PAULI_T3_VIZ_IDX["B"]]]
    rgb = linear_q_stretching(rgb, min_q, max_q, min_v, max_v)
    return rgb
