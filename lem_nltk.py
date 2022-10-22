import nltk
from nltk import CFG
from nltk.tokenize import word_tokenize
import pymorphy2

grammar = CFG.fromstring("""
S -> NP VP
VP -> V NP
NP -> "я"
V -> "ебал"
NP -> "собак"
""")

text = input("Введите текст: ").lower()

tokens = word_tokenize(text, language="russian")

rd_parser = nltk.RecursiveDescentParser(grammar)
for tree in rd_parser.parse(tokens):
    print(tree)
