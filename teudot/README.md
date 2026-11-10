# Teudot — document automation foundation

This directory is an isolated prototype on top of the upstream Hebrew OCR project. The original OCR package is unchanged.

## Scope
- Local OCR using the upstream ONNX Hebrew OCR engine.
- Configurable document-type keywords, number patterns, and output naming.
- **Dry run only:** emits OCR lines and a filename proposal as JSON; never moves, renames, or deletes source documents.
- Unrecognized or ambiguous documents require review.
- No Ollama, cloud AI, or telemetry.

## Setup
From repository root, with Python 3.11:

```bash
pip install -e .
pip install huggingface_hub
python -m teudot.cli /path/to/document.pdf --models /path/to/downloaded/models
python -m unittest discover -s teudot/tests
```

Download the required upstream ONNX models using the instructions in the repository root README. The models directory must contain the detector and recognizer expected by `HebrewOCR.word`.

## Important limitations
- This is **not** a working Windows EXE or complete background service.
- Rules are initial examples, not verified on user documents.
- OCR confidence, positional boxes, PDF page handling, vendor extraction, and safe automated file moves still need integration and testing.
- Do not commit client documents or personally identifying information to a public fork.
- Keep upstream LICENSE and NOTICE when distributing commercially.

## Next engineering steps
1. Add golden-document fixtures with redacted examples and manually verified expected results.
2. Benchmark OCR on Windows CPU and validate word bounding boxes.
3. Implement region-template teaching, anchored extraction, confidence thresholds and review queue.
4. Add background folder watcher, stable-file detection, idempotency, audit log, and undo.
5. Create UI with scanning overlays based on real OCR coordinates.
6. Build a portable Windows folder release using GitHub Actions and test on a clean machine.
