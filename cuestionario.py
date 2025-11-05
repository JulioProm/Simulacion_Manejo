import tkinter as tk
import pandas as pd
import random
from datetime import datetime
from db_manager import DBManager

class Cuestionario:
    def __init__(self, archivo_preguntas, db: DBManager):
        self.df = pd.read_csv(archivo_preguntas, encoding='latin1').fillna("")
        self.db = db
        self.errores = 0

    def generar_lista(self, cantidad):
        return random.sample(range(1, len(self.df)), cantidad)

    def iniciar(self, usuario_id, tipo, cantidad):
        num_preguntas = self.generar_lista(cantidad)
        self.errores = 0
        n_preg = 0

        root = tk.Tk()
        root.title("Simulador de examen de manejo")
        root.geometry("600x400")

        label_pregunta = tk.Label(root, text="", wraplength=550, justify="left")
        label_pregunta.pack(pady=10)

        selected_option = tk.StringVar(value=0)
        opciones = [tk.Radiobutton(root, variable=selected_option, value=x) for x in ['a','b','c','d']]
        for r in opciones:
            r.pack(anchor="w")

        label_tiempo = tk.Label(root, text="Tiempo restante: 60s")
        label_tiempo.pack(pady=10)
        tiempo_restante = [60]
        timer_id = [None]

        def actualizar_tiempo():
            if tiempo_restante[0] > 0:
                tiempo_restante[0] -= 1
                label_tiempo.config(text=f"Tiempo restante: {tiempo_restante[0]}s")
                timer_id[0] = root.after(1000, actualizar_tiempo)
            else:
                on_button_click() 

        def mostrar_pregunta():
            pregunta = self.df.iloc[num_preguntas[n_preg]]
            texto_pregunta = pregunta['pregunta'].replace('\\n', '\n')
            label_pregunta.config(text=f"{n_preg + 1}. {texto_pregunta}")
            
            for i, letra in enumerate(['a', 'b', 'c', 'd']):
                opciones[i].config(text=pregunta[letra])
            
            selected_option.set(0)
            tiempo_restante[0] = 60
            label_tiempo.config(text="Tiempo restante: 60s")
            timer_id[0] = root.after(1000, actualizar_tiempo)

        def on_button_click():
            nonlocal n_preg

            # Detener temporizador si está activo
            if timer_id[0]:
                root.after_cancel(timer_id[0])

            # Verificar respuesta
            respuesta_correcta = self.df['respuesta'].iloc[num_preguntas[n_preg]]
            respuesta_usuario = selected_option.get()
            print(respuesta_correcta)
            print(respuesta_usuario)
            if respuesta_correcta == respuesta_usuario :
                print("correcta")
            elif respuesta_usuario != respuesta_correcta :
                print("incorrecta")
                self.errores += 1
            else:
                print(f"Índice fuera de rango en pregunta {n_preg}")
           

            n_preg += 1

            if n_preg < len(num_preguntas):
                mostrar_pregunta()
            else:
                # Finalizar simulador
                self.finalizar(root, usuario_id, tipo, len(num_preguntas))

        tk.Button(root, text="Siguiente", command=on_button_click).pack(pady=10)
        mostrar_pregunta()
        root.mainloop()

    # Método FINALIZAR agregado
    def finalizar(self, root, usuario_id, tipo, total):
        puntos = 5 if tipo == "practica" else 2.5
        puntaje = ((total - self.errores) * puntos)
        porcentaje = (puntaje / (total * puntos)) * 100
        aprobado = 1 if porcentaje >= 75 else 0

        # Registrar el intento en la base de datos
        self.db.registrar_intento(usuario_id, tipo, porcentaje, aprobado)

        resultado = "Aprobado" if aprobado else "No aprobado"
        tk.Label(root, text=f"Resultado: {resultado}", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(root, text=f"Calificación: {porcentaje:.2f}%", font=("Arial", 12)).pack(pady=5)
        tk.Button(root, text="Finalizar", command=root.destroy).pack(pady=15)
