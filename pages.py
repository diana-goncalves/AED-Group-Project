import tkinter as tk
import tkinter.ttk as ttk
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
        self.user_manager = UserManager()

        self.menu = Menu(self)
        self.current = HomePage(self)

        self.root.mainloop()

    def create_sidebar(self):
        sidebar = tk.Frame(self.container, bg="gray", width=200)
        sidebar.pack(fill="y", side="left")

        btn_profile = tk.Button(sidebar, text="Profile", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command= self.show_profile_page)
        btn_profile.pack(fill="x", padx=5, pady=5)

        btn_profile = tk.Button(sidebar, text="Create Album", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command= self.show_create_album)
        btn_profile.pack(fill="x", padx=5, pady=5)

        btn_explore = tk.Button(sidebar, text="Explore", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: self.show(ExplorePage))
        btn_explore.pack(fill="x", padx=5, pady=5)

        btn_notifications = tk.Button(sidebar, text="Notifications", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command= self.show_notification_page)
        btn_notifications.pack(fill="x", padx=5, pady=5)

        btn_home = tk.Button(sidebar, text="Home", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: self.show(HomePage))
        btn_home.pack(fill="x", padx=5, pady=5)

    def show_create_album(self):
        if user.mail == "user":
            messagebox.showerror("Need Account", "Please log in or create an account to access")
            self.show(HomePage)
        else:
            self.show(CreateAlbumPage)

    def show_profile_page(self):
        if user.mail == "user":
            messagebox.showerror("Need Account", "Please log in or create an account to access")
            self.show(HomePage)
        else:
            self.show(ProfilePage)

    def show_notification_page(self):
        # if user.mail == "user":
        #     messagebox.showerror("Need Account", "Please log in or create an account to access")
        #     self.show(HomePage)
        # else:
        #     self.show(NotificationPage)
        self.show(NotificationPage)

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

    def show_with_Arguments(self, page):
        """ Destroi a página atual e mostra a página especificada. """

        self.current.destroy()
        self.current = page

class Menu:
    def __init__(self, app):
        """ Inicia o menu e as suas opções.
        Args:
        - app: A instância principal da aplicação. """

        menu = tk.Menu(app.root)
        options = tk.Menu(menu)
        options.add_command(label="Home", command=lambda: app.show(HomePage))
        if user.mail == "user":
            options.add_command(label="Login", command=lambda: app.show(LoginPage))
            options.add_command(label="Create Account", command=lambda: app.show(CreateAccountPage))
        else:
            options.add_command(label="Logout", command=lambda: self.logout(app))
        menu.add_cascade(label="Options", menu=options)
        app.root.config(menu=menu)

    def logout(self,app):
        option = messagebox.askquestion("Confirm Logout","Are you sure?")
        if option == "yes":
            user.autor_index = "0"
            user.mail = "user"
            user.senha = ""
            user.first_name = ""
            user.last_name = ""
            app.show(HomePage)

