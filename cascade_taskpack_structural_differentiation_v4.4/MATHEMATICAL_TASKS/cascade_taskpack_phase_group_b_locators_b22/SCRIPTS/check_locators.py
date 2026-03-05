
import json, sys, pathlib

path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text())

missing = []

for dep in data.get("dependency_table", []):
    if dep.get("dep_id", "").startswith("DEP.P1"):
        if not dep.get("locator"):
            missing.append(dep["dep_id"])

if missing:
    print("Missing locators:", missing)
    exit(1)

print("All Paper‑1 locators present.")
