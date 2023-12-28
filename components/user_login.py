import tkinter as tk
from tkinter import messagebox
import os
#
if not os.path.exists("./files"):#Confirma se o path existe, cria se nao
    os.mkdir("files")
    ficheiro = open("./files/users.txt","w")#criar ficheiro
    ficheiro.write("1;adm;12345\n")#criar conta adm
    ficheiro.close()
#



class login:
        def ler_infoUsers(self):
            users = []
            i = 0
            ficheiro = open("./files/users.txt","r")
            linhas = ficheiro.readlines()
            for linha in linhas:
                users.append([])
                linha = linha.split(";")
                linha[2] = linha[2].replace("\n","")
                for j in range(3):
                    users[i].append(linha[j])
                i+= 1
            ficheiro.close()
            return users


        def fazer_login(self):
            # Verificação do login
            users = self.ler_infoUsers()
            for i in range(len(users)):
                if str(self.user_email.get()) == str(users[i][1].strip()) and str(self.user_senha.get()) == str(users[i][2].strip()):
                    messagebox.showinfo("Login","Login Bem Sucedido")
                    self.login_window.destroy()
                    return
            messagebox.showerror("Login Invalido","Senha ou Email incorretos")
                

        def __init__(self):

            self.login_window = tk.Toplevel()  # Cria uma nova janela
            self.login_window.title("My Photos - Login")

            largura_janela = 1000
            altura_janela = 600

            # Dimensões da janela
            largura_tela = self.login_window.winfo_screenwidth()
            altura_tela = self.login_window.winfo_screenheight()

            # Calcula as coordenadas para colocar o contéudo ao centro
            posicao_x = (largura_tela - largura_janela) // 2
            posicao_y = (altura_tela - altura_janela) // 2

            # Define a geometria da janela com as coordenadas calculadas
            self.login_window.geometry("{0}x{1}+{2}+{3}".format(largura_janela, altura_janela, posicao_x, posicao_y))

            # Cria uma frame para organizar os elementos centralizados
            frame_centralizado = tk.Frame(self.login_window)
            frame_centralizado.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            # Cria o rótulo e entrada para o email dentro da frame centralizada
            label_email = tk.Label(frame_centralizado, text="Email:")
            label_email.pack()
            self.user_email = tk.StringVar()
            entry_email = tk.Entry(frame_centralizado, textvariable=self.user_email)
            entry_email.pack()

            # Cria o rótulo e entrada para a senha dentro da frame centralizada
            label_senha = tk.Label(frame_centralizado, text="Senha:")
            label_senha.pack()
            self.user_senha = tk.StringVar()
            entry_senha = tk.Entry(frame_centralizado, show="*", textvariable=self.user_senha)  # Para esconder a senha
            entry_senha.pack()

            # Botão de login dentro do frame centralizado
            botao_login = tk.Button(frame_centralizado, text="Login", command=self.fazer_login)
            botao_login.pack()

            self.login_window.mainloop()  # Garante o loop principal da janela de login


def criar_janela_login():
    login()