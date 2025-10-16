SEP005 <- FAST io
-----------------

Basic package to aniamte a 3DOF mass-spring-damper system to a an aribitray excitation force

Installation
------------
Regular install:
```
pip install git+https://github.com/<Abdulelah96>/three_dof_anim.git
```

Using the package
-----------------

```
from three_dof_anim.animation import make_animation, save_gif
import numpy as np

t = np.linspace(0, 10, 201)
x_t = np.vstack([
    0.1 * np.sin(2*np.pi*0.5*t),
    0.05 * np.sin(2*np.pi*0.8*t + 0.3),
    0.08 * np.sin(2*np.pi*1.2*t + 0.1)
]).T

fig, ani = make_animation(t, x_t, speed=2.0)  # x2 speed
save_gif(ani, 'three_dof_x2.gif')

```
Acknowledgements
----------------
This package was developed for the BrueFACE Mecanical Vibration Course Exercises Sessions, Academic Year 2025/2026
