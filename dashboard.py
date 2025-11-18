import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Dashboard:
    def __init__(self, db):
        self.db = db

        self.root = tk.Tk()
        self.root.title("Dashboard Administrativo")
        self.root.geometry("900x600")
        self.root.configure(bg="#2c3e50")

        tk.Label(self.root, text="Dashboard Administrativo",
                 font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(pady=20)

        # Marco principal
        frame = tk.Frame(self.root, bg="#34495e")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Resumen numérico
        self.label_resumen = tk.Label(frame, text="", bg="#34495e", fg="white", font=("Arial", 12))
        self.label_resumen.pack(pady=10)

        # Gráfica
        grafico_frame = tk.Frame(frame, bg="#34495e")
        grafico_frame.pack(fill="both", expand=True)

        self.fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=grafico_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.cargar_datos()

        tk.Button(self.root, text="Cerrar", command=self.root.destroy,
                  bg="red", fg="white").pack(pady=10)

        self.root.mainloop()

    # -----------------------------------------------
    # Cargar los datos del dashboard
    # -----------------------------------------------
    def cargar_datos(self):
        datos = self.db.obtener_estadisticas_dashboard()

        total_practica = datos["total_practica"]
        total_final = datos["total_final"]
        aprob_practica = datos["aprob_practica"]
        aprob_final = datos["aprob_final"]
        promedio = datos["promedio_global"]

        # ------- Resumen -------
        texto_resumen = f"""
        Total de simulaciones de práctica: {total_practica}
        Total de simulaciones finales: {total_final}

        Aprobados práctica: {aprob_practica}
        Aprobados final: {aprob_final}

        Promedio general de calificaciones: {promedio:.2f}%
        """
        self.label_resumen.config(text=texto_resumen)

        # ------- Gráfica -------
        self.ax.clear()
        self.ax.bar(["Práctica", "Final"], [total_practica, total_final], color=["#1abc9c", "#3498db"])
        self.ax.set_title("Intentos por tipo de simulación")
        self.ax.set_ylabel("Cantidad")

        self.canvas.draw()
