# PRIMARINE Research Prototype — Operational & Methodological Limitations

**Document Version:** 1.0.0 (Research Prototype)  
**Status:** Authoritative  

---

## 1. Scope Boundaries (What this Prototype is NOT)

This software artifact is a **Research Prototype** demonstrating a specific uncertainty quantification and selective prediction mechanism. It does **NOT**:
1. Connect to live maritime data feeds, Baltic Exchange APIs, or commercial shipping indices.
2. Ingest or stream real-time satellite AIS vessel positions.
3. Query port community systems (PCS) for live berth lineups or tidal window delays.
4. Execute binding commercial charter party contracts or financial trades.
5. Provide autonomous procurement decisions without authorized human approval.
6. Represent the complete multi-tier enterprise architecture of PRIMARINE.

---

## 2. Methodological Boundaries

- **Exchangeability Assumption:** Split-CQR finite-sample coverage guarantees hold under the assumption of exchangeability. Extreme out-of-distribution events (such as the COVID-19 pandemic shock where coverage degraded to 50.59%) require dynamic recalibration.
- **Threshold Specificity:** The pre-calibrated threshold $\tau = 5.9529$ was derived from the validation median width of the Baltic Dry Index dataset. Applying the system to new shipping corridors or tanker routes requires route-specific calibration.
- **Observational Correlation:** High conformal width is observationally associated with elevated false-breakout risk ($\text{AUC} = 0.6719$); it is a risk-gating signal, not an oracle predicting market movements with certainty.
