from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
print(f"header ready: {ROOT / 'assets' / 'header.svg'}")
