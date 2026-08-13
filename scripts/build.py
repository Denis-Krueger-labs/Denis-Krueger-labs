from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

for relative_path in (
    "assets/header.svg",
    "assets/footer.svg",
    "assets/activity.svg",
    "assets/languages.svg",
):
    path = ROOT / relative_path
    if not path.exists():
        raise FileNotFoundError(f"required profile asset is missing: {relative_path}")
    ET.parse(path)
    print(f"validated: {relative_path}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for marker in ("<<<<<<<", "=======", ">>>>>>>"):
    if marker in readme:
        raise RuntimeError(f"README.md contains unresolved merge marker: {marker}")

print("validated: README.md")
