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
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)             # ATIVAR DEPOIS !!!

        self.geometry()

        self.container = tk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True) # Configura o comportamento do Frame (self.container) dentro da janela principal (self.root), assegurando que o Frame ocupe e se ajuste dinamicamente ao tamanho da janela.

        self.create_sidebar()


        self.menu = Menu(self)
        self.current = HomePage(self)
        self.root.mainloop()


    def create_sidebar(self):
        sidebar = tk.Frame(self.container, bg="gray", width=200)
        sidebar.pack(fill="y", side="left")

        btn_profile = tk.Button(sidebar, text="Profile", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: self.show(Profile))
        btn_profile.pack(fill="x", padx=5, pady=5)

        btn_profile = tk.Button(sidebar, text="Create Album", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: self.show(Create_AlbumPage))
        btn_profile.pack(fill="x", padx=5, pady=5)

        btn_explore = tk.Button(sidebar, text="Explore", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: self.show(ExplorePage))
        btn_explore.pack(fill="x", padx=5, pady=5)

        btn_notifications = tk.Button(sidebar, text="Notifications", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: self.show(NotificationPage))
        btn_notifications.pack(fill="x", padx=5, pady=5)

    def geometry(self):
        """ Define a geometria da janela principal da aplicação com base no tamanho do ecrã. """

        width = 1280
        height = 720

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
        print("Explore")

    def profile(self):
        print("Profile")

    def create_album(self):
        """ Abre a janela de criação de álbum. """
        self.show(Create_AlbumPage)

    def notifications(self):
        print("Notifications")

class Menu:
    def __init__(self, app):
        """ Inicia o menu e as suas opções.
        Args:
        - app: A instância principal da aplicação. """

        menu = tk.Menu(app.root)
        options = tk.Menu(menu)
        options.add_command(label="Home", command=lambda: app.show(HomePage))
        options.add_command(label="Login", command=lambda: app.show(LoginPage))
        options.add_command(label="Create Account", command=lambda: app.show(CreateAccountPage))

        menu.add_cascade(label="Options", menu=options)
        app.root.config(menu=menu)
# ---------- Home Page ---------------
class HomePage:
    def __init__(self, app):
        """ Inicia o layout da Página Inicial.
        Args:
        - app: A instância principal da aplicação. """

        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # sidebar = tk.Frame(self.frame, bg="gray", width=200)
        # sidebar.pack(fill="y", side="left")

        # btn_profile = tk.Button(sidebar, text="Profile", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: app.show(Profile))
        # btn_profile.pack(fill="x", padx=5, pady=5)

        # btn_profile = tk.Button(sidebar, text="Create Album", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: app.show(Create_AlbumPage))
        # btn_profile.pack(fill="x", padx=5, pady=5)

        # btn_explore = tk.Button(sidebar, text="Explore", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=app.explore)
        # btn_explore.pack(fill="x", padx=5, pady=5)

        # btn_notifications = tk.Button(sidebar, text="Notifications", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=app.notifications)
        # btn_notifications.pack(fill="x", padx=5, pady=5)

    def destroy(self):
        """ Destrói o quadro da Página Inicial para exibir conteúdo dinâmico na abertura de outra janela. """
        self.frame.destroy()

class User_logged:
    def __init__(self,index,mail,senha,first_name,last_name):
        self.mail = mail
        self.autor_index = index
        self.senha = senha
        self.first_name = first_name
        self.last_name = last_name

# ---------- Login Page ---------------
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

        label_senha = tk.Label(self.frame, text="Password:")
        label_senha.pack()

        self.user_senha = tk.StringVar()
        entry_senha = tk.Entry(self.frame, show="*", textvariable=self.user_senha)
        entry_senha.pack()

        botao_login = tk.Button(self.frame, text="Login", command=self.login, width=15)
        botao_login.pack(pady=(20, 0))

        botao_criar_conta = tk.Button(self.frame, text="Create Account", command=lambda: app.show(CreateAccountPage), width=15)
        botao_criar_conta.pack(pady=(5, 20))


    def destroy(self):
        """ Destrói o quadro da Página de Início de Sessão para exibir conteúdo dinâmico na abertura de outra janela. """

        self.frame.destroy()

    def create_file(self):
        """ Cria um ficheiro e escreve dados iniciais se não existir. """

        if not os.path.exists("./files"):
            os.mkdir("files")
            ficheiro = open("./files/users.txt", "w")
            ficheiro.write("1;adm;12345;First;Last\n")  # ID;username;senha
            ficheiro.close()

    def read_InfoUser(self):
        """ Lê informações do utilizador do ficheiro users.txt."""

        self.create_file()
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

    def login(self):
        """ Realiza a ação de início de sessão e verifica as credenciais do utilizador. """
        users = self.read_InfoUser() # Lê os users

        for i in range(len(users)):
            if str(self.user_email.get()) == str(users[i][1].strip()) and str(self.user_senha.get()) == str(users[i][2].strip()):
                messagebox.showinfo("Login", "Successful Login")
                print(u1.mail)
                self.app.show(HomePage)
                self.app.root.update_idletasks()
                return
        messagebox.showerror("Invalid Login", "Wrong Credentials")

