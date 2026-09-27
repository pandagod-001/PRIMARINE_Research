# PRIMARINE Ideation Phase Claim Audit & Terminology Guardrails

**Document:** `research/FINAL_IDEATION_CLAIM_AUDIT.md`  
**Date:** 2026-09-24  
**Classification:** Scientific Integrity & Guardrail Audit  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Terminology Compliance Audit

This audit scanned all project documentation and verified that no inflated, unscientific, or ungrounded claims exist in the PRIMARINE ideation package.

| Risk Category | Prohibited / Flawed Terminology | Mandatory Approved Terminology | Verification Status |
|---|---|---|---|
| **Point Accuracy** | "PRIMARINE beats persistence in MAE" | "Persistence achieves lower point MAE (0.4175 vs 0.4644); PRIMARINE's edge is inflection detection." | **COMPLIANT** |
| **Inflection Gain** | "32.33% F1 improvement" | "PRIMARINE improves turning-point F1 by 32.33 percentage points over AR(5) (from 27.18% to 59.51%)." | **COMPLIANT** |
| **Directional Edge** | "Statistically significant directional prediction" | "Descriptive directional improvement (59.15% vs 50.70% SMA); formal significance not established (p=0.138)." | **COMPLIANT** |
| **Uncertainty** | "Guaranteed 100% error bounds" | "Split-CQR calibrated bands (88.19% empirical coverage); degrades during extreme stress to trigger ABSTAIN." | **COMPLIANT** |
| **Economic Impact** | "PRIMARINE guarantees 2.95% freight savings" | "Observed backtest advantage: +1.04% on untouched test set; +1.04%–+2.95% rolling. Illustrative scaling: $26K–$36K." | **COMPLIANT** |
| **ST-GNN Status** | "Real-time AIS disruption prediction" | "ST-GNN architectural proof-of-concept / controlled simulation; not historical measured telemetry." | **COMPLIANT** |
| **Hype Words** | "Revolutionary / First-ever / Flawless" | "Rigorous decision-intelligence system combining multimodal market forecasting with spatial network reasoning." | **COMPLIANT** |

---

## 2. Claim-by-Claim Verification Checklist

- [x] **Point MAE:** Persistence (`0.4175`) vs LightGBM (`0.4644`) accurately reported across all files.
- [x] **Inflection F1:** Correctly phrased as *32.33 percentage points* improvement over AR(5).
- [x] **Directional Accuracy:** Correctly labeled as *descriptive* with block-bootstrap CI `[45.70%, 67.86%]`, $p=0.138$.
- [x] **Conformal Coverage:** 90% nominal $\rightarrow$ 88.19% test coverage accurately stated.
- [x] **Stress Regime:** COVID-19 coverage drop to 50.59% explicitly documented as an abstention trigger.
- [x] **ST-GNN Simulation:** Disruption propagation labeled as *Controlled Simulation / Architectural POC* on all charts and tables.
- [x] **Spatial Attenuation:** Hop 0 (`+0.2204`) $\rightarrow$ Hop 1 (`+0.1545`) $\rightarrow$ Hop 2 (`+0.0325`) verified by script execution.
- [x] **Disconnected Control:** Rotterdam and Santos isolation ($\Delta = 0.0000$) verified by code.
- [x] **Implementation Boundaries:** High-frequency AIS and live port EDI clearly designated as *Future Implementation Phase*.
