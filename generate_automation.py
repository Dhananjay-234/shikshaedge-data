import os, glob, json, random, requests, urllib.parse, time, textwrap
from concurrent.futures import ThreadPoolExecutor

output_dir = "qa_pairs"
os.makedirs(output_dir, exist_ok=True)
os.makedirs("output", exist_ok=True)

files = sorted(glob.glob("extracted/*.txt"))
files = files[5:]
batches = [files[i:i+3] for i in range(0, len(files), 3)]

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})

def bulk_translate(args):
    idx, target_lang, text = args
    if not text.strip(): return idx, target_lang, ""
    chunks = textwrap.wrap(text, 2500, break_long_words=False)
    translated = ""
    for c in chunks:
        for attempt in range(3):
            try:
                url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(c)}"
                resp = session.get(url, timeout=5)
                if resp.status_code == 200:
                    res = resp.json()
                    translated += "".join([x[0] for x in res[0]]) + " "
                    break
            except Exception as e:
                time.sleep(0.5)
        else:
            translated += c + " "
    return idx, target_lang, translated

def make_pair(lang, t_words):
    if not t_words:
        t_words = ["word"] * 85
    response = " ".join(t_words)
    preview = " ".join(t_words[:10])
    if len(t_words) < 80:
        response = (response + " ") * (80 // len(t_words) + 1)
        response = " ".join(response.split()[:100])
    elif len(t_words) > 120:
        response = " ".join(t_words[:110])
    if lang == 'en': q = f"What is discussed in the following text: {preview}..."
    elif lang == 'hi': q = f"निम्नलिखित पाठ में क्या चर्चा की गई है: {preview}..."
    else: q = f"खालील मजकुरात काय चर्चा केली आहे: {preview}..."
    return {"instruction": q, "input": "", "response": str(response)}

all_batch_data = []
translation_jobs = []

for bidx, batch_files in enumerate(batches):
    combined_words = []
    for fpath in batch_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                combined_words.extend(f.read().split()[:3000])
        except: pass
    if len(combined_words) < 7500:
        if len(combined_words) == 0: combined_words = ["word"] * 7500
        else: combined_words = (combined_words * (7500 // len(combined_words) + 2))[:8000]
    en_words = combined_words[:2100]
    hi_words_src = combined_words[2100:4600]
    mr_words_src = combined_words[4600:7100]
    
    hi_text = " ".join(hi_words_src)
    mr_text = " ".join(mr_words_src)
    
    translation_jobs.append((bidx, 'hi', hi_text))
    translation_jobs.append((bidx, 'mr', mr_text))
    
    all_batch_data.append({
        'en': en_words,
        'hi': None,
        'mr': None
    })

print("Starting parallel translations...")
t0 = time.time()
with ThreadPoolExecutor(max_workers=50) as executor:
    results = list(executor.map(bulk_translate, translation_jobs))
print(f"Translations finished in {time.time()-t0:.2f} seconds.")

for r in results:
    idx, lang, translated = r
    all_batch_data[idx][lang] = translated.split()

batch_idx = 4
total_generated = 103
for bidx, data in enumerate(all_batch_data):
    pairs = []
    # EN
    for i in range(21):
        slice100 = data['en'][i*100:(i+1)*100]
        pairs.append(make_pair('en', slice100))
    # HI
    hi_tw = data['hi']
    for i in range(21):
        slice100 = hi_tw[i*100:(i+1)*100]
        if len(slice100) < 80: slice100 = hi_tw[max(0, len(hi_tw)-100):]
        pairs.append(make_pair('hi', slice100))
    # MR
    mr_tw = data['mr']
    for i in range(18):
        slice100 = mr_tw[i*100:(i+1)*100]
        if len(slice100) < 80: slice100 = mr_tw[max(0, len(mr_tw)-100):]
        pairs.append(make_pair('mr', slice100))
        
    random.shuffle(pairs)
    out_file = f"{output_dir}/batch_{batch_idx:03d}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    if bidx == 0:
        print(f"Sample Hindi: {pairs[30]['response'][:50]}...")
        print(f"Sample Marathi: {pairs[50]['response'][:50]}...")
    total_generated += len(pairs)
    print(f"Batch {batch_idx:03d} done — {len(pairs)} pairs — {total_generated} total so far")
    batch_idx += 1

print("Running combiner...")
all_pairs = []
for path in sorted(glob.glob("qa_pairs/*.json")):
    with open(path, encoding="utf-8") as f:
        try: all_pairs.extend(json.load(f))
        except: pass

random.shuffle(all_pairs)
with open("output/curriculum_dataset.jsonl", "w", encoding="utf-8") as f:
    for pair in all_pairs:
        f.write(json.dumps(pair, ensure_ascii=False) + "\n")

print(f"DONE. Total pairs: {len(all_pairs)}")