# ---------- Create Account Page ---------------
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
        ficheiro = open("./files/users.txt","r+")
        index = len(ficheiro.readlines())+1
        ficheiro.write("%s;%s;%s;%s;%s\n"%(str(index),email, password,first_name,last_name))
        ficheiro.close()
        # Para efeitos de demonstração, apenas apresentar os dados introduzidos numa caixa de mensagem
        messagebox.showinfo("Create Profile", "First Name: {0}\nLast Name: {1}\nEmail: {2}\nPassword: {3}". format(first_name,last_name, email, password))

        self.app.show(HomePage)

class Profile:
    def __init__(self, app):
        """ Inicia o layout do Profile. """

        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.pack(fill=tk.BOTH, expand=True)

        app.create_sidebar()

    def destroy(self):
        """ Destrói o quadro da Página de Criação de Album. """

        self.frame.destroy()


# ---------- Create Album Page ---------------
class Create_AlbumPage:
    def __init__(self, app):
        """ Inicia o layout da Página de Criação de Conta. """
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        #Entry
        tk.Label(self.frame, text="Nome:").pack(pady=5)
        self.album_nome = tk.StringVar()
        self.entry_nome = tk.Entry(self.frame, width=30, textvariable=self.album_nome)
        self.entry_nome.pack(pady=5)

        #Text Box
        tk.Label(self.frame, text="Description:").pack(pady=10)
        self.desc_txt = tk.Text(self.frame, width=50, height=10)
        self.desc_txt.pack(pady=5)

        ctg_frame = tk.LabelFrame(self.frame, text="Categories:", width=260, height=130, relief="sunken")
        ctg_frame.pack(pady=15)

        self.cb_nature = tk.IntVar()
        self.cb_art = tk.IntVar()
        self.cb_cars = tk.IntVar()
        self.cb_food = tk.IntVar()
        self.cb_landscape = tk.IntVar()
        self.cb_others = tk.IntVar()
        self.cb1 = tk.Checkbutton(ctg_frame, text="Nature", variable=self.cb_nature)
        self.cb2 = tk.Checkbutton(ctg_frame, text="Art", variable=self.cb_art)
        self.cb3 = tk.Checkbutton(ctg_frame, text="Cars", variable=self.cb_cars)
        self.cb4 = tk.Checkbutton(ctg_frame, text="Food", variable=self.cb_food)
        self.cb5 = tk.Checkbutton(ctg_frame, text="Landscape", variable=self.cb_landscape)
        self.cb6 = tk.Checkbutton(ctg_frame, text="Others", variable=self.cb_others)
        self.cb1.place(x=35, y=10)
        self.cb2.place(x=35, y=40)
        self.cb3.place(x=35, y=70)
        self.cb4.place(x=150, y=10)
        self.cb5.place(x=150, y=40)
        self.cb6.place(x=150, y=70)

        btn_gravar = tk.Button(self.frame, text="Choose Images and Create Album!", width=30, height=5, command=self.save_and_create_album)
        btn_gravar.pack(pady=10)

    def save_images(self):
        """ Save Images """

        caminhos = filedialog.askopenfilenames(
            title="Select Image",
            initialdir="./images",
            filetypes=(("png files", "*.png"), ("gif files", "*.gif"), ("all files", "*.*")),
        )

        # Cria o diretório de destino baseado na função create_album_path()
        destino_dir = "./Albuns/%s" % self.create_album_path()

        # Verifica se nenhum arquivo foi selecionado, exibe uma mensagem de erro e remove o diretório de destino
        if caminhos == "":
            messagebox.showerror("Error", "No image inserted. Insert at least 1 image!")
            os.rmdir(destino_dir)
        else:
            i = 0
            # Itera sobre os caminhos dos arquivos selecionados
            for caminho in caminhos:
                # Define um novo caminho para a imagem com base no diretório de destino e no índice
                novo_caminho = os.path.join(destino_dir, "{i}.png".format(i))
                i += 1

                # Abre a imagem selecionada com o módulo PIL e salva-a no novo caminho
                imagem_pil = Image.open(caminho)
                imagem_pil.save(novo_caminho)
                os.mkdir("./Albuns")

        # Obtém o índice para o novo álbum com base no número de pastas presentes em "./Albuns"
        index = len(os.listdir("./Albuns"))+1

        # Cria um novo diretório para o álbum
        novo_album_dir=os.path.join("./Albuns",str(index))

        # Retorna o índice do novo álbum
        return index

    def save_file_album(self,nome,desc,Categorias,data,user,index):
        """ Cria um diretório para os arquivos do álbum se não existir """

        if not os.path.exists("./files/Albuns"): # Confirma se o path existe, cria se nao

            # Abre o arquivo de texto onde serão registradas informações do álbum
            ficheiro = open("./files/Albuns","a")
            ficheiro.write(index+";"+nome+";"+desc+";"+Categorias+";"+data+";"+user+"\n")
            ficheiro.close()


    def save_and_create_album(self):
        """ Guarda Imagens e cria um album """
        index = self.save_images()  # Chama save_images diretamente para obter o índice
        data = date.datetime.now()
        user = u1.autor_index()
        Categorias= self.Categorias = str(self.cb_nature.get()) + str(self.cb_art.get()) + str(self.cb_cars.get()) + str(self.cb_food.get()) + str(self.cb_landscape.get()) + str(self.cb_others.get())
        user = "adm"
        self.save_file_album(self.entry_nome.get(), self.desc_txt.get(),Categorias, data.strftime("%d/%m/%Y"), user, index)


    def destroy(self):
        """ Destrói o quadro da Página de Criação de Album. """

        self.frame.destroy()


