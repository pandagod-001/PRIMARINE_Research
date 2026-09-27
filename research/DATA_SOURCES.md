# PRIMARINE Data Sources & Accessibility Audit

**Date:** 2026-09-24  
**Project:** PRIMARINE (SIH 2026 PS-26006)  
**Objective:** Document all potential data sources, accessibility status, authentication requirements, update frequency, and identify legitimate public proxies where proprietary data is gated.

---

## 1. Data Sources Prioritization & Audit Table

| Source Category | Source Name | Endpoint / Provider | Access Status | Authentication Required | Date Range / Frequency | Variables Captured | License / Limitations |
|---|---|---|---|---|---|---|---|
| **1. Freight Market (Actual Route Assessments)** | Baltic Exchange (BDI, BCI, BPI, BSI, C5/C3 route rates) | balticexchange.com | **ACCESS REQUIRED** (Paid / Commercial) | Yes (Paid Subscription / API Key) | Daily | Spot voyage assessments ($/tonne, $/day TC) | Proprietary, closed commercial API. Not accessible without institutional account. |
| **1. Freight Market (Actual Route Assessments)** | Platts / S&P Global Dry Freight Assessments (e.g., Australia–India Capesize) | spglobal.com/commodityinsights | **ACCESS REQUIRED** (Paid / Commercial) | Yes (Paid Subscription / Platts Dimensions Pro) | Daily | Coking coal freight rates (Hay Point to Paradip, $/t) | Proprietary closed commercial service. |
| **2. Public Freight Market Proxy** | **Breakwave Dry Bulk Shipping ETF (BDRY)** | Direct market feed / Yahoo Finance API (`BDRY`) | **ACTIVE & ACCESSIBLE** | No (Free / Open API) | 2018–Present / Daily | BDRY index price, volume, NAV (reflects near-dated Baltic Capesize, Panamax & Supramax freight futures contracts) | Public financial market proxy. Tracks underlying dry bulk freight forward curves directly. |
| **2. Public Freight Market Proxy** | **Baltic Dry Index (BDI Historical / Proxy Indices)** | Yahoo Finance / Investing.com / FRED | **ACTIVE & ACCESSIBLE** | No (Open Market Feeds) | Multi-year / Daily | Global Dry Bulk shipping rate sentiment & aggregate index | Standard public time-series data. |
| **3. Commodity Prices** | Thermal / Coking Coal Futures & Iron Ore Proxies | Yahoo Finance (`MTF=F` / `TIO=F` / Mining Proxies `BHP`, `RIO`, `VALE`) | **ACTIVE & ACCESSIBLE** | No | 2018–Present / Daily | Global seaborne bulk demand driver prices | Free market data. |
| **4. Economic & Macro Indicators** | US Dollar Index (`DX-Y.NYB`), USD/INR (`INR=X`), S&P Global Metals (`^SPGSCI`) | Yahoo Finance / Federal Reserve FRED | **ACTIVE & ACCESSIBLE** | No | 2018–Present / Daily | FX rates, global purchasing power, monetary tightening indices | Public open data. |
| **5. Fuel & Bunker Proxies** | Brent Crude Oil (`BZ=F`), WTI Crude (`CL=F`) | Yahoo Finance API | **ACTIVE & ACCESSIBLE** | No | 2018–Present / Daily | Global VLSFO / MGO marine fuel price proxy | Public commodity futures. |
| **6. Trade & Export Volumes** | UN Comtrade / World Bank / Port Authority Reports | comtradeapi.un.org / ipa.nic.in | **AVAILABLE (Periodic / Monthly)** | Free API Key / Public PDFs | Monthly / Annual | Aggregated coal/ore import volumes to Paradip/Vizag | Low frequency (monthly/quarterly lags), best for macro context. |
| **7. Weather & Marine Conditions** | Open-Meteo Marine Weather API / Copernicus Marine | open-meteo.com / marine.copernicus.eu | **ACTIVE & ACCESSIBLE** | No (Open Access) | Hourly / Daily (Global) | Significant wave height, wind speed, cyclone alerts | Open license for voyage estimation. |
| **8. AIS Vessel Tracking** | AISHub / Spire / MarineTraffic / VesselFinder | aishub.net / commercial APIs | **RESTRICTED / SIMULATED FEED** | Yes (Community / Paid) | Real-time | Vessel lat/lon, speed, heading, draught, destination | Live streaming requires hardware feeder or paid API. |

---

## 2. Target Selection and Explicit Proxy Notice

> [!IMPORTANT]
> ### MANDATORY DISCLOSURE FOR SIH EVALUATION:
> **PUBLIC PROXY — NOT THE PROPRIETARY ROUTE-SPECIFIC FREIGHT ASSESSMENT.**
>
> Commercial route assessments (such as Baltic C5 West Australia to Qingdao or Platts Hay Point to Paradip $/tonne) are proprietary financial benchmarks protected by paid commercial licenses.
> 
> For this reproducible empirical proof of concept, PRIMARINE utilizes the **Breakwave Dry Bulk Shipping Index (BDRY)** as our primary forecasting target. BDRY is an SEC-regulated exchange-traded instrument whose underlying holdings consist exclusively of **near-dated Baltic Capesize (50%), Panamax (40%), and Supramax (10%) freight futures contracts**. It represents the most accurate, continuous, real-world, un-fabricated public daily signal of global dry bulk freight charter market levels and volatility.

---

## 3. Explanatory Variables Matrix

The multi-modal feature matrix includes only genuine, accessible time-series data:

1. **Target:** `BDRY` (Dry Bulk Freight Futures Index Level)
2. **Marine Fuel / Bunker Proxy:** `BZ=F` (Brent Crude Futures, $/bbl)
3. **Seaborne Mineral / Mining Momentum:** `BHP` (BHP Group - Major Australian Coking Coal & Iron Ore Exporter)
4. **Global Dry Bulk Fleet Sentiment:** `VALE` (Vale S.A. - Major Global Bulk Shipper)
5. **Macro Purchasing Power & FX:** `DX-Y.NYB` (US Dollar Index) & `INR=X` (USD/INR Exchange Rate)
6. **Time & Seasonal Variables:** Month of year, Day of week, Rolling volatility (7d, 14d, 30d), Rolling Momentum, Exponential Moving Averages (EMA).
