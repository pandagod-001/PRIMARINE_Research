/**
 * PRIMARINE Decision Engine Logic
 * Pure function: calculates interval width, compares against research threshold,
 * and derives decision state and explanations without hard-coded outputs.
 */

export function calculateDecision(scenario, config) {
    if (!scenario || typeof scenario !== 'object') {
        throw new Error("Invalid scenario data provided.");
    }

    const { cqr_lower_bound, cqr_upper_bound, forecast_rate } = scenario;

    if (cqr_lower_bound == null || cqr_upper_bound == null || forecast_rate == null) {
        throw new Error("Missing required bounds or forecast rate in scenario.");
    }

    if (cqr_upper_bound < cqr_lower_bound) {
        throw new Error("Invalid interval: Upper bound cannot be less than lower bound.");
    }

    const width = Number((cqr_upper_bound - cqr_lower_bound).toFixed(4));
    const threshold = config.calibration_parameters.abstention_threshold; // 5.9529

    // Derive uncertainty stratum
    let uncertaintyLevel = "Moderate";
    if (width <= config.uncertainty_strata.low_max_width) {
        uncertaintyLevel = "Low";
    } else if (width > threshold) {
        uncertaintyLevel = "Elevated";
    }

    // Gating Decision Rule
    let decision = "PROCEED";
    let explanation = config.explanation_templates.PROCEED;

    if (width > threshold) {
        decision = "DEFER";
        explanation = config.explanation_templates.DEFER;
    }

    return {
        forecast_rate: scenario.forecast_rate,
        lower_bound: scenario.cqr_lower_bound,
        upper_bound: scenario.cqr_upper_bound,
        interval_width: width,
        threshold: threshold,
        relative_width_ratio: Number((width / threshold).toFixed(2)),
        uncertainty_level: uncertaintyLevel,
        decision: decision,
        explanation: explanation,
        is_elevated: width > threshold
    };
}
