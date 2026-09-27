// PRIMARINE Research Prototype Client Controller
// Sourced strictly from research/decision_boundary/decision_boundary_analysis.csv

const PRE_CALIBRATED_THRESHOLD_TAU = 5.9529; // 1.35 * Validation Median Width (4.4096)

// Pre-defined Controlled Demonstration Scenarios
const CONTROLLED_SCENARIOS = [
    {
        name: "Case 1: Low Uncertainty Width (Proceed / Enter Recommendation)",
        scenario_idx: "DEMO-01",
        date: "2024-03-15 (Illustrative Low-Width Case)",
        current_rate_B: 6.50,
        forecast_C: 7.10,
        cqr_lower_L: 5.20,
        cqr_upper_U: 9.60,
        interval_width_W: 4.40, // <= tau
        actual_future: 7.05,
        false_breakout: 0,
        timing_error: 0,
        decision_state: "LOWER_WIDTH_REGIME"
    },
    {
        name: "Case 2: Elevated Uncertainty Width (Abstain / Defer Recommendation)",
        scenario_idx: "DEMO-02",
        date: "2024-06-20 (Illustrative High-Width False Breakout)",
        current_rate_B: 6.20,
        forecast_C: 6.85,
        cqr_lower_L: 4.80,
        cqr_upper_U: 12.60,
        interval_width_W: 7.80, // > tau
        actual_future: 5.40, // Price dropped -> False breakout
        false_breakout: 1,
        timing_error: 1,
        decision_state: "ELEVATED_WIDTH_REGIME"
    },
    {
        name: "Case 3: Boundary-Crossing Demonstration (Negative Control)",
        scenario_idx: "DEMO-03",
        date: "2024-08-10 (Degenerate Boundary Crossing Observation)",
        current_rate_B: 5.80,
        forecast_C: 6.10,
        cqr_lower_L: 5.10,
        cqr_upper_U: 11.90,
        interval_width_W: 6.80,
        actual_future: 5.30,
        false_breakout: 1,
        timing_error: 1,
        decision_state: "BOUNDARY_CROSSING"
    },
    {
        name: "Case 4: Directional Sign Error Disconnect",
        scenario_idx: "DEMO-04",
        date: "2024-11-05 (Sign Error vs Conformal Spread)",
        current_rate_B: 5.90,
        forecast_C: 6.40,
        cqr_lower_L: 5.10,
        cqr_upper_U: 10.80,
        interval_width_W: 5.70,
        actual_future: 5.75,
        false_breakout: 1,
        timing_error: 1,
        decision_state: "DIRECTIONAL_DISCONNECT"
    }
];

let currentMode = "historical"; // 'historical' | 'scenarios'
let currentIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
    initUI();
    loadObservations();
    renderCurrentObservation();
});

function initUI() {
    const btnHist = document.getElementById("btn-historical");
    const btnScen = document.getElementById("btn-scenarios");
    const select = document.getElementById("scenario-select");
    const btnPrev = document.getElementById("btn-prev");
    const btnNext = document.getElementById("btn-next");

    btnHist.addEventListener("click", () => {
        currentMode = "historical";
        btnHist.classList.add("active");
        btnScen.classList.remove("active");
        currentIndex = 0;
        loadObservations();
        renderCurrentObservation();
    });

    btnScen.addEventListener("click", () => {
        currentMode = "scenarios";
        btnScen.classList.add("active");
        btnHist.classList.remove("active");
        currentIndex = 0;
        loadObservations();
        renderCurrentObservation();
    });

    select.addEventListener("change", (e) => {
        currentIndex = parseInt(e.target.value, 10);
        renderCurrentObservation();
    });

    btnPrev.addEventListener("click", () => {
        const dataset = getActiveDataset();
        if (currentIndex > 0) {
            currentIndex--;
            select.value = currentIndex;
            renderCurrentObservation();
        }
    });

    btnNext.addEventListener("click", () => {
        const dataset = getActiveDataset();
        if (currentIndex < dataset.length - 1) {
            currentIndex++;
            select.value = currentIndex;
            renderCurrentObservation();
        }
    });
}

