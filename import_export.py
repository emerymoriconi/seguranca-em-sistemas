from cripto import *
import sys
import re
from cripto import salvar_chave_publica, adicionar_email, salvar_chave_privada

def importar_chaves():
    while (True):
        email = input("Forneça o email associado ao par de chaves: ")
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            print("Email inválido.")
            continue
        else:
            break
    
    chave_publica_path = input("Forneça o caminho do arquivo da chave pública: ")
    while (True):
        resposta = input("Deseja importar chave privada? (S/N)")
        if resposta.lower() == 's':
            chave_privada_path = input("Forneça o caminho do arquivo da chave privada: ")
            senha = input("Forneça a senha da chave privada: ")

            break
        elif resposta.lower() == 'n':
            chave_privada_path = None
            break
        else:
            print("Input inválido")

    try:
        with open(chave_publica_path, "rb") as arquivo:
            dados = arquivo.read()
            chave_publica = RSA.import_key(dados)
            salvar_chave_publica(email, chave_publica)
            adicionar_email(email)
        if chave_privada_path:
            with open(chave_privada_path, "rb") as arquivo:
                dados = arquivo.read()
                chave_privada = RSA.import_key(dados, passphrase=senha)
                salvar_chave_privada(email, chave_privada, senha)
    except Exception as e:
        print(f"Erro ao importar as chaves: {e}")
        return