import fitz  # pip install pymupdf
import os
import glob

os.makedirs("extracted", exist_ok=True)

pdf_files = glob.glob("pdfs/**/*.pdf", recursive=True)
print(f"Found {len(pdf_files)} PDF files\n")

skipped = 0
for path in pdf_files:
    # Build output filename from folder + file name
    parts = path.replace("\\", "/").split("/")
    book_name = parts[1] if len(parts) > 2 else "misc"
    file_name = os.path.basename(path).replace(".pdf", ".txt")
    out_name  = f"{book_name}__{file_name}"
    out_path  = f"extracted/{out_name}"

    if os.path.exists(out_path):
        skipped += 1
        continue

    try:
        doc  = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)

        # Clean: remove blank lines and junk whitespace
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        text  = "\n".join(lines)

        if len(text) < 200:
            print(f"  skip (too short): {out_name}")
            continue

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"  ✓  {out_name}  ({len(text):,} chars)")

    except Exception as e:
        print(f"  ✗  {path}  →  {e}")

print(f"\nDone.  {len(pdf_files) - skipped} extracted,  {skipped} skipped (already existed).")
