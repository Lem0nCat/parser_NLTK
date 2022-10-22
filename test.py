from lib2to3.pgen2 import grammar
from traceback import print_tb
import nltk
from nltk import CFG
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from pymystem3 import Mystem
from nltk.stem import SnowballStemmer


russian_stopwords = stopwords.words("russian")
snowball = SnowballStemmer(language="russian")
mystem = Mystem() 


def initWfst(tokens, grammar):
    numtokens = len(tokens)
    wfst = [[None for i in range(numtokens + 1)] for j in range(numtokens + 1)]
    for i in range(numtokens):
        productions = grammar.productions(rhs=tokens[i])
        wfst[i][i + 1] = productions[0].lhs()
    return wfst


def complete_wfst(wfst, tokens, grammar, trace=False):
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    numtokens = len(tokens)
    for span in range(2, numtokens+1):
        for start in range(numtokens+1-span):
            end = start + span
            for mid in range(start+1, end):
                nt1, nt2 = wfst[start][mid], wfst[mid][end]
                if nt1 and nt2 and (nt1,nt2) in index:
                    wfst[start][end] = index[(nt1,nt2)]
                    if trace:
                        print("[%s] %3s [%s] %3s [%s] ==> [%s] %3s [%s]" % (start, nt1, mid, nt2, end, start, index[(nt1,nt2)], end))
    return wfst

def display(wfst, tokens):
    print('\nWFST ' + ' '.join([("%-6d" % i) for i in range(1, len(wfst))]))
    for i in range(len(wfst)-1):
        print("%d   " % i, end=" ")
        for j in range(1, len(wfst)):
            print("%-6s" % (wfst[i][j] or '.'), end=" ")
        print()


def preprocessText(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token != " " and token.strip() not in punctuation]
    
    # tokens = word_tokenize(text.lower(), language="russian")
    # tokens = [snowball.stem(token) for token in tokens if token not in russian_stopwords and token not in punctuation]

    return tokens


# grammar = CFG.fromstring("""
#  S -> NP VP
#  PP -> P NP
#  NP -> Det N | Det N PP | 'я' | 'никита'
#  VP -> V NP | VP PP
#  Det -> 'мой'
#  N -> 'слон' | 'обочина'
#  V -> 'стрелять'
#  P -> 'в' | 'на'
# """)

grammar = CFG.fromstring("""
    S -> NP VP
    PP -> P NP
    NP -> Det N | Det N PP | Adj N | 'я' | 'никита'
    VP -> V NP | VP PP | VP NP
    Det -> 'мой'
    N -> 'слон' | 'обочина'  | 'друг' | 'письмо' 
    Adj -> 'сильный' | 'старый'
    V -> 'стрелять' | 'писать'
    P -> 'в' | 'на'
""")

text = input("Введите текст: ")
# text = "Никита стрелял в слона на обочине"

tokens = preprocessText(text)
print(tokens)


sr_parser = nltk.ShiftReduceParser(grammar)
for tree in sr_parser.parse(tokens):
    print(tree)

wfst0 = initWfst(tokens, grammar)
wfst1 = complete_wfst(wfst0, tokens, grammar)
display(wfst1, tokens)


