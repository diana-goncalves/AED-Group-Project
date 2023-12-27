import tkinter as tk

def fazer_login():
    # Verificação do login
    print("Login realizado com sucesso!")

def criar_janela_login():
    login_window = tk.Toplevel()  # Cria uma nova janela
    login_window.title("My Photos - Login")

    largura_janela = 1000
    altura_janela = 600

    # Dimensões da janela
    largura_tela = login_window.winfo_screenwidth()
    altura_tela = login_window.winfo_screenheight()

    # Calcula as coordenadas para colocar o contéudo ao centro
    posicao_x = (largura_tela - largura_janela) // 2
    posicao_y = (altura_tela - altura_janela) // 2

    # Define a geometria da janela com as coordenadas calculadas
    login_window.geometry("{0}x{1}+{2}+{3}".format(largura_janela, altura_janela, posicao_x, posicao_y))

    # Cria uma frame para organizar os elementos centralizados
    frame_centralizado = tk.Frame(login_window)
    frame_centralizado.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Cria o rótulo e entrada para o email dentro da frame centralizada
    label_email = tk.Label(frame_centralizado, text="Email:")
    label_email.pack()
    entry_email = tk.Entry(frame_centralizado)
    entry_email.pack()

    # Cria o rótulo e entrada para a senha dentro da frame centralizada
    label_senha = tk.Label(frame_centralizado, text="Senha:")
    label_senha.pack()
    entry_senha = tk.Entry(frame_centralizado, show="*")  # Para esconder a senha
    entry_senha.pack()

    # Botão de login dentro do frame centralizado
    botao_login = tk.Button(frame_centralizado, text="Login", command=fazer_login)
    botao_login.pack()

    login_window.mainloop()  # Garante o loop principal da janela de login
