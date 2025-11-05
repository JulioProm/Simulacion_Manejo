from db_manager import DBManager
from cuestionario import Cuestionario
from login_window import LoginWindow
import tkinter as tk

def iniciar_simulador(usuario):
    """
    usuario: diccionario con los datos del usuario logueado.
    """
    db = DBManager()
    usuario_id = usuario['id_usuario']
    nombre = usuario['nombre']
    print(f"\n✅ Sesión iniciada con: {nombre} (ID: {usuario_id})")

    # Selección de modo
    print("\nSelecciona modo: (1) Práctica (2) Examen Final): ")
    modo = input("> ")

    if modo == "1":
        tipo, cantidad, limite = "practica", 20, 6
    elif modo == "2":
        tipo, cantidad, limite = "final", 40, 3
    else:
        print("❌ Modo no válido.")
        return

    # Verificar intentos
    intentos = db.contar_intentos(usuario_id, tipo)
    if intentos >= limite:
        print(f"⚠️ Ya alcanzaste el máximo de {limite} intentos para el modo '{tipo}'.")
        return

    # Iniciar cuestionario
    cuestionario = Cuestionario("preguntas_manejo.csv", db)
    cuestionario.iniciar(usuario_id, tipo, cantidad)

def main():
    # Crear ventana Tkinter
    root = tk.Tk()

    # Inicializar login
    login_app = LoginWindow(root)

    # Esperar hasta que se cierre la ventana
    root.mainloop()

    # Si el login fue exitoso, abrir simulador
    if hasattr(login_app, "usuario_logeado"):
        iniciar_simulador(login_app.usuario_logeado)
    else:
        print("❌ No se inició sesión.")

if __name__ == "__main__":
    main()
