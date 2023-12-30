import tkinter as tk
from tkinter import messagebox

import os

class App:
    def __init__(self):
        """ Inicia a janela principal da aplicação e as configurações básicas. """
        self.root = tk.Tk()
        self.root.title("My Photos")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.geometry()

        self.container = tk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True) # Configura o comportamento do Frame (self.container) dentro da janela principal (self.root), assegurando que o Frame ocupe e se ajuste dinamicamente ao tamanho da janela.


        self.menu = Menu(self)
        self.current = HomePage(self)
        self.root.mainloop()

    def geometry(self):
        """ Define a geometria da janela principal da aplicação com base no tamanho do ecrã. """

        width = 1000
        height = 600

        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()

        x = (screenwidth - width) // 2
        y = (screenheight - height) // 2

        self.root.geometry("{0}x{1}+{2}+{3}".format(width, height, x, y))

    def on_closing(self):
        """ Pede confirmação para fechar a aplicação e fecha a janela após confirmação. """

        if messagebox.askokcancel("Close", "Do you want to close My Photos?"):
            self.root.destroy()

    def show(self, page):
        """ Destroi a página atual e mostra a página especificada. """

        self.current.destroy()
        self.current = page(self)

    def explore(self):
        print("Explorar")

    def profile(self):
        print("Perfil")

    def notifications(self):
        print("Notifications")

class Menu:
    def __init__(self, app):
        """ Inicia o menu e as suas opções.
        Args:
        - app: A instância principal da aplicação. """

        menu = tk.Menu(app.root)

        options = tk.Menu(menu)
        options.add_command(label="Explore", command=app.explore)
        options.add_command(label="Profile", command=app.profile)
        options.add_command(label="Notifications", command=app.notifications)
        options.add_command(label="Login", command=lambda: app.show(LoginPage))

        menu.add_cascade(label="Options", menu=options)
        app.root.config(menu=menu)

class HomePage:
    def __init__(self, app):
        """ Inicia o layout da Página Inicial.
        Args:
        - app: A instância principal da aplicação. """

        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.pack(fill=tk.BOTH, expand=True)

        sidebar = tk.Frame(self.frame, bg="gray", width=200)
        sidebar.pack(fill="y", side="left")

        btn_profile = tk.Button(sidebar, text="Profile", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=app.profile)
        btn_profile.pack(fill="x", padx=5, pady=5)

        btn_explore = tk.Button(sidebar, text="Explore", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=app.explore)
        btn_explore.pack(fill="x", padx=5, pady=5)

        btn_notifications = tk.Button(sidebar, text="Notifications", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=app.notifications)
        btn_notifications.pack(fill="x", padx=5, pady=5)

    def destroy(self):
        """ Destrói o quadro da Página Inicial para exibir conteúdo dinâmico na abertura de outra janela. """
        self.frame.destroy()

class LoginPage:
    def __init__(self, app):
        """ Inicia o layout da Página de Início de Sessão. """

        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_email = tk.Label(self.frame, text="Email:")
        label_email.pack()
        self.user_email = tk.StringVar()
        entry_email = tk.Entry(self.frame, textvariable=self.user_email)
        entry_email.pack()

        label_senha = tk.Label(self.frame, text="Senha:")
        label_senha.pack()
        self.user_senha = tk.StringVar()
        entry_senha = tk.Entry(self.frame, show="*", textvariable=self.user_senha)
        entry_senha.pack()

        botao_login = tk.Button(self.frame, text="Login", command=self.fazer_login, width=15)
        botao_login.pack(pady=(20, 0))

        botao_criar_conta = tk.Button(self.frame, text="Create Account", command=lambda: app.show(CreateAccountPage))
        botao_criar_conta.pack(pady=(5, 20))

    def destroy(self):
        """ Destrói o quadro da Página de Início de Sessão para exibir conteúdo dinâmico na abertura de outra janela. """

        self.frame.destroy()

    def criar_ficheiro(self):
        """ Cria um ficheiro e escreve dados iniciais se não existir. """

        if not os.path.exists("./files"):
            os.mkdir("files")
            ficheiro = open("./files/users.txt", "w")
            ficheiro.write(";12345\n")
            ficheiro.close()

    def ler_infoUsers(self):
        """ Lê informações do utilizador do ficheiro users.txt."""

        self.criar_ficheiro()

        users = []
        i = 0
        ficheiro = open("./files/users.txt", "r")
        linhas = ficheiro.readlines()
        for linha in linhas:
            users.append([])
            linha = linha.split(";")
            linha[2] = linha[2].replace("\n", "")
            for j in range(3):
                users[i].append(linha[j])
            i += 1
        ficheiro.close()
        return users

    def fazer_login(self):
        """ Realiza a ação de início de sessão e verifica as credenciais do utilizador. """
        users = self.ler_infoUsers()

        for i in range(len(users)):
            if str(self.user_email.get()) == str(users[i][1].strip()) and str(self.user_senha.get()) == str(users[i][2].strip()):
                messagebox.showinfo("Login", "Successful Login")
                self.app.show(HomePage)
                return

        messagebox.showerror("Invalid Login", "Wrong Credentials")

class CreateAccountPage:
    def __init__(self, app):
        """ Inicia o layout da Página de Criação de Conta. """

        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Labels and Entries
        tk.Label(self.frame, text="First Name:").grid(row=0, column=0, sticky="w")
        self.entry_first_name = tk.Entry(self.frame)
        self.entry_first_name.grid(row=0, column=1)

        tk.Label(self.frame, text="Last Name:").grid(row=1, column=0, sticky="w")
        self.entry_last_name = tk.Entry(self.frame)
        self.entry_last_name.grid(row=1, column=1)

        tk.Label(self.frame, text="Email:").grid(row=2, column=0, sticky="w")
        self.entry_email = tk.Entry(self.frame)
        self.entry_email.grid(row=2, column=1)

        tk.Label(self.frame, text="Password:").grid(row=3, column=0, sticky="w")
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=3, column=1)

        # Create Account Button
        btn_create_account = tk.Button(self.frame, text="Create Account", command=self.create_account)
        btn_create_account.grid(row=4, columnspan=2, pady=10)

    def destroy(self):
        """ Destrói o quadro da Página de Criação de Conta. """

        self.frame.destroy()

    def create_account(self):
        """ Cria uma conta de utilizador com base nas informações inseridas. """

        # Obter valores dos campos de entrada
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        # Processar a criação da conta aqui
        # Para efeitos de demonstração, apenas apresentar os dados introduzidos numa caixa de mensagem
        messagebox.showinfo("Create Profile", "First Name: {0}\nLast Name: {1}\nEmail: {2}\nPassword: {3}". format(first_name,last_name, email, password))

        self.app.show(HomePage)

app = App()
