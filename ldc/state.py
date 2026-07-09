from dataclasses import dataclass

@dataclass
class LatentState:
    v: float = 0.0
    residue: float = 0.0
    phase_offset: float = 0.0

print('LatentState defined.')