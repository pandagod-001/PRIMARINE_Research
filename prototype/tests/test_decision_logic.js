import assert from 'assert';
import { calculateDecision } from '../logic/decisionEngine.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Robust config path resolution
const configPath = path.resolve(__dirname, '../config/research_config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

console.log("Running PRIMARINE Decision Logic Unit Tests...");

// Test Case 1: Low Width Scenario -> PROCEED
const lowWidthScenario = {
    cqr_lower_bound: 5.20,
    cqr_upper_bound: 9.60,
    forecast_rate: 7.10
};
const res1 = calculateDecision(lowWidthScenario, config);
assert.strictEqual(res1.interval_width, 4.40);
assert.strictEqual(res1.decision, "PROCEED");
assert.strictEqual(res1.uncertainty_level, "Low");
console.log("✓ Test Case 1 Passed: Low width correctly yields PROCEED");

// Test Case 2: Elevated Width Scenario -> DEFER
const highWidthScenario = {
    cqr_lower_bound: 4.80,
    cqr_upper_bound: 12.60,
    forecast_rate: 6.85
};
const res2 = calculateDecision(highWidthScenario, config);
assert.strictEqual(res2.interval_width, 7.80);
assert.strictEqual(res2.decision, "DEFER");
assert.strictEqual(res2.uncertainty_level, "Elevated");
console.log("✓ Test Case 2 Passed: High width correctly yields DEFER");

// Test Case 3: Invalid Bounds Check (Upper < Lower)
let threwError = false;
try {
    calculateDecision({ cqr_lower_bound: 8.0, cqr_upper_bound: 5.0, forecast_rate: 6.0 }, config);
} catch (e) {
    threwError = true;
}
assert.strictEqual(threwError, true);
console.log("✓ Test Case 3 Passed: Invalid bounds correctly rejected with error");

console.log("All Decision Logic Unit Tests Passed Successfully!");
