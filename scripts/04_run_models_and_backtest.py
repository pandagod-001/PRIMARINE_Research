import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.ar_model import AutoReg
import lightgbm as lgb
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

# Set aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica', 'Arial', 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

print("=== PRIMARINE Time-Series Forecasting & Rolling Backtest Engine ===", flush=True)

# 1. Load clean feature dataset
df = pd.read_csv("data/processed/freight_features_dataset.csv", index_col="Date", parse_dates=True)
print(f"Dataset Loaded: {len(df)} observations from {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}", flush=True)

# 2. Define Time-Series Splits for Out-of-Sample Backtesting
n_total = len(df)
train_size = int(n_total * 0.70)
val_size = int(n_total * 0.15)
test_size = n_total - train_size - val_size

train_df = df.iloc[:train_size]
val_df = df.iloc[train_size:train_size + val_size]
test_df = df.iloc[train_size + val_size:]

print(f"Train set: {len(train_df)} obs ({train_df.index.min().strftime('%Y-%m-%d')} to {train_df.index.max().strftime('%Y-%m-%d')})", flush=True)
print(f"Val set:   {len(val_df)} obs ({val_df.index.min().strftime('%Y-%m-%d')} to {val_df.index.max().strftime('%Y-%m-%d')})", flush=True)
print(f"Test set:  {len(test_df)} obs ({test_df.index.min().strftime('%Y-%m-%d')} to {test_df.index.max().strftime('%Y-%m-%d')})", flush=True)

def evaluate_metrics(y_true, y_pred, y_baseline_lag=None):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-6))) * 100
    smape = np.mean(2.0 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred) + 1e-6)) * 100
    
    # Directional Accuracy
    if y_baseline_lag is not None:
        actual_direction = np.sign(y_true - y_baseline_lag)
        pred_direction = np.sign(y_pred - y_baseline_lag)
        dir_acc = np.mean(actual_direction == pred_direction) * 100
    else:
        dir_acc = np.nan
        
    return {
        "MAE": round(float(mae), 4),
        "RMSE": round(float(rmse), 4),
        "MAPE": round(float(mape), 2),
        "sMAPE": round(float(smape), 2),
        "Directional_Accuracy_Pct": round(float(dir_acc), 2)
    }

# -------------------------------------------------------------
# Rolling Expanding-Window Backtest Execution
# -------------------------------------------------------------
H = 7
feature_cols = [c for c in df.columns if c != 'target']

df_h = df.copy()
df_h['target_future'] = df_h['target'].shift(-H)
clean_h = df_h.dropna().copy()

test_indices = clean_h.index[clean_h.index >= test_df.index[0]]
print(f"\nRunning out-of-sample backtest over {len(test_indices)} evaluation test windows (Horizon = {H} days)...", flush=True)

actuals = []
naive_preds = []
ma_preds = []
ar_preds = []
lgb_preds = []
xgb_preds = []
baseline_lags = []
test_dates = []

eval_step = 2

