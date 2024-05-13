from cripto import *
from import_export import *
import re
import sys

while True:
    # Códigos de cor
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    print(f'\n{BOLD}{CYAN}{"="*50}{RESET}')
    print(f'{BOLD}{CYAN}{"    CRIPTOGRAFIA RSA E GERENCIAMENTO DE CHAVES           "}{RESET}')
    print(f'{BOLD}{CYAN}{"                 MENU DE OPÇÕES           "}{RESET}')
    print(f'{BOLD}{CYAN}{"="*50}{RESET}')
    print(f'{GREEN}\t1 - Gerar par de chaves{RESET}')
    print(f'{GREEN}\t2 - Gerenciar chaves{RESET}')
    print(f'{GREEN}\t3 - Criptografar arquivo{RESET}')
    print(f'{GREEN}\t4 - Descriptografar arquivo{RESET}')
    print(f'{GREEN}\t5 - Importar chaves{RESET}')
    print(f'{GREEN}\t6 - Exportar chaves{RESET}')
    print(f'{RED}\t0 - Sair{RESET}')
    print(f'{BOLD}{CYAN}{"="*50}{RESET}\n')

    x = int(input())

    if x == 0:
        sys.exit()

    elif x == 1:
        chave_privada, chave_publica = gerar_par_chaves()

    elif x == 2:
        gerenciar_chaves()
    
    elif x == 3:
        email = selecionar_email()
        arquivo = selecionar_arquivo_criptografar()
        if not arquivo:
            print("Operação abortada. Arquivo não selecionado.")
        if criptografar(email, arquivo):
            print("Arquivo criptografado salvo com sucesso no diretório escolhido!")
        else:
            print("Erro ao criptografar o arquivo.")

    elif x == 4:
        email = selecionar_email()
        arquivo = selecionar_arquivo_descriptografar()
        if not arquivo:
            print("Operação abortada. Arquivo não selecionado.")
        if descriptografar_mensagem(email, arquivo):
            print("Arquivo descriptografado salvo com sucesso no diretório escolhido!")
        else:
            print("Erro ao descriptografar o arquivo.")

    elif x == 5:
        importar_chaves()

    elif x == 6:
        exportar_chaves()