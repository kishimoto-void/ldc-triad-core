import numpy as np
import math

def compute_restoring_force(state_i, state_j, wire, ideal_dist, elasticity=1.6, sensitivity=1.4):
    dist = np.linalg.norm(state_i.pos - state_j.pos)  # assume site.pos attached or passed
    error = (dist - ideal_dist) / ideal_dist
    overflow = max(abs(error) - 0.15, 0.0)
    if overflow <= 0:
        return 0.0, error
    strength = 0.8 + wire.neg_residue * 1.1 * sensitivity
    sign_factor = state_i.sign * state_j.sign
    force = -np.sign(error) * overflow * strength * sign_factor * elasticity
    return force, error

def compute_memory_contribution(residue: float) -> float:
    return math.tanh(residue) * 0.012

print('Force and Memory rules loaded.')