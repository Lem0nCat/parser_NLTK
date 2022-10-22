import nltk
from nltk import CFG
from nltk.tokenize import word_tokenize

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det Nom | PropN
Nom -> Adj Nom | N
VP -> V Adj | V NP | V S | V NP PP
PP -> P NP
PropN -> "никита" | "миша" | "андрей" | "андре ямайский"
Det -> "мой" | "наш" | "его"
N -> "дерево" | "кот" | "стол" | "пирога"
Adj -> "злой" | "добрый" | "розовый"
V -> "сказал" | "сообщил" | "побил" | "думал" | "хотелось"
P -> "не"
""")

#text = input("Введите текст: ").lower()
text = "хотелось пирога, но яблоки еще не созрели."

tokens = word_tokenize(text, language="russian")

rd_parser = nltk.RecursiveDescentParser(grammar)
for tree in rd_parser.parse(tokens):
    print(tree)
