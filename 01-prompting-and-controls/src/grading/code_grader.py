import json
import ast
import re


def clean_markdown_code(param):
    text = param["output"]
    """Remove ```language and closing ```"""
    # Remove code block markers
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()
        # Skip lines that are just ``` or ```python, ```json, etc.
        if stripped.startswith("```") and (stripped == "```" or stripped[3:].isalpha()):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip("`").strip()


def validate_json(text):
    try:
        json.loads(text)
        return 10
    except Exception:
        return 0


def validate_python(text):
    try:
        ast.parse(text)
        return 10
    except Exception:
        return 0


def validate_regex(text):
    try:
        re.compile(text)
        return 10
    except Exception:
        return 0


def grade_syntax(output_item, test_case):
    fmt = test_case.get("format", "").lower()

    if fmt == "json":
        return validate_json(output_item)
    elif fmt == "python":
        return validate_python(output_item)
    elif fmt in ["regex", "regexp"]:
        return validate_regex(output_item)
    else:
        return 0


def grade_syntax_all(outputs_list, test_cases_list):
    """Grade all test cases"""
    results = []

    for i in range(len(test_cases_list)):
        test_case = test_cases_list[i]
        output_item = outputs_list[i]
        score = grade_syntax(clean_markdown_code(output_item), test_case)
        results.append(score)
    return results


with open("eval/outputs_v2.json", "r") as f:
    output = json.load(f)

with open("eval/tasks.json", "r") as f:
    test_case = json.load(f)

score = grade_syntax_all(output, test_case)
print(score)
