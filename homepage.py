import tkinter as tk
from components.menu_bar import generate_menu
from components.user_login import criar_janela_login

def profile():
    print("Perfil")

def explore():
    print("Explorar")


def notifications():
    print("Notifications")

def fazer_login_window():
    criar_janela_login()

root = tk.Tk()
root.title("My Photos")
root.geometry("1000x600")

# Cria a barra lateral
sidebar = tk.Frame(root, bg="gray", width=200)
sidebar.pack(fill="y", side="left")

# Definição de botões para as três funções
btn_profile = tk.Button(sidebar, text="Profile", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=profile)
btn_profile.pack(fill="x", padx=5, pady=5)

btn_explore = tk.Button(sidebar, text="Explore", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=explore)
btn_explore.pack(fill="x", padx=5, pady=5)

btn_notifications = tk.Button(sidebar, text="Notifications", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=notifications)
btn_notifications.pack(fill="x", padx=5, pady=5)


# Cria o menu utilizando a função generate_menu do menu_bar.py
menu = generate_menu(root)
root.config(menu=menu)

root.mainloop()
