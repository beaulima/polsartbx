import logging

logger = logging.getLogger("pyatcortbx.polsarproc.decomposition")
import numpy as np
import scipy
import polsartbx
import polsartbx.polsarproc.definitions as defs
import matplotlib.pyplot as plt

EPS = 1e-10
RAD2DEG = 180.0 / np.pi
LOG3 = np.log(3)

import polsartbx.polsarproc.test_paths as ts
import polsartbx.polsarproc.definitions as defs
roi = ts.ROI

def haalpha_plot(M_in, title=None, bshow=True):

    import seaborn as sns
    sns.set()
    import matplotlib.pyplot as plt

    plt.scatter(M_in[defs.Entropy], M_in[defs.Alpha])
    plt.xlim(0, 1.0)
    plt.ylim(0, 90.0)
    plt.xlabel(r"Entropy ($H$)")
    plt.ylabel(r"$\alpha$ [$^{\circ}$]")
    if title is None:
        plt.title(r"$H/\alpha$ diagram")

    if bshow:
        plt.show()


def t3_haalpha_decomposition(M_in, full_computation=True):

    original_shape = M_in.shape
    if full_computation:
        nout = defs.len_keys(defs.HAAlpha_IDX)
    else:
        nout=3
    # MxMxHxW

    if len(original_shape) == 4:
        M_out = np.zeros((nout, original_shape[2], original_shape[3]))
        lambdak, V = np.linalg.eigh(M_in.transpose(2, 3, 0, 1), UPLO='L')
        # Descending order
        lambdak = lambdak[:, :, [2, 1, 0]]
        V = V[:, :, :, [2, 1, 0]].transpose(2, 3, 0, 1)
        V0 = V[0,:]
        V1 = V[1,:]
        V2 = V[2,:]
        lambdak = lambdak.transpose(2, 0, 1)
        lambdak[lambdak < 0] = 0.0
        pk = lambdak / (np.sum(lambdak, axis=0) + EPS)
        pk[pk > 1.0] = 1.0
        pk[pk < 0.0] = 0.0
        alphak = np.arccos(np.absolute(V0)) * RAD2DEG

        if full_computation:
            betak = np.arctan2(np.absolute(V2), EPS + np.absolute(V1)) * RAD2DEG
            phik = np.arctan2(V0.imag, EPS + V0.real)
            # Not getting same results for Delta anf Gamma (seem bad values)
            deltak = np.arctan2(V1.imag, EPS + V1.real) - phik
            deltak = np.arctan2(np.sin(deltak), np.cos(deltak) + EPS) * RAD2DEG
            gammak = np.arctan2(V2.imag, EPS + V2.real) - phik
            gammak = np.arctan2(np.sin(gammak), np.cos(gammak) + EPS) * RAD2DEG

        Entropy = -np.sum(pk * np.log(pk + EPS), axis=0) / LOG3
        Anisotropy = (pk[1] - pk[2]) / (pk[1] + pk[2] + EPS)
        Alpha = np.sum(pk * alphak, axis=0)
        if full_computation:
            Beta = np.sum(pk * betak, axis=0)
            Delta = np.sum(pk * deltak, axis=0)
            Gamma = np.sum(pk * gammak, axis=0)
            Lambda = np.sum(pk * lambdak, axis=0)

        M_out[defs.Entropy] = Entropy
        M_out[defs.Anisotropy] = Anisotropy
        M_out[defs.Alpha] = Alpha
        if full_computation:
            M_out[defs.Beta] = Beta
            M_out[defs.Delta] = Delta
            M_out[defs.Delta] = Gamma
            M_out[defs.Lambda] = Lambda
            M_out[defs.Lambda1] = lambdak[0]
            M_out[defs.Lambda2] = lambdak[1]
            M_out[defs.Lambda3] = lambdak[2]
            M_out[defs.Alpha1] = alphak[0]
            M_out[defs.Alpha2] = alphak[1]
            M_out[defs.Alpha3] = alphak[2]

    return M_out
