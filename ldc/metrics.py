import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class CreativityMetrics:
    diversity_history: List[float] = field(default_factory=list)
    novelty_history: List[float] = field(default_factory=list)
    tagged_events: List[Dict[str, Any]] = field(default_factory=list)  # GPS-tagged creative events

    def compute_diversity(self, states) -> float:
        vs = np.array([s.v for s in states])
        residues = np.array([s.residue for s in states])
        # Diversity: variance + spread
        v_var = np.var(vs) if len(vs) > 1 else 0.0
        res_var = np.var(residues) if len(residues) > 1 else 0.0
        pairwise_dist = np.mean([np.abs(vs[i] - vs[j]) for i in range(len(vs)) for j in range(i+1, len(vs))]) if len(vs) > 1 else 0.0
        diversity = v_var + res_var + pairwise_dist * 0.5
        self.diversity_history.append(diversity)
        return diversity

    def compute_novelty(self, states, prev_states=None) -> float:
        if prev_states is None:
            novelty = 0.0
        else:
            curr_vs = np.array([s.v for s in states])
            prev_vs = np.array([s.v for s in prev_states])
            delta = np.mean(np.abs(curr_vs - prev_vs))
            # Novelty boost from high residue or new spread
            res_novelty = np.mean([s.residue for s in states]) * 0.3
            novelty = delta + res_novelty
        self.novelty_history.append(novelty)
        return novelty

    def tag_creative_event(self, t: int, state_idx: int, wire_key: str, residue: float, 
                           halluc_intensity: float, shift: float, source: str = 'hallucination') -> Dict:
        """GPS-like tagging for origin tracing of hallucination/creative event"""
        event = {
            't': t,
            'state_idx': state_idx,
            'wire_key': wire_key,
            'residue': residue,
            'halluc_intensity': halluc_intensity,
            'creative_shift': shift,
            'source': source,
            'gps': f"step{t}_wire{wire_key}_state{state_idx}",  # GPS probe string
            'mark': f"[HALLUC-{source}] from {wire_key} @ state{state_idx} (res={residue:.3f}, int={halluc_intensity:.2f})"
        }
        self.tagged_events.append(event)
        return event

    def get_recent_gps(self, n: int = 5) -> List[str]:
        return [e['gps'] for e in self.tagged_events[-n:]]

    def summary(self) -> Dict:
        return {
            'avg_diversity': np.mean(self.diversity_history) if self.diversity_history else 0,
            'avg_novelty': np.mean(self.novelty_history) if self.novelty_history else 0,
            'total_creative_events': len(self.tagged_events),
            'recent_gps': self.get_recent_gps(3)
        }

print('CreativityMetrics with GPS tagging loaded.')