# ---------- Home Page ---------------
class HomePage:
    def __init__(self, app):
        """ Inicia o layout da Página Inicial.
        Args:
        - app: A instância principal da aplicação. """

        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.pack(fill=tk.BOTH, expand=True)
        app.root.title("My Photos - HomePage")
        Menu(self.app)

        # Adiciona um Canvas para o scroll
        canvas = tk.Canvas(self.frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Adiciona uma barra de scroll vertical
        scrollbar = tk.Scrollbar(self.frame, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Conteúdo da HomePage
        self.image_frame = tk.Frame(canvas, width=400, height=100)
        self.image_frame.pack(side="top", pady=5)

        self.displayAlbuns()

        # Configura o Canvas para dar scroll com o rato
        canvas.bind("<Configure>", lambda event, canvas=canvas: self.on_canvas_configure(event, canvas))
        canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

    def on_canvas_configure(self, event, canvas):
        """ Ajusta a região de rolagem do Canvas quando o tamanho do conteúdo é alterado. """
        canvas.configure(scrollregion=canvas.bbox("all"))

    def displayAlbuns(self):
        # Suponho que 'album_path' e 'albuns_list' sejam definidos anteriormente nesta função.
        album_path = "./Albuns"
        albuns_list = os.listdir(album_path)

        row_val = 0
        col_val = 0

        for album_index in albuns_list:
            current_album_path = os.path.join(album_path, album_index)

            # Verifica se é um diretório antes de processar as imagens
            if os.path.isdir(current_album_path):
                data_album = AlbumPage.read_AlbumData(album_index)

                # Verifica se data_album é válido e tem elementos suficientes
                if data_album and len(data_album) >= 7:
                    album_title = AlbumPage.get_album_title(current_album_path)

                    # Aqui, você processa a primeira imagem do álbum para exibição
                    images_dir = [file for file in os.listdir(current_album_path)
                                if os.path.isfile(os.path.join(current_album_path, file)) and file.endswith('.png')]
                    images_dir = [file for file in images_dir if file != '.DS_Store']
                    first_image = images_dir[0] if images_dir else None

                    if first_image:
                        img_path = os.path.join(current_album_path, first_image)
                        img = Image.open(img_path)
                        img = img.resize((240, 240))
                        img_Tk = ImageTk.PhotoImage(img)

                        label = tk.Label(self.image_frame, image=img_Tk, width=240, height=240)
                        label.image = img_Tk
                        label.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nw")
                        label.bind("<Button-1>", lambda event, index=album_index: self.show_album(index))

                        album_header = tk.Frame(self.image_frame)
                        album_header.grid(row=row_val + 1, column=col_val, padx=5, pady=5, sticky="nw")
                        title = tk.Label(album_header, text="{} {} likes".format(album_title, data_album[6]))
                        title.pack(side="left", anchor="w")

                        col_val += 1
                        if col_val >= 3:
                            col_val = 0
                            row_val += 2
                else:
                    print("erro")
                    continue  # Simplesmente pula para o próximo álbum


    def show_album(self, index):
        album_path = os.path.join("./Albuns", index)
        self.app.show_with_Arguments(AlbumPage(self.app,album_path))

    def destroy(self):
        """ Destrói o quadro da Página Inicial para exibir conteúdo dinâmico na abertura de outra janela. """
        self.frame.destroy()

# ---------- User management ---------------
class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        """ Carrega informações dos user do arquivo users.txt """
        if not os.path.exists("./files/users.txt"):
            return
        with open("./files/users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(";")
                user = User_logged(parts[0], parts[1], parts[2], parts[3], parts[4])
                self.users.append(user)

    def save_user(self, user):
        """ Guarda as informações do user no arquivo users.txt """
        with open("./files/users.txt", "a") as file:
            file.write(f"{user.autor_index};{user.mail};{user.senha};{user.first_name};{user.last_name}\n")

    def create_user(self, mail, senha, first_name, last_name):
        """ Cria um novo user e guarda suas informações """
        index = str(len(self.users) + 1)
        user = User_logged(index, mail, senha, first_name, last_name)
        self.users.append(user)
        self.save_user(user)
        return user

class User_logged:
    def __init__(self,index,mail,senha,first_name,last_name):
        self.mail = mail
        self.autor_index = index
        self.senha = senha
        self.first_name = first_name
        self.last_name = last_name
        self.albums = []  # list_images para armazenar os álbuns do user para exibir no ProfilePage

# ---------- Login Page ---------------
class LoginPage:
    def __init__(self, app):
        """ Inicia o layout da Página de Início de Sessão. """
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        app.root.title("My Photos - Login")

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

    def read_InfoFileUsersUser(self):
        """ Lê informações do utilizador do ficheiro users.txt."""

        self.create_file()

        users = []
        with open("./files/users.txt", "r") as ficheiro:
            linhas = ficheiro.readlines()
            for linha in linhas:
                users.append(linha.strip().split(";"))
        return users

    def login(self):
        """ Realiza a ação de início de sessão e verifica as credenciais do utilizador. """
        users = self.read_InfoFileUsersUser()  # Lê os usuários

        for i in range(len(users)):
            if str(self.user_email.get()) == str(users[i][1].strip()) and str(self.user_senha.get()) == str(users[i][2].strip()):
                messagebox.showinfo("Login", "Successful Login")
                # Atualização dos dados do usuário
                user.autor_index = users[i][0].strip()
                user.mail = users[i][1].strip()
                user.senha = users[i][2].strip()
                user.first_name = users[i][3].strip()
                user.last_name = users[i][4].strip()
                #
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
        app.root.title("My Photos - Create Account")

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

    def create_account(self):             # Alterado devido à nova class UserManager !!!!
        """ Cria uma conta de utilizador com base nas informações inseridas. """
        # Obter valores dos campos de entrada
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        # Criar um user através do UserManager
        user = self.app.user_manager.create_user(email, password, first_name, last_name)

        messagebox.showinfo("Create Profile", "User created successfully:\nEmail: {0}\nPassword: {1}".format(email,password))

        self.app.show(HomePage)

# ---------- Create Album Page ---------------
class CreateAlbumPage:
    def __init__(self, app):
        """ Inicia o layout da Página de Criação de Conta. """
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        app.root.title("My Photos - Create Album")

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

        # Var selected
        self.selected = tk.StringVar()
        #Radio Button
        self.cb1 = tk.Radiobutton(ctg_frame, text="Nature", value="nature",variable=self.selected)
        self.cb2 = tk.Radiobutton(ctg_frame, text="Art", value="art",variable=self.selected)
        self.cb3 = tk.Radiobutton(ctg_frame, text="Cars", value="cars",variable=self.selected)
        self.cb4 = tk.Radiobutton(ctg_frame, text="Food", value="food",variable=self.selected)
        self.cb5 = tk.Radiobutton(ctg_frame, text="Landscape", value="landscape",variable=self.selected)
        self.cb6 = tk.Radiobutton(ctg_frame, text="Others", value="others",variable=self.selected)
        self.cb1.place(x=35, y=10)
        self.cb2.place(x=35, y=40)
        self.cb3.place(x=35, y=70)
        self.cb4.place(x=150, y=10)
        self.cb5.place(x=150, y=40)
        self.cb6.place(x=150, y=70)

        btn_gravar = tk.Button(self.frame, text="Choose Images and Create Album!", width=30,height=5, command=self.save_and_create_album)
        btn_gravar.pack(pady=10)

    def create_album_path(self):
        """ Cria a pasta para o álbum e retorna o índice """
        # Obtém a lista de subdiretórios numerados
        subdiretorios_numerados = [
            int(d) for d in os.listdir("./Albuns")
            if os.path.isdir(os.path.join("./Albuns", d)) and d.isdigit()
        ]

        # Escolhe o próximo número disponível
        index = 1 if not subdiretorios_numerados else max(subdiretorios_numerados) + 1

        novo_album_dir = os.path.join("./Albuns", str(index))
        os.makedirs(novo_album_dir)

        return index

    def save_images(self,index):
        """ Pede as imagens ao utilizador e guarda-as """
        caminhos = filedialog.askopenfilenames(
            title="Select Image",
            initialdir="./images",
            #filetypes=(("png files", "*.png"), ("gif files", "*.gif"), ("all files", "*.*")),
            filetypes = [("Image files", "*.png *.gif *.jpg *.jpeg *.bmp *.tif *.tiff")]

        )

        # Cria o diretório de destino baseado na função create_album_path()
        destino_dir = "./Albuns/%s" %str(index)

        # Verifica se nenhum arquivo foi selecionado, exibe uma mensagem de erro e remove o diretório de destino
        if caminhos == "":
            messagebox.showerror("Error", "No image inserted. Insert at least 1 image!")
            os.rmdir(destino_dir)
            return "cancel"
        else:
            i = 0
            for caminho in caminhos:
                # Define um novo caminho para a imagem com base no diretório de destino e no índice
                novo_caminho = os.path.join(destino_dir, "{}.png".format(i))
                i += 1

                # Abre a imagem selecionada com o módulo PIL e salva-a no novo caminho
                imagem_pil = Image.open(caminho)
                imagem_pil.save(novo_caminho)
        return

    def save_file_album(self,nome,desc,Categorias,data,user_index,index):
        """ Guarda os dados do album """
        if not os.path.isfile("./files/albuns.txt"): # Confirma se o path existe, cria se nao
            ficheiro = open("./files/albuns.txt","w")
        else:
            ficheiro = open("./files/albuns.txt","a")
         # Abre o arquivo de texto onde serão registradas informações do álbum (index album; nome; descrição; Categorias; data criação; user index; likes)
        ficheiro.write(str(index) + ";" + nome + ";" + desc + ";" + Categorias + ";" + data + ";" + user_index + ";" + str(0) + "\n")
        ficheiro.close()

    def save_and_create_album(self):
        """ Guarda Imagens e cria um album """
        try:
            if self.selected.get() == "":
                messagebox.showerror("Error Categories", "Need to select the category,\n try again")
                return

            index = self.create_album_path()
            aux_img = self.save_images(index)  # retorma uma var que ajuda a saber se ocorreu problema no processo
            if aux_img == "cancel":  # se sim, pára o processo
                return
            data = date.datetime.now()
            user_index = str(user.autor_index)
            self.save_file_album(self.entry_nome.get(), self.desc_txt.get("1.0", "end-1c"), self.selected.get(),
                                  data.strftime("%d/%m/%Y"), user_index, index)
            user.albums.append((index, self.entry_nome.get()))
            messagebox.showinfo("Album Created!", "Album created successfully")
            self.app.show(ProfilePage)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def destroy(self):
        """ Destrói o quadro da Página de Criação de Album. """

        self.frame.destroy()

# ---------- Profile Page ---------------
class ProfilePage:
    def __init__(self, app):
        """ Inicia o layout do Profile. """
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.pack(fill=tk.BOTH, expand=True)
        app.root.title("My Photos - Profile")

        self.user_albums = self.load_user_albums(user.autor_index)

        if user.mail == "adm":
            btn_master = tk.Button(self.frame,text="Administation Menu", command=lambda: app.show(adminPage))
            btn_master.pack()

        for album_info in user.albums:
            album_index, album_name = album_info
            label = tk.Label(self.frame, text="Album {0}: {1}".format(album_index, album_name))
            label.pack()

            # Cria um novo frame para as imagens
            image_frame = tk.Frame(self.frame)
            image_frame.pack()

            # Mostra imagens para cada álbum em uma grelha de 3 colunas
            self.display_images_for_album(album_index, image_frame)

    def load_user_albums(self, user_index):
        """ Carrega álbuns do usuário especificado. """
        user_albums = []
        with open("./files/albuns.txt", "r") as file:
            for line in file:
                parts = line.strip().split(";")
                if parts[5] == user_index:  # O índice do usuário é o sexto elemento (indexação começa em 0)
                    user_albums.append((parts[0], parts[1]))  # Adiciona o index e o nome do álbum
        return user_albums

    def display_images_for_album(self, album_index, image_frame):
        album_path = f"./Albuns/{album_index}"
        images_dir = os.listdir(album_path)

        # Coloca as imagens do álbum numa list_images
        image_files = [image for image in images_dir if image.endswith('.png')]

        row_val = 0
        col_val = 0

        for image_file in image_files:
            img_path = os.path.join(album_path, image_file)
            img = Image.open(img_path)
            img = img.resize((240, 240))
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(image_frame, image=img_tk, width=240, height=240)
            label.image = img_tk
            label.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nw")

            col_val += 1
            if col_val >= 3:
                col_val = 0
                row_val += 1


    def destroy(self):
        """ Destrói o quadro da Página de Criação de Album. """

        self.frame.destroy()

# ---------- Explore Page ---------------
class ExplorePage:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        app.root.title("My Photos - Explore")

        """ Search Bar """
        self.search_frame = tk.Frame(self.frame)
        self.search_frame.pack(side="top", pady=(5, 5))
        self.search_text = tk.StringVar()

        self.search_bar = tk.Entry(self.search_frame, width=100, textvariable=self.search_text)
        self.search_bar.pack(side="top", pady=(5, 0))  # Adicionei pady para ajustar a posição vertical da Entry

        self.search_button = tk.Button(self.search_frame, text="Search:", command=self.do_search)
        self.search_button.pack(side="top", pady=(5, 0))  # Adicionei pady para ajustar a posição vertical do botão

        # Adicionando barra de rolagem vertical à página
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        # Canvas para as imagens
        self.canvas = tk.Canvas(self.frame, yscrollcommand=self.scrollbar.set, width=400, height=300)
        self.canvas.pack(side="top", pady=5, expand=True, fill=tk.BOTH)

        # Frame interno para conter as imagens
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor=tk.NW)

        # Configurar a barra de rolagem
        self.scrollbar.config(command=self.canvas.yview)

    def do_search(self):
        search_query = self.search_text.get()
        self.displayAlbum(search_query)

    def displayAlbum(self, album_index):
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        album_path = f"./Albuns/{album_index}"
        images_dir = os.listdir(album_path)

        image_files = [image for image in images_dir if image.endswith('.png')]

        row_val = 0
        col_val = 0

        for image_file in image_files:
            img_path = os.path.join(album_path, image_file)
            img = Image.open(img_path)
            img = img.resize((240, 240))
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(self.image_frame, image=img_tk, width=240, height=240)
            label.image = img_tk
            label.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nw")

            col_val += 1
            if col_val >= 3:
                col_val = 0
                row_val += 1

        # Atualizar o tamanho do frame interno ao tamanho das imagens
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def destroy(self):
            """ Destrói o quadro da Página de Explore. """
            self.frame.destroy()

# ---------- AlbumPage ---------------
class AlbumPage:
    @staticmethod
    def get_album_title(album_path):
        """ Obtem o nome do album """
        file_path = "./files/albuns.txt"
        file = open(file_path, "r")
        data = file.readlines()
        file.close()

        album_index = int(os.path.basename(album_path))
        album_title = ""

        for linha in data:
            values = linha.split(";")
            index = int(values[0])
            if album_index == index:
                album_title = values[1].strip()
                break

        return album_title

    def read_AlbumData(index):
        """ Lê informações do álbum do ficheiro albuns.txt. """
        try:
            with open("./files/albuns.txt", "r") as file:
                for line in file:
                    campos = line.strip().split(";")
                    if len(campos) < 7:
                        continue  # Ignora linhas que não têm campos suficientes
                    if campos[0] == index:
                        return campos
        except IOError:
            print("Erro ao abrir o arquivo albuns.txt")
            return None

        return None  # Retorna None se o álbum com o índice especificado não for encontrado

    def __init__(self,app, album_path):

        """ Obter dados do ficheiro para evitar repetição """
        file_path = "./files/albuns.txt"
        with open(file_path, "r") as file:
            data = file.readlines()

        self.album_index = int(os.path.basename(album_path))
        self.image_index = 0

        """Album page """
        self.album_title = self.get_album_title(album_path)
        self.images_dir = os.listdir(album_path)
        self.app = app
        self.album_path = album_path
        self.frame = tk.Frame(app.container)
        self.frame.pack(side="top",anchor="center")
        app.root.title(f"My Photos - {str(self.album_title)}")

        # frame auxiliar para organização
        self.container = tk.Frame(self.frame, width=1080)
        self.container.pack(side="top", anchor="center")
        # frame das imagens
        self.images_frame = tk.Frame(self.container, bg="white", width=240, height = 350 )
        self.images_frame.pack(side="right", anchor="center", padx=100)
        # botões de avançar e retroceder
        self.avancar = tk.Button(self.container,text=">", command=self.next_image, width=6)
        self.avancar.pack(side="right", padx=1, anchor="s")
        self.retroceder = tk.Button(self.container,text="<", command=self.prev_image, width=6)
        self.retroceder.pack(side="left", padx=1, anchor="s")
        #  list_images com as paths da imagem
        self.list = tk.Listbox(self.container, bg="white", width=200, height= 15)
        self.list.pack(side="top", padx=12)
        # botao para remover imagem selecionada
        self.remover = tk.Button(self.container, width=10, height=2, text="remove image", command=self.remoview_images)
        self.remover.pack(side="bottom", anchor="center")

        heart_button = tk.Button(self.container, text="    ❤️", font=("Arial", 16), command=None)
        heart_button.pack(pady=20)

        self.list_images()
        self.view_images()

    def list_images(self):
        """ Adcionar paths à listbox. """
        for path in self.images_dir:
            self.list.insert("end",path)

        if self.images_dir:
            self.list.selection_set(0)
        else:
            messagebox.showwarning("ERROR", "no images found.")
            self.frame.destroy()


    def remoview_images(self):
        """ Remove a imagem selecionada na listbox """
        imagens_selecionadas = self.list.curselection()

        if imagens_selecionadas:
            for image in reversed(imagens_selecionadas):
                self.list.delete(image)
        else:
            messagebox.showwarning("ERROR", "Please select an item to remove.")

    def view_images(self):
        """ Mostrar as imagens """

        imagens = self.images_dir

        if imagens:
            # path da imagem atual
            image_index = self.image_index
            img_name = imagens[image_index]
            img_path = os.path.join(self.album_path, img_name)

            # Resize imagem
            img = Image.open(img_path)
            img = img.resize((600, 350))

            img_tk = ImageTk.PhotoImage(img)

            # Apagar foto anterior
            for widget in self.images_frame.winfo_children():
                widget.destroy()

            # Label para as imagens
            label = tk.Label(self.images_frame, image=img_tk, bg="Grey")
            label.image = img_tk
            label.pack(side="left", padx=5)

    def selection_update(self, index):
        """ Mudar a seleção atual na listbox """
        self.list.selection_clear(0, "end")
        self.album_index = index
        self.list.selection_set(index)

    def next_image(self):
        """ Proxima imagem """
        imagens = self.images_dir
        total   = len(imagens)

        self.image_index = (self.image_index + 1 ) % total
        self.selection_update(self.image_index)
        self.view_images()

    def prev_image(self):
        """ Imagem anterior """
        imagens = self.images_dir
        total   = len(imagens)

        self.image_index = (self.image_index - 1 ) % total
        self.selection_update(self.image_index)
        self.view_images()


    def destroy(self):
            """ Destrói o quadro da Página de Notification Page. """

            self.frame.destroy()

# ---------- Notification Page ---------------
class NotificationPage:
   
    def __init__(self,app):
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        app.root.title("My Photos - Notifications")

        # Label com o username
        user_header = tk.Label(self.frame, text="{}'s new notifications:".format(user.first_name))
        user_header.pack(side="top", anchor="w")
        # Canvas
        self.canvas = tk.Canvas(self.frame, bg="white", width= 900, height=600)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Adicionar scroll ao canvas
        scrollbar = tk.Scrollbar(self.frame, command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Frame que vai ter as notificações
        self.notifications_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.notifications_frame, anchor="nw")

        
        # Index do user que fez login 
        self.current_user = user.autor_index
        
        self.get_notifications(self.current_user)
        

    def get_notifications(self, user_index):
        
        """ CTT, lê as notificações todas e entrega ao user"""
        
        notifications_path = "./files/notifications.txt"

        with open(notifications_path, "r") as file:
            all_notifications = file.readlines()
            # noti é abreviatura de notification!!
            for line in all_notifications:
                noti_data = line.strip().split(";")
                if noti_data[0] == user_index:
                    noti_sender = noti_data[1]
                    noti_type = noti_data[2]
                    noti_message = noti_data[3]
                    noti_album = noti_data[4]
                    noti_day = noti_data[5]

                    self.format_notification(noti_sender, noti_type, noti_message, noti_album, noti_day)

    
    def format_notification(self, sender, noti_type, message, album, day):

        """ Formatar a informação do notifications.txt e criar a mensagem da notificação"""

        sender_name = user.mail
        print(noti_type)
        match noti_type:
            case "1":
                # like num album
                noti_text = "{0} liked your album".format(sender_name)

            case _:
                # comment
                noti_text = "error"

        self.display_notification(noti_text, day)
    
    
    def display_notification(self, noti_text, day):
        
        """ Mostrar as notificações """
        message = noti_text

        # Frame para 1 notificação
        notification_frame = tk.Canvas(self.notifications_frame, bg="white", width=850, height=30)
        notification_frame.pack(fill=tk.X, padx=40, pady=20)

        # Label com data
        data_noti = tk.Label(notification_frame, text=day, bg="white")
        data_noti.pack(side="left", anchor="w", padx=20)

        # Label com texto da notificação
        txt_noti = tk.Label(notification_frame, text=message, bg="white", wraplength=600)
        txt_noti.pack(side="left", fill="x", anchor="w")

        # Botão remover notificação
        remove_noti = tk.Button(notification_frame, text="remove", bg="white")
        remove_noti.pack(side="right", anchor="e", padx=20)

        # Dar uptade à canvas
        self.canvas.update_idletasks()
        # Definir o scroll baseado na "bbox" (bounding box) de todos os elementos
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def destroy(self):
        """ Destrói o quadro da Página de Notification Page. """
        self.frame.destroy()

class adminPage:
    def __init__(self,app):
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


        # Frame da esquerda (users_tree e btn_userRemove)
        self.left_frame = tk.Frame(self.frame)
        self.left_frame.pack(side="left", padx=10, pady=20)

        self.users_tree = ttk.Treeview(self.left_frame, selectmode="browse", columns=("Index","First Name","Last Name","Email"), show="headings")
        self.users_tree.column("Index",width=50,anchor="c")
        self.users_tree.column("First Name",width=100,anchor="c")
        self.users_tree.column("Last Name",width=100,anchor="c")
        self.users_tree.column("Email",width=100,anchor="c")
        self.users_tree.heading("Index",text="Index")
        self.users_tree.heading("First Name",text="First Name")
        self.users_tree.heading("Last Name",text="Last Name")
        self.users_tree.heading("Email",text="Email")
        self.users_tree.pack(pady=15)

        self.btn_userRemove = tk.Button(self.left_frame, text="Remove User",  height=5, width=20, command=self.remove_users)
        self.btn_userRemove.pack()

        # Frame da direita (album_tree e btn_albumRemove)
        self.right_frame = tk.Frame(self.frame)
        self.right_frame.pack(side="right", padx=50)

        self.album_tree = ttk.Treeview(self.right_frame, selectmode="browse", columns=("Index","Author","Title","Category","Number of Photos"), show="headings")
        self.album_tree.column("Index",width=50,anchor="c")
        self.album_tree.column("Author",width=100,anchor="c")
        self.album_tree.column("Title",width=100,anchor="c")
        self.album_tree.column("Category",width=100,anchor="c")
        self.album_tree.column("Number of Photos",width=100,anchor="c")
        self.album_tree.heading("Index",text="Index")
        self.album_tree.heading("Author",text="Author")
        self.album_tree.heading("Title",text="Title")
        self.album_tree.heading("Category",text="Category")
        self.album_tree.heading("Number of Photos",text="Number of Photos")
        self.album_tree.pack(pady=15)

        self.btn_albumRemove = tk.Button(self.right_frame, text="Remove Album",  height=5, width=20, command=self.remove_albums)
        self.btn_albumRemove.pack()

        self.fill_users()
        self.fill_albuns()

    def read_InfoFiles(self,path,aux):
        """ Lê informações do utilizador do ficheiro users.txt."""
        data = []
        i=0
        ficheiro = open(path, "r")
        linhas = ficheiro.readlines()
        for linha in linhas:
            data.append([])
            linha = linha.split(";")
            linha[aux-1] = linha[aux-1].replace("\n", "")
            for j in range(aux):
                data[i].append(linha[j])
            i+=1
        ficheiro.close()
        return data

    def fill_users(self):
        list_images= self.read_InfoFileUsers("./files/users.txt",5) # Cria a list_images com os dados do ficheiro
        self.users_tree.delete(*self.users_tree.get_children()) # Apaga o conteudo
        for i in range(1,len(list_images)): # Preenche com todo o conteudo do ficheiro
            self.users_tree.insert("","end", values= (list_images[i][0],list_images[i][1],list_images[i][2],list_images[i][3],list_images[i][4]))

    def fill_albuns(self):
        list_images= self.read_InfoFileUsers("./files/albuns.txt",6)
        self.album_tree.delete(*self.album_tree.get_children())
        for i in range(len(list_images)):
            self.album_tree.insert("","end", values= (list_images[i][0],list_images[i][1],list_images[i][2],list_images[i][3],list_images[i][4],list_images[i][5]))

    def remove_users(self):
        if self.users_tree.focus() == "":
            messagebox.showerror("Error","Select item first")
            return
        else:
            row_id = self.users_tree.focus() # Obtem o id que o adm selecionou
            self.users_tree.delete(row_id) # Apaga os dados na tree
        self.save_treeview(self.users_tree,"./files/users.txt")


    def remove_albums(self):
        if self.album_tree.focus() == "":
            messagebox.showerror("Error","Select item first")
            return
        else:
            row_id = self.album_tree.focus()
            album_deleted = self.album_tree.item(row_id,"values") # Obtem os dados do album

            destino_dir = "./Albuns/%s" %str(album_deleted[0]) # Cria o path para as fotos do album

            for imagem in os.listdir(destino_dir): # Percorre as imagens e elimina-as
                caminho_imagem = os.path.join(destino_dir,imagem)
                os.remove(caminho_imagem)
            os.rmdir(destino_dir)
            self.album_tree.delete(row_id)
        self.save_treeview(self.album_tree,"./files/albuns.txt")

    def save_treeview(self, treeview, nome_do_ficheiro):
        with open(nome_do_ficheiro, 'w') as ficheiro:
            # Obtemos as colunas da treeview
            colunas = treeview["columns"]
            if treeview == self.users_tree:
                ficheiro.write("1;adm;12345;First;Last\n")
            # Iteramos sobre os itens da treeview
            for item in treeview.get_children():
                # Obtemos os valores de cada coluna para o item atual
                valores = [treeview.item(item, 'values')[coluna] for coluna in range(len(colunas))]##ver
                # Escrevemos os valores no arquivo, separados por ponto e vírgula
                ficheiro.write(';'.join(map(str, valores)) + '\n')

    def destroy(self):
        """ Destrói o quadro da Página de Administration Page. """

        self.frame.destroy()

global user
user = User_logged("0", "user", "", "", "")
global app
app = App()
