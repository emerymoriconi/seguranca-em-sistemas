from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import hashlib

# onde as chaves serão armazenadas
diretorio_chaves = "chaves/"

lista_emails = []

def gerar_par_chaves(email, tamanho_chave=2048, senha=None):

    chave = RSA.generate(tamanho_chave)
    chave_privada = chave.export_key()
    chave_publica = chave.publickey().export_key()
    
    '''with open("private.pem", "wb") as f:
        f.write(chave_privada)

    with open("receiver.pem", "wb") as f:
        f.write(chave_publica)'''

    
    # salvar a chave privada em um arquivo com o nome do email, protegida por senha
    senha = input("Digite uma senha para proteger a chave privada: ")
    '''
    # derivar uma chave de criptografia a partir da senha
    chave_derivada = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), b'salt', 100000)
    # cria um objeto de cifra AES
    cipher_aes = AES.new(chave_derivada, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(chave_privada)

    # Cria o diretório se ele não existir
    os.makedirs(diretorio_chaves, exist_ok=True)

    with open(os.path.join(diretorio_chaves, f"{email}_privada.enc"), "wb") as arquivo_privado:
        for x in (cipher_aes.nonce, tag, ciphertext):
            arquivo_privado.write(x)
    '''
    
    with open(os.path.join(diretorio_chaves, f"{email}_privada.pem"), "wb") as f:
        if senha:
            f.write(chave.export_key(passphrase=senha, pkcs=8, protection="scryptAndAES128-CBC"))
        else:
            f.write(chave.export_key())

    # salvar a chave pública em um arquivo com o nome do email
    with open(os.path.join(diretorio_chaves, f"{email}_publica.pem"), "wb") as arquivo_publico:
        arquivo_publico.write(chave_publica)

    # adicionar o email à lista de emails
    lista_emails.append(email)
    return chave_privada, chave_publica

def pesquisar_chaves_por_email(email):
    # verificar se o email está na lista de emails
    if email not in lista_emails:
        raise ValueError("E-mail não encontrado")
    
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


def listar_pares_chaves():
    # Exibir todos os pares de chaves na lista
    for email in lista_emails:
        print(f"Email: {email}")
        # Listar a chave pública
        with open(os.path.join(diretorio_chaves, f"{email}_publica.pem"), "rb") as arquivo_publico:
            chave_publica = arquivo_publico.read()
            print("Chave Pública:")
            print(chave_publica.decode('utf-8'))

        # Listar a chave privada encriptada
        with open(os.path.join(diretorio_chaves, f"{email}_privada.pem"), "rb") as arquivo_privado:
            print("Chave Privada (encriptada na tela):")
            print(arquivo_privado.read())

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
                        print(chave_publica)
                    break
                except ValueError as e:
                    print(e)
                    print("Por favor, insira um e-mail válido.\n")

