import tkinter as tk
from tkinter import messagebox,filedialog
from PIL import Image, ImageTk
import os
import datetime as date
#from user_login import Login
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
    def __init__(self):
        """ Inicia o layout da Página de Criação de Conta. """
        self.create_album = tk.Tk()
        self.create_album.geometry("1000x600")


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
        

        self.btn_gravar = tk.Button(self.create_album, text="Escolher Imagens e Criar Album!",width=30, height=5, command=self.guardar)
        self.btn_gravar.pack(pady=10)
        self.create_album.mainloop()

    def guardar_imagens(self,index):
        caminhos= filedialog.askopenfilenames(title="Select Image", initialdir="./images",
                                            filetypes=(("png files","*.png"),("gif files","*.gif"), ("all files","*.*")))#le as imagens do utilizador
        destino_dir = "./Albuns/%s"%index#destino
        if caminhos == "":#se o utlilizador nao escolher nenhuma imagem
            messagebox.showerror("Error","Nenhuma imagem inserir\nIntroduza pelo menos 1 Imagem!")#erro
            os.rmdir(destino_dir)#apaga o album
        else:
            i=0
            for caminho in caminhos:#percorre todas as imagens
                novo_caminho = os.path.join(destino_dir,"%s.png"%i)#cria o novo caminho
                i += 1#actualiza o index
                imagem_pil = Image.open(caminho)#abre a imagem
                imagem_pil.save(novo_caminho)#guarda no caminho novo

    def cria_caminho_album(self):
        """
            Cria uma pasta para o meu album
        """
        if not os.path.exists("./Albuns"):#Confirma se o path existe, cria se nao
            os.mkdir("./Albuns")#cria
        index = len(os.listdir("./Albuns"))+1#ve quantos albuns ja tem
        novo_album_dir=os.path.join("./Albuns",str(index))#cria o destimo novo
        os.mkdir(novo_album_dir)#criaa pasta para o album
        return index

    def guardar_album_ficheiro(self,nome,desc,Categorias,data,user,index):
        ficheiro = open("./files/albuns.txt","a")#abre o ficheiro com as informacoes do album
        ficheiro.write(str(index)+";"+nome+";"+desc+";"+Categorias+";"+str(data)+";"+user+"\n")#introduz as informações
        ficheiro.close()#fecha ficheiro

    def guardar(self):
        """
            Guarda Imagens e cria um album
        """
        index = self.cria_caminho_album()
        self.guardar_imagens(index)
        data = date.datetime.now() #recolher data 
        #user = Login().fazer_login() #recolher nome do autor 
        user = "adm"
        self.guardar_album_ficheiro(self.entry_nome.get(),self.desc_txt.get("1.0","end-1c"),self.cb_natur.get(),self.cb_arte.get(),self.cb_carros.get(),self.cb_comida.get(),data.strftime("%d/%m/%Y"),user,index)

    def destroy(self):
        """ Destrói o quadro da Página de Criação de Album. """

        self.frame.destroy()

Create_AlbumPage()