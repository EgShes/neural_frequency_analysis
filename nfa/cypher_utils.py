import random

import numpy as np


class Key:

    cls_random = random
    # j is missing
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

    @classmethod
    def seed(cls, i):
        cls.cls_random.seed(i)

    @classmethod
    def generate_key(cls):
        alph = cls.alphabet.copy()
        cls.cls_random.shuffle(alph)
        return cls(alph)

    @classmethod
    def from_list(cls, l):
        if set(l) != set(cls.alphabet):
            raise ValueError('Cant create key from given alphabet')
        return cls(l)

    @classmethod
    def from_str(cls, s):
        if set(s) != set(cls.alphabet):
            raise ValueError('Cant create key from given alphabet')
        return cls(list(s))

    def __init__(self, letters):
        self._table = np.array(letters).reshape((5, 5))
        self._enc_table = self._create_lookup_dict()
        self._dec_table = {encrypted: origin for origin, encrypted in self._enc_table.items()}
        # make sure i was not overwritten by j
        self._dec_table[self._enc_table['i']] = 'i'

    def _create_lookup_dict(self):
        d = {}
        rows, cols = self._table.shape
        for row in range(rows):
            for col in range(cols):
                new_row = row + 1 if row + 1 < rows else 0
                d[self._table[row, col]] = self._table[new_row, col]
        # j and i are treated as the same
        d['j'] = d['i']
        return d

    def encrypt_text(self, text):
        enc_text = ''
        for ch in text:
            enc_text += self._enc_table[ch] if ch in self._enc_table else ch
        return enc_text

    def decrypt_text(self, text):
        dec_text = ''
        for ch in text:
            dec_text += self._dec_table[ch] if ch in self._dec_table else ch
        return dec_text

    def __str__(self):
        return ''.join(self._table.flatten())