function getActiveDataset() {
    return currentMode === "historical" ? RESEARCH_DATA : CONTROLLED_SCENARIOS;
}

function loadObservations() {
    const select = document.getElementById("scenario-select");
    select.innerHTML = "";
    const dataset = getActiveDataset();

    dataset.forEach((item, idx) => {
        const opt = document.createElement("option");
        opt.value = idx;
        if (currentMode === "historical") {
            const fbTag = item.false_breakout == 1 ? " [False Breakout]" : "";
            const wTag = ` (W=${parseFloat(item.interval_width_W).toFixed(2)})`;
            opt.textContent = `Idx ${item.scenario_idx}: ${item.date} - Spot: $${parseFloat(item.current_rate_B).toFixed(2)}${wTag}${fbTag}`;
        } else {
            opt.textContent = item.name;
        }
        select.appendChild(opt);
    });

    select.value = currentIndex;
}

function renderCurrentObservation() {
    const dataset = getActiveDataset();
    const obs = dataset[currentIndex];
    if (!obs) return;

    const spot = parseFloat(obs.current_rate_B);
    const forecast = parseFloat(obs.forecast_C);
    const lower = parseFloat(obs.cqr_lower_L);
    const upper = parseFloat(obs.cqr_upper_U);
    const width = parseFloat(obs.interval_width_W);
    const actual = parseFloat(obs.actual_future);
    const isFalseBreakout = parseInt(obs.false_breakout, 10) === 1;
    const isTimingError = parseInt(obs.timing_error, 10) === 1;

    // Update Metric Bar
    document.getElementById("m-spot").textContent = `$${spot.toFixed(2)}`;
    document.getElementById("m-forecast").textContent = `$${forecast.toFixed(2)}`;
    document.getElementById("m-bounds").textContent = `[$${lower.toFixed(2)}, $${upper.toFixed(2)}]`;
    document.getElementById("m-width").textContent = width.toFixed(4);

    // Decision Logic
    const isElevated = width > PRE_CALIBRATED_THRESHOLD_TAU;
    const regimeBadge = document.getElementById("regime-badge");
    const decisionCard = document.getElementById("decision-card");
    const decisionTitle = document.getElementById("decision-title");
    const decisionReason = document.getElementById("decision-reason");
    const outcomeText = document.getElementById("outcome-text");

    if (isElevated) {
        regimeBadge.textContent = "ELEVATED WIDTH REGIME (W > \u03c4)";
        regimeBadge.className = "regime-badge elevated";
        decisionCard.className = "card decision-card abstain";
        decisionTitle.textContent = "ABSTAIN / DEFER";
        decisionReason.innerHTML = `Conformal interval width (<strong>W = ${width.toFixed(4)}</strong>) exceeds the pre-calibrated validation threshold (&tau; = <strong>${PRE_CALIBRATED_THRESHOLD_TAU.toFixed(4)}</strong>).`;
    } else {
        regimeBadge.textContent = "LOWER WIDTH REGIME (W \u2264 \u03c4)";
        regimeBadge.className = "regime-badge lower";
        decisionCard.className = "card decision-card enter";
        decisionTitle.textContent = "PROCEED / ENTER";
        decisionReason.innerHTML = `Conformal interval width (<strong>W = ${width.toFixed(4)}</strong>) is within the pre-calibrated validation threshold (&tau; = <strong>${PRE_CALIBRATED_THRESHOLD_TAU.toFixed(4)}</strong>).`;
    }

    const fbLabel = isFalseBreakout ? "<strong style='color:#ef4444;'>YES (False Breakout)</strong>" : "<strong style='color:#10b981;'>NO</strong>";
    const errLabel = isTimingError ? "<strong style='color:#f59e0b;'>YES</strong>" : "<strong style='color:#10b981;'>NO</strong>";
    outcomeText.innerHTML = `Actual Future Rate: <strong>$${actual.toFixed(2)}/MT</strong> | Forced Error: ${errLabel} | False Breakout: ${fbLabel}`;

    // Render Canvas Chart
    drawForecastChart(spot, forecast, lower, upper, actual, width, isElevated);
}

