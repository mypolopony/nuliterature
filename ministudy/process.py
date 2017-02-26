import string
import glob
import re
import numpy as np
from collections import OrderedDict


def sanitize(s):
    allowed = {' '}.union(string.ascii_lowercase)
    return ''.join([letter for letter in s.lower() if letter in allowed])

newlinepattern = re.compile('[\n]+')       # Capture sentences

g = [f for f in glob.glob('*') if '.py' not in f]
articles = dict.fromkeys(g)

for source in g:
    text = open(source,'r').read()
    articles[source] = {'sentences': list()}
    articles[source]['sentences'].append([sanitize(sentence) for sentence in newlinepattern.split(text) if 'www' not in sentence and 'http' not in sentence])

words = set()

for a in articles.keys():
    for s in articles[a]['sentences']:
        for w in s.split(' '):
            if w is not '':
                words.add(w)

words = list(sorted(words))
print(words)

for source in list(articles.keys()):
    for idx,sentence in enumerate(articles[source]['sentences']):
        articles[source]['sentences']['vec'] = np.zeros(len(words),dtype=int)
        for idx,sentence in enumerate(articles[source]['sentences']):
for word in sentence.split(' '):
    idx = words.index(word)
    articles[source]['sentences'][idx] += 1

            for w in words:
                print('{}\n\t{}'.format(source,articles[source]['vec']))

print(articles)