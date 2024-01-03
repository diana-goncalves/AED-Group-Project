import tkinter as tk
from tkinter import messagebox,filedialog
from PIL import Image, ImageTk
import os
import datetime as date


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
#####################################################################################################################################
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
#####################################################################################################################################
class HomePage:
    def __init__(self, app):
        """ Inicia o layout da Página Inicial.
        Args:
        - app: A instância principal da aplicação. """

        print(u1.mail)

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
#####################################################################################################################################

class User_logged:
    def __init__(self,index,mail,senha,first_name,last_name):
        self.mail = mail
        self.autor_index = index
        self.senha = senha
        self.first_name = first_name
        self.last_name = last_name

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
            ficheiro.write("1;adm;12345;First;Last\n")  # ID;username;senha
            ficheiro.close()

    def ler_infoUsers(self):
        """ Lê informações do utilizador do ficheiro users.txt."""

        self.criar_ficheiro()
        #index;email;pass;firstname;surname
        users = []
        i = 0
        ficheiro = open("./files/users.txt", "r")
        linhas = ficheiro.readlines()
        for linha in linhas:
            users.append([])
            linha = linha.split(";")
            linha[4] = linha[4].replace("\n", "")
            for j in range(5):
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
                print(u1.mail)
                #u1 = User_logged(users[i][0].strip(),users[i][1].strip(),users[i][2].strip(),users[i][3].strip(),users[i][4].strip())
                u1.mail = users[i][1].strip()
                print(u1.mail)
                self.app.show(HomePage)
                return
        messagebox.showerror("Invalid Login", "Wrong Credentials")
#####################################################################################################################################
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
#####################################################################################################################################
class Create_AlbumPage:
    def __init__(self, app):
        """ Inicia o layout da Página de Criação de Conta. """
        self.create_album = tk.Tk()
        self.create_album = tk.Frame(app.container)
        self.create_album.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


        tk.Label(self.create_album,text="Nome:").pack(pady=5)
        self.album_nome = tk.StringVar()
        self.entry_nome = tk.Entry(self.create_album, width=30, textvariable=self.album_nome)
        self.entry_nome.pack(pady=5)

        tk.Label(self.create_album,text="Descrição:").pack(pady=10)
        self.desc_txt = tk.Text(self.create_album, width=50, height=10)
        self.desc_txt.pack(pady=5)

        cat_frame = tk.LabelFrame(text="Categorias:", width=260,height=130, relief="sunken")
        cat_frame.pack(pady=15)

        self.cb_natur = tk.IntVar()
        self.cb_arte = tk.IntVar()
        self.cb_carros = tk.IntVar()
        self.cb_comida = tk.IntVar()
        self.cb_paisagem = tk.IntVar()
        self.cb_outros = tk.IntVar()

        self.cb1 = tk.Checkbutton(cat_frame, text="Natureza",variable = self.cb_natur)
        self.cb2 = tk.Checkbutton(cat_frame, text="Arte",variable = self.cb_arte)
        self.cb3 = tk.Checkbutton(cat_frame, text="Carros",variable = self.cb_carros)
        self.cb4 = tk.Checkbutton(cat_frame, text="Comida",variable = self.cb_comida)
        self.cb5 = tk.Checkbutton(cat_frame, text="Paisagem",variable = self.cb_paisagem)
        self.cb6 = tk.Checkbutton(cat_frame, text="Outros...",variable = self.cb_outros)
        self.cb1.place(x=35,y=10)
        self.cb2.place(x=35,y=40)
        self.cb3.place(x=35,y=70)
        self.cb4.place(x=150,y=10)
        self.cb5.place(x=150,y=40)
        self.cb6.place(x=150,y=70)
        self.Categorias = str(self.cb_natur.get())+str(self.cb_arte.get())+str(self.cb_carros.get())+str(self.cb_comida.get())+str(self.cb_paisagem.get())+str(self.cb_outros.get())


        btn_gravar = tk.Button(self.create_album, text="Escolher Imagens e Criar Album!",width=30, height=5, command=self.guardar)
        btn_gravar.pack(pady=10)
        self.create_album.mainloop()

    def guardar_imagens(index):
        caminhos= filedialog.askopenfilenames(title="Select Image", initialdir="./images",
                                            filetypes=(("png files","*.png"),("gif files","*.gif"), ("all files","*.*")))
        destino_dir = "./Albuns/%s"%index
        if caminhos == "":
            messagebox.showerror("Error","Nenhuma imagem inserir\nIntroduza pelo menos 1 Imagem!")
            os.rmdir(destino_dir)
        else:
            i=0
            for caminho in caminhos:
                novo_caminho = os.path.join(destino_dir,"%s.png"%i)
                i += 1
                imagem_pil = Image.open(caminho)
                imagem_pil.save(novo_caminho)
    def cria_caminho_album(self):
        """
            Cria uma pasta para o meu album
        """
        if not os.path.exists("./Albuns"):#Confirma se o path existe, cria se nao
            os.mkdir("./Albuns")
        index = len(os.listdir("./Albuns"))+1
        novo_album_dir=os.path.join("./Albuns",str(index))
        os.mkdir(novo_album_dir)
        return index

    def guardar_album_ficheiro(self,nome,desc,Categorias,data,user,index):
        if not os.path.exists("./files/Albuns"):#Confirma se o path existe, cria se nao
            os.mkdir("./files/Albuns")
        ficheiro = open("./files/Albuns","a")
        ficheiro.write(index+";"+nome+";"+desc+";"+Categorias+";"+data+";"+user+"\n")
        ficheiro.close()

    def guardar(self):
        """
            Guarda Imagens e cria um album
        """
        index = self.cria_caminho_album()
        self.guardar_imagens(index)
        data = date.datetime.now() #recolher data 
        user = u1.autor_index() #recolher nome do autor 
        self.guardar_album_ficheiro(self.entry_nome.get(),self.desc_txt.get(),self.Categorias,data.strftime("%d/%m/%Y"),user,index)

    def destroy(self):
        """ Destrói o quadro da Página de Criação de Album. """

        self.frame.destroy()

global u1
u1 = User_logged("0","user","","","")
app = App()