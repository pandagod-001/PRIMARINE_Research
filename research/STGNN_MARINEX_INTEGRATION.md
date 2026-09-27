# PRIMARINE ST-GNN Integration with Core Decision Engine

**Document:** `research/STGNN_PRIMARINE_INTEGRATION.md`  
**Date:** 2026-09-24  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Multi-Layer Decision Pipeline

The Spatio-Temporal Graph Neural Network (ST-GNN) integrates directly into the existing validated PRIMARINE chartering decision engine as a **spatial risk multiplier**:

```text
                        MULTIMODAL MARKET SIGNALS
                  (BDRY Futures, Brent, BHP, Vale, FX)
                                   │
                                   ▼
                       TEMPORAL FORECAST ENGINE
                         (LightGBM Regressor)
                                   │
                                   ▼
                         7-DAY FREIGHT FORECAST
                                   │
                   ┌───────────────┴───────────────┐
                   │                               │
                   ▼                               ▼
       SPLIT-CQR UNCERTAINTY             ST-GNN NETWORK RISK
         (Calibrated Bands)            (Disruption Propagation)
                   │                               │
                   └───────────────┬───────────────┘
                                   ▼
                       CHARTERING DECISION ENGINE
                                   │
           ┌───────────────────────┼───────────────────────┐
           ▼                       ▼                       ▼
      [ ENTER_NOW ]          [ DEFER_ENTRY ]         [ ABSTAIN / MONITOR ]
(Rising Freight + Low   (Softening Freight +    (High Disruption Risk OR
   Disruption Risk)       Low Disruption Risk)      CQR Interval Degraded)
```

---

## 2. Formal Decision Rule Formulation

Let $\Delta_{\text{pred}} = (\hat{y}_{t+7} - y_t) / y_t \times 100$ be the predicted market movement, $W_{\text{CQR}}(t)$ be the 90% conformal interval width, and $R_{\text{route}}(t) \in [0, 1]$ be the ST-GNN propagated route disruption risk.

$$\text{Decision}(t) = \begin{cases}
\text{ABSTAIN / HIGH\_UNCERTAINTY} & \text{if } W_{\text{CQR}}(t) > 1.35 \cdot \text{Median}(W) \text{ or } R_{\text{route}}(t) > 0.65 \\
\text{ENTER\_NOW} & \text{if } \Delta_{\text{pred}} \ge +2.0\% \text{ and } R_{\text{route}}(t) \le 0.40 \\
\text{DEFER\_ENTRY} & \text{if } \Delta_{\text{pred}} \le -2.0\% \text{ and } R_{\text{route}}(t) \le 0.40 \\
\text{MONITOR} & \text{otherwise}
\end{cases}$$

---

## 3. Practical Value for Ministry of Steel Charterers

- **Scenario 1 (Pure Market Signal):** If market futures point upward (+5%) but port operations are normal ($R_{\text{route}} = 0.35$), the system triggers `ENTER_NOW` to lock in favorable rates before fixture prices rise.
- **Scenario 2 (Spatial Network Disruption):** If market futures look stable (+0.5%) but a major cyclone disrupts Hay Point and propagates severe congestion down the Singapore–Paradip corridor ($R_{\text{route}} = 0.55$), the system prevents premature commitments and triggers `ABSTAIN / HIGH_UNCERTAINTY` to protect against laycan breaches and demurrage.
