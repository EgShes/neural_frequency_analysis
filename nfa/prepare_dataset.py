import argparse
import os
import os.path as osp
from tqdm import tqdm

import pandas as pd
from nfa.cypher_utils import Key


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--seed', type=int, default=0, help='Seed used for key generation')
    parser.add_argument('--data_path', type=str, default='../data', help='Path to data folder')

    args = parser.parse_args()

    Key.seed(args.seed)

    if not osp.isdir(osp.join(args.data_path, 'processed')):
        os.mkdir(osp.join(args.data_path, 'processed'))

    for file in os.listdir(osp.join(args.data_path, 'interim')):
        df = pd.read_csv(osp.join(args.data_path, 'interim', file))
        df = df.dropna()

        for i, row in tqdm(df.iterrows(), desc=f'Processing {file}', total=len(df)):
            key = Key.generate_key()
            df.at[i, 'enc_text'] = key.encrypt_text(row['text'])
            df.at[i, 'key'] = str(key)

        df.to_csv(osp.join(args.data_path, 'processed', file), index=False)
