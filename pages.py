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

    def create_account(self):
        print("Create Album")

    def notifications(self):
        print("Notifications")


class Menu:
    def __init__(self, app):
        """ Inicia o menu e as suas opções.
        Args:
        - app: A instância principal da aplicação. """

        menu = tk.Menu(app.root)

        options = tk.Menu(menu)
        options.add_command(label="Login", command=lambda: app.show(LoginPage))
        options.add_command(label="Create Account", command=lambda: app.show(CreateAccountPage))

        menu.add_cascade(label="Options", menu=options)
        app.root.config(menu=menu)

# Main Page
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

        btn_profile = tk.Button(sidebar, text="Create Account", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=app.create_account)
        btn_profile.pack(fill="x", padx=5, pady=5)

        btn_explore = tk.Button(sidebar, text="Explore", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=app.explore)
        btn_explore.pack(fill="x", padx=5, pady=5)

        btn_notifications = tk.Button(sidebar, text="Notifications", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=app.notifications)
        btn_notifications.pack(fill="x", padx=5, pady=5)

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
#Login Page
class LoginPage:
    def __init__(self, app):
        """ Inicia o layout da Página de Início de Sessão. """

        self.app = app
        self.frame = tk.Frame(app.container)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        #Label Email
        label_email = tk.Label(self.frame, text="Email:")
        label_email.pack()

        #Entry Email
        self.user_email = tk.StringVar()
        entry_email = tk.Entry(self.frame, textvariable=self.user_email)
        entry_email.pack()

        #Label Senha
        label_senha = tk.Label(self.frame, text="Senha:")
        label_senha.pack()

        #Entry Senha
        self.user_senha = tk.StringVar()
        entry_senha = tk.Entry(self.frame, show="*", textvariable=self.user_senha)
        entry_senha.pack()

        #Button Login
        botao_login = tk.Button(self.frame, text="Login", command=self.fazer_login, width=15)
        botao_login.pack(pady=(20, 0))

        #Button Create Account
        botao_criar_conta = tk.Button(self.frame, text="Create Account", command=lambda: app.show(CreateAccountPage), width=15)
        botao_criar_conta.pack(pady=(5, 20))

        #Button Cancel
        botao_cancelar = tk.Button(self.frame, text="Cancel", width=15, command=lambda: app.show(HomePage))
        botao_cancelar.pack(pady=(0,0))

    def destroy(self):
        """ Destrói o quadro da Página de Início de Sessão para exibir conteúdo dinâmico na abertura de outra janela. """

        self.frame.destroy()

    def criar_ficheiro(self):
        """ Cria um ficheiro e escreve dados iniciais se não existir. """

        if not os.path.exists("./files"):#ask if path dont exist
            os.mkdir("files")#make path
            ficheiro = open("./files/users.txt", "w")#open ficheiro
            ficheiro.write("1;adm;12345;First;Last\n")  #write admin account
            ficheiro.close()#close ficheiro

    def ler_infoUsers(self):
        """ Lê informações do utilizador do ficheiro users.txt."""

        self.criar_ficheiro()
        #index;email;pass;firstname;surname
        users = [] # var to create user
        i = 0 
        ficheiro = open("./files/users.txt", "r") #open ficheiro
        linhas = ficheiro.readlines()# reads all lines 
        for linha in linhas:#goes through all lines
            users.append([])#add index
            linha = linha.split(";")# create sub strings 
            linha[4] = linha[4].replace("\n", "")#delete \n
            for j in range(5):#fill
                users[i].append(linha[j])
            i += 1#advance to the next line
        ficheiro.close()#close 
        return users

    def fazer_login(self):
        """ Realiza a ação de início de sessão e verifica as credenciais do utilizador. """
        users = self.ler_infoUsers() # read users

        for i in range(len(users)):#for to see all users
            if str(self.user_email.get()) == str(users[i][1].strip()) and str(self.user_senha.get()) == str(users[i][2].strip()):#asks if there is any data equal to those entered
                messagebox.showinfo("Login", "Successful Login")
                #u1 = User_logged(users[i][0].strip(),users[i][1].strip(),users[i][2].strip(),users[i][3].strip(),users[i][4].strip())
                u1.mail = users[i][1].strip()
                print(u1.mail)
                self.app.show(HomePage)#return to homePage
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



