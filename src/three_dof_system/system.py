# src/three_dof_anim/system.py
import numpy as np
from scipy import linalg
from scipy.signal import lsim, lti

def build_3DOF_matrices(m: float, c: float, c1: float, k: float, k1: float):
    M = np.array([[m, 0, 0],
                  [0, m, 0],
                  [0, 0, m]])
    K = np.array([[k1+k, -k, 0],
                  [-k, 2*k, -k],
                  [0, -k, k]])
    C = np.array([[c1+c, -c, 0],
                  [-c, 2*c, -c],
                  [0, -c, c]])
    return M, C, K

def state_space_matrices(M, C, K):
    A = np.block([[np.zeros((3, 3)), np.eye(3)],
                  [-np.linalg.inv(M) @ K, -np.linalg.inv(M) @ C]])
    B = np.block([[np.zeros((3, 3))],
                  [np.linalg.inv(M)]])
    Cmat = np.block([[np.eye(3), np.zeros((3, 3))]])
    D = np.zeros((3, 3))
    return A, B, Cmat, D

def simulate_response(A, B, C, D, t, u):
    """Simulate time response using scipy.signal.lsim"""
    system = lti(A, B, C, D)
    tout, yout, xout = lsim(system, u, t)
    return tout, yout, xout

def eigen_properties(M, K):
    lamb, psi = linalg.eig(K, M)
    idx = np.argsort(np.real(lamb))
    lamb = np.real(lamb[idx])
    psi = np.real(psi[:, idx])
    freqs = np.sqrt(lamb) / (2 * np.pi)
    return lamb, psi, freqs
