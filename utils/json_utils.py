"""
Safe JSON parsing utilities used by every stage.
"""
import json
import re

def safe_parse(raw: str) -> dict:
    """
    Parse JSON from LLM output.
    Handles: markdown fences, leading text, trailing text.
    Raises: ValueError with detail on failure.
    """
    # 1. Strip markdown fences
    raw = raw.strip()
    if raw.startswith("```"):
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
        if match:
            raw = match.group(1).strip()

    # 2. Find first { or [ and last } or ]
    start = next((i for i, c in enumerate(raw) if c in "{["), None)
    end_curly = raw.rfind("}")
    end_bracket = raw.rfind("]")
    end = max(end_curly, end_bracket)

    if start is None or end == -1:
        raise ValueError(f"No JSON object found in output. Raw (first 300): {raw[:300]}")

    raw = raw[start:end+1]

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON decode error: {e}. Raw (first 300): {raw[:300]}")
