import urllib.request
import os
import zipfile

os.makedirs("pdfs", exist_ok=True)

books = [
    # Science English
    ("https://ncert.nic.in/textbook/pdf/hesc1dd.zip", "science_class6_en"),
    ("https://ncert.nic.in/textbook/pdf/gesc1dd.zip", "science_class7_en"),
    ("https://ncert.nic.in/textbook/pdf/hesc108.zip", "science_class8_en"),
    ("https://ncert.nic.in/textbook/pdf/iesc1dd.zip", "science_class9_en"),
    ("https://ncert.nic.in/textbook/pdf/jesc1dd.zip", "science_class10_en"),
    # Math English
    ("https://ncert.nic.in/textbook/pdf/hemh1dd.zip", "math_class8_en"),
    ("https://ncert.nic.in/textbook/pdf/iemh1dd.zip", "math_class9_en"),
    ("https://ncert.nic.in/textbook/pdf/jemh1dd.zip", "math_class10_en"),
    # Science Hindi
    ("https://ncert.nic.in/textbook/pdf/hhsc1dd.zip", "science_class6_hi"),
    ("https://ncert.nic.in/textbook/pdf/ghsc1dd.zip", "science_class7_hi"),
    ("https://ncert.nic.in/textbook/pdf/hhsc108.zip", "science_class8_hi"),
    ("https://ncert.nic.in/textbook/pdf/ihsc1dd.zip", "science_class9_hi"),
    ("https://ncert.nic.in/textbook/pdf/jhsc1dd.zip", "science_class10_hi"),
]

for url, name in books:
    zip_path = f"pdfs/{name}.zip"
    extract_path = f"pdfs/{name}"

    print(f"Downloading {name}...", end=" ", flush=True)
    try:
        urllib.request.urlretrieve(url, zip_path)
        os.makedirs(extract_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_path)
        os.remove(zip_path)
        pdf_count = len([f for f in os.listdir(extract_path) if f.endswith(".pdf")])
        print(f"✓  {pdf_count} PDFs")
    except Exception as e:
        print(f"✗  failed ({e})")

print("\nAll done. Check the pdfs/ folder.")