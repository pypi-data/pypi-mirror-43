from cfg import ContextFreeGrammar, PushdownAutomata

grammarString = """
S -> 0 B | $
A -> 0 B | $
B -> A 0
"""

grammar = ContextFreeGrammar(grammarString)
print(grammar)
pda = grammar.toPDA()
print(pda)
grammar = pda.toCFG()
#grammar.simplify()
print(grammar)