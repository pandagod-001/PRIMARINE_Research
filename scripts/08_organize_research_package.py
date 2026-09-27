import os
import shutil

src_files = [
    ("research/CURRENT_POC_AUDIT.md", "PRIMARINE_RESEARCH_STRENGTHENED/01_CURRENT_POC_AUDIT.md"),
    ("research/LITERATURE_REVIEW.md", "PRIMARINE_RESEARCH_STRENGTHENED/02_LITERATURE_REVIEW.md"),
    ("research/RESEARCH_GAP.md", "PRIMARINE_RESEARCH_STRENGTHENED/03_RESEARCH_GAP.md"),
    ("research/FINAL_RESEARCH_CONTRIBUTION.md", "PRIMARINE_RESEARCH_STRENGTHENED/06_FINAL_RESEARCH_CONTRIBUTION.md")
]

for src, dst in src_files:
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"Copied {src} -> {dst}")

print("PRIMARINE_RESEARCH_STRENGTHENED package organized successfully.")
