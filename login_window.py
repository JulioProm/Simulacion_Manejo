# login_window.py
import tkinter as tk
from tkinter import messagebox
from db_manager import DBManager

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Manejo - Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")

        # 👇 IMPORTANTE: usar DBManager (no UserManager)
        self.db = DBManager()

        tk.Label(root, text="Simulador de Examen de Manejo",
                 fg="white", bg="#2c3e50", font=("Arial", 14, "bold")).pack(pady=20)

        frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
        frame.pack(pady=10)

        tk.Label(frame, text="Correo electrónico:", bg="#34495e", fg="white").grid(row=0, column=0, sticky="w")
        self.entry_email = tk.Entry(frame, width=30)
        self.entry_email.grid(row=0, column=1)

        tk.Label(frame, text="Contraseña:", bg="#34495e", fg="white").grid(row=1, column=0, sticky="w")
        self.entry_password = tk.Entry(frame, show="*", width=30)
        self.entry_password.grid(row=1, column=1)

        tk.Button(frame, text="Iniciar Sesión", bg="#27ae60", fg="white",
                  width=15, command=self.login).grid(row=2, columnspan=2, pady=10)

        tk.Button(frame, text="Registrarse", bg="#2980b9", fg="white",
                  width=15, command=self.registrar).grid(row=3, columnspan=2)

    def login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()

        if not email or not password:
            messagebox.showwarning("Faltan datos", "Ingresa correo y contraseña.")
            return

        # 👇 usar DBManager
        usuario = self.db.validar_login(email, password)
        if usuario:
            self.usuario_logeado = usuario        # <- para que main.py lo lea
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario['nombre']}!")
            self.root.destroy()                   # cierra login
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def registrar(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        if not email or not password:
            messagebox.showwarning("Faltan datos", "Ingresa correo y contraseña.")
            return

        nombre = email.split("@")[0].capitalize()
        # 👇 usar el método que agregaste en DBManager
        ok = self.db.registrar_usuario_login(nombre, email, password)
        if ok:
            messagebox.showinfo("Registro", "Usuario registrado correctamente. Ya puedes iniciar sesión.")
        else:
            messagebox.showwarning("Aviso", "El usuario ya existe.")
