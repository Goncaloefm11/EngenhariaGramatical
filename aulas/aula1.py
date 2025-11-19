import re
''' Exercico 1
Verdadeira
Falsa 
Falsa
Falsa
'''

#Exercico 2

def verifica_automato(var):
    padrao = r'[A-Z][A-Z]-[0-9][0-9]-([A-Z][A-Z]|[0-9][0-9])|[0-9]]0-9]-[0-9][0-9]-[A-Z]A-Z]'
    if re.fullmatch(padrao, var):
        return print("True")
    else:
        return print("False") 

def verifica_email(email):
    padrao = r'[a-z0-9_%+-]+(\.[a-z0-9_%+-]+)*@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(padrao, email):
        return print("True")
    else:
        return print("False")

def verifica_data(data):
    padrao = r'(\d{4}-\d{2}-\d{2})'
    if re.fullmatch(padrao, data):
        return print("True")
    else:
        return print("False")

def verifica_maiuscula(texto):
    padrao = r'[A-Z][a-z]*(?:\s[A-Z][a-z])*'
    resutlado = re.findall(padrao, texto)
    return resutlado

def verifica_flutuante(numero):
    padrao = r'-?\d+\.\d+$'
    if re.fullmatch(padrao, numero):
        return print("True")
    else:
        return print("False")

def troca_palavras(texto):
    padrao = r'\b(CAO|GATO|PATO)\b'
    dicionario = {'CAO':'auau', 'GATO':'miaumiau', 'PATO':'quackquack'}
    resultado = re.sub(padrao, lambda m: dicionario[m.group(0)], texto)
    return resultado


print(troca_palavras("o cao faz CAO, o gato faz GATO e o pato faz PATO"))
