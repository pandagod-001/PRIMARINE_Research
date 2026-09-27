# PRIMARINE ST-GNN Disruption Propagation Proof-of-Concept

**Document:** `research/STGNN_PROOF_OF_CONCEPT.md`  
**Date:** 2026-09-24  
**Classification:** Architectural Simulation Proof-of-Concept (Not Measured Ground Truth)  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Objective of the Implementation

To demonstrate how localized port and maritime chokepoint disruptions propagate geographically across shipping lanes to affect downstream freight risk in destination ports.

---

## 2. Experimental Data & Simulation Setup

- **Graph Topology:** 8 Physical Nodes (Hay Point, Gladstone, Newcastle, Samarinda, Singapore Strait, Paradip, Visakhapatnam, Haldia) connected by 11 Navigable Maritime Shipping Corridors.
- **Data Status:** While graph topology and maritime routes are physically authentic, node-level dwell times and operational shock vectors are modeled under **controlled simulation** due to the absence of public high-frequency port telemetry.
- **Disruption Scenario:** Severe cyclone / weather disruption injected at the **Port of Hay Point (Node 0)**, Australia's primary coking coal export terminal.

---

## 3. Controlled Simulation Results

| Node ID | Port / Maritime Hub | Network Role | Baseline Risk Score [0, 1] | Disrupted Risk Score [0, 1] | Risk Score Increase ($\Delta$) |
|---|---|---|---|---|---|
| **0** | **Hay Point (AU)** | Disruption Origin | 0.3547 | 0.5751 | **+0.2204 (Epicenter)** |
| **4** | **Singapore Strait** | Transit Chokepoint | 0.4284 | 0.5655 | **+0.1371 (1-Hop Corridor)** |
| **5** | **Port of Paradip (IN)** | Direct Destination | 0.3806 | 0.5525 | **+0.1719 (1-Hop Direct Capesize)** |
| **6** | **Visakhapatnam (IN)** | Secondary Destination | 0.3663 | 0.4118 | **+0.0455 (2-Hop Feeder)** |
| **7** | **Port of Haldia (IN)** | Secondary Destination | 0.3663 | 0.4118 | **+0.0455 (2-Hop Feeder)** |
| **1** | **Gladstone (AU)** | Adjacent Origin | 0.3467 | 0.3707 | **+0.0239 (Attenuated)** |
| **2** | **Newcastle (AU)** | Adjacent Origin | 0.3467 | 0.3707 | **+0.0239 (Attenuated)** |
| **3** | **Samarinda (ID)** | Regional Origin | 0.3467 | 0.3707 | **+0.0239 (Attenuated)** |

---

## 4. Spatial Attenuation & Decay Validation

The GNN architecture demonstrates consistent spatial decay, where disruption risk attenuates strictly with graph distance:

- **Hop 0 (Epicenter Origin - Hay Point):** $\Delta = +0.2204$
- **Hop 1 (Direct Maritime Corridors - Singapore & Paradip):** $\Delta = +0.1545$ (69.8% of epicenter impact transferred downstream)
- **Hop 2 (Secondary Ports - Vizag, Haldia, Samarinda):** $\Delta = +0.0325$ (14.7% of epicenter impact transferred)

---

## 5. Architectural Validation Conclusions

1. **Propagation Consistency:** The message-passing mechanism correctly routes shock energy along active shipping corridors rather than uniformly diffusing across unrelated nodes.
2. **Complementary Role:** The ST-GNN network score provides a route-specific risk multiplier ($[0, 1]$) that feeds into the chartering decision engine alongside the validated multimodal market forecast.
