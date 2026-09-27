# Comprehensive Literature Review & Prior-Art Gap Study

**Project:** PRIMARINE (SIH 2026 PS-26006)  
**Research Focus:** Freight Rate Forecasting, Regime-Switching Dynamics, Probabilistic Conformal Prediction, and Maritime Decision Optimization.

---

## 1. Prior-Art & Competitor Matrix

| Research Paper / Model Family | Data Inputs | Predictive Target | Horizon | Key Strength | Critical Limitation | PRIMARINE Novelty Opportunity |
|---|---|---|---|---|---|---|
| **Alizadeh & Nomikos (2009)** *Investment in Dry Bulk* | Historical Baltic FFA contracts, spot rates | Baltic Freight Index (BDI, BCI, BPI) | 1–3 months | Rigorous econometric cointegration modeling | Assumes linear stationarity; fails during violent regime shifts | **Nonlinear Regime Detection:** Incorporate explicit volatility-regime states into charter timing. |
| **Kavussanos & Tsouknidis (2014)** *J. Banking & Finance* | Spot & time-charter rates, macroeconomic factors | Freight rate volatility (GARCH / Markov Switching) | Daily / Weekly | Discovers freight rates exhibit distinct high/low volatility regimes | Descriptive econometric model; does not generate operational charter timing actions | **Actionable Timing Engine:** Translate volatility regime shifts into risk-calibrated `ENTER_NOW` / `DEFER` decisions. |
| **Chen et al. (MKG-GNN, 2026)** *Ocean Engineering* | Heterogeneous AIS data, port graphs | Ship speed and port congestion | Daily / Hourly | Graph convolutions capture spatial connectivity across ports | Requires high-frequency terrestrial/satellite AIS; does not model global freight forward curves | **Multi-Modal Macro-to-Voyage Coupling:** Link macro commodity demand with voyage-specific cost pressures. |
| **Romano & Candès (CQR, 2019)** *NeurIPS* | Tabular / continuous features | Any regression target $Y$ | Point prediction | Finite-sample distribution-free coverage guarantee | Generic ML method; never applied to maritime shipping chartering cycles | **Conformal Maritime Uncertainty:** Implement strict Conformalized Quantile Regression with formal coverage guarantees. |
| **Guo et al. (2026)** *Transp. Res. Part E* | Voyage route, speed, fuel prices, emissions | Voyage cost & GHG emissions | Voyage level | Multi-objective optimization under environmental regulations | Assumes deterministic freight rates at decision time | **Uncertainty-Aware Chartering:** Integrate freight distribution into Harit Sagar green voyage landed cost. |

---

## 2. Identified Research Gaps

1. **Gap 1: The Single Global Model Fallacy in Freight Forecasting**  
   Existing maritime AI literature fits single global models (ARIMA, LSTM, generic XGBoost) across all historical periods. However, dry bulk shipping is structurally asymmetric: 80% of days are quiet, mean-reverting regimes where naive persistence wins, while 20% of days are violent supply-tightening surges where naive models fail catastrophically.
   
2. **Gap 2: Point Predictions vs Decision-Making Under Uncertainty**  
   Commercial chartering managers do not need a single point forecast ($\hat{y} = \$15.42$). They need to know the *probability of adverse market spikes* ($P(\Delta y > +5\%)$) and the *confidence interval* to decide whether to lock in a contract now or wait.

3. **Gap 3: Disconnect Between Forecasting Accuracy and Economic Utility**  
   Existing papers optimize solely for MAE/RMSE. A model with 5% lower MAE that predicts flat prices during a 30% rate surge causes massive financial loss for steel mills. A procurement model must optimize for *economic regret* and *directional precision*.
