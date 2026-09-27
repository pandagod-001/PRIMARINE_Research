# PRIMARINE Research Prototype — Decision Logic Specification

**Document Version:** 1.0.0  
**Status:** Authoritative  

---

## 1. Decision Logic Formulation

The core calculation is implemented as a pure function in `prototype/logic/decisionEngine.js`:

```javascript
// 1. Calculate conformal interval width
const width = upper_bound - lower_bound;

// 2. Fetch pre-calibrated threshold
const threshold = config.calibration_parameters.abstention_threshold; // 5.9529

// 3. Derive uncertainty stratum
if (width <= 4.50) {
    uncertainty_level = "Low";
} else if (width > 5.9529) {
    uncertainty_level = "Elevated";
} else {
    uncertainty_level = "Moderate";
}

// 4. Decision Gate
if (width > threshold) {
    decision = "DEFER";
    explanation = config.explanation_templates.DEFER;
} else {
    decision = "PROCEED";
    explanation = config.explanation_templates.PROCEED;
}
```

---

## 2. Validation Constraints

- If `upper_bound < lower_bound`, the engine throws an error (`Invalid interval`).
- If data fields are missing or null, the engine throws an error (`Missing required bounds`).
- All calculations are deterministic and verified against unit test assertions in `prototype/tests/test_decision_logic.js`.
