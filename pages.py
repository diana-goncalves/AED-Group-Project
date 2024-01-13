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

        btn_profile = tk.Button(sidebar, text="Profile", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: self.show(ProfilePage))
        btn_profile.pack(fill="x", padx=5, pady=5)

        btn_profile = tk.Button(sidebar, text="Create Album", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=lambda: self.show(CreateAlbumPage))
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

        """ Image frame """
        # frame criado para que as imagens não interfiram com a side bar
        self.image_frame = tk.Frame(self.frame, width=400, height=100)
        self.image_frame.pack(side="top", pady=5)
    
        #variavel que guarda a primeira imagem de cada album 
        self.showcase = []

    def albumShowcase(self):
        albuns_path = ("./Albuns")
        if not os.path.exists("./Albuns"): #confirmar se existe a pasta albuns
            os.mkdir("./Albuns")
        
        albuns = os.listdir(albuns_path)

        for album_path in albuns:
            album_path = os.path.join(albuns_path,album_path)

            images = []
            for img in album_path:
                if img.endswith(("png files", "*.png"), ("gif files", "*.gif"), ("all files", "*.*")):
                    images.append(img)
                    if len(images)>=0:
                        first_image = os.path.join(album_path, images[0])
                        self.showcase.append((album_path,first_image))
            
        return self.showcase
    
    def displayAlbum(self, showcase):
        albuns_path = ("./Albuns")

        image_files = []
        for image in showcase:
            if image.endswith('.png'):
                image_files.append(image)

        row_val = 0
        col_val = 0

        for image_file in image_files:
            img_path = os.path.join(albuns_path, image_file)
            img = Image.open(img_path)
            img = img.resize((240, 240))
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(self.image_frame, image=img_tk, width=240, height=240)
            label.image = img_tk 
            label.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nw")
            
            col_val += 1
            if col_val >= 3:  #numero de colunas
                col_val = 0
                row_val += 1

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
                # Actualização dos dados do user
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

# ---------- Create Album Page ---------------
class CreateAlbumPage:
    def __init__(self, app):
        """ Inicia o layout da Página de Criação de Conta. """
        # if user.mail == "user":
        #     messagebox.showerror("Need Account","Please log in or create an account to access")
        #     app.show(HomePage)
        # else:
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

    def create_album_path(self):#cria a pasta para o album e retorna o index
        """
            Create path to a new album
        """
        if not os.path.exists("./Albuns"):#Confirms if the path exists, creates it if not
            os.mkdir("./Albuns")
        index = len(os.listdir("./Albuns"))+1#read how many albums you have and create the new index
        novo_album_dir=os.path.join("./Albuns",str(index))#make the path for the new album
        os.mkdir(novo_album_dir)
        return index#return index

    def save_images(self,index):#pede as imagens ao utilizador e as guarda
        """ Save Images """

        caminhos = filedialog.askopenfilenames(
            title="Select Image",
            initialdir="./images",
            filetypes=(("png files", "*.png"), ("gif files", "*.gif"), ("all files", "*.*")),
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
            # Itera sobre os caminhos dos arquivos selecionados
            for caminho in caminhos:
                # Define um novo caminho para a imagem com base no diretório de destino e no índice
                novo_caminho = os.path.join(destino_dir, "{}.png".format(i))
                i += 1

                # Abre a imagem selecionada com o módulo PIL e salva-a no novo caminho
                imagem_pil = Image.open(caminho)
                imagem_pil.save(novo_caminho)
        return
   
    def save_file_album(self,nome,desc,Categorias,data,user_index,index):#guarda os dados do album
        """ Cria um diretório para os arquivos do álbum se não existir """

        if not os.path.isfile("./files/albuns.txt"): # Confirma se o path existe, cria se nao
            ficheiro = open("./files/albuns.txt","w")
        else:
            ficheiro = open("./files/albuns.txt","a")
         # Abre o arquivo de texto onde serão registradas informações do álbum
        ficheiro.write(str(index)+";"+nome+";"+desc+";"+Categorias+";"+data+";"+user_index+"\n")
        ficheiro.close()


    def save_and_create_album(self):
        """ Guarda Imagens e cria um album """
        if self.selected.get() == "":
            messagebox.showerror("Error Categories","Need to selectthe category,\n try again")
            return
        index = self.create_album_path()  # Chama save_images diretamente para obter o índice
        aux_img = self.save_images(index)#retorma uma var que ajuda a saber se ouve problema no processo
        if aux_img == "cancel":# se sim, para processo
            return
        data = date.datetime.now()
        user_index = str(user.autor_index)
        self.save_file_album(self.entry_nome.get(), self.desc_txt.get("1.0", "end-1c"), self.selected.get(), data.strftime("%d/%m/%Y"), user_index, index)
        messagebox.showinfo("Album Created!","Album created successfully")
        self.app.show(ProfilePage)

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

    def destroy(self):
        """ Destrói o quadro da Página de Criação de Album. """

        self.frame.destroy()

# ---------- Explore Page ---------------
class ExplorePage:
    def __init__(self,app):
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        """ Search Bar """
        #frame para colocar a search bar e respetivo botão
        self.search_frame = tk.Frame(self.frame)
        self.search_frame.pack(side="top", pady=(0,5))
        #variavel que guarda o texto da search bar
        self.search_text = tk.StringVar()

        self.search_bar = tk.Entry(self.search_frame, width=100, textvariable=self.search_text)
        self.search_bar.pack(side= "left")

        self.search_button = tk.Button(self.search_frame, text="Search:", command=self.do_search)
        self.search_button.pack(side="left")
        
        """ Image frame """
        # frame criado para que as imagens não interfiram com a side bar
        self.image_frame = tk.Frame(self.frame, width=400, height=100)
        self.image_frame.pack(side="top", pady=5)
        
    def do_search(self):
        # Receber pesquisa
        search_query = self.search_text.get()
        # Mostrar album baseado na pesquisa
        self.displayAlbum(search_query)

    def displayAlbum(self, album_index):
        
        album_path = f"./Albuns/{album_index}"
        images_dir = os.listdir(album_path)
        
        # Coloca as imagens do album numa lista
        image_files = []
        for image in images_dir:
            if image.endswith('.png'):
                image_files.append(image)

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
            if col_val >= 3:  #numero de colunas
                col_val = 0
                row_val += 1
    
    def destroy(self):
        """ Destrói o quadro da Página de Explore. """

        self.frame.destroy()

# ---------- Notification Page ---------------
class NotificationPage:
    def __init__(self,app):
        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def destroy(self):
            """ Destrói o quadro da Página de Notification Page. """

            self.frame.destroy()


global user
user = User_logged("0","user","","","")
global app
app = App()