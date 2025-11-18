# pruebas_fake_bd.py
import random
import string
import tkinter as tk

from db_manager import DBManager
from cuestionario import Cuestionario  

ARCHIVO_PREGUNTAS = "preguntas_manejo.csv"

NUM_USUARIOS_FAKE = 20

LIMITE_PRACTICA = 6
LIMITE_FINAL = 3

def generar_usuario_fake(db: DBManager) -> int:
    
    nombre = "user" + "".join(random.choices(string.ascii_lowercase, k=5))
    email = nombre + "@fake.com"
    password = "1234"

    db.registrar_usuario(nombre, email, password)

    usuario = db.validar_login(email, password)
    if not usuario:
        raise RuntimeError(f"No se pudo recuperar el usuario {email} después de registrarlo.")

    print(f"[USUARIO FAKE] id={usuario['id_usuario']} | email={email}")
    return usuario["id_usuario"]


def simular_intento(db: DBManager, id_usuario: int, tipo: str, cantidad_preguntas: int):
    
    q = Cuestionario(ARCHIVO_PREGUNTAS, db)
    q.errores = 0

    
    indices_preguntas = q.generar_lista(cantidad_preguntas)

    for idx in indices_preguntas:
        respuesta_correcta = q.df["respuesta"].iloc[idx]

        if random.random() <= 0.7:
            respuesta_usuario = respuesta_correcta
        else:
            opciones = ["a", "b", "c", "d"]
            if respuesta_correcta in opciones:
                opciones.remove(respuesta_correcta)
            respuesta_usuario = random.choice(opciones)

        if respuesta_usuario != respuesta_correcta:
            q.errores += 1  

    total = len(indices_preguntas)

    
    root = tk.Tk()
    root.withdraw()  
    q.finalizar(root, id_usuario, tipo, total)
    root.destroy()

    print(
        f"[INTENTO FAKE] user={id_usuario} | tipo={tipo} | "
        f"preguntas={total} | errores={q.errores}"
    )


def main():
    
    db = DBManager()

    for _ in range(NUM_USUARIOS_FAKE):
        
        id_usuario = generar_usuario_fake(db)

        
        intentos_previos_practica = db.contar_intentos(id_usuario, "practica")
        restantes_practica = max(0, LIMITE_PRACTICA - intentos_previos_practica)

        for _ in range(restantes_practica):
            simular_intento(db, id_usuario, "practica", cantidad_preguntas=20)

        # ---- Modo final ----
        intentos_previos_final = db.contar_intentos(id_usuario, "final")
        restantes_final = max(0, LIMITE_FINAL - intentos_previos_final)

        for _ in range(restantes_final):
            simular_intento(db, id_usuario, "final", cantidad_preguntas=40)

    print(
        f"se generaron intentos fake para {NUM_USUARIOS_FAKE} usuarios "
    )


if __name__ == "__main__":
    main()