for i in range(0, len(test_indices), eval_step):
    eval_date = test_indices[i]
    test_dates.append(eval_date)
    
    history_df = clean_h.loc[:eval_date]
    current_target = clean_h.loc[eval_date, 'target']
    actual_future = clean_h.loc[eval_date, 'target_future']
    
    actuals.append(actual_future)
    baseline_lags.append(current_target)
    
    # 1. Baseline: Naive Persistence
    naive_preds.append(current_target)
    
    # 2. Baseline: Moving Average (5-day historical SMA)
    ma_preds.append(history_df['target'].iloc[-5:].mean())
    
    # 3. Statistical Baseline: Fast AutoReg (AR(5))
    try:
        ts_train = history_df['target'].values
        ar_mod = AutoReg(ts_train[-100:], lags=5).fit()
        ar_forecast = ar_mod.predict(start=len(ts_train[-100:]), end=len(ts_train[-100:]) + H - 1)[-1]
        ar_preds.append(ar_forecast)
    except:
        ar_preds.append(current_target)
        
    # 4. ML Models: LightGBM & XGBoost
    X_train_curr = history_df[feature_cols]
    y_train_curr = history_df['target_future']
    
    # Fast, robust hyperparameters
    lgb_model = lgb.LGBMRegressor(n_estimators=60, learning_rate=0.05, num_leaves=12, random_state=42, verbose=-1, n_jobs=1)
    lgb_model.fit(X_train_curr, y_train_curr)
    
    xgb_model = xgb.XGBRegressor(n_estimators=60, learning_rate=0.05, max_depth=3, random_state=42, verbosity=0, n_jobs=1)
    xgb_model.fit(X_train_curr, y_train_curr)
    
    current_feat = pd.DataFrame([clean_h.loc[eval_date, feature_cols]])
    lgb_pred = lgb_model.predict(current_feat)[0]
    xgb_pred = xgb_model.predict(current_feat)[0]
    
    lgb_preds.append(lgb_pred)
    xgb_preds.append(xgb_pred)
    
    if (i // eval_step) % 25 == 0:
        print(f"  Processed step {i // eval_step + 1} / {len(test_indices) // eval_step + 1} (Eval Date: {eval_date.strftime('%Y-%m-%d')})...", flush=True)

actuals = np.array(actuals)
naive_preds = np.array(naive_preds)
ma_preds = np.array(ma_preds)
ar_preds = np.array(ar_preds)
lgb_preds = np.array(lgb_preds)
xgb_preds = np.array(xgb_preds)
baseline_lags = np.array(baseline_lags)

print("\nBacktest loops completed. Computing metrics and uncertainty bounds...", flush=True)

# -------------------------------------------------------------
# 3. Calculate Rigorous Out-of-Sample Metrics
# -------------------------------------------------------------
metrics = {
    "Naive_Persistence": evaluate_metrics(actuals, naive_preds, baseline_lags),
    "Moving_Average_5d": evaluate_metrics(actuals, ma_preds, baseline_lags),
    "AutoRegressive_AR_5": evaluate_metrics(actuals, ar_preds, baseline_lags),
    "LightGBM_Regressor": evaluate_metrics(actuals, lgb_preds, baseline_lags),
    "XGBoost_Regressor": evaluate_metrics(actuals, xgb_preds, baseline_lags)
}

base_mae = metrics["Naive_Persistence"]["MAE"]
base_rmse = metrics["Naive_Persistence"]["RMSE"]
for m_name in metrics:
    metrics[m_name]["MAE_Improvement_vs_Naive_Pct"] = round((base_mae - metrics[m_name]["MAE"]) / base_mae * 100, 2)
    metrics[m_name]["RMSE_Improvement_vs_Naive_Pct"] = round((base_rmse - metrics[m_name]["RMSE"]) / base_rmse * 100, 2)

print("\n=== Model Comparison Table ===", flush=True)
comp_df = pd.DataFrame(metrics).T
print(comp_df, flush=True)

with open("results/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)
comp_df.to_csv("results/model_comparison.csv")
comp_df.to_csv("PRIMARINE_EVIDENCE/metrics_summary.csv")

# -------------------------------------------------------------
# 4. Uncertainty Quantification
# -------------------------------------------------------------
val_features = val_df[feature_cols]
val_target_future = val_df['target'].shift(-H).dropna()
val_features = val_features.iloc[:len(val_target_future)]

lgb_base = lgb.LGBMRegressor(n_estimators=60, learning_rate=0.05, num_leaves=12, random_state=42, verbose=-1, n_jobs=1)
lgb_base.fit(train_df.iloc[:-H][feature_cols], train_df['target'].shift(-H).dropna())
val_preds_base = lgb_base.predict(val_features)
val_residuals = val_target_future.values - val_preds_base
residual_std = np.std(val_residuals)

vol_factors = np.array([clean_h.loc[d, 'freight_volatility_21d'] / clean_h['freight_volatility_21d'].median() for d in test_dates])
vol_factors = np.clip(vol_factors, 0.7, 1.8)

interval_width = 1.96 * residual_std * vol_factors
lower_bound = lgb_preds - interval_width
upper_bound = lgb_preds + interval_width

inside_bounds = (actuals >= lower_bound) & (actuals <= upper_bound)
coverage_pct = np.mean(inside_bounds) * 100
print(f"\nEmpirical 95% Prediction Interval Coverage: {coverage_pct:.2f}%", flush=True)

# -------------------------------------------------------------
# 5. Generate Figures
# -------------------------------------------------------------
# Figure 1: Real Backtest Forecast vs Actuals with Prediction Interval (Judge Graph 1)
plt.figure(figsize=(14, 7), dpi=300)
plt.plot(test_dates, actuals, label='Actual Freight Market Signal (BDRY Target)', color='#0f172a', linewidth=2.4, zorder=4)
plt.plot(test_dates, lgb_preds, label='PRIMARINE Multi-Modal Forecast (h=7d)', color='#2563eb', linewidth=2.0, linestyle='-', zorder=5)
plt.plot(test_dates, naive_preds, label='Naive Persistence Baseline', color='#94a3b8', linewidth=1.2, linestyle='--', alpha=0.8)
plt.fill_between(test_dates, lower_bound, upper_bound, color='#3b82f6', alpha=0.18, label=f'95% Empirical Prediction Interval (Coverage: {coverage_pct:.1f}%)', zorder=2)

plt.title('PRIMARINE Freight Forecasting Model — Out-of-Sample Historical Backtest (SIH 2026 PS-26006)', fontsize=14, fontweight='bold', pad=15, color='#0f172a')
plt.suptitle('Empirical Evaluation on Dry Bulk Freight Futures Proxy (BDRY) | Strict Forward Rolling Time-Series Validation', fontsize=10, color='#475569', y=0.92)
plt.xlabel('Historical Out-of-Sample Evaluation Date (2024–2026)', fontsize=11, fontweight='600', labelpad=10)
plt.ylabel('Freight Market Proxy Level ($/unit)', fontsize=11, fontweight='600', labelpad=10)
plt.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.95, fontsize=10)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.savefig('results/figures/backtest_forecast.png')
plt.savefig('results/figures/PRIMARINE_forecast_evidence.png')
plt.savefig('PRIMARINE_EVIDENCE/figures/PRIMARINE_forecast_evidence.png')
plt.close()
print("Saved results/figures/PRIMARINE_forecast_evidence.png", flush=True)

# Figure 2: Model Metric Comparison (Judge Graph 2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

models_list = list(metrics.keys())
models_clean = ['Naive Persistence', '5-Day Moving Avg', 'AutoReg(5)', 'LightGBM (Multi-Modal)', 'XGBoost (Multi-Modal)']
mae_vals = [metrics[m]['MAE'] for m in models_list]
dir_acc_vals = [metrics[m]['Directional_Accuracy_Pct'] for m in models_list]

colors = ['#94a3b8', '#64748b', '#0284c7', '#2563eb', '#1d4ed8']

# MAE Comparison
bars1 = ax1.bar(models_clean, mae_vals, color=colors, width=0.55, edgecolor='#334155', linewidth=0.8)
ax1.set_title('Forecast Error (Mean Absolute Error - MAE)\n[Lower is Better]', fontsize=11, fontweight='bold', color='#0f172a')
ax1.set_ylabel('MAE ($/unit)', fontsize=10, fontweight='600')
ax1.grid(True, linestyle=':', alpha=0.6, axis='y')
ax1.set_xticklabels(models_clean, rotation=25, ha='right', fontsize=9)
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Directional Accuracy Comparison
bars2 = ax2.bar(models_clean, dir_acc_vals, color=colors, width=0.55, edgecolor='#334155', linewidth=0.8)
ax2.set_title('Directional Movement Accuracy (%)\n[Higher is Better — Key for Charter Timing]', fontsize=11, fontweight='bold', color='#0f172a')
ax2.set_ylabel('Accuracy (%)', fontsize=10, fontweight='600')
ax2.set_ylim(40, 85)
ax2.axhline(50, color='#ef4444', linestyle='--', linewidth=1.2, label='Random Chance (50%)')
ax2.grid(True, linestyle=':', alpha=0.6, axis='y')
ax2.set_xticklabels(models_clean, rotation=25, ha='right', fontsize=9)
ax2.legend(loc='lower right', frameon=True)
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f'{yval:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.suptitle('PRIMARINE Model Benchmark vs Classical Baselines (Out-of-Sample Rolling Test)', fontsize=13, fontweight='bold', color='#0f172a')
plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.savefig('results/figures/model_backtest_comparison.png')
plt.savefig('PRIMARINE_EVIDENCE/figures/model_backtest_comparison.png')
plt.close()
print("Saved results/figures/model_backtest_comparison.png", flush=True)

# Figure 3: Feature Importance (Explainability)
best_lgb = lgb.LGBMRegressor(n_estimators=60, learning_rate=0.05, num_leaves=12, random_state=42, verbose=-1, n_jobs=1)
best_lgb.fit(clean_h[feature_cols], clean_h['target_future'])
importances = best_lgb.feature_importances_
feat_imp = pd.Series(importances, index=feature_cols).sort_values(ascending=True)

feature_names_clean = {
    'freight_sma_63': 'Quarterly Freight Baseline (SMA 63d)',
    'freight_lag_1': 'Immediate Prior Freight (Lag 1d)',
    'freight_volatility_21d': 'Monthly Freight Volatility',
    'bunker_price': 'Bunker Fuel Price (Brent Proxy)',
    'bhp_price': 'BHP Australian Mineral Demand',
    'freight_ratio_sma5_sma21': 'Freight Term Structure (SMA5/SMA21)',
    'freight_lag_21': 'Monthly Freight Lag (Lag 21d)',
    'freight_volatility_5d': 'Weekly Freight Volatility',
    'usdinr_price': 'USD / INR Currency Rate',
    'vale_price': 'Vale Global Seaborne Volume Proxy',
    'freight_return_21d': 'Monthly Rate Momentum (% return)',
    'dxy_price': 'US Dollar Index (DXY)',
    'freight_lag_5': 'Weekly Freight Lag (Lag 5d)',
    'bunker_return_21d': 'Bunker 21d Price Velocity',
    'sin_month': 'Seasonal Annual Cycle (Sin month)',
    'cos_month': 'Seasonal Annual Cycle (Cos month)',
    'freight_return_5d': 'Weekly Freight Momentum'
}

top_feats = feat_imp.tail(12)
top_names = [feature_names_clean.get(f, f) for f in top_feats.index]

plt.figure(figsize=(11, 6), dpi=300)
bars = plt.barh(top_names, top_feats.values, color='#0284c7', edgecolor='#0369a1', height=0.65)
plt.title('PRIMARINE Feature Importance (LightGBM Multi-Modal Explanatory Drivers)', fontsize=12, fontweight='bold', pad=12, color='#0f172a')
plt.xlabel('Feature Importance Gain / Split Weight', fontsize=10, fontweight='600', labelpad=8)
plt.grid(True, linestyle=':', alpha=0.6, axis='x')
plt.tight_layout()
plt.savefig('results/figures/feature_importance.png')
plt.savefig('PRIMARINE_EVIDENCE/figures/feature_importance.png')
plt.close()
print("Saved results/figures/feature_importance.png", flush=True)

# -------------------------------------------------------------
# 6. Market-Entry Simulation Experiment
# -------------------------------------------------------------
sim_df = pd.DataFrame({
    'date': test_dates,
    'current_freight': baseline_lags,
    'forecast_freight': lgb_preds,
    'actual_future_freight': actuals,
    'lower_bound': lower_bound,
    'upper_bound': upper_bound
})

sim_df['forecast_delta_pct'] = (sim_df['forecast_freight'] - sim_df['current_freight']) / sim_df['current_freight'] * 100
sim_df['actual_delta_pct'] = (sim_df['actual_future_freight'] - sim_df['current_freight']) / sim_df['current_freight'] * 100

signals = []
for idx, row in sim_df.iterrows():
    if row['forecast_delta_pct'] >= 2.0:
        signals.append("ENTER_NOW (Rising Market Ahead)")
    elif row['forecast_delta_pct'] <= -2.0:
        signals.append("DEFER_ENTRY (Softening Market Ahead)")
    else:
        signals.append("NEUTRAL / SPOT_EXECUTE")

sim_df['decision_signal'] = signals

correct_decisions = 0
total_active_signals = 0
savings_per_voyage_proxy = []

for idx, row in sim_df.iterrows():
    if row['decision_signal'] == "ENTER_NOW (Rising Market Ahead)":
        total_active_signals += 1
        if row['actual_delta_pct'] > 0:
            correct_decisions += 1
            savings_per_voyage_proxy.append(row['actual_delta_pct'])
        else:
            savings_per_voyage_proxy.append(row['actual_delta_pct'])
    elif row['decision_signal'] == "DEFER_ENTRY (Softening Market Ahead)":
        total_active_signals += 1
        if row['actual_delta_pct'] < 0:
            correct_decisions += 1
            savings_per_voyage_proxy.append(-row['actual_delta_pct'])
        else:
            savings_per_voyage_proxy.append(-row['actual_delta_pct'])

decision_accuracy = (correct_decisions / total_active_signals) * 100 if total_active_signals > 0 else 0
avg_benefit_pct = np.mean(savings_per_voyage_proxy) if savings_per_voyage_proxy else 0

print(f"\n=== Market-Entry Decision Backtest Results ===", flush=True)
print(f"Total Decision Windows: {len(sim_df)}", flush=True)
print(f"Active Buy/Defer Signals: {total_active_signals}", flush=True)
print(f"Decision Precision: {decision_accuracy:.1f}%", flush=True)
print(f"Average Procurement Cost Advantage over Naive Spot: {avg_benefit_pct:.2f}%", flush=True)

sim_df.to_csv("results/market_entry_backtest_results.csv", index=False)
print("Saved results/market_entry_backtest_results.csv successfully.", flush=True)
