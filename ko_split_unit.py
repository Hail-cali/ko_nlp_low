import numpy as np
import re
from itertools import  permutations
from bs4 import BeautifulSoup
import requests

class BaseExtract:
    IN_TYPE = [list, str]
    OUT_TYPE = [list, str]

class Extractkr(BaseExtract):
    def __init__(self):
        from pirivatekey import SearchKey
        self.k = None
        self.text = None
        self.decomposed = None
        self.combiedword = []
        self.key = SearchKey().key
        self.candidates= []
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
        if isinstance(text, list):
            self.text = text
        elif isinstance(text, str):
            self.text = [text]
        tokens = self._split_text()
        units = self.makeToken(tokens)

        return units

    def fit_transform(self, text):
        if isinstance(text, list):
            self.text = text
        elif isinstance(text, str):
            self.text = [text]

        tokens = self._split_text()
        units = self.makeToken(tokens)
        self.make_word(units)
        return self.combiedword

    def transform(self):
        pass

    def make_word(self, units):
        for unit in units:
            word = self.permutate(unit, len(unit)//3)
            self.combiedword.append(word)

    def permutate(self, unit, k):
        word = []
        if k == 2:
            single = list(permutations(unit, 3))
            for s in single:
                try:
                    w1 = self._compose_token(s[0], s[1], s[2])
                    pair = list(permutations([u for u in unit if u not in s], 3))
                    for p in pair:
                        try:
                            w2 = self._compose_token(p[0], p[1], p[2])
                            word.append(w1 + w2)
                        except:
                            continue
                except:
                    continue
        elif k == 3:
            single = list(permutations(unit, 3))
            for s in single:
                try:
                    w1 = self._compose_token(s[0], s[1], s[2])
                    second = list(permutations([u for u in unit if u not in s], 3))
                    for p in second:
                        try:
                            w2 = self._compose_token(p[0], p[1], p[2])
                            third = list(permutations([u for u in unit if u not in s+p], 3))
                            for q in third:
                                try:
                                    w3 = self._compose_token(q[0], q[1], q[2])
                                    word.append(w1+w2+w3)
                                except:
                                    continue
                        except:
                            continue
                except:
                    continue

        return list(set(word))

    def makeToken(self, tokens):
        uni_tokens = []
        for token in tokens:
            uni = [ord(t) for t in token]
            unit = []
            for u in (self._decompose_token(u) for u in uni):
                unit.extend(u)
            uni_tokens.append(unit)
        return uni_tokens

    def _split_text(self):
        token = [tuple(word) for word in self.text]
        return token

    def _decompose_token(self, t):
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

    def searchword(self):
        url = 'https://opendict.korean.go.kr/api/search'

        for words in self.combiedword:
            candidates = []
            if len(words) > 0:
                for idx, word in enumerate(words):
                    res = requests.get(url, {'key': self.key, 'q': word})
                    text = res.text
                    soup = BeautifulSoup(text, 'html.parser')

                    if int(soup.find('total').get_text()) > 0:
                        result = soup.find('word').get_text()
                        print(result)
                        if len(result) == len(word):
                            candidates.append(result)

            self.candidates.append(candidates)
        return self.candidates

    def _split_unit(self, t):
        f = (t - 44032) // 588
        m = (t - 44032 - (f * 588)) // 28
        l = (t - 44032 - (f * 588) - (m * 28))
        return f, m, l

if __name__ == '__main__':

    # hangle = np.array([chr(code) for code in range(44032, 55204)])
    # hangle = hangle.reshape(19, 21, 28)
    # print(hangle)
    #
    # print(f"{'':->30}")

    target = ['능볏', '급대훈']
    et = Extractkr()
    x = et.fit_transform(target)
    print(f'X: \t{type(x)} first word count {len(x[0])}')
    print(f'{x[0]}')
    print(f'X: \t{type(x)} second word count {len(x[1])}')
    print(f'{x[1]}')

    candidates = et.searchword()
    print(candidates)
