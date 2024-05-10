from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import hashlib

# onde as chaves serão armazenadas
diretorio_chaves = "chaves/"

# verifica se o diretório existe e cria-o se não existir
if not os.path.exists(diretorio_chaves):
    os.makedirs(diretorio_chaves)

def gerar_par_chaves(email, tamanho_chave=2048, senha=None):

    chave = RSA.generate(tamanho_chave)
    chave_privada = chave.export_key()
    chave_publica = chave.publickey().export_key()
    
    # salvar a chave privada em um arquivo com o nome do email, protegida por senha
    senha = input("Digite uma senha para proteger a chave privada: ")
    
    with open(os.path.join(diretorio_chaves, f"{email}_privada.pem"), "wb") as arquivo_privado:
        if senha:
            arquivo_privado.write(chave.export_key(passphrase=senha, pkcs=8, protection="scryptAndAES128-CBC"))
        else:
            arquivo_privado.write(chave_privada)

    # salvar a chave pública em um arquivo com o nome do email
    with open(os.path.join(diretorio_chaves, f"{email}_publica.pem"), "wb") as arquivo_publico:
        arquivo_publico.write(chave_publica)

    # adicionar o email ao arquivo de lista de emails, evitando duplicatas
    if not os.path.exists("lista_emails.txt"):
        with open("lista_emails.txt", "w") as arquivo:
            arquivo.write(email + "\n")
    else:
        emails_existentes = set()
        with open("lista_emails.txt", "r") as arquivo:
            for linha in arquivo:
                emails_existentes.add(linha.strip())
        
        if email not in emails_existentes:
            with open("lista_emails.txt", "a") as arquivo:
                arquivo.write(email + "\n")
    
    # retorno das chaves
    return chave_privada, chave_publica

def pesquisar_chaves_por_email(email):
    # verificar se o email está na lista de emails
    with open("lista_emails.txt", "r") as arquivo:
        for linha in arquivo:
            if email in linha:
                # Verificar se o arquivo da chave privada existe
                caminho_chave_privada = os.path.join(diretorio_chaves, f"{email}_privada.pem")
                if os.path.exists(caminho_chave_privada):
                    # ler a chave privada encriptada do arquivo correspondente ao email
                    with open(caminho_chave_privada, "rb") as arquivo_privado:
                        chave_privada = arquivo_privado.read()
                else:
                    chave_privada = None

                # Verificar se o arquivo da chave pública existe
                caminho_chave_publica = os.path.join(diretorio_chaves, f"{email}_publica.pem")
                if os.path.exists(caminho_chave_publica):
                    # ler a chave pública encriptada do arquivo correspondente ao email
                    with open(caminho_chave_publica, "rb") as arquivo_publico:
                        chave_publica = arquivo_publico.read()
                else:
                    chave_publica = None
                
                return chave_privada, chave_publica
        raise ValueError("E-mail não encontrado")

def listar_pares_chaves():
    # Exibir todos os pares de chaves na lista
    with open("lista_emails.txt", "r") as arquivo:
        for email in arquivo:
            email = email.strip()
            print(f"Email: {email}")
            # Listar a chave pública
            with open(os.path.join(diretorio_chaves, f"{email}_publica.pem"), "rb") as arquivo_publico:
                chave_publica = arquivo_publico.read()
                print("Chave Pública:")
                print(chave_publica.decode('utf-8'))

            # Listar a chave privada
            with open(os.path.join(diretorio_chaves, f"{email}_privada.pem"), "rb") as arquivo_privado:
                chave_privada = arquivo_privado.read()
                print("Chave Privada:")
                print(chave_privada.decode('utf-8'))

def gerenciar_chaves():
    menu = '''
    1 - Pesquisar par de chaves
    2 - Remover par de chaves
    3 - Voltar
    '''

    while True:
        print(menu)
        x = int(input())
        if (x == 3):
            break
        if (x == 1):
            while(True):
                email = input("Digite o email: ")
                try:
                    chave_privada, chave_publica = pesquisar_chaves_por_email(email)
                    if chave_privada:
                        print("Chave privada:")
                        print(chave_privada.decode('utf-8'))
                    if chave_publica:
                        print("Chave pública:")
                        print(chave_publica.decode('utf-8'))
                    break
                except ValueError as e:
                    print(e)
                    print("Por favor, insira um e-mail válido.\n")
