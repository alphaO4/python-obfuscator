# Python Obfuscator

This tool obfuscates your Python code by replacing all **identifiers** (variables, functions, classes, and built-in functions like `print`, `len`, etc.) with randomly chosen **real English words**.

The result is a completely unreadable version of your code — but it still runs normally **as long as the mapping file is present**.

## Features

- Obfuscates all non-keyword identifiers (including built-ins like `print`)
- Leaves Python syntax and operators untouched
- Outputs a single `.py` file that runs without any external dependencies
- Uses a `mapping.json` file to deobfuscate code at runtime
- Easy to use from the command line

---

## How It Works

### Example

**Original:**
```python
def greet(name):
    print("Hello", name)

greet("world")
```

**Obfuscated:**
```python
# --- Obfuscated Python Script ---
import json
import re

with open("mapping.json", "r") as f:
    _mapping = json.load(f)

_code = """Banana Apple(Pear):
    Nova("Hello", Pear)

Apple("world")
"""

for obf in sorted(_mapping.values(), key=lambda x: -len(x)):
    orig = [k for k, v in _mapping.items() if v == obf][0]
    _code = re.sub(rf'\b{re.escape(obf)}\b', orig, _code)

exec(_code, globals())
```

**mapping.json:**
```json
{
  "greet": "Apple",
  "name": "Pear",
  "print": "Nova"
}
```

---

## Installation

Clone the repo or just download `obfuscate.py`.

```bash
git clone https://github.com/yourname/python-obfuscator.git
cd python-obfuscator
```

---

## Usage

### Step 1: Obfuscate your code

```bash
python obfuscate.py original.py -o obfuscated.py -m mapping.json
```

- `original.py`: your source code
- `obfuscated.py`: output Python file with obfuscated identifiers
- `mapping.json`: mapping used to restore original names at runtime

### Step 2: Run the obfuscated file

```bash
python obfuscated.py
```

> **Important:** `mapping.json` must be present at runtime for the code to work!

---

## Why This Works

The obfuscated code is stored in a raw string and isn’t executed until the runtime logic:
- Loads the mapping
- Restores all obfuscated names
- Runs the restored code using `exec()`

---

## Security Notes

This isn’t intended to provide bulletproof security. It’s great for:
- Obscuring logic in open source projects
- Teaching about code transformation and execution
- Light code protection

Want stronger protection? Ask about:
- String obfuscation
- AST-level rewriting
- Control flow flattening
- Mapping encryption

---

## License

This project is licensed under the **GNU General Public License v3.0**.

You are free to use, modify, and redistribute the code under the terms of the license. See the [`LICENSE`](LICENSE) file for full details.

> TL;DR: You can use and modify this freely, but you must preserve the same license in derivative works.