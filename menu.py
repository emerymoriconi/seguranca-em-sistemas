from cripto import *
import sys

while True:
    print('SELECIONE UMA DAS OPÇÕES ABAIXO:')
    print('1 - Gerar par de chaves')
    print('2 - Listar par de chaves')
    print('3 - Gerenciar chaves')
    print('4 - Criptografar mensagem')
    print('5 - Descriptografar mensagem')
    print('0 - Sair')

    x = int(input())

    if x == 0:
        sys.exit()

    elif x == 1:
        email = input("Forneça o email para geração das chaves: ")
        chave_privada, chave_publica = gerar_par_chaves(email)

    elif x == 2:
        listar_pares_chaves()

    elif x == 3:
        gerenciar_chaves()
    
    elif x == 4:
        while True:
            emails = listar_pares_chaves()
            escolha = input("Escolha um email pelo número: ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(emails):
                email = emails[int(escolha) - 1]
                break
            else:
                print("Escolha inválida. Tente novamente.")
        print("Email escolhido: ", email)
        mensagem = input("Forneça a mensagem para criptografar: ")
        usar_chave_privada = input("Deseja usar a chave privada para criptografar? (S/N): ")
        if usar_chave_privada == 'S':
            usar_chave_privada = True
        elif usar_chave_privada == 'N':
            usar_chave_privada = False
        try:
            print("Mensagem criptografada: ", criptografar_mensagem(email, mensagem, usar_chave_privada))
        except Exception as e:
            print(f"Erro ao criptografar a mensagem: {e}")

    elif x == 5:
        while True:
            emails = listar_pares_chaves()
            escolha = input("Escolha um email pelo número: ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(emails):
                email = emails[int(escolha) - 1]
                break
            else:
                print("Escolha inválida. Tente novamente.")
        print("Email escolhido: ", email)
        mensagem = input("Forneça a mensagem para descriptografar: ")
        try:
            print("Mensagem descriptografada: ", descriptografar_mensagem(email, mensagem))
        except Exception as e:
            print(f"Erro ao descriptografar a mensagem: {e}")