# ---------- Explore Page ---------------
class ExplorePage:
    def __init__(self,app):
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


# ---------- Notification Page ---------------
class NotificationPage:
    def __init__(self,app):
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)



u1 = User_logged("0","user","","","")
app = App()

#     def create_album_path(self):
#         """ Cria uma pasta para o álbum se não existir """
#         if not os.path.exists("./Albuns"): # Confirma se o path existe, cria se nao

#     def create_album_path(self):
#         """ Cria uma pasta para o álbum se não existir """
#         if not os.path.exists("./Albuns"): # Confirma se o path existe, cria se nao

#     def cria_caminho_album(self):
#         """
#             Cria uma pasta para o album
#         """
#         if not os.path.exists("./Albuns"):#Confirms if the path exists, creates it if not
#             os.mkdir("./Albuns")
#         index = len(os.listdir("./Albuns"))+1#read how many albums you have and create the new index
#         novo_album_dir=os.path.join("./Albuns",str(index))#make the path for the new album
#         os.mkdir(novo_album_dir)
#         return index#return index

#     def guardar_album_ficheiro(self,nome,desc,Categorias,data,user,index):
#         if not os.path.exists("./files/Albuns"):#Confirms if the path exists, creates it if not
#             os.mkdir("./files/Albuns")
#         ficheiro = open("./files/Albuns","a")
#         ficheiro.write(index+";"+nome+";"+desc+";"+Categorias+";"+data+";"+user+"\n")
#         ficheiro.close()

#     def guardar(self):
#         """
#             Guarda Imagens e cria um album
#         """
#         index = self.cria_caminho_album()
#         self.save_images(index)
#         data = date.datetime.now() #get data
#         user = "user"
#         #user = u1.autor_index() #get name
#         #user = Login().login() #recolher nome do autor3
#         self.guardar_album_ficheiro(self.entry_nome.get(),self.desc_txt.get(),self.Categorias,data.strftime("%d/%m/%Y"),user,index)#guarda dados

#     def add_img(self,index):
#         print

#     def remove_img(self,index):
#         print

#     def change_title(self,index):
#         print

#     def chage_desc(self,index):
#         print

#     def destroy(self):
#         """ Destrói o quadro da Página de Criação de Album. """

#         self.frame.destroy()
