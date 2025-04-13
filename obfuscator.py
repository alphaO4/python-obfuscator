import keyword
import builtins
import json
import random
import re
import argparse

# Word list for replacing identifiers and built-ins
WORDLIST = [
    "Banana", "Apple", "Pear", "Spoon", "Melon", "Frozen", "Derp", "Mozart", "Chad",
    "Falcon", "Tiger", "Laser", "Pixel", "Quartz", "Nimbus", "Echo", "Nova", "Frost",
    "Blizzard", "Drift", "Comet", "Razor", "Shadow", "Ranger", "Dune", "Flare"
]

# Python syntax keywords — we will NOT obfuscate these
RESERVED = set(keyword.kwlist)

def get_word_generator():
    used = set()
    index = 0
    while True:
        if index >= len(WORDLIST):
            word = random.choice(WORDLIST) + str(random.randint(0, 999))
        else:
            word = WORDLIST[index]
            index += 1
        while word in used:
            word += str(random.randint(0, 999))
        used.add(word)
        yield word

def obfuscate_code(input_file, output_file, mapping_file):
    with open(input_file, 'r') as f:
        code = f.read()

    # Match all identifiers
    all_identifiers = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code))

    # Obfuscate everything EXCEPT keywords (but include built-ins like print, len, etc.)
    identifiers_to_obfuscate = [word for word in all_identifiers if word not in RESERVED]

    word_gen = get_word_generator()
    mapping = {token: next(word_gen) for token in identifiers_to_obfuscate}

    # Apply the mapping
    sorted_tokens = sorted(mapping.keys(), key=lambda x: -len(x))
    obf_code = code
    for token in sorted_tokens:
        replacement = mapping[token]
        obf_code = re.sub(rf'\b{re.escape(token)}\b', replacement, obf_code)

    # Save mapping to external file
    with open(mapping_file, 'w') as f:
        json.dump(mapping, f, indent=2)

    # Inject runtime loader that loads the mapping and replaces back the identifiers
    runtime = f'''
# --- Obfuscated Python Script ---
import json
import re

with open("{mapping_file}", "r") as f:
    _mapping = json.load(f)

_code = \"\"\"{obf_code.replace('\"\"\"', '\\\"\\\"\\\"')}\"\"\"

for obf in sorted(_mapping.values(), key=lambda x: -len(x)):
    orig = [k for k, v in _mapping.items() if v == obf][0]
    _code = re.sub(rf'\\b{{re.escape(obf)}}\\b', orig, _code)

exec(_code, globals())
# --- End of Runtime ---
'''

    with open(output_file, 'w') as f:
        f.write(runtime)

    print(f"Obfuscation complete:\n- Output: {output_file}\n- Mapping: {mapping_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Obfuscate all Python identifiers and builtins (not keywords).")
    parser.add_argument("input", help="Input Python source file")
    parser.add_argument("-o", "--output", default="obfuscated.py", help="Obfuscated output file")
    parser.add_argument("-m", "--mapping", default="mapping.json", help="Mapping file to store identifier mapping")
    args = parser.parse_args()

    obfuscate_code(args.input, args.output, args.mapping)