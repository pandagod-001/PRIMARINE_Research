# PRIMARINE Spatio-Temporal Graph Neural Network (ST-GNN) Research Design

**Document:** `research/STGNN_RESEARCH_DESIGN.md`  
**Classification:** Research Extension & Architectural Proof-of-Concept  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Research Question

> **"Can spatial maritime-network information complement market-level freight intelligence by identifying how localized port or route disruptions may propagate into downstream freight risk?"**

---

## 2. Research Role Separation: Market Layer vs Network Layer

To maintain absolute scientific rigor, PRIMARINE clearly separates tasks:

```text
┌───────────────────────────────────────────────────────────────┐
│ 1. Temporal Market Layer (Validated Core)                     │
│    - Model: LightGBM Multi-Modal + Split-CQR                  │
│    - Target: Near-term global dry bulk freight momentum (BDRY)│
│    - Output: 7-day forecast, turning-point signal, uncertainty│
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ 2. Spatial Maritime Network Layer (ST-GNN Proof-of-Concept)   │
│    - Model: Spatio-Temporal Graph Neural Network (GCN/GAT)    │
│    - Target: Regional port disruption & route risk propagation│
│    - Output: Node & Route Risk Scores [0, 1]                  │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ 3. Integrated Chartering Decision Engine                      │
│    - Translates Market Forecast + Uncertainty + Network Risk  │
│    - Action: ENTER_NOW / DEFER_ENTRY / MONITOR / ABSTAIN      │
└───────────────────────────────────────────────────────────────┘
```

---

## 3. Maritime Graph Topology & Schema

The proof-of-concept graph models key bulk shipping hubs between Australia, Indonesia, and the East Coast of India:

### Nodes ($V = 8$ Major Ports/Hubs)
1. `N0: Hay Point (Australia)` — Major Coking Coal Export Terminal
2. `N1: Gladstone (Australia)` — Major Coking Coal & Alumina Port
3. `N2: Newcastle (Australia)` — Thermal/Coking Coal Terminal
4. `N3: Samarinda (Indonesia)` — Thermal Coal Export Anchorage
5. `N4: Singapore Straits` — Key Maritime Chokepoint & Bunkering Hub
6. `N5: Port of Paradip (India)` — Primary East Coast Coking Coal Import Port
7. `N6: Port of Visakhapatnam (India)` — Deepwater Bulk Import Port
8. `N7: Port of Haldia / SMPK (India)` — Draft-Restricted Riverine Bulk Port

### Edges ($E = 11$ Navigable Shipping Corridors)
- $(N0, N4), (N1, N4), (N2, N4)$ [Australia $\rightarrow$ Malacca/Singapore Corridor]
- $(N3, N4)$ [Indonesia $\rightarrow$ Singapore Corridor]
- $(N4, N5)$ [Singapore $\rightarrow$ Paradip Corridor]
- $(N4, N6)$ [Singapore $\rightarrow$ Visakhapatnam Corridor]
- $(N4, N7)$ [Singapore $\rightarrow$ Haldia Corridor]
- $(N5, N6), (N6, N7), (N5, N7)$ [Indian Coastal Feeder / Alternate Discharge Edges]
- $(N0, N5)$ [Direct Deep-Sea Capesize Route]

---

## 4. ST-GNN Architecture Specification

A lightweight, robust 2-stage Spatio-Temporal architecture:

1. **Temporal Node Feature Encoder:**  
   $h_v^{(0)} = \text{Linear}(\text{Concat}(X_{v, t-T:t})) \in \mathbb{R}^{d}$  
   Encodes historical rolling congestion, dwell time, and weather disturbance over $T=5$ lag steps.
2. **Spatial Graph Convolution Layer (GCN / Message Passing):**  
   $$h_v^{(1)} = \sigma\left( W \sum_{u \in \mathcal{N}(v) \cup \{v\}} \frac{1}{\sqrt{\tilde{d}_u \tilde{d}_v}} h_u^{(0)} \right)$$  
   Propagates disruption signals across directly connected shipping routes and adjacent ports.
3. **Disruption Risk & Downstream Impact Head:**  
   $$\text{Risk}_v = \text{Sigmoid}(\text{MLP}(h_v^{(1)})) \in [0, 1]$$  
   $$\text{Network\_Impact} = \text{Mean}(\{\text{Risk}_u : u \in \text{Destination Nodes}\})$$

---

## 5. Explicit Data Boundary & Limitations

> [!IMPORTANT]
> **SIMULATION & PROOF-OF-CONCEPT DISCLOSURE:**  
> While the graph topology and shipping routes are physically authentic, node-level daily dwell times and congestion metrics are constructed under controlled simulation scenarios. This ST-GNN module is an architectural proof-of-concept demonstrating how spatial network reasoning integrates with the validated market engine.
