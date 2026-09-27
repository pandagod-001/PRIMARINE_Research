# FUTURE RESEARCH EXTENSION — SPATIO-TEMPORAL GRAPH NEURAL NETWORKS (ST-GNN)

**Document:** `results/research/FUTURE_GNN_EXTENSION.md`  
**Classification:** Conceptual Architecture & Future Work Specification  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Context & Architectural Distinction

Current validated PRIMARINE operates primarily on **multimodal market time-series signals** (freight futures proxies, bunker fuel, upstream mining velocity, macroeconomic FX, and volatility regimes).

The next research stage can introduce a **Spatio-Temporal Graph Neural Network (ST-GNN)** to explicitly model how localized maritime disruptions propagate geographically across shipping corridors.

---

## 2. Proposed Graph Formulation

```text
  [ Port of Hay Point ] ──────────────► [ Port of Paradip ]
          │                                      │
          ▼                                      ▼
  [ Port of Newcastle ] ──────────────► [ Port of Visakhapatnam ]
```

### A. Graph Nodes:
- Major Origin & Destination Ports (e.g., Hay Point, Gladstone, Newcastle, Paradip, Visakhapatnam, Haldia, Tuticorin)
- Maritime Chokepoints & Terminals
- Regional Vessel Fleets & Anchorages

### B. Graph Edges:
- Navigable Shipping Corridors & Distance-weighted Routes
- Historical Vessel Flow Density & Fleet Positioning Connectivity
- Port Substitution / Alternative Discharge Relationships

### C. Node & Edge Dynamic Features:
- Port-level Congestion & Dwell Time
- Vessel Waiting Counts & Anchorage Queues
- Local Meteorological Disruption Alerts (Significant Wave Height, Cyclone Tracks)
- Berth-level Draft Availability & Siltation Constraints

### D. Temporal Dynamic Signals:
- High-Frequency AIS Telemetry (Speed, Draught, Destination, ETA)
- Notice of Readiness (NOR) and Berth Event Logs
- Port Disruption and Congestion Propagation History

---

## 3. Objective of the Future Extension

The primary objective is to **propagate localized port disruptions through the maritime network and estimate downstream freight impact** (e.g., how a 5-day cyclone delay at Paradip or severe congestion at Newcastle shifts regional Capesize vessel supply and spot charter rates).

---

## 4. Critical Limitation & Validation Boundary

> [!IMPORTANT]
> **EXPLICIT RESEARCH BOUNDARY FOR EVALUATION:**  
> **ST-GNN is a future extension and is not included in the current validated experimental results because the required high-frequency port/AIS graph telemetry is not currently part of the validated public dataset.**
>
> All empirical metrics presented in PRIMARINE (F1 score: 59.51%, Directional Accuracy: 59.15%, CQR Coverage: 88.19%, Procurement Advantage: +1.04% to +2.95%) belong strictly to the validated multimodal time-series engine. No fabricated accuracy, F1, MAE, or economic metrics are claimed for ST-GNN.
