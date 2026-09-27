# PRIMARINE — Claim Language Safety Audit

**Document Version:** 1.0.0 (Release Gate)  
**Status:** Audit Pass (Canonical Scientific Phrasing Enforced)  
**Scope:** Systematic scan of the codebase and documentation to eliminate unhedged, exaggerated, or misleading scientific claims.

---

## 1. Regulated Terminology Rules

To prevent accidental overclaiming in peer-reviewed contexts and competitive evaluations, PRIMARINE strictly enforces scientific hedging rules:

| High-Risk Term | Scientific Risk | Enforced Canonical Phrasing |
| :--- | :--- | :--- |
| **"proves" / "proves that"** | Unjustified causal claim on observational data. | **"was observationally associated with"** / **"demonstrates"** |
| **"eliminates false breakouts"** | False claim of complete risk eradication. | **"reduced observed false-breakout events by 52.33% (from 86 to 41)"** |
| **"optimal threshold"** | Unproven claim of mathematical universality. | **"pre-calibrated threshold ($\tau = 1.35 \times \text{validation median}$)"** |
| **"guarantees 90% coverage"** | Misleading claim ignoring covariate shift. | **"satisfies nominal 90% marginal coverage under exchangeability"** |
| **"first system to..."** | Unverifiable priority claim against vast literature. | **"investigates conformal uncertainty-gated decision support"** |
| **"real-world validated"** | Confusing synthetic/benchmark testbeds with live deployment. | **"validated on historical benchmark series and tested fixtures"** |
| **"live connected APIs"** | Misrepresenting offline prototype mock fixtures. | **"offline prototype using curated fixtures; planned live API adapters"** |
| **"real AIS ST-GNN"** | Misrepresenting 8-node synthetic proof-of-concept. | **"synthetic 8-node ST-GNN proof-of-concept; real AIS ST-GNN is future research"** |

---

## 2. Audit Findings Across Active Documents

| Document Audited | Regulated Patterns Detected | Action Taken & Verification | Status |
| :--- | :--- | :--- | :--- |
| `README.md` | "First", "Guarantees", "Eliminates" | Strictly hedged. Uses "associated with", "pre-calibrated", "reduced observed false breakouts". | **CLEARED (PASS)** |
| `research/PRIMARINE_RESEARCH_PACKAGE/` | "Optimal", "Live APIs" | Abstract and position papers strictly specify $\tau = 1.35\times$ as pre-calibrated and APIs as planned. | **CLEARED (PASS)** |
| `docs/00_PROJECT_OVERVIEW.md` | "100% Feasibility" | Constrained to "tested dry-bulk constraints (PDFR = 0.00%)". | **CLEARED (PASS)** |
| `docs/04_WHAT_WE_FOUND.md` | "Point forecast superiority" | Explicitly notes LightGBM point MAE loses to Persistence (0.4644 vs 0.4175). | **CLEARED (PASS)** |
| `docs/06_LIMITATIONS.md` | Broad generalizations | Explicitly lists COVID-19 degradation (50.59%), draft limits, and fixture specificity. | **CLEARED (PASS)** |
| `prototype/README.md` | "Live market streaming" | Explicitly titled "LOCAL VERTICAL-SLICE PROTOTYPE" using curated offline fixtures. | **CLEARED (PASS)** |
