import re

ficheiro = open('train.txt', 'r', encoding='UTF-8')

dicionario = {}
dicAux = {}


def insereElemSemRepetidos(actualName, actualPosition, actualCategoria):
    jaExiste = False
    size = len(dicionario[actualCategoria])
    i = 0
    while (i < size and (not jaExiste)):
        (elem, _) = dicionario[actualCategoria][i]
        if (elem == actualName):
            jaExiste = True
        i += 1
    if (not jaExiste):
        dicionario[actualCategoria].append((actualName, actualPosition))
        dicAux[actualCategoria] += 1


def insereElemComRepetidos(actualName, actualPosition, actualCategoria):
    dicionario[actualCategoria].append((actualName, actualPosition))
    dicAux[actualCategoria] += 1


def parser(funcInsere):
    expressao = re.compile(r'([BI])-(\w+)[\t ]+(\w+)')
    actualCategoria = ""
    actualName = ""
    actualPosition = 0
    for i, l in enumerate(ficheiro):
        res = expressao.search(l)
        if res:
            if res.group(1) in 'BI':
                if res.group(1) == 'B':
                    if not dicionario.__contains__(actualCategoria):
                        dicionario[actualCategoria] = []
                        dicAux[actualCategoria] = 0
                    # Insere com repetidos ou sem repetidos
                    funcInsere(actualName, actualPosition, actualCategoria)
                    # Atualiza o elemento
                    actualCategoria = res.group(2)
                    actualName = res.group(3)
                    actualPosition = i
                else:
                    actualName = actualName + " " + res.group(3)

    funcInsere(actualName, actualPosition, actualCategoria)
    del dicionario[""]


def pagPrincipal(ficheiro):
    ficheiro.write(f'''<!DOCTYPE html>
    <html>
        <head>
            <title>Pagina Principal</title>
            <meta charset=UTF-8/>
        </head>''')
    ficheiro.write('<body>\n')
    ficheiro.write(f'\t<h1>Categorias</h1>\n')
    ficheiro.write(f'\t<ul>\n')
    for k, v in dicionario.items():
        ficheiro.write(f'\t\t<li><a href="pag{k}.html">{k}</a> Contem: {len(v)} elementos!</li>\n')
        print("Categoria: ", k, ",Contem: ", len(v))
    ficheiro.write(f'\t</ul>\n')
    ficheiro.write(f'</body>')


def pagSecundaria(key, ficheiro):
    ficheiro.write(f'''<!DOCTYPE html>
     <html>
         <head>
             <title>Pagina do elemento {key} </title>
             <meta charset=UTF-8/>
         </head>''')
    ficheiro.write(f'<body>\n')
    ficheiro.write(f'\t<h1><a href="pagInicial.html">Listagem da key: {key}</a></h1>\n')
    ficheiro.write(f'\t<ul>\n')
    for v in dicionario[key]:
        ficheiro.write(f'\t\t<li>{v}</li>\n')
    ficheiro.write(f'\t</ul>\n')
    ficheiro.write(f'</body>')


print('Pretende ter em consideracao os reptidos? (S/N)')
opcao = input('Escolha: ')
if opcao in 'Ss':
    parser(insereElemComRepetidos)
elif opcao in 'nN':
    parser(insereElemSemRepetidos)
else:
    print('Opcao invalida!')

pagIni = open('./Paginas/pagInicial.html', 'w')
pagPrincipal(pagIni)

for k in dicionario.keys():
    pagSec = open(f'./Paginas/pag{k}.html', 'w')
    pagSecundaria(k, pagSec)


