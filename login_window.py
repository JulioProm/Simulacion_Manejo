import tkinter as tk
from tkinter import messagebox
from db_manager import DBManager

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Manejo - Login")
        self.root.geometry("400x400")
        self.root.configure(bg="#2c3e50")
        
        self.db = DBManager()
        
        tk.Label(root, text="Simulador de Examen de Manejo", fg="white", bg="#2c3e50", font=("Arial", 14, "bold")).pack(pady=20)
        
        self.frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
        self.frame.pack(pady=10)
        
        tk.Label(self.frame, text="Correo electrónico:", bg="#34495e", fg="white").grid(row=0, column=0, sticky="w")
        self.entry_email = tk.Entry(self.frame, width=30)
        self.entry_email.grid(row=0, column=1)
        
        tk.Label(self.frame, text="Contraseña:", bg="#34495e", fg="white").grid(row=1, column=0, sticky="w")
        self.entry_password = tk.Entry(self.frame, show="*", width=30)
        self.entry_password.grid(row=1, column=1)
        
        tk.Button(self.frame, text="Iniciar Sesión", bg="#27ae60", fg="white", width=15, command=self.login).grid(row=2, columnspan=2, pady=10)
        tk.Button(self.frame, text="Registrarse", bg="#2980b9", fg="white", width=15, command=self.registrar).grid(row=3, columnspan=2)

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        user = self.db.validar_login(email, password)
        if user:
            messagebox.showinfo("Éxito", f"Bienvenido, {user['nombre']}!")
            self.usuario_logeado = user  # <-- Guarda los datos para main.py
            self.root.destroy()
            import main  # ← aquí enlaza tu simulador principal
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def registrar(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        nombre = email.split("@")[0].capitalize()
        if self.db.registrar_usuario(nombre, email, password):
            messagebox.showinfo("Registro", "Usuario registrado correctamente.")
        else:
            messagebox.showwarning("Aviso", "El usuario ya existe.")
