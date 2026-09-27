import shutil
import os

os.makedirs("PRIMARINE_EVIDENCE", exist_ok=True)
if os.path.exists("DATA_SOURCES.md"):
    shutil.copy("DATA_SOURCES.md", "PRIMARINE_EVIDENCE/data_sources.md")
    print("Copied DATA_SOURCES.md to PRIMARINE_EVIDENCE/data_sources.md")
