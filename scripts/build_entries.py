"""Regenerate picker metadata for the single BSG skill."""
import json
from pathlib import Path

def build(root):
    folder = root / "bsg" / "agents"
    folder.mkdir(parents=True, exist_ok=True)
    values = {"display_name": "BSG", "short_description": "Shape ideas and coordinate delivery with BSG", "default_prompt": "Use $bsg to continue my project with BSG."}
    (folder / "openai.yaml").write_text("interface:\n" + "".join(f"  {key}: {json.dumps(value)}\n" for key, value in values.items()), encoding="utf-8")

if __name__ == "__main__":
    build(Path(__file__).resolve().parents[1] / "skills")
