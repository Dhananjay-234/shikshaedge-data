import json

lines = open('output/curriculum_dataset.jsonl', encoding='utf-8').readlines()
cleaned = []
removed = 0

for line in lines:
    pair = json.loads(line)
    instr = pair['instruction']
    if 'following text' in instr.lower() or len(instr) < 20 or len(pair['response']) < 30:
        removed += 1
        continue
    cleaned.append(line)

with open('output/curriculum_dataset.jsonl', 'w', encoding='utf-8') as f:
    f.writelines(cleaned)

print(f'Removed: {removed} bad pairs')
print(f'Clean pairs remaining: {len(cleaned)}')

