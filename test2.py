from lib2to3.pgen2 import grammar
import nltk
from nltk import CFG

grammar = CFG.fromstring("""
  S -> NP VP
  VP -> V NP | V NP PP
  PP -> P NP
  V -> "saw" | "ate" | "walked"
  NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
  Det -> "a" | "an" | "the" | "my"
  N -> "man" | "dog" | "cat" | "telescope" | "park"
  P -> "in" | "on" | "by" | "with"
""")

rd_parser = nltk.RecursiveDescentParser(grammar)
sent = 'Mary saw a dog'.split()
for t in rd_parser.parse(sent):
    print(t)

print("\n")

sr_parse = nltk.ShiftReduceParser(grammar)
for t in sr_parse.parse(sent):
    print(t)