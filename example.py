from ldc.triad import CreativeTriad

print('=== CreativeTriad with Diversity, Novelty & GPS-tagged Hallucination ===')
creative = CreativeTriad(halluc_intensity=0.45, creativity_threshold=0.7)
results = creative.run(steps=300)

print('\nFinal Summary:')
print(creative.get_creativity_summary())

print('\nSample recent tagged events (GPS probe):')
for event in creative.metrics.tagged_events[-5:]:
    print(event['mark'], '-> GPS:', event['gps'])

print('\nLast few step results (diversity/novelty/creative_events):')
for r in results[-5:]:
    print(r)