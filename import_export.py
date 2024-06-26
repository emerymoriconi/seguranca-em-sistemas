import shutil
from cripto import *
import sys
import re
from cripto import salvar_chave_publica, adicionar_email, salvar_chave_privada
import tkinter as tk
from tkinter import filedialog

def selecionar_arquivo_criptografar():
    # selecionando um arquivo com tkinter
    root = tk.Tk()
    try:
        print("Selecione o arquivo para criptografar:")
        arquivo = filedialog.askopenfilename(initialdir="/", title="Selecione arquivo para criptografar", filetypes=(("Todos os arquivos", "*.*"), ("Arquivos de texto", "*.txt")))
        with open(arquivo, "r") as file:
            root.destroy()
            return arquivo
    except Exception as e:
        print(f"Erro ao selecionar arquivo: {e}")
    return None

def selecionar_arquivo_descriptografar():
    # selecionando um arquivo com tkinter
    root = tk.Tk()
    try:
        print("Selecione o arquivo para descriptografar:")
        arquivo = filedialog.askopenfilename(initialdir="/", title="Selecione arquivo para descriptografar", filetypes=(("Todos os arquivos", "*.*"), ("Arquivos de texto", "*.txt")))
        with open(arquivo, "r") as file:
            root.destroy()
            return arquivo
    except Exception as e:
        print(f"Erro ao selecionar arquivo: {e}")
    return None

def selecionar_arquivo(chave):
    # criando janela de seleção de arquivo com tkinter 
    root = tk.Tk()
    try:
        print(f"Selecione o arquivo da chave {chave}:")
        arquivo = filedialog.askopenfilename(initialdir="/", title=f"Selecione arquivo da chave {chave}", filetypes=(("Todos os arquivos", "*.*"), ("Arquivos de texto", "*.txt")))
        with open(arquivo, "r") as file:
            root.destroy()
            return arquivo
    except Exception as e:
        print(f"Erro ao selecionar arquivo: {e}")
    return None


def importar_chaves():
    while (True):
        email = input("Forneça o email associado ao par de chaves: ")
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            print("Email inválido.")
            continue
        else:
            break
    
    chave_publica_path = selecionar_arquivo("pública")
    if not chave_publica_path:
        print("Operação abortada. Arquivo não selecionado.")
        return
    #input("Forneça o caminho do arquivo da chave pública: ")
    while (True):
        resposta = input("Deseja importar chave privada? (S/N)")
        if resposta.lower() == 's':
            chave_privada_path = selecionar_arquivo("privada")
            if not chave_privada_path:
                print("Operação abortada. Arquivo não selecionado.")
                return
            #input("Forneça o caminho do arquivo da chave privada: ")
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
        print("Chaves importadas com sucesso.")
    except Exception as e:
        print(f"Erro ao importar as chaves: {e}")
        return
    

def exportar_chaves():
    while (True):
        email = input("Forneça o email associado ao par de chaves: ")
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            print("Email inválido.")
            continue
        else:
            break

    # diretório de exportação
    root = tk.Tk()
    print("Selecione o diretório de exportação:")
    diretorio = filedialog.askdirectory(initialdir="/", title="Selecione o diretório de exportação")
    if not diretorio:
        print("Operação abortada. Diretório não selecionado.")
        return

    root.destroy()
    with open("lista_emails.txt", "r") as arquivo:
        for linha in arquivo:
            if email in linha:
                # Verificar se o arquivo da chave privada existe
                caminho_chave_privada = os.path.join(diretorio_chaves, f"{email}_privada.pem")
                if os.path.exists(caminho_chave_privada):
                    # copiar o arquivo para o diretório de exportação
                    shutil.copy(caminho_chave_privada, diretorio)

                # Verificar se o arquivo da chave pública existe
                caminho_chave_publica = os.path.join(diretorio_chaves, f"{email}_publica.pem")
                if os.path.exists(caminho_chave_publica):
                    # copiar o arquivo para o diretório de exportação
                    shutil.copy(caminho_chave_publica, diretorio)

                print("Chaves exportadas com sucesso.")
                return
        raise ValueError("E-mail não encontrado")