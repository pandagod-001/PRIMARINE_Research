# PRIMARINE Research Prototype — Test Scenarios & Deterministic Cases

**Document Version:** 1.0.0 (Research Prototype)  
**Status:** Authoritative  

---

## 1. Deterministic Demonstration Test Cases

The prototype incorporates four pre-configured demonstration cases in addition to the full 288-sample chronological testbed:

### Case 1: Lower-Width Regime ($W \le \tau$)
- **Parameters:** Current Spot = $6.50/MT, Forecast = $7.10/MT, CQR Bounds = [$5.20, $9.60], Interval Width $W = 4.40$ ($\le 5.9529$).
- **Expected Action:** **`PROCEED / ENTER`**
- **Observed Outcome:** Realized Rate = $7.05/MT (Price increased; timing commitment profitable; zero false breakout).

### Case 2: Elevated-Width Regime ($W > \tau$)
- **Parameters:** Current Spot = $6.20/MT, Forecast = $6.85/MT, CQR Bounds = [$4.80, $12.60], Interval Width $W = 7.80$ ($> 5.9529$).
- **Expected Action:** **`ABSTAIN / DEFER`**
- **Observed Outcome:** Realized Rate = $5.40/MT (Price dropped; point forecast would have triggered a false breakout; abstention protected capital).

### Case 3: Boundary-Crossing Demonstration (Negative Control)
- **Parameters:** Current Spot = $5.80/MT, Forecast = $6.10/MT, CQR Bounds = [$5.10, $11.90], Interval Width $W = 6.80$.
- **Demonstration:** Illustrates that interval encompasses spot price ($L \le B \le U$), but boundary crossing alone has random discrimination ($\text{AUC} = 0.5025$). Decision relies on width threshold $\tau$.

### Case 4: Directional Sign Error Disconnect
- **Parameters:** Current Spot = $5.90/MT, Forecast = $6.40/MT, CQR Bounds = [$5.10, $10.80], Interval Width $W = 5.70$.
- **Demonstration:** Illustrates that conformal width measures volatility and epistemic spread, not binary point forecast sign correctness ($\text{AUC} = 0.4487$).
