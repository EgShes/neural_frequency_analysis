import torch
from torch.utils.data import Dataset


class CharVocab:

    def __init__(self, text):
        self.vocab = list(set(text))
        self.vocab.insert(0, self.sos_token)
        self.vocab.insert(1, self.eos_token)
        self.tok2int = {tok: i for i, tok in enumerate(self.vocab)}
        self.int2tok = {i: tok for tok, i in self.tok2int.items()}

    def state_dict(self):
        return {
            'vocab': self.vocab,
            'tok2int': self.tok2int,
            'int2tok': self.int2tok
        }

    @classmethod
    def from_state_dict(cls, state_dict):
        vocab = cls('')
        vocab.vocab = state_dict['vocab']
        vocab.tok2int = state_dict['tok2int']
        vocab.int2tok = state_dict['int2tok']
        return vocab

    # start of sequence token
    @property
    def sos_token(self):
        return 'sos'

    # end of sequence token
    @property
    def eos_token(self):
        return 'eos'


class TextKeyDataset(Dataset):

    def __init__(self, vocab: CharVocab, df, max_seq_len=512):
        self.vocab = vocab
        self.df = df
        self.mxl = max_seq_len

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        x, y = row['enc_text'][:self.mxl - 2], row['key']
        x, y = [self.vocab.tok2int[ch] for ch in x], [self.vocab.tok2int[ch] for ch in y]
        x, y = self.add_sos_eos(x), self.add_sos_eos(y)
        x, y = torch.LongTensor(x), torch.LongTensor(y)
        return x, y

    def add_sos_eos(self, seq):
        assert isinstance(seq, list)
        return [self.vocab.tok2int[self.vocab.sos_token]] + seq + [self.vocab.tok2int[self.vocab.eos_token]]
