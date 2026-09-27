# PRIMARINE — Repository Migration & Path Mapping

**Document Version:** 1.0.0 (Frozen Consolidation)  
**Status:** Canonical Reference  
**Purpose:** Map legacy, preliminary, and exploratory file paths to their final canonical locations in the organized PRIMARINE repository structure.

---

## 1. Migration Philosophy

To prevent broken links, orphaned references, or accidental data loss, all legacy artifacts have been mapped to standardized canonical locations according to the four reality states.

- **Canonical Locations:** `research/PRIMARINE_RESEARCH_PACKAGE/`, `docs/PRIMARINE_PRODUCT_BLUEPRINT/`, `prototype/PRIMARINE-demo/`, `data/`, `results/`, `scripts/`.
- **Superseded Artifacts:** Archived in `archive/superseded/` to maintain a permanent forensic record without cluttering the operational root.

---

## 2. File Path Migration Mapping

| Legacy / Original File Path | New Canonical File Path | Status | Action Taken / Rationale |
| :--- | :--- | :--- | :--- |
| `research/FINAL_RESEARCH_POSITION.md` | `research/PRIMARINE_RESEARCH_PACKAGE/FINAL_RESEARCH_POSITION.md` | CANONICAL | Consolidated into official frozen research package |
| `research/ABSTRACT.md` | `research/PRIMARINE_RESEARCH_PACKAGE/ABSTRACT.md` | CANONICAL | Primary abstract for academic publication and SIH review |
| `research/FINAL_CLAIM_MATRIX.md` | `research/PRIMARINE_RESEARCH_PACKAGE/FINAL_CLAIM_MATRIX.md` | CANONICAL | Matrix linking claims to empirical validation data |
| `research/PRIOR_ART_REVIEW.md` | `research/PRIMARINE_RESEARCH_PACKAGE/PRIOR_ART_REVIEW.md` | CANONICAL | Systematic comparative literature review |
| `research/REPRODUCIBILITY_MANIFEST.md` | `research/PRIMARINE_RESEARCH_PACKAGE/REPRODUCIBILITY_MANIFEST.md` | CANONICAL | Detailed experimental execution manifest |
| `research/FIGURE_INDEX.md` | `research/PRIMARINE_RESEARCH_PACKAGE/FIGURE_INDEX.md` | CANONICAL | Canonical metadata index of all research figures |
| `research/STRATEGIC_PITCH_AND_PAPER_PLAYBOOK.md` | `research/PRIMARINE_RESEARCH_PACKAGE/STRATEGIC_PITCH_AND_PAPER_PLAYBOOK.md` | CANONICAL | Defence playbook for reviewers and evaluators |
| `research/FRAGILITY_RESEARCH_REPORT.md` | `research/PRIMARINE_RESEARCH_PACKAGE/FRAGILITY_RESEARCH_REPORT.md` | CANONICAL | Complete scientific report on fragility experiments |
| `SIH_PS26006_Comprehensive_Technical_Concept(2).md` | `docs/01_ORIGINAL_SYSTEM_VISION.md` & Root Doc | CANONICAL | Primary technical concept specification (updated with Sections 63–67) |
| `docs/PRIMARINE_PRODUCT_BLUEPRINT/01_PRODUCT_VISION_AND_ORIGINAL_SYSTEM_DESIGN.md` | `docs/01_ORIGINAL_SYSTEM_VISION.md` | CANONICAL | Complete 8-stage enterprise product blueprint |
| `docs/PRIMARINE_PRODUCT_BLUEPRINT/04_API_INTEGRATION_STATUS_AND_DATA_ROADMAP.md` | `docs/api/API_INTEGRATION_STATUS.md` | CANONICAL | Full specification of provider adapters and connection status |
| `prototype/PRIMARINE-demo/index.html` | `prototype/PRIMARINE-demo/index.html` | CANONICAL | Interactive demonstrator front-end entry point |
| `prototype/PRIMARINE-demo/css/styles.css` | `prototype/PRIMARINE-demo/css/styles.css` | CANONICAL | Modern dark-mode dashboard styling with glassmorphism |
| `prototype/PRIMARINE-demo/js/app.js` | `prototype/PRIMARINE-demo/js/app.js` | CANONICAL | Main application controller and UI event orchestrator |
| `prototype/PRIMARINE-demo/js/engine.js` | `prototype/PRIMARINE-demo/js/engine.js` | CANONICAL | Client-side execution of Split-CQR uncertainty gating |
| `prototype/PRIMARINE-demo/data/fixtures.json` | `prototype/PRIMARINE-demo/data/fixtures.json` | CANONICAL | Curated port, vessel, market, and disruption fixture data |
| `research/experiments/01_baseline_forecasting.py` | `scripts/experiments/01_baseline_forecasting.py` | CANONICAL | Benchmark forecasting script (Persistence, SMA, AR, LightGBM, XGBoost) |
| `research/experiments/02_cqr_calibration.py` | `scripts/experiments/02_cqr_calibration.py` | CANONICAL | Split-CQR conformal calibration and coverage evaluation script |
| `research/experiments/03_feasibility_invariance.py` | `scripts/experiments/03_feasibility_invariance.py` | CANONICAL | Hard-constraint physical feasibility invariance evaluation script |
| `research/experiments/07_stgnn_poc.py` | `scripts/experiments/07_stgnn_poc.py` | CANONICAL | Synthetic 8-node spatio-temporal graph disruption script |
| `research/experiments/08_fragility_surface.py` | `scripts/experiments/08_fragility_surface.py` | CANONICAL | Multi-dimensional perturbation and fragility surface generator |
| `research/experiments/09_abstention_vs_forced.py` | `scripts/experiments/09_abstention_vs_forced.py` | CANONICAL | Selective abstention policy and Wilcoxon significance test |
| `research/experiments/10_timing_flip_threshold.py` | `scripts/experiments/10_timing_flip_threshold.py` | CANONICAL | False-breakout ROC analysis and threshold calibration |
| `research/experiments/13_boundary_proximity.py` | `scripts/experiments/13_boundary_proximity.py` | CANONICAL | Spot boundary-crossing degeneracy experiment script |

---

## 3. Preservation Verification

- **Total Canonical Files Verified:** 345 files cataloged in `research/MASTER_FILE_INVENTORY.csv`.
- **Zero-Loss Rule:** No experimental code or empirical data has been discarded or overwritten.
