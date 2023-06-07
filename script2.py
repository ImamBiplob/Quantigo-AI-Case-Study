import json
import glob
from pathlib import Path

data = {"combined_file": []}

files = glob.glob("./*.json")

for file in files:
    file = Path(file[2:]).read_text()
    data["combined_file"].append(json.loads(file))

data["combined_file"][0]["objects"][0]["classTitle"] = "car"
data["combined_file"][0]["objects"][1]["classTitle"] = "car"
data["combined_file"][1]["objects"][0]["classTitle"] = "number"

jsonString = json.dumps(data)
Path(f"./Combined File/combined_file.json").write_text(jsonString)
