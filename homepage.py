import tkinter as tk
from tkinter import messagebox
from components.menu_bar import generate_menu
from components.user_login import Login

login_window = None

def profile():
    print("Perfil")

def explore():
    print("Explorar")

def notifications():
    print("Notifications")

def fazer_login_window():
    global login_window
    login_window = Login().criar_janela_conta()

def on_closing():
    global login_window
    if login_window:
        login_window.fechar_janela_login()
    if messagebox.askokcancel("Fechar", "Deseja sair do My Photos?"):
        root.destroy()

root = tk.Tk()
root.title("My Photos")
root.geometry("1000x600")

sidebar = tk.Frame(root, bg="gray", width=200)
sidebar.pack(fill="y", side="left")

btn_profile = tk.Button(sidebar, text="Profile", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=profile)
btn_profile.pack(fill="x", padx=5, pady=5)

btn_explore = tk.Button(sidebar, text="Explore", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=explore)
btn_explore.pack(fill="x", padx=5, pady=5)

btn_notifications = tk.Button(sidebar, text="Notifications", bg="white", pady=10, padx=5, relief="raised", cursor="hand2", command=notifications)
btn_notifications.pack(fill="x", padx=5, pady=5)

menu = generate_menu(root)
root.config(menu=menu)

root.mainloop()
