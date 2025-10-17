# src/three_dof_anim/forces.py
import numpy as np
from scipy.signal import chirp

def sine_force(t, freq, amp=1.0):
    return amp * np.sin(2 * np.pi * freq * t)

def chirp_force(t, f0, f1, amp=1.0, phase=90):
    return amp * chirp(t, f0=f0, f1=f1, t1=t[-1], phi=phase)

def build_input(t, dof_index, f_t, ndof=3):
    u = np.zeros((len(t), ndof))
    u[:, dof_index] = f_t
    return u
