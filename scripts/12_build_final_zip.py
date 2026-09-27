import os
import shutil
import zipfile

print("=== Assembling Clean PRIMARINE_FINAL Package and Creating ZIP ===")

base_dir = "PRIMARINE_FINAL"
if os.path.exists(base_dir):
    shutil.rmtree(base_dir)
os.makedirs(base_dir, exist_ok=True)

# Copy core clean folders and files
folders_to_copy = [
    ("data", os.path.join(base_dir, "data")),
    ("scripts", os.path.join(base_dir, "scripts")),
    ("results", os.path.join(base_dir, "results")),
    ("research", os.path.join(base_dir, "research")),
    ("PRIMARINE_RESEARCH_STRENGTHENED", os.path.join(base_dir, "PRIMARINE_RESEARCH_STRENGTHENED")),
    ("PRIMARINE_EVIDENCE", os.path.join(base_dir, "PRIMARINE_EVIDENCE"))
]

for src, dst in folders_to_copy:
    if os.path.exists(src):
        shutil.copytree(src, dst)
        print(f"Copied folder {src} -> {dst}")

files_to_copy = [
    "FINAL_PRIMARINE_README.md",
    "FINAL_FREEZE_CHECK.md",
    "PROJECT_STATUS.md",
    "DATA_SOURCES.md"
]

for f in files_to_copy:
    if os.path.exists(f):
        shutil.copy(f, os.path.join(base_dir, f))
        print(f"Copied file {f} -> {os.path.join(base_dir, f)}")

# Create ZIP archive
zip_name = "PRIMARINE_FINAL_SIH2026.zip"
if os.path.exists(zip_name):
    os.remove(zip_name)

with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, os.path.dirname(base_dir))
            zipf.write(file_path, arcname)

print(f"\nSuccessfully created {zip_name} (Size: {os.path.getsize(zip_name) / (1024*1024):.2f} MB)")
