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

        tk.Label(self.root, 
                 text=f"Bienvenido, {usuario['nombre']}", 
                 bg="#2c3e50", fg="white", 
                 font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Label(self.root, 
                 text="Selecciona el modo de examen:", 
                 bg="#2c3e50", fg="white", 
                 font=("Arial", 12)
        ).pack(pady=10)

        # Botón Práctica
        tk.Button(
            self.root,
            text="🟩 Práctica",
            bg="#27ae60", fg="white",
            width=15, height=2,
            command=self.modo_practica
        ).pack(pady=10)

        # Botón Examen Final
        tk.Button(
            self.root,
            text="🟦 Examen Final",
            bg="#2980b9", fg="white",
            width=15, height=2,
            command=self.modo_final
        ).pack(pady=10)

        # ----------------------------------------------------------
        # ✔ Botón Dashboard SOLO PARA ADMIN
        # ----------------------------------------------------------
        if self.usuario["rol"] == "admin":
            tk.Button(
                self.root,
                text="📊 Dashboard",
                bg="#f39c12",
                fg="black",
                width=15,
                height=2,
                command=self.abrir_dashboard
            ).pack(pady=10)

        # ----------------------------------------------------------
        # ✔ Botón CERRAR SESIÓN (para ambos roles)
        # ----------------------------------------------------------
        tk.Button(
            self.root,
            text="Cerrar sesión",
            bg="#c0392b",
            fg="white",
            width=15,
            height=1,
            command=self.cerrar_sesion
        ).pack(pady=15)

        self.root.mainloop()

    def modo_practica(self):
        self.iniciar_modo("practica", 20, 6)

    def modo_final(self):
        self.iniciar_modo("final", 40, 3)

    def iniciar_modo(self, tipo, cantidad, limite):
        usuario_id = self.usuario["id_usuario"]
        intentos = self.db.contar_intentos(usuario_id, tipo)

        if intentos >= limite:
            messagebox.showwarning(
                "Límite alcanzado", 
                f"Ya alcanzaste los {limite} intentos del modo '{tipo}'."
            )
            return

        # Cerrar ventana actual antes de abrir el cuestionario
        self.root.destroy()

        # Ejecutar el cuestionario
        cuestionario = Cuestionario("preguntas_manejo.csv", self.db)
        cuestionario.iniciar(usuario_id, tipo, cantidad)

    # ----------------------------------------------------------------
    # ✔ Abrir Dashboard (solo admin)
    # ----------------------------------------------------------------
    def abrir_dashboard(self):
        from dashboard import Dashboard
        Dashboard(self.db)

    # ----------------------------------------------------------------
    # ✔ Cerrar sesión (para ambos roles)
    # ----------------------------------------------------------------
    def cerrar_sesion(self):
        self.root.destroy()
        from login_window import LoginWindow
        import tkinter as tk

        nuevo_root = tk.Tk()
        LoginWindow(nuevo_root)
