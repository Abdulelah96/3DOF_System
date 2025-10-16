# src/three_dof_anim/animation.py
from typing import Optional, Sequence
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

def _get_spring_data(x, y0, y1, coils=4, width=0.05):
    ys = np.linspace(y0, y1, coils * 2)
    xs = np.tile([x - width, x + width], len(ys) // 2)
    if len(xs) < len(ys):
        xs = np.append(xs, x)
    return xs, ys

def _draw_damper(ax, x, y0, y1, width=0.1):
    h = y1 - y0
    rod1 = ax.plot([x, x], [y0, y0 + h * 0.3], color='black', lw=2)[0]
    box = Rectangle((x - width/2, y0 + h * 0.3), width, h * 0.2, color='black')
    ax.add_patch(box)
    rod2 = ax.plot([x, x], [y0 + h * 0.5, y1], color='black', lw=2)[0]
    return (rod1, box, rod2)

def make_animation(
    t: np.ndarray,
    x_t: np.ndarray,
    colors: Sequence[str] = ('blue', 'orange', 'green'),
    base_y: Optional[np.ndarray] = None,
    mass_width: float = 0.6,
    mass_height: float = 0.2,
    fps: int = 10,
    speed: float = 1.0,
    figsize=(12, 6)
):
    """
    Build the matplotlib FuncAnimation for the 3-DOF system.

    Parameters
    ----------
    t : 1D numpy array of time stamps
    x_t : 2D numpy array shaped (len(t), 3) with displacements for each mass
    speed : float multiplier for playback speed (1.0 normal, 2.0 twice as fast, 0.5 half speed)
    fps   : base frames per second used when saving
    """
    if base_y is None:
        base_y = np.array([2.4, 1.6, 0.8])

    fig, ax = plt.subplots(ncols=2, figsize=figsize)
    ax[0].set_xlim(-1, 1)
    ax[0].set_ylim(0, 3.2)
    ax[0].axis('off')

    # right subplot
    for i in range(3):
        ax[1].plot(t, x_t[:, i], label=f'Mass {i+1}', zorder=2-i, color=colors[i])
    moving_dots = [ax[1].plot([], [], 'o', color=color)[0] for color in colors]
    ax[1].set_xlim(0, t[-1])
    ax[1].set_ylim(np.min(x_t)*1.2, np.max(x_t)*1.2)
    ax[1].legend()
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Displacement (m)')
    ax[1].grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.2)

    # masses on left
    masses = [Rectangle((-mass_width/2, y - mass_height/2), mass_width, mass_height, color=color)
              for y, color in zip(base_y, colors)]
    for m in masses:
        ax[0].add_patch(m)

    ax[0].plot([-0.5, 0.5], [3.0, 3.0], 'k', lw=4)

    # springs and dampers
    springs = []
    spring_y_pairs = [(3.0, base_y[0]+0.1),
                      (base_y[0]-0.1, base_y[1]+0.1),
                      (base_y[1]-0.1, base_y[2]+0.1)]
    for y0, y1 in spring_y_pairs:
        xs, ys = _get_spring_data(-0.2, y0, y1)
        spring_line, = ax[0].plot(xs, ys, color='gray', lw=1.5)
        springs.append(spring_line)
    dampers = [_draw_damper(ax[0], 0.2, y0, y1) for y0, y1 in spring_y_pairs]

    time_text = ax[1].text(0.95, 0.95, '', transform=ax[1].transAxes,
                           ha='right', va='top', fontsize=10)

    def update(i):
        y = base_y + x_t[i, :]

        for j, m in enumerate(masses):
            m.set_y(y[j] - mass_height / 2)

        spring_coords = [(3.0, y[0] + 0.1),
                         (y[0] - 0.1, y[1] + 0.1),
                         (y[1] - 0.1, y[2] + 0.1)]
        for j in range(3):
            xs, ys = _get_spring_data(-0.2, *spring_coords[j])
            springs[j].set_data(xs, ys)

        for j in range(3):
            y0, y1 = spring_coords[j]
            h = y1 - y0
            dampers[j][0].set_data([0.2, 0.2], [y0, y0 + h * 0.3])
            dampers[j][1].set_y(y0 + h * 0.3)
            dampers[j][1].set_height(h * 0.2)
            dampers[j][2].set_data([0.2, 0.2], [y0 + h * 0.5, y1])

        for j, dot in enumerate(moving_dots):
            dot.set_data([t[i]], [x_t[i, j]])

        time_text.set_text(f"t = {t[i]:.2f} s")
        return masses + springs + [d for group in dampers for d in group] + moving_dots + [time_text]

    # compute interval such that speed multiplier is applied
    duration = float(t[-1]) if len(t) > 0 else 1.0
    base_interval = 1000 * duration / len(t) if len(t) > 0 else 100  # ms
    interval = base_interval / max(speed, 1e-8)  # faster -> smaller interval

    ani = animation.FuncAnimation(fig, update, frames=len(t), interval=interval)
    ani._metadata = {'fps': int(fps * speed)}  # store intended fps for saving convenience
    return fig, ani

def save_gif(ani, filename: str, fps: Optional[int] = None):
    """
    Save FuncAnimation to GIF using Pillow writer.
    fps: if None, tries to read fps from ani._metadata
    """
    from PIL import Image  # ensure pillow present
    writer = animation.PillowWriter(fps=fps or ani._metadata.get('fps', 10))
    ani.save(filename, writer=writer)
