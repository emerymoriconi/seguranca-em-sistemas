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

#lista_emails = []

def gerar_par_chaves(email, tamanho_chave=2048):
    par_chaves = RSA.generate(tamanho_chave)

    chave_privada = par_chaves.export_key()
    chave_publica = par_chaves.public_key().export_key()

    # salvar a chave privada em um arquivo com o nome do email, protegida por senha
    senha = input("Digite uma senha para proteger a chave privada: ")
    # derivar uma chave de criptografia a partir da senha
    chave_derivada = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), b'salt', 100000)

    # cria um objeto de cifra AES
    cipher_aes = AES.new(chave_derivada, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(chave_privada)

    with open(os.path.join(diretorio_chaves, f"{email}_privada.enc"), "wb") as arquivo_privado:
        for x in (cipher_aes.nonce, tag, ciphertext):
            arquivo_privado.write(x)

    # salvar a chave pública em um arquivo com o nome do email
    with open(os.path.join(diretorio_chaves, f"{email}_publica.pem"), "wb") as arquivo_publico:
        arquivo_publico.write(chave_publica)

    # adicionar o email ao arquivo de lista de emails
    with open("lista_emails.txt", "a") as arquivo:
        arquivo.write(email + "\n")

def pesquisar_chaves_por_email(email):
    # verificar se o email está na lista de emails
    with open("lista_emails.txt", "r") as arquivo:
        for linha in arquivo:
            if email in linha:
                # ler a chave privada encriptada do arquivo correspondente ao email
                with open(os.path.join(diretorio_chaves, f"{email}_privada.enc"), "rb") as arquivo_privado:
                    nonce, tag, ciphertext = [arquivo_privado.read(x) for x in (16, 16, -1)]

                    senha = input("Digite a senha para descriptografar a chave privada: ")

                    # derivar a chave de criptografia a partir da senha
                    chave_derivada = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), b'salt', 100000)

                    cipher_aes = AES.new(chave_derivada, AES.MODE_EAX, nonce)

                    try:
                        # decriptação da chave privada e verificação da sua integridade usando a tag
                        chave_privada = cipher_aes.decrypt_and_verify(ciphertext, tag)
                        # Retornar a chave pública e a chave privada decriptada
                        with open(os.path.join(diretorio_chaves, f"{email}_publica.pem"), "rb") as arquivo_publico:
                            chave_publica = arquivo_publico.read()
                        
                        print("Chave Pública:")
                        print(chave_publica.decode('utf-8'))

                        print("Chave Privada:")
                        print(chave_privada.decode('utf-8'))

                        return chave_publica, chave_privada
                    except ValueError:
                        print('Senha incorreta.')
                        return None, None
        print('O email não foi encontrado.')
        return None, None

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

            # Listar a chave privada encriptada
            with open(os.path.join(diretorio_chaves, f"{email}_privada.enc"), "rb") as arquivo_privado:
                print("Chave Privada (encriptada na tela):")
                print(arquivo_privado.read())

