import tkinter as tk
from tkinter import messagebox

class CreateAccountWindow:
    def __init__(self):
        self.create_account_window = tk.Toplevel()
        self.create_account_window.title("My Photos - Create Account")

        width = 1000
        height = 600
        screen_width = self.create_account_window.winfo_screenwidth()
        screen_height = self.create_account_window.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.create_account_window.geometry("{0}x{1}+{2}+{3}".format(width, height, int(x), int(y)))

        frame = tk.Frame(self.create_account_window)
        frame.pack(padx=20, pady=20)

        # Labels and Entries
        tk.Label(frame, text="First Name:").grid(row=0, column=0, sticky="w")
        self.entry_first_name = tk.Entry(frame)
        self.entry_first_name.grid(row=0, column=1)

        tk.Label(frame, text="Last Name:").grid(row=1, column=0, sticky="w")
        self.entry_last_name = tk.Entry(frame)
        self.entry_last_name.grid(row=1, column=1)

        tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w")
        self.entry_email = tk.Entry(frame)
        self.entry_email.grid(row=2, column=1)

        tk.Label(frame, text="Password:").grid(row=3, column=0, sticky="w")
        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.grid(row=3, column=1)

        # Create Account Button
        btn_create_account = tk.Button(frame, text="Criar conta", command=self.create_account)
        btn_create_account.grid(row=4, columnspan=2, pady=10)

    def create_account(self):
        # Get values from entries
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        messagebox.showinfo("Create Profile", "First Name: {0}\nLast Name: {1}\nEmail: {2}\nPassword: {3}". format(first_name,last_name, email, password))

        self.create_account_window.destroy()

def criar_janela_login():
    create_account_window = CreateAccountWindow()
    create_account_window.create_account_window.mainloop()
