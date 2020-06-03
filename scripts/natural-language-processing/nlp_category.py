import urllib.request
# response =  urllib.request.urlopen('https://en.wikipedia.org/wiki/SpaceX')
# response =  urllib.request.urlopen('https://en.wikipedia.org/wiki/Coronavirus')
# response =  urllib.request.urlopen('https://simple.wikipedia.org/wiki/Quantum_mechanics')
response =  urllib.request.urlopen('https://en.wikipedia.org/wiki/Battlestar_Galactica')

html = response.read()
print(html)

from bs4 import BeautifulSoup
soup = BeautifulSoup(html,'html5lib')
# soup = BeautifulSoup(html,'lxml')
text = soup.get_text(strip = True)
print(text)

tokens = [t for t in text.split()]
print(tokens)

import nltk
from nltk.corpus import stopwords
sr= stopwords.words('english')
clean_tokens = tokens[:]
for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)

# The most basic form of analysis on textual data is to take out the word frequency. 
freq = nltk.FreqDist(clean_tokens)

print(freq.most_common(10))


for key,val in freq.items():
    print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)