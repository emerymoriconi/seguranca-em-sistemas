from cripto import *

while True:
    print('SELECIONE UMA DAS OPÇÕES ABAIXO:')
    print('1 - Gerar par de chaves')
    print('2 - Listar par de chaves')
    print('3 - Gerenciar chaves')

    x = int(input())

    if x == 1:
        chave_privada, chave_publica = gerar_par_chaves("exemplo@email.com")

    if x == 2:
        listar_pares_chaves()

    if x == 3:
        gerenciar_chaves()