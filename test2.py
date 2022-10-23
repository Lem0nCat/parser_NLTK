from lib2to3.pgen2 import grammar, token
import nltk
from nltk import CFG
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from pymystem3 import Mystem

# from nltk.stem import SnowballStemmer
 

grammar = CFG.fromstring("""
    S -> NP VP
    NP -> Adj N | N
    VP -> V NP
    N -> 'письмо' | 'друг' | 'я'
    V -> 'писать'
    Adj -> 'старый'
""")

russian_stopwords = stopwords.words("russian")
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
    return tokens


text = input("Введите текст: ")

tokens = preprocessText(text)

parser = nltk.ShiftReduceParser(grammar)
trees = parser.parse(tokens)
for tree in trees:
     print(tree)

print(nltk.parse.chart.demo(1, print_times=False, trace=0, sent='I saw John with a dog', numparses=2))