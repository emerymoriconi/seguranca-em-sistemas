from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import Padding
from getpass import getpass
from tkinter import Tk
from tkinter import filedialog
import os
import base64
import re

# onde as chaves serão armazenadas
diretorio_chaves = "chaves/"

# verifica se o diretório existe e cria-o se não existir
if not os.path.exists(diretorio_chaves):
    os.makedirs(diretorio_chaves)

def selecionar_email():
    while True:
        emails = listar_pares_chaves()
        escolha = input("Escolha um email pelo número: ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(emails):
            email = emails[int(escolha) - 1]
            break
        else:
            print("Escolha inválida. Tente novamente.")
    print("Email escolhido: ", email)
    return email

def verifica_email():
    while (True):
        email = input("Forneça o email associado ao par de chaves: ")
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            print("Email inválido.")
            continue
        else:
            break
    return email

def criptografar(email, arquivo):
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
    
    if criptografar_mensagem(email, arquivo, usar_chave_privada):
        return True
    


    
def salvar_chave_privada(email, chave, senha):
    with open(os.path.join(diretorio_chaves, f"{email}_privada.pem"), "wb") as arquivo_privado:
        arquivo_privado.write(chave.export_key(passphrase=senha, pkcs=8, protection="scryptAndAES128-CBC"))

def salvar_chave_publica(email, chave):
    with open(os.path.join(diretorio_chaves, f"{email}_publica.pem"), "wb") as arquivo_publico:
        arquivo_publico.write(chave.publickey().export_key())

def adicionar_email(email):
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

def gerar_par_chaves(tamanho_chave=2048):

    email = verifica_email()

    chave = RSA.generate(tamanho_chave)
    chave_privada = chave.export_key()
    chave_publica = chave.publickey().export_key()
    
    # salvar a chave privada em um arquivo com o nome do email, protegida por senha
    senha = input("Digite uma senha para proteger a chave privada: ")
    while not senha.strip():
        print("Senha não pode ser vazia. Por favor, tente novamente.")
        senha = input("Digite uma senha para proteger a chave privada: ")
    
    salvar_chave_privada(email, chave, senha)

    # salvar a chave pública em um arquivo com o nome do email
    salvar_chave_publica(email, chave.publickey())

    # adicionar o email ao arquivo de lista de emails, evitando duplicatas
    adicionar_email(email)
    
    # retorno das chaves
    return chave_privada, chave_publica

def pesquisar_chaves_por_email(email, usar_lista):

    if usar_lista:
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
                    
                    return chave_publica, chave_privada
            # verifica se o e-mail não encontrado está na lista de e-mails e apaga-o da lista
            with open("lista_emails.txt", "r") as arquivo:
                emails = [linha.strip() for linha in arquivo]
                if email in emails:
                    emails.remove(email)
            raise ValueError("E-mail não encontrado")
    else:
        # verificar se há ao menos uma instância de chave privada ou pública salva localmente
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
            
            return chave_publica, chave_privada


def listar_pares_chaves():
    # Verificar se o arquivo existe e criá-lo se não existir
    if not os.path.exists("lista_emails.txt"):
        open("lista_emails.txt", "w").close()

    with open("lista_emails.txt", "r") as arquivo:
        emails = [linha.strip() for linha in arquivo]

    if not emails:
        print("Nenhum par de chaves foi gerado até agora.")
        return
    
    # para cada e-mail na lista, verifica se há ao menos uma instância de chave privada ou pública salva localmente
    # caso contrário, apaga o e-mail da lista e do arquivo de emails
    for email in emails:
        chave_publica, chave_privada = pesquisar_chaves_por_email(email, False)
        if chave_privada is None and chave_publica is None:
            emails.remove(email)

    # apagando arquivo de emails e recriando-o com os emails válidos
    os.remove("lista_emails.txt")
    with open("lista_emails.txt", "w") as arquivo:
        for email in emails:
            arquivo.write(email + "\n")

    print("Emails associados aos pares de chaves gerados até agora:")
    for i, email in enumerate(emails, start=1):
        print(f"{i} - {email}")
    return emails



def apagar_par_de_chaves(email):

    with open("lista_emails.txt", "r") as arquivo:
        emails = [linha.strip() for linha in arquivo]

    if email not in emails:
        raise ValueError("E-mail não encontrado.")

    try:
        os.remove(os.path.join(diretorio_chaves, f"{email}_publica.pem"))
        if os.path.exists(os.path.join(diretorio_chaves, f"{email}_privada.pem")):
            os.remove(os.path.join(diretorio_chaves, f"{email}_privada.pem"))

        # Remover o email da lista
        emails.remove(email)

        # Atualizar o arquivo de emails
        with open("lista_emails.txt", "w") as arquivo:
            for email in emails:
                arquivo.write(email + "\n")

    except FileNotFoundError:
        raise ValueError("Arquivos de chave não encontrados para o e-mail fornecido.")

    return "Par de chaves apagado com sucesso!"

def gerenciar_chaves():
    menu = '''
    1 - Pesquisar par de chaves
    2 - Listar pares de chaves
    3 - Remover par de chaves
    4 - Voltar
    '''

    while True:
        print(menu)
        x = int(input())
        if (x == 1):
            while(True):
                email = input("Digite o email: ")
                if email == '0':
                    break
                try:
                    chave_publica, chave_privada = pesquisar_chaves_por_email(email, True)
                    if chave_privada:
                        print("Chave privada:")
                        print(chave_privada.decode('utf-8'))
                    if chave_publica:
                        print("Chave pública:")
                        print(chave_publica.decode('utf-8'))
                    if not chave_privada and not chave_publica:
                        print("Nenhum par de chaves encontrado para o email fornecido.")
                    break
                except ValueError as e:
                    print(e)
                    print("Por favor, insira um e-mail válido ou digite 0 para voltar.\n")
        if (x == 2):
            listar_pares_chaves()
        if (x == 3):
            while(True):
                email = input("Digite o email associado ao par de chaves que deseja remover: ")
                if email == '0':
                    break
                try:
                    print(apagar_par_de_chaves(email))
                    break
                except ValueError as e:
                    print(e)
                    print("Por favor, insira um e-mail válido ou digite 0 para voltar.\n")
        if (x == 4):
            break

def criptografar_mensagem(email, arquivo, usar_chave_privada):
    chave_publica, chave_privada = pesquisar_chaves_por_email(email, True)
    if usar_chave_privada:
        senha = getpass("Digite a senha para desbloquear a chave privada: ")
        try:
            chave = RSA.import_key(chave_privada, passphrase=senha)
            if not chave.has_private():
                print("Senha incorreta.")
                return False
        except ValueError:
            print("Senha incorreta.")
            return False
    else:
        chave = RSA.import_key(chave_publica)
    
    if chave is None:
        print("Não foi possível decriptar a chave privada.")
        return False

    cipher_rsa = PKCS1_OAEP.new(chave)
    try:
        with open(arquivo, "rb") as arquivo:
            mensagem = arquivo.read()
            mensagem_cifrada = cipher_rsa.encrypt(mensagem)

        '''
        # definindo o nome do arquivo para salvar a mensagem cifrada
        while True:
            nome_do_arquivo = input("Digite o nome do arquivo para salvar a mensagem cifrada: ")
            if not nome_do_arquivo.strip():
                print("Nome do arquivo não pode ser vazio.")
                continue
            else:
                break

        # definindo o diretório de exportação
        diretorio_exportacao = input("Forneça o diretório de exportação: ")
        if not os.path.exists(diretorio_exportacao):
            os.makedirs(diretorio_exportacao)
        '''
        # definindo o nome do arquivo para salvar a mensagem cifrada
        while True:
            nome_do_arquivo = filedialog.asksaveasfilename(filetypes=[("Arquivos de texto", "*.txt")])
            if not nome_do_arquivo.strip():
                print("Nome do arquivo não pode ser vazio.")
                continue
            else:
                break

        # salvando a mensagem cifrada no arquivo    
        with open(nome_do_arquivo, "wb") as arquivo_cifrado:
            arquivo_cifrado.write(base64.b64encode(mensagem_cifrada))
            return True
    except ValueError:
        print("A mensagem não pôde ser criptografada com a chave fornecida.")
        return False



def descriptografar_mensagem(email, arquivo_cifrado):
    chave_publica, chave_privada = pesquisar_chaves_por_email(email, True)
    senha = getpass("Digite a senha para desbloquear a chave privada: ")
    try:
        chave = RSA.import_key(chave_privada, passphrase=senha)
    except ValueError:
        print("Senha incorreta.")
        return None
    
    if chave is None:
        print("Não foi possível decriptar a chave privada.")
        return None

    cipher_rsa = PKCS1_OAEP.new(chave)
    try:
        with open(arquivo_cifrado, "rb") as arquivo:
            mensagem_cifrada = base64.b64decode(arquivo.read())
            mensagem = cipher_rsa.decrypt(mensagem_cifrada)
        
        '''
        # definindo o nome do arquivo para salvar a mensagem decifrada
        while True:
            nome_do_arquivo = input("Digite o nome do arquivo para salvar a mensagem decifrada: ")
            if not nome_do_arquivo.strip():
                print("Nome do arquivo não pode ser vazio.")
                continue
            else:
                break

        # definindo o diretório de exportação
        diretorio_exportacao = input("Forneça o diretório de exportação: ")
        if not os.path.exists(diretorio_exportacao):
            os.makedirs(diretorio_exportacao)
        '''

        # definindo o nome do arquivo para salvar a mensagem decifrada
        while True:
            nome_do_arquivo = filedialog.asksaveasfilename(filetypes=[("Arquivos de texto", "*.txt")])
            if not nome_do_arquivo.strip():
                print("Nome do arquivo não pode ser vazio.")
                continue
            else:
                break

        # salvando a mensagem decifrada no arquivo    
        with open(nome_do_arquivo, "wb") as arquivo_decifrado:
            arquivo_decifrado.write(mensagem)
            return True
    except ValueError:
        print("A mensagem não pôde ser descriptografada com a chave fornecida.")
        return False