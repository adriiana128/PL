

from compilador_lex import tokens
import ply.yacc as yacc
import sys

def p_Programa(p):
    "Programa : BlocoDeclarativo BlocoInstrutivo"
    p[0] = p[1] + "START\n" + p[2] + "STOP\n"
    #pass

def p_BlocoDeclarativo_fim(p):
    " BlocoDeclarativo : "
    p[0] = ""


def p_BlocoDeclarativo(p):
    " BlocoDeclarativo : BlocoDeclarativo Declaracao ';'"
    p[0] = p[1] + p[2]


def p_BlocoInstrutivo_fim(p):
    " BlocoInstrutivo : "
    p[0] = ""


def p_BlocoInstrutivo(p):
    " BlocoInstrutivo : BlocoInstrutivo Instrucao ';'"
    p[0] = p[1] + p[2]


def p_Declaracao_d(p):
    " Declaracao : INT ID"
    parser.declaracoes[p[2]] = parser.totDeclar
    parser.totDeclar += 1
    p[0] = "PUSHI 0" + "\n"


def p_Declaracao_array(p):
    " Declaracao : INT ID '[' NUM ']'"
    parser.declaracoes[p[2]] = parser.totDeclar
    parser.totDeclar += int(p[4])
    p[0] = "PUSHN " + p[4] + "\n"


def p_Instrucao_atrib(p):
    " Instrucao : Atribuicao"
    p[0] = p[1]


def p_Instrucao_if_else(p):
    "Instrucao : IF '(' Condicao ')' '{' BlocoInstrutivo '}' ELSE '{' BlocoInstrutivo '}'"
    parser.totEtiquetas += 1
    x = str(parser.totEtiquetas)
    p[0] = p[3] + "JZ else" + x + "\n" + p[6] + "JUMP end" + x + "\n" + "else" + x + ":\n" + p[10] + "end" + x + ":\n"


def p_Instrucao_if(p):
    "Instrucao : IF '(' Condicao ')' '{' BlocoInstrutivo '}'"
    parser.totEtiquetas += 1
    x = str(parser.totEtiquetas)
    p[0] = p[3] + "JZ end" + x + "\n" + p[6] + "end" + x + ":\n"


def p_Instrucao_for(p):
    "Instrucao : FOR '(' Atribuicao ';' Condicao ';' Atribuicao ')' '{' BlocoInstrutivo '}'"
    parser.totEtiquetas += 1
    x = str(parser.totEtiquetas)
    p[0] = p[3] + "startFor" + x + ":\n" + p[5] + "JZ endFor" + x + "\n" + p[10] + p[7] + "JUMP startFor" + x + "\n" + "endFor" + x + ":\n"


def p_Instrucao_while(p):
    "Instrucao : WHILE '(' Condicao ')' '{' BlocoInstrutivo '}'"
    parser.totEtiquetas += 1
    x = str(parser.totEtiquetas)
    p[0] = "startWhile" + x + ":\n" + p[3] + "JZ endWhile" + x + "\n" + p[6] + "JUMP startWhile" + x + "\n" + "endWhile" + x + ":\n"


def p_Instrucao_print(p):
    " Instrucao : PRINT '(' ID ')'"
    if parser.declaracoes.__contains__(p[3]):
        x = parser.declaracoes[p[3]]
        p[0] = "PUSHG " + str(x) + "\nWRITEI\n"
    else:
        p[0] = ""
        print("Erro '", p[3], "' nao esta declarado!")


def p_Instrucao_print_num(p):
    " Instrucao : PRINT '(' Exp ')'"
    p[0] = p[3] + "WRITEI\n"


def p_Instrucao_printArray(p):
    " Instrucao : PRINT '(' ID '[' Exp ']' ')'"
    if parser.declaracoes.__contains__(p[3]):
        x = parser.declaracoes[p[3]]
        p[0] = "PUSHGP\n" + "PUSHI " + str(x) + "\n" + p[5] + "ADD\n" + "LOADN\n" + "WRITEI\n"
    else:
        p[0] = ""
        print("Erro '", p[3], "' nao esta declarado!")

def p_Atribuicao_exp(p):
    " Atribuicao : ID '=' Exp"
    if parser.declaracoes.__contains__(p[1]):
        x = parser.declaracoes[p[1]]
        p[0] = p[3] + "STOREG " + str(x) + "\n"
    else:
        p[0] = ""
        print("Erro '", p[1], "' nao esta declarado!")


def p_Atribuicao_expArray(p):
    " Atribuicao : ID '[' Exp ']' '=' Exp"
    if parser.declaracoes.__contains__(p[1]):
        x = parser.declaracoes[p[1]]
        p[0] = "PUSHGP\n" + "PUSHI " + str(x) + "\n" + p[3] + "ADD\n" + p[6] + "STOREN\n"
    else:
        p[0] = ""
        print("Erro '", p[1], "' nao esta declarado!")


