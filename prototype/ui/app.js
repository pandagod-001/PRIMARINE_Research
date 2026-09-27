import { calculateDecision } from '../logic/decisionEngine.js';

let researchConfig = null;
let researchScenarios = [];
let currentScenario = null;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Resolve paths correctly whether served from / or /ui/
        const configPath = window.location.pathname.includes('/ui/') ? '../config/research_config.json' : 'config/research_config.json';
        const scenariosPath = window.location.pathname.includes('/ui/') ? '../data/research_scenarios.json' : 'data/research_scenarios.json';

        const configRes = await fetch(configPath);
        researchConfig = await configRes.json();

        const scenariosRes = await fetch(scenariosPath);
        researchScenarios = await scenariosRes.json();

        initUI();
    } catch (err) {
        console.error("Failed to load prototype data:", err);
        document.getElementById('val-explanation').textContent = "Research data unavailable for this scenario.";
    }
});

function initUI() {
    const select = document.getElementById('scenario-select');
    select.innerHTML = '';

    researchScenarios.forEach((scen, idx) => {
        const opt = document.createElement('option');
        opt.value = idx;
        opt.textContent = `${scen.corridor} (${scen.date})`;
        select.appendChild(opt);
    });

    select.addEventListener('change', (e) => {
        const idx = parseInt(e.target.value, 10);
        updateScenario(researchScenarios[idx]);
    });

    // Modal controls
    const btnWhy = document.getElementById('btn-why');
    const modal = document.getElementById('modal-why');
    const btnClose = document.getElementById('btn-close-modal');

    btnWhy.addEventListener('click', () => {
        modal.classList.remove('hidden');
    });

    btnClose.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });

    if (researchScenarios.length > 0) {
        updateScenario(researchScenarios[0]);
    }
}

function updateScenario(scenario) {
    currentScenario = scenario;
    
    // Pure calculation via decision engine
    const result = calculateDecision(scenario, researchConfig);

    // Update UI elements
    document.getElementById('val-forecast').textContent = `$${result.forecast_rate.toFixed(2)} / MT`;
    document.getElementById('val-interval').textContent = `$${result.lower_bound.toFixed(2)} — $${result.upper_bound.toFixed(2)}`;
    
    const uncEl = document.getElementById('val-uncertainty');
    uncEl.textContent = result.uncertainty_level;
    uncEl.className = `metric-pill ${result.uncertainty_level.toLowerCase()}`;

    const decEl = document.getElementById('val-decision');
    decEl.textContent = result.decision;
    decEl.className = `decision-status ${result.decision.toLowerCase()}`;

    document.getElementById('val-explanation').textContent = result.explanation;

    // Update modal explanation
    const modalText = document.getElementById('modal-dynamic-text');
    if (result.is_elevated) {
        modalText.innerHTML = `The forecast interval (<strong>W = ${result.interval_width.toFixed(2)}</strong>) is <strong>above</strong> the pre-calibrated uncertainty threshold (&tau; = ${result.threshold.toFixed(4)}).`;
    } else {
        modalText.innerHTML = `The forecast interval (<strong>W = ${result.interval_width.toFixed(2)}</strong>) is <strong>below</strong> the pre-calibrated uncertainty threshold (&tau; = ${result.threshold.toFixed(4)}).`;
    }
}
