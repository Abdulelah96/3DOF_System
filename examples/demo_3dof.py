import numpy as np
import matplotlib.pyplot as plt
from three_dof_system.system import build_3DOF_matrices, state_space_matrices, simulate_response, eigen_properties
from three_dof_system.forces import sine_force, build_input
from three_dof_system.animation import make_animation, save_gif

# Define system parameters
m, c, c1, k, k1 = 1.0, 0.1, 0.1, 16, 16
M, C, K = build_3DOF_matrices(m, c, c1, k, k1)
A, B, Cmat, D = state_space_matrices(M, C, K)
lamb, psi, f_res = eigen_properties(M, K)

# Define input force
t = np.linspace(0, 600, 6000)
f_t = sine_force(t, freq=0.05, amp=1.0)
u = build_input(t, dof_index=0, f_t=f_t)

# Simulate response
tout, yout, xout = simulate_response(A, B, Cmat, D, t, u)
x_t = xout[:, :3]  # animate only 3 DOFs

# Create animation
fig, ani = make_animation(tout, x_t, speed=6)
plt.show()

# Save as GIF
save_gif(ani, 'three_dof_demo.gif')
print("Animation saved as three_dof_demo.gif")