class Album:# dadosdo album
    def __init__(self,index):
        self.index= index

    def adicionar_foto(self):
        """
            Adicionar foto nova
        """
        print()
    def retornar_foto(self):
        print()
    def salvar_album(self):
        """
            Salval Album no ficheiro
        """
        print()
    def procurar_album(self):
        """
            atravez do index, retorna os dados de um album(ou autor)
        """
        print()

class Create_AlbumPage:
    def __init__(self, app):
        """ Inicia o layout da Página de Criação de Conta. """
        self.create_album = tk.Tk()
        self.create_album = tk.Frame(app.container)
        self.create_album.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        #Entry
        tk.Label(self.create_album,text="Nome:").pack(pady=5)
        self.album_nome = tk.StringVar()
        self.entry_nome = tk.Entry(self.create_album, width=30, textvariable=self.album_nome)
        self.entry_nome.pack(pady=5)

        #Text Box
        tk.Label(self.create_album,text="Descrição:").pack(pady=10)
        self.desc_txt = tk.Text(self.create_album, width=50, height=10)
        self.desc_txt.pack(pady=5)

        #Label Frame
        cat_frame = tk.LabelFrame(text="Categorias:", width=260,height=130, relief="sunken")
        cat_frame.pack(pady=15)

        #Vars
        self.cb_natur = tk.IntVar()
        self.cb_arte = tk.IntVar()
        self.cb_carros = tk.IntVar()
        self.cb_comida = tk.IntVar()
        self.cb_paisagem = tk.IntVar()
        self.cb_outros = tk.IntVar()

        #Checkbuttons
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

        #Button
        btn_gravar = tk.Button(self.create_album, text="Escolher Imagens e Criar Album!",width=30, height=5, command=self.guardar)
        btn_gravar.pack(pady=10)
        self.create_album.mainloop()

    def guardar_imagens(index):
        """
            Save Images
        """
        caminhos= filedialog.askopenfilenames(title="Select Image", initialdir="./images",filetypes=(("png files","*.png"),("gif files","*.gif"), ("all files","*.*")))#guarda caminho da imagem
        destino_dir = "./Albuns/%s"%index
        if caminhos == "":#If you don't select images, an error message appears
            messagebox.showerror("Error","Nenhuma imagem inserir\nIntroduza pelo menos 1 Imagem!")
            os.rmdir(destino_dir)# delete album
        else:
            i=0
            for caminho in caminhos:#scroll through all images
                novo_caminho = os.path.join(destino_dir,"%s.png"%i)#make new path
                i += 1
                imagem_pil = Image.open(caminho)#open image
                imagem_pil.save(novo_caminho)#save image in the new path
    def cria_caminho_album(self):
        """
            Cria uma pasta para o album
        """
        if not os.path.exists("./Albuns"):#Confirms if the path exists, creates it if not
            os.mkdir("./Albuns")
        index = len(os.listdir("./Albuns"))+1#read how many albums you have and create the new index
        novo_album_dir=os.path.join("./Albuns",str(index))#make the path for the new album
        os.mkdir(novo_album_dir)
        return index#return index

    def guardar_album_ficheiro(self,nome,desc,Categorias,data,user,index):
        if not os.path.exists("./files/Albuns"):#Confirms if the path exists, creates it if not
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
        data = date.datetime.now() #get data 
        user = u1.autor_index() #get name
        #user = Login().fazer_login() #recolher nome do autor
        user = "adm"
        self.guardar_album_ficheiro(self.entry_nome.get(),self.desc_txt.get(),self.Categorias,data.strftime("%d/%m/%Y"),user,index)#guarda dados

    def destroy(self):
        """ Destrói o quadro da Página de Criação de Album. """

        self.frame.destroy()

u1 = User_logged("0","user","","","")
app = App()