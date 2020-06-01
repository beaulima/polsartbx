import os

X0 = 715
Y0 = 7478
X1 = 2011
Y1 = 8808

W = X1 - X0 + 1
H = Y1 - Y0 + 1

ROI = (X0, Y0, W, H)

BASE_TEST_IMAGE_PATH = "/misc/data20/visi/POLSAR_TEST"

DATA_FLAG = {
    "R2_PRODUCT": "RS2-SLC-FQ9-ASC-09-Apr-2008_02/product.xml",
    "DIM_PRODUCT": "RS2-SLC-FQ9-ASC-09-Apr-2008_02.data",
    "TIFF_PRODUCT": "RS2-SLC-FQ9-ASC-09-Apr-2008_02.tif",
    "SUBSET_DIM": "subset_0_of_RS2-SLC-FQ9-ASC-09-Apr-2008_02.data",
    "SUBSET_DIM_C3": "subset_0_of_RS2-SLC-FQ9-ASC-09-Apr-2008_02_mat_C3.data",
    "SUBSET_DIM_T3": "subset_0_of_RS2-SLC-FQ9-ASC-09-Apr-2008_02_mat_T3.data",
    "SUBSET_DIM_HAALPHA_1x1": "subset_0_of_RS2-SLC-FQ9-ASC-09-Apr-2008_02_Decomp_HAALPHA_1x1.data",
    "SUBSET_DIM_HAALPHA_5x5": "subset_0_of_RS2-SLC-FQ9-ASC-09-Apr-2008_02_mat_T3_Boxcar_5x5_Decomp_haalpha.data",
    "SUBSET_DIM_T3_BOXCAR_5x5": "subset_0_of_RS2-SLC-FQ9-ASC-09-Apr-2008_02_mat_T3_Boxcar_5x5.data"
}

def get_data_path(data_flag):
    file_path = os.path.join(BASE_TEST_IMAGE_PATH,DATA_FLAG[data_flag])
    return file_path