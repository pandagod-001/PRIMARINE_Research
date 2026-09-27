# PRIMARINE — Uncertainty-Gated Freight Decision Support Prototype

**System Classification:** Research Demonstration Prototype  
**Scope:** Simple, clean, believable decision-support prototype demonstrating the specific uncertainty-gated procurement mechanism validated in the PRIMARINE research program.

---

## 1. Prototype Purpose

This prototype demonstrates ONE specific research mechanism:
```
FREIGHT FORECAST
        ↓
CONFORMAL PREDICTION INTERVAL
        ↓
UNCERTAINTY WIDTH (W = U - L)
        ↓
DECISION GATE (W vs tau)
        ↓
PROCEED / DEFER
```

It is **NOT** the complete PRIMARINE enterprise platform. It does not connect to live AIS, stream market feeds, or execute autonomous charter contracts.

---

## 2. Quickstart Instructions

The prototype is lightweight and runs directly in any modern browser via local HTTP server:

```bash
# Navigate to the prototype directory
cd prototype

# Launch local server
python -m http.server 8000
```
Open **`http://localhost:8000/ui/index.html`** in your browser.

- **Main Decision Tool:** `http://localhost:8000/ui/index.html`
- **Research Evidence Page:** `http://localhost:8000/ui/research.html`

---

## 3. Data-Driven Architecture

```
[ prototype/data/research_scenarios.json ]  <-- Derived directly from testbed research results
                     ↓
[ prototype/config/research_config.json ]    <-- Authoritative pre-calibrated threshold (tau = 5.9529)
                     ↓
[ prototype/logic/decisionEngine.js ]        <-- Pure function calculating width & gating logic
                     ↓
[ prototype/ui/app.js & index.html ]        <-- Clean, minimal UI displaying decision & "Why?" modal
```

- **Zero Hard-Coded Decisions:** Every decision (`PROCEED` vs `DEFER`) is computed dynamically by `calculateDecision()` by comparing interval width against the configured threshold.
- **Zero Fabricated Scenarios:** All observations come from the empirical Baltic Dry Index evaluation testbed (`research/decision_boundary/decision_boundary_analysis.csv`).

---

## 4. Running Unit Tests

```bash
node prototype/tests/test_decision_logic.js
```
