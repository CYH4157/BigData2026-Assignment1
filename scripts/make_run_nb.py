"""Make a copy of finetune_q1-q3.ipynb configured for one experiment.

usage: make_run_nb.py NAME BASELINE(true/false) [rank:component ...]
Each run writes to its own outputs/Assignment1/NAME/ so parallel runs never
overwrite each other's benchmark_results.csv.
"""
import json
import sys
from pathlib import Path

REPO = Path.home() / 'BigData2026-Assignment1'
name, baseline, specs = sys.argv[1], sys.argv[2].lower() == 'true', sys.argv[3:]

runs = ''.join(
    f"   {{'rank': {int(s.split(':')[0])}, 'component': '{s.split(':')[1]}'}},\n"
    for s in specs
)

REPLACEMENTS = [
    ("RESULT_ROOT = Path.home() / 'BigData2026-Assignment1' / 'outputs' / 'Assignment1'",
     f"RESULT_ROOT = Path.home() / 'BigData2026-Assignment1' / 'outputs' / 'Assignment1' / '{name}'"),
    ("MANUAL_RUNS = [\n   {'rank': 16, 'component': 'default'},\n]",
     f"MANUAL_RUNS = [\n{runs}]"),
    ('RUN_FRESH_BASELINE = True', f'RUN_FRESH_BASELINE = {baseline}'),
]

nb = json.loads((REPO / 'finetune_q1-q3.ipynb').read_text(encoding='utf-8'))
for old, new in REPLACEMENTS:
    hits = [c for c in nb['cells'] if old in c['source']]
    assert len(hits) == 1, f'expected one match for {old[:40]!r}, got {len(hits)}'
    hits[0]['source'] = hits[0]['source'].replace(old, new)

out_dir = REPO / 'outputs' / 'runs'
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / f'{name}.ipynb'
out.write_text(json.dumps(nb, ensure_ascii=False), encoding='utf-8')
print(out)
