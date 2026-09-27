import os
import re

files = [
    'research/FINAL_RESEARCH_CONTRIBUTION.md',
    'research/VALIDATION_AUDIT.md',
    'results/research/PPT_RESEARCH_CLAIMS.md',
    'results/research/turning_point_analysis.md',
    'results/research/uncertainty_validation.md',
    'results/research/decision_strategy_analysis.md',
    'results/research/directional_significance.md'
]

forbidden_patterns = [
    (r'(?i)32\.33%\s+improvement', '32.33% improvement (should be percentage points)'),
    (r'(?i)saves\s+2\.95%', 'saves 2.95% (should be rolling range/advantage)'),
    (r'(?i)statistically\s+significant\s+directional\s+improvement', 'statistically significant directional improvement'),
    (r'(?i)universal\s+savings', 'universal savings'),
    (r'(?i)COVID\s+coverage\s+proves\s+calibration', 'COVID coverage proves calibration'),
    (r'(?i)beats\s+persistence\s+in\s+MAE', 'beats persistence in MAE')
]

errors = []
for f in files:
    if os.path.exists(f):
        content = open(f, encoding='utf-8').read()
        for pat, desc in forbidden_patterns:
            matches = re.findall(pat, content)
            if matches:
                errors.append(f'{f}: Found forbidden pattern "{desc}": {matches}')

if errors:
    print('Language check FAILED:')
    for e in errors:
        print('  -', e)
else:
    print('ALL SCIENTIFIC LANGUAGE & TERMINOLOGY CHECKS PASSED PERFECTLY!')
