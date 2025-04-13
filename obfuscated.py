
# --- Obfuscated Python Script ---
import json
import re

with open("mapping.json", "r") as f:
    _mapping = json.load(f)

_code = """def Banana():
    Spoon("Apple Pear")

Banana()"""

for obf in sorted(_mapping.values(), key=lambda x: -len(x)):
    orig = [k for k, v in _mapping.items() if v == obf][0]
    _code = re.sub(rf'\b{re.escape(obf)}\b', orig, _code)

exec(_code, globals())
# --- End of Runtime ---
