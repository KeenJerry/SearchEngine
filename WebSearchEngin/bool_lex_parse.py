import ply.lex as lex
import ply.yacc as yacc
import nltk

from WebSearchEngin.views import AND, OR, NOT
from query import find_term


# List of token names
tokens = (
	'TK',
	'AND',
	'OR',
	'NOT',
	'LPAREN',
	'RPAREN',	
)

t_ignore = " \t"

def t_AND(t):
	r'AND'
	return t

def t_OR(t):
	r'OR'
	return t

def t_NOT(t):
	r'NOT'
	return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_TK(t):
    r'[^ ]+'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer    
lexer = lex.lex()

precedence = (  
	('left', 'OR'),
	('left', 'AND'),  
	('left', 'NOT'),  
)

def p_expression_binop(p):
    '''expression : expression AND expression
    | expression OR expression'''
    if p[2] == 'AND' : p[0] = AND(p[1], p[3])
    elif p[2] == 'OR' : p[0] = OR(p[1], p[3])
    # elif p[2] == 'NOT': p[0] = NOT(p[1], p[3])

def p_expression_not(p):
    "expression : NOT expression"
    p[0] = NOT(all, p[2])

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]

def p_expression_token(p):
    "expression : TK"
    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    node = find_term(stemmer.stem(p[1]))
    if not node:
        pass
    else:
        p[0] = node.index


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
all = {}
for i in range(0, 10788):
    all[str(i)] = '0'
parser = yacc.yacc()
# data = "( happy OR glad ) AND angry"
# result = parser.parse(data)
# print(result)