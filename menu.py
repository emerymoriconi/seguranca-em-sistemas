from cripto import *
from import_export import *
import re
import sys

while True:
    print('\nSELECIONE UMA DAS OPÇÕES ABAIXO:')
    print('1 - Gerar par de chaves')
    print('2 - Gerenciar chaves')
    print('3 - Criptografar mensagem')
    print('4 - Descriptografar mensagem')
    print('5 - Importar chaves')
    print('6 - Exportar chaves')
    print('0 - Sair\n')

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