import json
from pathlib import Path

BASE = Path("chat_history")
BASE.mkdir(exist_ok=True)

def save_history(chat_id, prompt, initial, critiques, defenses, judge):
    path = BASE / f"{chat_id}.json"

    log = {
        "prompt": prompt,
        "initial": initial,
        "critiques": critiques,
        "defenses": defenses,
        "judge": judge
    }

    if path.exists():
        old = json.loads(path.read_text())
        old.append(log)
        path.write_text(json.dumps(old, indent=2))
    else:
        path.write_text(json.dumps([log], indent=2))
