"""Run the upstream OCR engine and emit a JSON review proposal. No files are moved."""
import argparse
import json
from pathlib import Path
from .engine import classify

def main():
    parser = argparse.ArgumentParser(description="Teudot OCR dry-run")
    parser.add_argument("document", type=Path)
    parser.add_argument("--models", required=True, type=Path)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.example.json"))
    args = parser.parse_args()
    if not args.document.is_file():
        parser.error("document does not exist")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    from paddleocr_hebrew import HebrewOCR
    ocr = HebrewOCR.word(str(args.models))
    result = ocr.read(str(args.document))
    lines = [line.get("text", "") for line in result.get("lines", [])]
    proposal = classify(lines, config["rules"])
    print(json.dumps({"source": str(args.document), "ocr_lines": lines,
                      "proposal": proposal.__dict__}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
