import numpy as np
from three_dof_anim.animation import make_animation

def test_make_animation_smoke():
    t = np.linspace(0, 5, 51)
    x_t = np.zeros((len(t), 3))
    fig, ani = make_animation(t, x_t)
    assert ani is not None
    # optionally test that frames > 0
    assert len(t) == ani.frame_seq.stop
