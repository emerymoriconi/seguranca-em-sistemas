from cripto import *

while True:
    print('SELECIONE UMA DAS OPÇÕES ABAIXO:')
    print('1 - Gerar par de chaves')
    print('2 - Listar par de chaves')
    print('3 - Pesquisar par de chaves')

    x = int(input())

    if x == 1:
        gerar_par_chaves("exemplo@email.com")

    if x == 2:
        listar_pares_chaves()

    if x == 3:
        email = input('Insira um email associado a um par de chaves existente: ')
        chave_publica, chave_privada = pesquisar_chaves_por_email(email=email)