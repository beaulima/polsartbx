import logging
import polsartbx.polsarproc.definitions as defs

logger = logging.getLogger("pyatcortbx.polsarproc.definitions")
import numpy as np

SQRT2 = np.sqrt(2.)

def get_s2_i_q_parts(M_in):
    i_HH = M_in[defs.HH].real
    i_VV = M_in[defs.VV].real
    i_HV = M_in[defs.HV].real
    i_VH = M_in[defs.VH].real
    q_HH = M_in[defs.HH].imag
    q_VV = M_in[defs.VV].imag
    q_HV = M_in[defs.HV].imag
    q_VH = M_in[defs.VH].imag
    return i_HH, i_VV, i_HV, i_VH, q_HH, q_VV, q_HV, q_VH

def convert_i_q_float_to_i_q_complex(M_in):
    data = []

def get_m3_parts(M_in):
    """
    :param M_in: a 9xDIMS
    :return:
    """
    M11 = M_in[defs.M11]
    M12_real = M_in[defs.M12_real]
    M12_imag = M_in[defs.M12_imag]
    M13_real = M_in[defs.M13_real]
    M13_imag = M_in[defs.M13_imag]
    M22 = M_in[defs.M22]
    M23_real = M_in[defs.M23_real]
    M23_imag = M_in[defs.M23_imag]
    M33 = M_in[defs.M33]
    return M11, M12_real, M12_imag, M13_real, M13_imag, M22, M23_real, M23_imag, M33


def S2_to_T3(M_in):
    i_HH, i_VV, i_HV, i_VH, q_HH, q_VV, q_HV, q_VH = get_s2_i_q_parts(M_in)
    k1r = (i_HH + i_VV) / SQRT2
    k1i = (q_HH + q_VV) / SQRT2
    k2r = (i_HH - i_VV) / SQRT2
    k2i = (q_HH - q_VV) / SQRT2
    k3r = (i_HV + i_VH) / SQRT2
    k3i = (q_HV + q_VH) / SQRT2
    M_out = []
    M_out.append(k1r * k1r + k1i * k1i)
    M_out.append(k1r * k2r + k1i * k2i)
    M_out.append(k1i * k2r - k1r * k2i)
    M_out.append(k1r * k3r + k1i * k3i)
    M_out.append(k1i * k3r - k1r * k3i)
    M_out.append(k2r * k2r + k2i * k2i)
    M_out.append(k2r * k3r + k2i * k3i)
    M_out.append(k2i * k3r - k2r * k3i)
    M_out.append(k3r * k3r + k3i * k3i)
    M_out = np.dstack(M_out).transpose(2, 0, 1)
    return M_out


def S2_to_C3(M_in):
    i_HH, i_VV, i_HV, i_VH, q_HH, q_VV, q_HV, q_VH = get_s2_i_q_parts(M_in)
    k1r = i_HH
    k1i = q_HH
    k2r = (i_HV + i_VH) / SQRT2
    k2i = (q_HV + q_VH) / SQRT2
    k3r = i_VV
    k3i = q_VV
    M_out = []
    M_out.append(k1r * k1r + k1i * k1i)
    M_out.append(k1r * k2r + k1i * k2i)
    M_out.append(k1i * k2r - k1r * k2i)
    M_out.append(k1r * k3r + k1i * k3i)
    M_out.append(k1i * k3r - k1r * k3i)
    M_out.append(k2r * k2r + k2i * k2i)
    M_out.append(k2r * k3r + k2i * k3i)
    M_out.append(k2i * k3r - k2r * k3i)
    M_out.append(k3r * k3r + k3i * k3i)
    M_out = np.dstack(M_out).transpose(2, 0, 1)
    return M_out


def T3_to_C3(M_in):
    T11, T12_real, T12_imag, T13_real, T13_imag, T22, T23_real, T23_imag, T33 = get_m3_parts(M_in)
    M_out = []
    M_out.append((T11 + 2 * T12_real + T22) / 2.0)
    M_out.append((T13_real + T23_real) / SQRT2)
    M_out.append((T13_imag + T23_imag) / SQRT2)
    M_out.append((T11 - T22) / 2.0)
    M_out.append(-T12_imag)
    M_out.append(T33)
    M_out.append((T13_real - T23_real) / SQRT2)
    M_out.append((-T13_imag + T23_imag) / SQRT2)
    M_out.append((T11 - 2.0 * T12_real + T22) / 2.0)
    return M_out


def X3_to_MX3(M_in):
    """

    :param M_in: a 9xMxN
    :return:
    """
    M11, M12_real, M12_imag, M13_real, M13_imag, M22, M23_real, M23_imag, M33 = get_m3_parts(M_in)
    M_out = np.zeros((3, 3, M_in.shape[1], M_in.shape[2]))+1j*np.zeros((3, 3, M_in.shape[1], M_in.shape[2]))
    M_out[0, 0] = M11+1j*np.zeros((M_in.shape[1], M_in.shape[2]))
    M_out[0, 1] = M12_real + 1j * M12_imag
    M_out[1, 0] = np.conj(M_out[0, 1])
    M_out[0, 2] = M13_real + 1j * M13_imag
    M_out[2, 0] = np.conj(M_out[0, 2])
    M_out[1, 1] = M22 + 1j * np.zeros((M_in.shape[1], M_in.shape[2]))
    M_out[1, 2] = M23_real + 1j * M23_imag
    M_out[2, 1] = np.conj(M_out[1, 2])
    M_out[2, 2] = M33 + 1j * np.zeros((M_in.shape[1], M_in.shape[2]))
    return M_out


def MX3_to_X3(M_in):
    M_out = np.zeros((9, M_in.shape[2], M_in.shape[3]))
    M_out[defs.M11] = M_in[0, 0].real
    M_out[defs.M12_real] = M_in[0, 1].real
    M_out[defs.M12_imag] = M_in[0, 1].imag
    M_out[defs.M13_real] = M_in[0, 2].real
    M_out[defs.M13_imag] = M_in[0, 2].imag
    M_out[defs.M22] = M_in[1, 1].real
    M_out[defs.M23_real] = M_in[1, 2].real
    M_out[defs.M23_imag] = M_in[1, 2].imag
    M_out[defs.M33] = M_in[2, 2].real
    return M_out


def C3_to_T3(M_in):
    C11, C12_real, C12_imag, C13_real, C13_imag, C22, C23_real, C23_imag, C33 = get_m3_parts(M_in)
    M_out = []
    M_out.append((C11 + 2 * C13_real + C33) / 2.0)
    M_out.append((C11 - C33) / 2.0)
    M_out.append(-C13_imag)
    M_out.append((C12_real + C23_real) / SQRT2)
    M_out.append((C12_imag - C23_imag) / SQRT2)
    M_out.append((C11 - 2 * C13_real + C33) / 2.0)
    M_out.append((C12_real - C23_real) / SQRT2)
    M_out.append((C12_imag + C23_imag) / SQRT2)
    M_out.append(C22)
    return M_out
