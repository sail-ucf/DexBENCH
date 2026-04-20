import json
import re
import os


input_file = "cruxeval.jsonl"
output_dir = "formatted_cruxeval_programs"


os.makedirs(output_dir, exist_ok=True)


CONTROL_KEYWORDS = ["if", "elif", "else", "for", "while"]


STANDARD_LIBS = [
    "math", "datetime", "sys", "io", "unittest", "re", "random",
    "collections", "itertools", "heapq", "functools", "bisect",
    "statistics", "string", "operator"
]

def contains_control_flow(code: str) -> bool:
    """Return True if code contains at least one control-flow structure."""
    pattern = r"\b(" + "|".join(CONTROL_KEYWORDS) + r")\b"
    return bool(re.search(pattern, code))

def extract_function_name(code: str) -> str | None:
    """Extract the function name from a def line."""
    match = re.search(r"def\s+(\w+)\s*\(", code)
    return match.group(1) if match else None

def detect_imports(code: str) -> list[str]:
    """Detect which standard libs are used in the code."""
    used = []
    for lib in STANDARD_LIBS:
        if re.search(rf"\b{lib}\.", code):
            used.append(lib)

    if "unittest" not in used:
        used.append("unittest")
    return used

def build_test_line(func_name: str, input_str: str, output_str: str) -> str:
    """Construct a unittest-style assertion."""
    return f"unittest.TestCase().assertEqual({func_name}({input_str}), {output_str})"


with open(input_file, "r") as infile:
    count_kept = 0
    total = 0

    for line in infile:
        total += 1
        try:
            item = json.loads(line)
            code = item.get("code", "")
            input_str = item.get("input", "")
            output_str = item.get("output", "")
            sample_id = item.get("id", f"sample_{total}")


            if not contains_control_flow(code):
                continue

            func_name = extract_function_name(code)
            if not func_name:
                continue

            test_line = build_test_line(func_name, input_str, output_str)
            imports = detect_imports(code)
            import_block = "\n".join(f"import {lib}" for lib in sorted(imports))


            script_content = f"{import_block}\n\n{code}\n\n{test_line}\n"


            output_path = os.path.join(output_dir, f"{sample_id}.py")
            with open(output_path, "w") as outfile:
                outfile.write(script_content)

            count_kept += 1

        except Exception as e:
            print(f"Skipping malformed entry: {e}")

print(f"OK Processed {total} samples. Saved {count_kept} programs with loops/conditionals in '{output_dir}'.")
