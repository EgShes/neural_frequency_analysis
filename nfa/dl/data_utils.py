import torch
from torch.utils.data import Dataset


class CharVocab:

    def __init__(self, text):
        self.vocab = list(set(text))
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


