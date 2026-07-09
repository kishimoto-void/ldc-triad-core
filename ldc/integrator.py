import random
import math
import numpy as np
from .site import BASE_IDEAL_DIST, TOLERANCE
from .rules import compute_restoring_force, compute_memory_contribution

def integrate_step(states, wires, sites, params, t: int):
    # Simple triad assumption for demo
    mean_v = sum(s.v for s in states) / len(states)
    pulsation = params.get('pulsation', True)
    pulse_period = params.get('pulse_period', 40)
    ideal = BASE_IDEAL_DIST
    if pulsation:
        phase = 2 * math.pi * t / pulse_period
        ideal *= (1 + 0.08 * math.sin(phase))
    
    total_forces = [0.0] * len(states)
    for i in range(len(states)):
        for j in range(i+1, len(states)):
            key = f'{min(i,j)}-{max(i,j)}'
            wire = wires[key]
            f, error = compute_restoring_force(
                states[i], states[j], wire, ideal, 
                params.get('elasticity', 1.6), params.get('sensitivity', 1.4)
            )
            total_forces[i] += f
            total_forces[j] += f  # symmetric approx
            wire.update(error, params.get('sensitivity', 1.4))
    
    for i, s in enumerate(states):
        base = mean_v - s.v
        noise = random.uniform(-0.5, 0.5) * 0.18
        mem = compute_memory_contribution(s.residue)
        s.v += noise + 0.10 * base + total_forces[i] + mem
        s.v = max(-4.5, min(4.5, s.v))
    
    return states, wires

print('Integrator ready.')