import tkinter as tk
from tkinter import filedialog
from cripto import *
from import_export import *
from import_export import importar_chave_publica

janela = tk.Tk()

def email_valido(email):
    return re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)

class pop_up_email_invalido:
    def __init__(self):
        self.janela = tk.Toplevel()
        self.janela.title("Email inválido")
        self.janela.geometry("400x200")
        self.janela.resizable(False, False)
        self.janela.configure(bg="#292929")

        self.janela.mainloop()

    def frames(self):
        self.frame = tk.Frame(self.janela, bg="white")
        self.frame.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.35)

    def botoes(self):
        self.botao1 = tk.Button(self.frame, text="Ok", bg="#292929", fg="white", command=self.janela.destroy)
        self.botao1.place(relx=0.1, rely=0.1, relwidth=0.38, relheight=0.2)

    def campos(self):
        self.email = tk.Label(self.janela, text="Email inválido. Por favor, insira um email válido.", bg="#292929", fg="white")
        self.email.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.1)


class janela_importar_chaves:
    def __init__(self, email):
        if (not self.email_valido(email)):
            pop_up_email_invalido()
            return
        else:
            self.janela = tk.Toplevel()
            self.janela.title("Importar chaves")
            self.janela.geometry("800x600")
            self.janela.resizable(False, False)
            self.janela.configure(bg="#292929")

            self.janela.mainloop()

    def frames(self):
        self.frame = tk.Frame(self.janela, bg="white")
        self.frame.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.35)

    def botoes(self):
        # Botão para abrir uma nova janela caso o usuário confirme o email e este seja válido, passando o email como parâmetro da função jane
        self.botao1 = tk.Button(self.frame, text="Confirmar", bg="#292929", fg="white", command=self.janela_importar_chaves(self.email))
        self.botao1.place(relx=0.1, rely=0.1, relwidth=0.38, relheight=0.2)

    def campos(self):
        # Campo de email, informando ao usuário que ele deve digitar um email
        self.email = tk.Label(self.janela, text="Digite o email associado ao par de chaves que deseja importar:", bg="#292929", fg="white")
        self.email.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.1)

class JanelaImportarChaves:
    def __init__(self):
        self.janela = tk.Toplevel()
        self.tela()
        self.frames()
        self.botoes()
        self.campos()
        self.janela.mainloop()

    def tela(self):
        janela.title("Gerenciador de chaves")
        janela.geometry("800x600")
        janela.resizable(False, False)
        janela.configure(bg="#292929")

    def frames(self):
        self.frame = tk.Frame(self.janela, bg="white")
        self.frame.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.35)

    def botoes(self):
        # Botão para abrir uma nova janela caso o usuário confirme o email e este seja válido
        self.botao1 = tk.Button(self.frame, text="Confirmar", bg="#292929", fg="white", command=self.janela_importar_chaves)
        self.botao1.place(relx=0.1, rely=0.1, relwidth=0.38, relheight=0.2)

    def campos(self):
        # Campo de email, informando ao usuário que ele deve digitar um email
        self.email = tk.Label(self.janela, text="Digite o email associado ao par de chaves que deseja importar:", bg="#292929", fg="white")
        self.email.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.1)
        
class Aplicacao:
    def __init__(self):
        self.frames()
        self.botoes()
        self.titulo()
        self.tela()
        janela.mainloop()
        
    def tela(self):
        janela.title("Gerenciador de chaves")
        janela.geometry("800x600")
        janela.resizable(False, False)
        janela.configure(bg="#292929")

    def frames(self):
        self.frame = tk.Frame(janela, bg="white")
        self.frame.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.35)

    def botoes(self):

        # Botão de importar chaves
        self.botao1 = tk.Button(self.frame, text="Importar chaves", bg="#292929", fg="white", command=JanelaImportarChaves)
        self.botao1.place(relx=0.1, rely=0.1, relwidth=0.38, relheight=0.2)

        # Botão de exportar chaves
        self.botao2 = tk.Button(self.frame, text="Exportar chaves", bg="#292929", fg="white")
        self.botao2.place(relx=0.52, rely=0.1, relwidth=0.38, relheight=0.2)

        # Botão de gerenciar chaves
        self.botao3 = tk.Button(self.frame, text="Gerenciar chaves", bg="#292929", fg="white")
        self.botao3.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.2)

        # Botão de criptografar mensagem
        self.botao4 = tk.Button(self.frame, text="Criptografar mensagem", bg="#292929", fg="white")
        self.botao4.place(relx=0.1, rely=0.7, relwidth=0.38, relheight=0.2)

        # Botão de descriptografar mensagem
        self.botao5 = tk.Button(self.frame, text="Descriptografar mensagem", bg="#292929", fg="white")
        self.botao5.place(relx=0.52, rely=0.7, relwidth=0.38, relheight=0.2)

        # Botão de saída
        self.botao6 = tk.Button(janela, text="Sair", bg="#292929", fg="white")
        self.botao6.place(relx=0.45, rely=0.8, relwidth=0.1, relheight=0.05)

    def titulo(self):
        self.titulo = tk.Label(janela, text="Gerenciador de chaves e criptografia - AKM", bg="#292929", fg="white", font=("Arial", 15))
        self.titulo.place(relx=0.15, rely=0.2, relwidth=0.70, relheight=0.1)

    
Aplicacao()