function drawForecastChart(spot, forecast, lower, upper, actual, width, isElevated) {
    const canvas = document.getElementById("forecast-canvas");
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;

    ctx.clearRect(0, 0, w, h);

    const padLeft = 70;
    const padRight = 50;
    const padTop = 30;
    const padBottom = 40;

    const plotW = w - padLeft - padRight;
    const plotH = h - padTop - padBottom;

    // Y-scale range
    const minY = Math.min(spot, forecast, lower, actual) - 0.8;
    const maxY = Math.max(spot, forecast, upper, actual) + 0.8;

    const getY = (val) => padTop + plotH - ((val - minY) / (maxY - minY)) * plotH;

    // Grid lines
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    const steps = 5;
    for (let i = 0; i <= steps; i++) {
        const val = minY + (i / steps) * (maxY - minY);
        const y = getY(val);
        ctx.beginPath();
        ctx.moveTo(padLeft, y);
        ctx.lineTo(w - padRight, y);
        ctx.stroke();

        ctx.fillStyle = "#64748b";
        ctx.font = "11px 'JetBrains Mono'";
        ctx.textAlign = "right";
        ctx.fillText(`$${val.toFixed(1)}`, padLeft - 10, y + 4);
    }

    // X-coordinates
    const xSpot = padLeft + plotW * 0.2;
    const xForecast = padLeft + plotW * 0.55;
    const xActual = padLeft + plotW * 0.85;

    // X-labels
    ctx.fillStyle = "#94a3b8";
    ctx.font = "12px 'Inter'";
    ctx.textAlign = "center";
    ctx.fillText("Day t (Spot)", xSpot, h - 15);
    ctx.fillText("Day t+7 (Forecast & Bounds)", xForecast, h - 15);
    ctx.fillText("Day t+7 (Observed)", xActual, h - 15);

    // 1. Draw Conformal Band (Interval)
    const yLower = getY(lower);
    const yUpper = getY(upper);
    const bandW = 60;

    ctx.fillStyle = isElevated ? "rgba(239, 68, 68, 0.15)" : "rgba(59, 130, 246, 0.15)";
    ctx.strokeStyle = isElevated ? "rgba(239, 68, 68, 0.6)" : "rgba(59, 130, 246, 0.6)";
    ctx.lineWidth = 2;

    ctx.fillRect(xForecast - bandW / 2, yUpper, bandW, yLower - yUpper);
    ctx.strokeRect(xForecast - bandW / 2, yUpper, bandW, yLower - yUpper);

    // Width label
    ctx.fillStyle = isElevated ? "#fca5a5" : "#93c5fd";
    ctx.font = "11px 'JetBrains Mono'";
    ctx.textAlign = "left";
    ctx.fillText(`Width W = ${width.toFixed(2)}`, xForecast + bandW / 2 + 10, (yLower + yUpper) / 2);

    // 2. Trajectory Lines
    ctx.strokeStyle = "#475569";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(xSpot, getY(spot));
    ctx.lineTo(xForecast, getY(forecast));
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(xSpot, getY(spot));
    ctx.lineTo(xActual, getY(actual));
    ctx.stroke();
    ctx.setLineDash([]);

    // 3. Draw Points
    // Spot Point
    drawCircle(ctx, xSpot, getY(spot), 6, "#94a3b8", "#0f172a");
    // Forecast Point
    drawCircle(ctx, xForecast, getY(forecast), 7, "#3b82f6", "#0f172a");
    // Conformal Bound Caps
    drawCircle(ctx, xForecast, yUpper, 4, isElevated ? "#ef4444" : "#3b82f6", "#0f172a");
    drawCircle(ctx, xForecast, yLower, 4, isElevated ? "#ef4444" : "#3b82f6", "#0f172a");
    // Observed Actual Point
    drawCircle(ctx, xActual, getY(actual), 6, "#10b981", "#0f172a");
}

function drawCircle(ctx, x, y, r, fill, stroke) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = fill;
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = stroke;
    ctx.stroke();
}
