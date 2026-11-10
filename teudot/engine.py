"""Conservative rule-based extraction from OCR lines. No invented values."""
import re
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Match:
    rule_id: str | None
    label: str | None
    number: str | None
    filename: str | None
    review: bool
    reason: str

def classify(lines, rules):
    text = "\n".join(lines)
    candidates = []
    for rule in rules:
        hits = sum(1 for word in rule.get("keywords", []) if word in text)
        if hits:
            candidates.append((hits, rule))
    if not candidates:
        return Match(None, None, None, None, True, "no matching rule")
    candidates.sort(key=lambda item: item[0], reverse=True)
    if len(candidates) > 1 and candidates[0][0] == candidates[1][0]:
        return Match(None, None, None, None, True, "ambiguous document type")
    rule = candidates[0][1]
    pattern = rule.get("number_pattern")
    if not pattern:
        return Match(rule["id"], rule["label"], None, None, True, "number pattern missing")
    try:
        found = re.findall(pattern, text)
    except re.error:
        return Match(rule["id"], rule["label"], None, None, True, "invalid number pattern")
    numbers = sorted(set(v if isinstance(v, str) else v[0] for v in found))
    if len(numbers) != 1:
        return Match(rule["id"], rule["label"], None, None, True, "number missing or ambiguous")
    number = numbers[0]
    safe_number = re.sub(r"[^0-9A-Za-z_-]", "-", number).strip("-")
    safe_type = re.sub(r'[<>:"/\\|?*]', "_", rule["label"]).strip(". ")
    template = rule.get("filename", "{type}_{number}.pdf")
    if set(re.findall(r"{([^{}]+)}", template)) - {"type", "number"}:
        return Match(rule["id"], rule["label"], number, None, True, "unsupported filename placeholder")
    filename = template.replace("{type}", safe_type).replace("{number}", safe_number)
    if Path(filename).name != filename or not filename.lower().endswith(".pdf"):
        return Match(rule["id"], rule["label"], number, None, True, "unsafe filename template")
    return Match(rule["id"], rule["label"], number, filename, False, "matched")
