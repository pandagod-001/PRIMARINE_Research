import os
import shutil
import zipfile

print("=== Assembling Clean PRIMARINE_IDEATION_EVIDENCE Package & Distribution ZIP ===", flush=True)

base_dir = "PRIMARINE_IDEATION_EVIDENCE"
os.makedirs(os.path.join(base_dir, "results"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "scripts"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "figures"), exist_ok=True)

# Copy Key Result Files
result_files = [
    "results/research/final_research_scorecard.csv",
    "results/research/turning_point_metrics.csv",
    "results/research/coverage_vs_width.csv",
    "results/research/decision_strategy_comparison.csv",
    "results/research/stgnn_scenario_results.csv",
    "results/research/stgnn_spatial_attenuation.csv",
    "results/research/stgnn_sanity_checks.csv",
    "results/research/STGNN_RESULTS.json",
    "results/research/STGNN_RESULTS.md"
]

for src in result_files:
    if os.path.exists(src):
        dst = os.path.join(base_dir, "results", os.path.basename(src))
        shutil.copy2(src, dst)
        print(f"Copied {src} -> {dst}")

# Copy Key Execution Scripts
script_files = [
    "scripts/01_data_ingestion.py",
    "scripts/02_feature_engineering.py",
    "scripts/07_research_strengthening_engine.py",
    "scripts/09_validation_strengthening_engine.py",
    "scripts/13_run_stgnn_extension.py"
]

for src in script_files:
    if os.path.exists(src):
        dst = os.path.join(base_dir, "scripts", os.path.basename(src))
        shutil.copy2(src, dst)
        print(f"Copied {src} -> {dst}")

# Copy Key Presentation Figures
figure_files = [
    "figures/ideation_evidence/01_PRIMARINE_system_architecture.png",
    "figures/ideation_evidence/02_point_forecast_reality.png",
    "figures/ideation_evidence/03_turning_point_f1.png",
    "figures/ideation_evidence/04_directional_accuracy.png",
    "figures/ideation_evidence/05_cqr_uncertainty.png",
    "figures/ideation_evidence/06_maritime_graph.png",
    "figures/ideation_evidence/07_stgnn_hop_propagation.png",
    "figures/ideation_evidence/08_stgnn_counterfactual.png",
    "figures/ideation_evidence/09_connected_vs_isolated.png",
    "figures/ideation_evidence/10_evidence_boundary.png",
    "figures/ideation_evidence/11_decision_intelligence.png",
    "figures/ideation_evidence/FIGURE_INDEX.md",
    "results/research/stgnn_propagation_scenario.png",
    "results/research/stgnn_counterfactual_comparison.png"
]

for src in figure_files:
    if os.path.exists(src):
        dst = os.path.join(base_dir, "figures", os.path.basename(src))
        shutil.copy2(src, dst)
        print(f"Copied {src} -> {dst}")

# Build ZIP
zip_name = "PRIMARINE_IDEATION_EVIDENCE_SIH2026.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, os.path.dirname(base_dir))
            zipf.write(full_path, rel_path)

zip_size_mb = os.path.getsize(zip_name) / (1024 * 1024)
print(f"\nSuccessfully created {zip_name} (Size: {zip_size_mb:.2f} MB)", flush=True)
