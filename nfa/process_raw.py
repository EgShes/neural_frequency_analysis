import os
import os.path as osp
import re

import pandas as pd

data_path_raw = '../data/raw'
data_path_proc = '../data/interim'

for file in os.listdir(data_path_raw):
    print(f'Processing {file}')
    with open(osp.join(data_path_raw, file), 'r') as f:
        text = f.read().lower()

    text = re.sub('<unk>', '', text)
    text = re.sub(" '", "'", text)
    text = re.sub('[^\w\s=]', '', text)
    text = re.sub(' +', ' ', text)
    text = re.sub('\n \n \n ', '\n \n \n \n', text)

    lines = []
    for i, line in enumerate(re.split('\n \n', text)):
        if i == 0:
            lines.append(line.strip())
            continue
        if line == ' ':
            if '=' not in lines[-1]:
                continue
            lines.append(line)
        else:
            lines.append(line.strip())

    titles, articles = zip(*[(lines[i], lines[i+1]) for i in range(0, len(lines) - 2, 2)])

    df = pd.DataFrame.from_dict({
        'title': titles, 'text': articles
    })

    df = df[df['text'] != ' ']
    df['title'] = df['title'].apply(lambda x: re.sub('=', '', x))

    df.to_csv(osp.join(data_path_proc, f'{file}.csv'), index=False)
