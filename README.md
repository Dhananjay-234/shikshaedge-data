ShikshaEdge — NCERT Dataset Extraction Pipeline

ShikshaEdge is a data extraction and dataset generation pipeline built for converting NCERT textbooks into multilingual AI training datasets. The project extracts text from NCERT PDFs, generates question-answer pairs in Hindi, Marathi, and English, cleans low-quality outputs, and exports the final dataset in JSONL format.

Project Workflow:

NCERT PDFs → Text Extraction → Q&A Generation → Dataset Cleaning → JSONL Dataset

Main Scripts:

- download.py
  Downloads NCERT textbook PDFs

- extract.py
  Extracts chapter-wise text using PyMuPDF

- generate_automation.py
  Generates multilingual Q&A pairs using Claude/Gemini APIs

- clean.py
  Removes low-quality and OCR-corrupted entries

Dataset Information:

- Total Q&A Pairs: 2,170
- Languages: English, Hindi, Marathi
- Source: NCERT Class 6–10 Science & Math
- Format: JSONL

Technologies Used:

- Python
- PyMuPDF
- Claude API
- Gemini API

Project Link:
https://github.com/dhananjay-234/shikshaedge-app

Dataset Link:
https://www.kaggle.com/datasets/dhananjayyyyyy/shikshaedge-ncert-curriculum-dataset
