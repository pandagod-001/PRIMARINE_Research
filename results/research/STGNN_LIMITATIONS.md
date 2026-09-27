# PRIMARINE ST-GNN Limitations & Data Boundary Disclosures

**Document:** `results/research/STGNN_LIMITATIONS.md`  
**Date:** 2026-09-24  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Explicit Data Boundary & Access Limitations

1. **AIS Telemetry Gaps:** High-frequency terrestrial and satellite AIS streaming messages (e.g. Spire, MarineTraffic) require commercial institutional subscriptions. No fabricated live AIS streams are claimed.
2. **Port Congestion Telemetry:** Real-time port dwell times, berth queues, and anchorage waiting counts are not publicly available via free REST APIs. Controlled simulation scenarios are used to validate the graph diffusion equations.
3. **Graph Topology Completeness:** The current proof-of-concept models 8 major bulk ports and 11 shipping corridors. A production deployment requires expanding the topology to 50+ global hub nodes and multi-tier canal corridors (Suez, Panama, Malacca).

---

## 2. Distinction Between Validated Core vs ST-GNN Extension

- **Validated Core (Ready for Evaluation):** LightGBM Multimodal Forecasting, 7-Day Turning-Point Inflection Detection, Split-Conformalized Quantile Regression (CQR), and the Economic Charter Decision Engine. (Trained on 1,920+ authentic daily market observations).
- **ST-GNN Extension (Architectural Prototype):** Spatial disruption propagation across graph nodes, demonstrating message-passing and spatial attenuation under controlled scenarios.