def p_Atribuicao_read(p):
    " Atribuicao : ID '=' READ '(' ')'"
    if parser.declaracoes.__contains__(p[1]):
        x = parser.declaracoes[p[1]]
        p[0] = "READ\n" + "ATOI\n" + "STOREG " + str(x) + "\n"
    else:
        p[0] = ""
        print("Erro '", p[1], "' nao esta declarado!")


def p_Atribuicao_readArray(p):
    " Atribuicao : ID '[' Exp ']' '=' READ '(' ')'"
    if parser.declaracoes.__contains__(p[1]):
        x = str(parser.declaracoes[p[1]])
        p[0] = "PUSHGP\n" + "PUSHI " + x + "\n" + p[3] + "ADD\n" + "READ\n" + "ATOI\n" + "STOREN\n"
    else:
        p[0] = ""
        print("Erro '", p[1], "' nao esta declarado!")


def p_Condicao_igual(p):
    "Condicao : Condicao EQUALS Afirmacao"
    p[0] = p[1] + p[3] + "EQUAL\n"


def p_Condicao_conj(p):
    "Condicao : Condicao CONJ Afirmacao"
    p[0] = p[1] + p[3] + "MUL\n"


def p_Condicao_disj(p):
    "Condicao : Condicao DISJ Afirmacao"
    p[0] = p[1] + p[3] + "ADD\n"


def p_Condicao_desigual(p):
    "Condicao : Condicao NOTEQUAL Afirmacao"
    p[0] = p[1] + p[3] + "EQUAL\n" + "NOT\n"


def p_Condicao_afirm(p):
    "Condicao : Afirmacao"
    p[0] = p[1]


def p_Afirmacao_Negacao(p):
    "Afirmacao : '!' Afirmacao"
    p[0] = p[2] + "NOT\n"


def p_Afirmacao_True(p):
    "Afirmacao : TRUE"
    p[0] = "PUSHI 1\n"


def p_Afirmacao_False(p):
    "Afirmacao : FALSE"
    p[0] = "PUSHI 0\n"


def p_Afirmacao_Greater(p):
    "Afirmacao : Exp '>' Exp"
    p[0] = p[1] + p[3] + "SUP\n"


def p_Afirmacao_Lower(p):
    "Afirmacao : Exp '<' Exp"
    p[0] = p[1] + p[3] + "INF\n"


def p_Afirmacao_GreaterEQ(p):
    "Afirmacao : Exp GREATEQUAL Exp"
    p[0] = p[1] + p[3] + "SUPEQ\n"


def p_Afirmacao_LowerEQ(p):
    "Afirmacao : Exp LOWEREQUAL Exp"
    p[0] = p[1] + p[3] + "INFEQ\n"


def p_Afirmacao_Equals(p):
    "Afirmacao : Exp EQUALS Exp"
    p[0] = p[1] + p[3] + "EQUAL\n"


def p_Afirmacao_notEquals(p):
    "Afirmacao : Exp NOTEQUAL Exp"
    p[0] = p[1] + p[3] + "EQUAL\n" + "NOT\n"


def p_Exp_add(p):
    " Exp : Exp '+' Termo"
    p[0] = p[1] + p[3] + "ADD\n"


def p_Exp_sub(p):
    " Exp : Exp '-' Termo"
    p[0] = p[1] + p[3] + "SUB\n"


def p_Exp(p):
    "Exp : Termo"
    p[0] = p[1]


def p_Termo_mul(p):
    "Termo : Termo '*' Fator"
    p[0] = p[1] + p[3] + "MUL\n"


def p_Termo_div(p):
    "Termo : Termo '/' Fator"
    p[0] = p[1] + p[3] + "DIV\n"


def p_Termo_mod(p):
    "Termo : Termo '%' Fator"
    p[0] = p[1] + p[3] + "MOD\n"


def p_Termo(p):
    "Termo : Fator"
    p[0] = p[1]


def p_Fator_varArray(p):
    "Fator : ID '[' Exp ']'"
    x = parser.declaracoes[p[1]]
    p[0] = "PUSHGP\n" + "PUSHI " + str(x) + "\n" + p[3] + "ADD\n" + "LOADN\n"


def p_Fator_num(p):
    "Fator : NUM"
    p[0] = "PUSHI " + p[1] + "\n"


def p_Fator_var(p):
    "Fator : ID"
    x = parser.declaracoes[p[1]]
    p[0] = "PUSHG " + str(x) + "\n"


def p_Fator(p):
    "Fator : '(' Exp ')'"
    p[0] = p[2]


def p_error(p):
    print('Erro sintatico: ', p)
    parser.sucesso = False

# Constroi o parser
parser = yacc.yacc()

parser.sucesso = True
parser.totDeclar = 0
parser.totEtiquetas = 0
parser.declaracoes = {}


# Consome input
out = open('output.vm', "w")
inp = open('input.txt', "r").read()

parser.sucesso = True
result = parser.parse(inp)

if parser.sucesso:
    print('Valido: ', inp)
    out.write(result)
else:
    print('Invalido: ', inp)
