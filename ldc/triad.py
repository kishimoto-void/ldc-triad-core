import random
from dataclasses import dataclass, field
from typing import List, Dict
from .site import SITES, LatentSite
from .state import LatentState
from .wire import InteractionWire
from .integrator import integrate_step

@dataclass
class MinimalTriad:
    seed: int = 42
    phase_pattern: str = 'even120'
    elasticity: float = 1.6
    sensitivity: float = 1.4
    pulse_period: int = 40

    def __post_init__(self):
        rng = random.Random(self.seed)
        chosen = [0, 1, 5]
        self.sites: List[LatentSite] = [LatentSite(**SITES[i]) for i in chosen]  # attach pos/sign
        if self.phase_pattern == 'even120':
            offsets = [0.0, 2*3.1416/3, 4*3.1416/3]
        else:
            offsets = [0.0]*3
        self.states = [LatentState(phase_offset=o) for o in offsets]
        self.wires: Dict[str, InteractionWire] = {
            '0-1': InteractionWire(), '0-5': InteractionWire(), '1-5': InteractionWire()
        }
        self.params = {'elasticity': self.elasticity, 'sensitivity': self.sensitivity, 'pulse_period': self.pulse_period}

    def step(self, t: int):
        self.states, self.wires = integrate_step(self.states, self.wires, self.sites, self.params, t)
        return {'t': t, 'total_v': sum(s.v for s in self.states)}

    def run(self, steps: int = 800):
        return [self.step(i) for i in range(steps)]

if __name__ == '__main__':
    triad = MinimalTriad()
    results = triad.run(100)
    print('Triad run complete. Sample v:', [r['total_v'] for r in results[-3:]])