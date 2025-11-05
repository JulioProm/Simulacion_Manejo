# main.py
from login_window import LoginWindow
from menu_modo import MenuModo
import tkinter as tk

def main():
    # Ventana de login
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()

    # Si el login fue exitoso, abre el menú gráfico de modos
    if hasattr(login_app, "usuario_logeado"):
        MenuModo(login_app.usuario_logeado)
    else:
        print("No se inició sesión.")

if __name__ == "__main__":
    main()
