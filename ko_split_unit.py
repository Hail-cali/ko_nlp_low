import numpy as np
import re
from itertools import combinations, permutations

class BaseExtract:
    IN_TYPE = [list, str]
    OUT_TYPE = [list, str]

class Extractkr(BaseExtract):
    def __init__(self):
        self.k = None
        self.text = None
        self.decomposed = None
        self.first = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
                      'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ',
                      'ㅎ']
        self.middle = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ',
                       'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ',
                       'ㅡ', 'ㅢ', 'ㅣ']
        self.last = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ',
                     'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ',
                     'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        self.reverse_f = dict(zip(self.first, range(len(self.first))))
        self.reverse_m = dict(zip(self.middle, range(len(self.middle))))
        self.reverse_l = dict(zip(self.last, range(len(self.last))))

    def fit(self, text):

        return

    def fit_transform(self, text):
        if isinstance(text, list):
            self.text = text
        elif isinstance(text, str):
            self.text = [text]

        tokens = self._split_text()
        units = self.makeToken(tokens)
        self.make_word(units)
        return units

    def transform(self):
        pass

    def make_word(self, units):
        for unit in units:
            word = []
            single = list(permutations(unit, 3))
            print(f'len {len(single)} {single}')
            for s in single:
                try:
                    pair = list(permutations([u for u in unit if u not in s], 3))
                    w1 = self._compose_token(s[0],s[1],s[2])
                    print(w1)
                    for p in pair:
                        try:
                            w2 = self._compose_token(p[0],p[1],p[2])
                            word.append(w1+w2)
                        except:
                            continue
                except:
                    continue
            print(word)
            print(len(word))

        return

    def makeToken(self, tokens):
        uni_tokens= []
        for token in tokens:
            uni = [ord(t) for t in token]

            unit = []
            for u in (self._split_jamo(u) for u in uni):
                unit.extend(u)
            uni_tokens.append(unit)
        return uni_tokens

    def _split_text(self):
        token = [tuple(word) for word in self.text]
        return token

    def _split_unit(self, t):
        f = (t - 44032) // 588
        m = (t - 44032 - (f * 588)) // 28
        l = (t - 44032 - (f * 588) - (m * 28))
        return f, m, l

    def _decompose_token(self,t):


        return
    def _split_jamo(self, t):
        f = (t - 44032) // 588
        m = (t - 44032 - (f * 588)) // 28
        l = (t - 44032 - (f * 588) - (m * 28))
        return self.first[f], self.middle[m], self.last[l]

    def _compose_token(self, f, m, l):
        #splited unit into token
        first = self.reverse_f[f]
        middle = self.reverse_m[m]
        last = self.reverse_l[l]
        uni_compost = ((first*588) + (middle*28) + last) + 44032
        return chr(uni_compost)

    def _decompose_token(self):
        #splited token into unit
        return

if __name__ == '__main__':
    hangle = np.array([chr(code) for code in range(44032, 55204)])
    hangle = hangle.reshape(19, 21, 28)
    print(hangle)
    print(f"{'':->30}")
    target = ['능볏', '급대훈']
    ee = Extractkr()
    x = ee.fit_transform(target[0])
    #print(f'X:\t{type(x)} {x[0]}')
