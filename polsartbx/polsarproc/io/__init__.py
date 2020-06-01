import logging

logger = logging.getLogger("pyatcortbx.polsarproc.io")
import gdal
import numpy as np
import thelper
import os
import polsartbx.polsarproc.definitions as defs

UNCALIB = 0
BETA0 = 1
SIGMA0 = 2
GAMMA = 3

RSAT2_PROCESSING = ["RADARSAT_2_CALIB:UNCALIB", "RADARSAT_2_CALIB:BETA0", "RADARSAT_2_CALIB:SIGMA0",
                    "RADARSAT_2_CALIB:GAMMA"]


def gdal_read_rs2_dim_format(data_dir_path, roi=None):
    rbs0 = {}
    rb_keys = defs.S2_SLC_IDX
    if roi is not None:
        x0 = roi[0]
        y0 = roi[1]
        w = roi[2]
        h = roi[3]
    ds_list = []
    for k, key in enumerate(rb_keys.keys()):
        file_path = os.path.join(data_dir_path, f"{key}.img")
        ds_list.append(gdal.OpenShared(file_path, gdal.GA_ReadOnly))
        rb = ds_list[k]
        rbs0[key] = rb

    rbs = []
    rbs.append(rbs0['i_HH'].ReadAsArray(x0, y0, w, h) + 1j * rbs0['q_HH'].ReadAsArray(x0, y0, w, h))
    rbs.append(rbs0['i_HV'].ReadAsArray(x0, y0, w, h) + 1j * rbs0['q_HV'].ReadAsArray(x0, y0, w, h))
    rbs.append(rbs0['i_VH'].ReadAsArray(x0, y0, w, h) + 1j * rbs0['q_VH'].ReadAsArray(x0, y0, w, h))
    rbs.append(rbs0['i_VV'].ReadAsArray(x0, y0, w, h) + 1j * rbs0['q_VV'].ReadAsArray(x0, y0, w, h))

    data = {}
    data['BANDS_IDX'] = defs.S2_IDX
    data['X0_ORIGINAL'] = x0
    data['Y0_ORIGINAL'] = y0
    data['W_ORIGINAL'] = w
    data['H_ORIGINAL'] = h
    data['RASTER_BANDS'] = np.dstack(rbs).transpose(2, 0, 1)
    ds_list = None
    return data

def read_as_array(rb, roi):
    if roi is not None:
        x0 = roi[0]
        y0 = roi[1]
        w = roi[2]
        h = roi[3]
    if roi:
        return rb.ReadAsArray(x0, y0, w, h)
    else:
        return rb.ReadAsArray()

def gdal_read_dim_format(data_dir_path, rb_keys, roi=None):
    rbs = []
    ds_list = []
    for k, key in enumerate(rb_keys.keys()):
        file_path = os.path.join(data_dir_path, f"{key}.img")
        ds = gdal.OpenShared(file_path, gdal.GA_ReadOnly)
        if ds is None:
            raise Exception(f"unable to open {file_path}")
        ds_list.append(gdal.OpenShared(file_path, gdal.GA_ReadOnly))
        rb = ds_list[k]
        rbs.append(read_as_array(rb,roi))
    if roi is not None:
        x0 = roi[0]
        y0 = roi[1]
        w = roi[2]
        h = roi[3]
    else:
        x0 = 0
        y0 = 0
        w = ds_list[0].RasterXSize
        h = ds_list[0].RasterYSize



    data = {}
    data['BANDS_IDX'] = rb_keys
    data['X0_ORIGINAL'] = x0
    data['Y0_ORIGINAL'] = y0
    data['W_ORIGINAL'] = w
    data['H_ORIGINAL'] = h
    data['RASTER_BANDS'] = np.dstack(rbs).transpose(2, 0, 1)
    ds_list = None
    return data


def gdal_read_rs2_array(file_path, roi=None, preprocessing=UNCALIB):
    if os.path.isdir(file_path):
        logger.debug("trying to load a beam-dimap")
        data = gdal_read_rs2_dim_format(file_path, roi=roi)
        return data

    file_path0 = file_path
    if preprocessing != UNCALIB:
        file_path0 = f"{RSAT2_PROCESSING[preprocessing]}:{file_path}"

    print(file_path0)
    ds = gdal.OpenShared(file_path0, gdal.GA_ReadOnly)
    if ds is None:
        raise Exception(f"unable to read product {file_path}")
    driver_name = ds.GetDriver().ShortName

    x0 = 0
    y0 = 0
    w = ds.RasterXSize
    h = ds.RasterYSize
    chs = ds.RasterCount

    rbs = []
    idx = {}
    data = None

    if driver_name == "RS2":
        data = {}
        rbs0 = {}
        for k in range(chs):
            rb = ds.GetRasterBand(k + 1)
            metadata = rb.GetMetadata()
            id = metadata["POLARIMETRIC_INTERP"]
            rbs0[id] = rb
        for key, chn in zip(defs.S2_IDX.keys(), defs.S2_IDX.values()):
            rbs.append(read_as_array(rbs0[key], roi))
        idx = defs.S2_IDX.keys()

    elif driver_name == "GTiff":
        data = {}
        for key, k in zip(defs.S2_IDX.keys(), defs.S2_IDX.values()):
            i = 2 * k + 1
            q = 2 * k + 2
            rb_i = ds.GetRasterBand(i)
            rb_q = ds.GetRasterBand(q)
            rbs.append(read_as_array(rb_i, roi) + 1j * read_as_array(rb_q, roi))
        idx = defs.S2_IDX.keys()
    else:
        return data

    data['BANDS_IDX'] = idx
    data['X0_ORIGINAL'] = x0
    data['Y0_ORIGINAL'] = y0
    data['W_ORIGINAL'] = w
    data['H_ORIGINAL'] = h
    data['RASTER_BANDS'] = np.dstack(rbs).transpose(2, 0, 1)
    ds = None
    return data


def gdal_read_t3_array(file_path, roi=None):
    ds = gdal.OpenShared(file_path, gdal.GA_ReadOnly)
    if ds is None:
        raise Exception(f"unable to read product {file_path}")
    driver_name = ds.GetDriver().ShortName
