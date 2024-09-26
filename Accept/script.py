#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Script lê um arquivo de configuração "accept_config.txt" e cria uma copia do codigo fonte, adiciona o cabeçalho da biblioteca contendo os somadores
e modifica os loops cujo y é diferente de 0, com parâmetro x. 


- O programa assume que o loop tem incremento e apenas um incremento
- O programa assume que os incrementos incrementam de 1 em 1. O incremento deve somar em função de si pŕoprio
- O programa assume que o arquivo accept_config.txt esta no formato correto: x y loop at z.c:w 
"""

from sys import argv, exit

cabecalho = 'somadores.h'
funcao = 'ADDX'
config_accept = []
minha_perfuracao = []
numeroLinha = []

# Armazena em uma lista todos as configurações sobre o loop perfuration
def le_config_accept():
    nome_do_arquivo = "accept_config.txt"

    try:
        with open(nome_do_arquivo, 'r') as arquivo:
            conteudo = arquivo.readlines()
    
    except IOError as e:
        print("Error: Unable to open the file:  " + nome_do_arquivo + ":        " + str(e))
        exit(1)

    
    except Exception as e:
        print("Error: An error occurred while reading the file. " + nome_do_arquivo + ":", type(e).__name__)
        exit(1)

            
    if not conteudo:
        print(nome_do_arquivo + " is empty")
        exit(1)

    for linha in conteudo:
        aux = linha.split()
        if 'paralellize' not in linha and 'while' not in linha:    
            config_accept.append(linha)


# Salva as linhas das perfurações marcadas com 1 em uma lista "numeroLinha"
def salvar_linhas():
    for i in minha_perfuracao:
        numeroLinha.append(obter_linha(i))


# Retorna o nome do codigo fonte .c
def obter_nome_cod_fonte():
    line = config_accept[0].split()[4]
    name = ''
    for i in line:
        if i == '.':
            break
        name += i
    
    return name


# Retorna a linha do loop
def obter_linha(linha):
    i = linha.index(':')
    return int(linha[i+1:-1])


# Procura apenas modificações que não são do accept e armazena na lista notAccept
def obter_perfuracoes():
    for i in config_accept:
        aux = i.split()
        if aux[1] == '1' and aux[0] != '0':
            minha_perfuracao.append(i)
    if len(minha_perfuracao) == 0:
        print("There are only accept perforations or 0's parameters, no modifications were made.")
        exit(0)


# Dado um string loop for retorna o incremento
def obter_incremento(linha):
    pos_i = 0
    pos_f = 0

    cont = 0
    for i in range(len(linha)):
        if linha[i] == ';':
            cont += 1
        
        if cont == 2:
            i += 1
            while(linha[i] == ' '):
                i += 1
            pos_i = i
            while(linha[i] != ')'):
                i += 1
            pos_f = i - 1
        
            break
        
    return [linha[pos_i:pos_f + 1], pos_i, pos_f]


# Retorna incremento modificado
def modifica_incremento(dados, param):
    incremento = dados[0]
    param = str(2 ** int(param))
    var = ''

    tam = len(incremento)

    for i in range(tam):
        while i < tam and (incremento[i] != '_' and not incremento[i].isalnum()):
            i += 1
        
        while i < tam and (incremento[i].isalnum() or incremento[i] == '_'):
            var += incremento[i]
            i += 1

        break

    if '+' in incremento:
        dados[0] = var + ' = ' + funcao + '(' + var + ', ' + str(param) + ')'
    elif '-' in incremento:
        dados[0] = var + ' = ' + var + ' - ' + str(param)


# Transforma o antigo loop para o novo loop com o incremento modificado
def modifica_loop_for(instrucaoFor, param):
    incremento = obter_incremento(instrucaoFor)
    modifica_incremento(incremento, param)

    nova_linha = ''

    i = 0
    while(i < len(instrucaoFor)):
        if i != incremento[1]:
            nova_linha += instrucaoFor[i]
            i += 1
        else:
            nova_linha += incremento[0]
            i = incremento[2] + 1

    return nova_linha
    

# Retorna uma string do cabeçalho das funções
def retorna_cabecalho(cabecalho):
    return '#include <' + cabecalho + '>\n'




le_config_accept()
obter_perfuracoes()
salvar_linhas()

perf_linha = {numeroLinha[i] : minha_perfuracao[i] for i in range(len(numeroLinha))}
perf_linha = dict(sorted(perf_linha.items()))

arquivo_original = obter_nome_cod_fonte()
novo_arquivo = arquivo_original + '_modificado.c'
arquivo_original += '.c'

if len(argv) > 1:
    funcao = argv[-1].upper()

try:
    with open(arquivo_original, 'r') as codigo_original:
        conteudo_codigo = codigo_original.readlines()

except IOError as e:
    print("Error: " + arquivo_original + " not found. Nothing to be done : \t" + str(e))
    exit(1)

except Exception as e:
    print("Error: An error occurred while reading the file. " + arquivo_original + ":", type(e).__name__)
    exit(1)

if not conteudo_codigo:
    print(arquivo_original + " is empty")
    exit(1)

with open(novo_arquivo, 'w') as codigo_modificado:
    cabecalho = retorna_cabecalho(cabecalho)
    codigo_modificado.write(cabecalho)
    for linha_instrucao, instrucao in enumerate(conteudo_codigo, start=1):
        if linha_instrucao in numeroLinha:
            param = perf_linha[linha_instrucao].split()[0]
            nova_instrucao = modifica_loop_for(instrucao, param)
            codigo_modificado.write(nova_instrucao)
        else:
            codigo_modificado.write(instrucao)
