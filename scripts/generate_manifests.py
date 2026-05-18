import argparse, json
from pathlib import Path

DEFAULT_UNITS_DIR = Path(__file__).parent.parent / "units"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
DEFAULT_INTERVAL = 15000
DEFAULT_TRANSITION = 2000

parser = argparse.ArgumentParser(description="TEST")
parser.add_argument("--units-dir", default=DEFAULT_UNITS_DIR, type=Path)

if __name__ == "__main__":
    args = parser.parse_args()
    units_dir = args.units_dir
    for facility in units_dir.iterdir():
        for unit in facility.iterdir():

            wallpapers = unit / "wallpapers"
            if wallpapers.is_dir():
                images = sorted( [
                    f.name
                    for f in wallpapers.iterdir()
                    if f.suffix.lower() in SUPPORTED_EXTENSIONS
                ])

            manifest_path = unit / "images.json"
            if manifest_path.exists():
                with open(manifest_path) as f:
                    existing = json.load(f)
                interval = existing.get("interval", DEFAULT_INTERVAL)
                transition = existing.get("transition", DEFAULT_TRANSITION)
            else:
                interval = DEFAULT_INTERVAL
                transition = DEFAULT_TRANSITION

            manifest = {
                "images": images,
                "interval": interval,
                "transition": transition
            }

            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=2)

            print(f"    wrote {manifest_path.name} ({len(images)} images)")
            
            print(interval, transition)
