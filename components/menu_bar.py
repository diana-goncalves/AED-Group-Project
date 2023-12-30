import tkinter as tk
import components.user_login as user_login

def explore():
    print("Explorar")

def profile():
    print("Perfil")

def notifications():
    print("Notifications")

def fazer_login():
    login_window = user_login.Login()

def generate_menu(root):
    menu = tk.Menu(root)
    root.config(menu=menu)

    opcoes_menu = tk.Menu(menu)
    menu.add_cascade(label="Options", menu=opcoes_menu)
    opcoes_menu.add_command(label="Explore", command=explore)
    opcoes_menu.add_command(label="Profile", command=profile)
    opcoes_menu.add_command(label="Notifications", command=notifications)
    opcoes_menu.add_command(label="Login", command=fazer_login)

    return menu
