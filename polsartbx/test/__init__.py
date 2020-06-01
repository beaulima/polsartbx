import  polsartbx

def test_gdal_read_rs2():

    '''
    TESTING GDAL reading RS2 data quadPol from: DIM, RS2 and TIFF product
    :return:
    '''

    import numpy as np
    import polsartbx.polsarproc.test_paths as ts
    import polsartbx.polsarproc.definitions as defs
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams["figure.dpi"] = 300
    roi = ts.ROI

    r2_protducts = {}
    for product_type in ["DIM_PRODUCT", "R2_PRODUCT", "TIFF_PRODUCT"]:
        file_path = ts.get_data_path(product_type)
        raster_data = polsartbx.polsarproc.io.gdal_read_rs2_array(file_path=file_path, roi=roi)
        r2_protducts[product_type] = raster_data["RASTER_BANDS"]
        rgb_img = polsartbx.polsarproc.viz.rgb_pauli_from_s2_polsar(raster_bands=raster_data["RASTER_BANDS"])
        assert rgb_img.shape[0] == 3, "number of channels must be 3"
        assert rgb_img.shape[1] == ts.H, f"width must be {ts.H}"
        assert rgb_img.shape[2] == ts.W, f"height must be {ts.W}"
        plt.title(f"PAULI from RS2 product: {product_type}")
        plt.imshow((rgb_img.transpose(1, 2, 0) * 255).astype('uint8'))
        plt.show()

    for key1 in  r2_protducts.keys():
        for key2 in r2_protducts.keys():
            if key1 != key2:
                dd = r2_protducts[key1]
                result=np.isclose(r2_protducts[key1], r2_protducts[key2])
                ok = np.count_nonzero(result)
                print(key1, key2, ok/float(r2_protducts[key1].size))
                toto = 0

    r2_protducts = None

def test_gdal_read_t3():

    """
    TESTING T3 conversion, compare with snap results
    :return:
    """

    import numpy as np
    import polsartbx.polsarproc.test_paths as ts
    import polsartbx.polsarproc.definitions as defs
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams["figure.dpi"] = 300
    roi = ts.ROI

    file_path = ts.get_data_path("R2_PRODUCT")
    raster_data = polsartbx.polsarproc.io.gdal_read_rs2_array(file_path=file_path, roi=roi)
    data_T3 = polsartbx.polsarproc.convert.S2_to_T3(M_in=raster_data["RASTER_BANDS"])
    rgb_img = polsartbx.polsarproc.viz.rgb_pauli_from_t3_polsar(raster_bands=data_T3)
    assert rgb_img.shape[0] == 3, "number of channels must be 3"
    assert rgb_img.shape[1] == ts.H, f"width must be {ts.H}"
    assert rgb_img.shape[2] == ts.W, f"height must be {ts.W}"
    plt.title(f"PAULI from RS2 product: S2_to_T3")
    plt.imshow((rgb_img.transpose(1, 2, 0) * 255).astype('uint8'))
    plt.show()

    file_path = ts.get_data_path("SUBSET_DIM_T3")
    raster_data_T3_1 = polsartbx.polsarproc.io.gdal_read_dim_format(data_dir_path=file_path, rb_keys=defs.T3_IDX)
    data_T3_1 = raster_data_T3_1["RASTER_BANDS"]
    rgb_img = polsartbx.polsarproc.viz.rgb_pauli_from_t3_polsar(raster_bands=data_T3_1)
    assert rgb_img.shape[0] == 3, "number of channels must be 3"
    assert rgb_img.shape[1] == ts.H, f"width must be {ts.H}"
    assert rgb_img.shape[2] == ts.W, f"height must be {ts.W}"
    plt.title(f"PAULI from SUBSET_DIM_T3: T3")
    plt.imshow((rgb_img.transpose(1, 2, 0) * 255).astype('uint8'))
    plt.show()

    result = np.isclose(data_T3, data_T3_1)
    results = np.sum(result, axis=0)
    mask = np.zeros((result.shape[1], result.shape[2]))
    mask[results < 9] = 255.0
    ok = np.count_nonzero(result)
    ok2 = np.count_nonzero(mask)
    print("R2_PRODUCT_T3", "SUBSET_DIM_T3", ok / float(data_T3_1.size), 1.0 - ok2 / float(mask.size))
    plt.title(f"T3 DIFFERENCES")
    plt.imshow((mask * 255).astype('uint8'))
    plt.show()

def test_t3_haalpha_decomposition():

    import numpy as np
    import polsartbx.polsarproc.test_paths as ts
    import polsartbx.polsarproc.definitions as defs
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams["figure.dpi"] = 300
    roi = ts.ROI

    file_path = ts.get_data_path("SUBSET_DIM_T3_BOXCAR_5x5")
    raster_data_T3_1 = polsartbx.polsarproc.io.gdal_read_dim_format(data_dir_path=file_path, rb_keys=defs.T3_IDX)
    data_T3 = raster_data_T3_1["RASTER_BANDS"]
    rgb_img = polsartbx.polsarproc.viz.rgb_pauli_from_t3_polsar(raster_bands=data_T3)
    assert rgb_img.shape[0] == 3, "number of channels must be 3"
    assert rgb_img.shape[1] == ts.H, f"width must be {ts.H}"
    assert rgb_img.shape[2] == ts.W, f"height must be {ts.W}"
   # plt.title(f"PAULI from SUBSET_DIM_T3: T3")
    #plt.imshow((rgb_img.transpose(1, 2, 0) * 255).astype('uint8'))
    #plt.show()

    #data_T3 = np.expand_dims(polsartbx.polsarproc.definitions.C1_SIG, axis=(1,2))
    data_3x3 = polsartbx.polsarproc.convert.X3_to_MX3(data_T3)

    HAAlpha_data = polsartbx.polsarproc.decomposition.t3_haalpha_decomposition(data_3x3,full_computation=False)

    file_path = ts.get_data_path("SUBSET_DIM_HAALPHA_5x5")
    raster_data_HAAlpha = polsartbx.polsarproc.io.gdal_read_dim_format(data_dir_path=file_path, rb_keys=defs.HAAlpha_MINIDX)

    polsartbx.polsarproc.decomposition.haalpha_plot(HAAlpha_data)

    for key, value in zip(defs.HAAlpha_MINIDX.keys(), defs.HAAlpha_MINIDX.values()):

        image_data = raster_data_HAAlpha["RASTER_BANDS"][value]
        compute_data = HAAlpha_data[value]

        plt.scatter(image_data.flatten(), compute_data.flatten())
        plt.title(key)
        plt.show()
        toto = 0
