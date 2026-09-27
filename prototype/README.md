# PRIMARINE — Uncertainty-Gated Procurement Research Prototype

**System Classification:** Research Demonstration Prototype  
**Scope:** Interactive demonstration of the specific uncertainty-gated decision support mechanism investigated and validated in the PRIMARINE research program.  
**Authoritative Evidence:** `research/PRIMARINE_RESEARCH_PACKAGE/`, `research/EVIDENCE_REGISTRY.csv`, `research/decision_boundary/decision_boundary_analysis.csv`

---

## 1. Prototype Purpose & Scope

This prototype demonstrates the exact empirical research chain:
```
FREIGHT-RATE FORECAST
        ↓
CONFORMAL PREDICTION INTERVAL (Split-CQR)
        ↓
INTERVAL WIDTH (W)
        ↓
FALSE-BREAKOUT RISK ASSESSMENT
        ↓
SELECTIVE ABSTENTION (tau = 1.35x)
        ↓
SUGGESTED PROCUREMENT ACTION (ENTER vs DEFER / ABSTAIN)
```

> **IMPORTANT BOUNDARY:** This prototype does **NOT** implement live AIS, satellite vessel tracking, live port APIs, or autonomous charter party execution. It is a focused interactive demonstrator of the **validated uncertainty-gating research component**.

---

## 2. Quickstart Instructions

The prototype is a standalone, dependency-free single page application requiring only a standard web browser.

```bash
# Navigate to prototype directory
cd prototype/primarine_research_prototype

# Launch local HTTP server (Python 3)
python -m http.server 8080
```
Open **`http://localhost:8080`** in your browser to interact with:
- **Historical Testbed Mode:** Step through 288 chronological test scenarios from the Baltic Dry Index testbed.
- **Controlled Demonstration Cases:** Inspect explicit test scenarios illustrating lower-width vs elevated-width decisions.
- **Dynamic Conformal Chart:** Visualizes central forecast, Split-CQR bounds, interval width, and actual market outcomes.
- **Selective Abstention Scorecard:** Compares Forced Decision Policy (86 false breakouts) vs Uncertainty-Gated Policy (41 false breakouts, 52.33% reduction).
- **Negative Results Panel:** Highlights degenerate boundary crossing ($\text{AUC} = 0.5025$) and sign error non-correlation ($\text{AUC} = 0.4487$).

---

## 3. Directory Layout

```
prototype/primarine_research_prototype/
├── index.html                  <-- Main interactive demonstrator interface
├── css/
│   └── style.css               <-- Dark-mode CSS styling & responsive layout
├── js/
│   ├── app.js                  <-- Canvas chart rendering & decision controller
│   └── data.js                 <-- 288 verified testbed observations (JSON)
├── DATA_PROVENANCE.md          <-- Origin & split documentation
├── RESEARCH_TRACEABILITY.md    <-- Mapping to Evidence Registry IDs
├── PROTOTYPE_LIMITATIONS.md    <-- Methodological & operational boundaries
└── TEST_SCENARIOS.md           <-- Test cases & expected behaviors
```
