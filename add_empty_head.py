"""Add the `empty_head` block from make_demo_data.py to the existing data/latest.json, without regenerating it.

make_demo_data.py counts every date from the day it runs, so a full rerun moves the whole demo by days.
This script reads only the `empty_head` literal (it has no dates) and puts it into latest.json.

Run: python3 add_empty_head.py
"""
import ast
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'make_demo_data.py'), encoding='utf-8').read()
node = next(n for n in ast.parse(src).body
            if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == 'empty_head')
empty_head = ast.literal_eval(node.value)

path = os.path.join(HERE, 'data', 'latest.json')
data = json.load(open(path, encoding='utf-8'))
data['empty_head'] = empty_head
with open(path + '.tmp', 'w', encoding='utf-8') as fh:
    json.dump(data, fh, ensure_ascii=False, indent=1)
os.replace(path + '.tmp', path)
print('empty_head:', len(empty_head), 'sets,', sum(len(s['vars']) for s in empty_head), 'ideas ->', path)
