import numpy as np
from dataclasses import dataclass

CUBE_POSITIONS = np.array([
    [-1., -1., -1.], [-1., -1., 1.], [-1., 1., -1.], [-1., 1., 1.],
    [1., -1., -1.], [1., -1., 1.], [1., 1., -1.], [1., 1., 1.]
], dtype=float)

def get_sign(pos):
    mapped = [int((p + 1) // 2) for p in pos]
    return 1 if sum(mapped) % 2 == 0 else -1

SITES = [{
    'pos': CUBE_POSITIONS[i],
    'sign': get_sign(CUBE_POSITIONS[i]),
    'idx': i
} for i in range(8)]

BASE_IDEAL_DIST = np.sqrt(3) * 1.22
TOLERANCE = 0.15

@dataclass(frozen=True)
class LatentSite:
    pos: np.ndarray
    sign: int
    idx: int

print('LatentSite and base geometry loaded.')