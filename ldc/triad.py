import random
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .site import SITES, LatentSite
from .state import LatentState
from .wire import InteractionWire
from .integrator import integrate_step
from .metrics import CreativityMetrics

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
        self.sites: List[LatentSite] = [LatentSite(**SITES[i]) for i in chosen]
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

@dataclass
class CreativeTriad(MinimalTriad):
    halluc_intensity: float = 0.35
    creativity_threshold: float = 0.8

    def __post_init__(self):
        super().__post_init__()
        self.metrics = CreativityMetrics()
        self.halluc_intensity = self.halluc_intensity
        self.creativity_threshold = self.creativity_threshold
        self.creative_events_count = 0
        self.prev_states = None

    def step(self, t: int):
        # 現実力学
        self.states, self.wires = integrate_step(self.states, self.wires, self.sites, self.params, t)
        
        # 創造性メトリクス計算
        diversity = self.metrics.compute_diversity(self.states)
        novelty = self.metrics.compute_novelty(self.states, self.prev_states)
        self.prev_states = [LatentState(v=s.v, residue=s.residue, phase_offset=s.phase_offset) for s in self.states]
        
        # ハルシネーション駆動の創造イベント（各state/wireにマーク）
        for i, s in enumerate(self.states):
            for wire_key, wire in self.wires.items():
                halluc_delta = abs(wire.error) * self.halluc_intensity * (1 + wire.neg_residue * 0.5)
                if halluc_delta > self.creativity_threshold:
                    shift = halluc_delta * random.uniform(0.6, 1.4)
                    s.v += shift * 0.4
                    s.residue += shift * 0.2
                    
                    # GPSタグ付きイベント記録
                    event = self.metrics.tag_creative_event(
                        t=t,
                        state_idx=i,
                        wire_key=wire_key,
                        residue=s.residue,
                        halluc_intensity=self.halluc_intensity,
                        shift=shift,
                        source='controlled_hallucination'
                    )
                    self.creative_events_count += 1
        
        return {
            't': t,
            'total_v': sum(s.v for s in self.states),
            'diversity': diversity,
            'novelty': novelty,
            'creative_events': self.creative_events_count,
            'recent_gps': self.metrics.get_recent_gps(2)
        }

    def run(self, steps: int = 800):
        results = []
        for i in range(steps):
            res = self.step(i)
            results.append(res)
        return results

    def get_creativity_summary(self):
        return self.metrics.summary()

if __name__ == '__main__':
    triad = MinimalTriad()
    results = triad.run(100)
    print('MinimalTriad sample:', [r['total_v'] for r in results[-3:]])
    
    creative = CreativeTriad(halluc_intensity=0.4)
    cres = creative.run(150)
    print('CreativeTriad final diversity/novelty:', creative.get_creativity_summary())
    print('Sample GPS marks:', [r.get('recent_gps') for r in cres[-3:] if r.get('recent_gps')])