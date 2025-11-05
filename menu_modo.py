import tkinter as tk
from tkinter import messagebox
from cuestionario import Cuestionario
from db_manager import DBManager

class MenuModo:
    def __init__(self, usuario):
        self.usuario = usuario
        self.db = DBManager()

        self.root = tk.Tk()
        self.root.title("Selecciona el modo de simulación")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")

        tk.Label(self.root, text=f"Bienvenido, {usuario['nombre']}", bg="#2c3e50", fg="white", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text="Selecciona el modo de examen:", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(pady=10)

        # Botones
        tk.Button(self.root, text="🟩 Práctica", bg="#27ae60", fg="white", width=15, height=2, command=self.modo_practica).pack(pady=10)
        tk.Button(self.root, text="🟦 Examen Final", bg="#2980b9", fg="white", width=15, height=2, command=self.modo_final).pack(pady=10)

        self.root.mainloop()

    def modo_practica(self):
        self.iniciar_modo("practica", 20, 6)

    def modo_final(self):
        self.iniciar_modo("final", 40, 3)

    def iniciar_modo(self, tipo, cantidad, limite):
        usuario_id = self.usuario["id_usuario"]
        intentos = self.db.contar_intentos(usuario_id, tipo)

        if intentos >= limite:
            messagebox.showwarning("Límite alcanzado", f"Ya alcanzaste los {limite} intentos del modo '{tipo}'.")
            return

        # Cerrar ventana actual antes de abrir el cuestionario
        self.root.destroy()

        # Ejecutar el cuestionario
        cuestionario = Cuestionario("preguntas_manejo.csv", self.db)
        cuestionario.iniciar(usuario_id, tipo, cantidad)
