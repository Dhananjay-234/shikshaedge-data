# 📊 ShikshaEdge — Dataset Generation Pipeline

Scripts used to build the ShikshaEdge NCERT curriculum dataset —  
2,170 Q&A pairs in Hindi, Marathi, and English for fine-tuning Gemma 3.

Part of the [ShikshaEdge project](https://github.com/dhananjay-234/shikshaedge-app).

---

## Pipeline Overview
NCERT PDFs → Extract text → Generate Q&A pairs → Clean → JSONL dataset
---

## Scripts

| Script | What it does |
|--------|-------------|
| `download.py` | Downloads NCERT textbook ZIPs from ncert.nic.in |
| `extract.py` | Extracts text from PDFs using PyMuPDF |
| `generate_automation.py` | Generates Q&A pairs using Claude/Gemini API |
| `clean.py` | Removes low-quality pairs from the dataset |

---

## How to Run

### Step 1 — Download NCERT PDFs
```bash
pip install pymupdf
python download.py
```
Downloads Science and Math textbooks for Class 6–10 in English and Hindi.

### Step 2 — Extract text
```bash
python extract.py
```
Creates one `.txt` file per chapter in `extracted/`.

### Step 3 — Generate Q&A pairs
```bash
pip install anthropic  # or google-generativeai
python generate_automation.py
```
Generates 20 Q&A pairs per chunk — 7 Hindi, 7 English, 6 Marathi.
Each pair: `{"instruction": "...", "input": "", "response": "..."}`

### Step 4 — Clean the dataset
```bash
python clean.py
```
Removes pairs with generic instructions, too-short responses, or OCR artifacts.

---

## Output Format

JSONL file — one JSON object per line:
```json
{"instruction": "प्रकाश संश्लेषण क्या है?", "input": "", "response": "प्रकाश संश्लेषण वह प्रक्रिया है..."}
{"instruction": "What is the Fundamental Theorem of Arithmetic?", "input": "", "response": "The Fundamental Theorem states..."}
{"instruction": "त्रिकोणाचे प्रकार सांगा", "input": "", "response": "त्रिकोणाचे तीन प्रकार आहेत..."}
```

---

## Dataset Stats

| Metric | Value |
|--------|-------|
| Total pairs | 2,170 |
| English pairs | ~35% |
| Hindi pairs | ~35% |
| Marathi pairs | ~30% |
| Source | NCERT Class 6–10 Science & Math |
| Format | JSONL |

---

## Published Dataset

Final dataset available on Kaggle:  
[ShikshaEdge NCERT Curriculum Dataset](https://www.kaggle.com/datasets/dhananjayyyyyy/shikshaedge-ncert-curriculum-dataset)

---

## License

CC BY 4.0 — derived from NCERT textbooks (public domain in India).
