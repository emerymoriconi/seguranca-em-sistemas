from cripto import *
import sys

while True:
    print('SELECIONE UMA DAS OPÇÕES ABAIXO:')
    print('1 - Gerar par de chaves')
    print('2 - Listar par de chaves')
    print('3 - Gerenciar chaves')
    print('0 - Sair')

    x = int(input())

    if x == 0:
        sys.exit()

    elif x == 1:
        email = input("Forneça o email para geração das chaves:")
        chave_privada, chave_publica = gerar_par_chaves(email)

    elif x == 2:
        listar_pares_chaves()

    elif x == 3:
        gerenciar_chaves()

    else:
        print("Valor inválido")