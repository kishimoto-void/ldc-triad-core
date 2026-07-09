from ldc.triad import MinimalTriad

triad = MinimalTriad(phase_pattern='random', sensitivity=1.7)
print('Running Minimal Triad...')
results = triad.run(steps=200)
print('Done. Final total_v approx:', sum(s.v for s in triad.states))