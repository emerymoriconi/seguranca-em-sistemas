from cripto import *
from import_export import *
import sys

while True:
    print('\nSELECIONE UMA DAS OPÇÕES ABAIXO:')
    print('1 - Gerar par de chaves')
    print('2 - Listar par de chaves')
    print('3 - Gerenciar chaves')
    print('4 - Criptografar mensagem')
    print('5 - Descriptografar mensagem')
    print('6 - Importar chaves')
    print('7 - Exportar chaves')
    print('0 - Sair\n')

    x = int(input())

    if x == 0:
        sys.exit()

    elif x == 1:
        while (True):
            email = input("Forneça o email para a geração do par de chaves: ")
            if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
                print("Email inválido.")
                continue
            else:
                break
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
        while True:
            usar_chave_privada = input("Deseja usar a chave privada para criptografar? (S/N): ")
            if usar_chave_privada.lower() == 's':
                usar_chave_privada = True
                break
            elif usar_chave_privada.lower() == 'n':
                usar_chave_privada = False
                break
            else:
                print("Input inválido")
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

    elif x == 6:
        importar_chaves()

    elif x == 7:
        exportar_chaves()