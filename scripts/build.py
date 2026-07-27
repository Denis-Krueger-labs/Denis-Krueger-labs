from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
for name in ("header.svg", "footer.svg"):
    path = ROOT / "assets" / name
    ET.parse(path)
    print(f"validated: {path}")

activity = ROOT / "assets" / "activity.svg"
if not activity.exists():
    print("note: preserve your existing assets/activity.svg and its generator")
