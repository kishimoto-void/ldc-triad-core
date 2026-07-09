from dataclasses import dataclass

@dataclass
class InteractionWire:
    error: float = 0.0
    neg_residue: float = 0.0
    pos_storage: float = 0.0
    last_overflow: float = 0.0

    def update(self, current_error: float, sensitivity: float = 1.0):
        overflow = max(abs(current_error) - 0.15, 0.0)
        if overflow > 0:
            self.neg_residue = 0.93 * self.neg_residue + 0.07 * overflow * sensitivity
        if overflow < self.last_overflow and self.last_overflow > 0.05:
            recovered = self.last_overflow - overflow
            self.pos_storage = 0.91 * self.pos_storage + 0.09 * recovered * 0.45 * sensitivity
        self.last_overflow = overflow
        self.error = current_error

print('InteractionWire ready.')