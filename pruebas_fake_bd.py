# pruebas_fake_bd.py
import random
import string
import pandas as pd
from db_manager import DBManager

ARCHIVO_PREGUNTAS = "preguntas_manejo.csv"

# CUÁNTOS USUARIOS FAKE QUIERES CREAR EN ESTA CORRIDA
NUM_USUARIOS_FAKE = 20  # puedes cambiar a 5, 10, 50, etc.

# LÍMITES POR TIPO DE SIMULADOR (por usuario)
LIMITE_PRACTICA = 6
LIMITE_FINAL = 3


# --------------------------------------------------------
# 1. Crear usuario fake y devolver su id_usuario
# --------------------------------------------------------
def generar_usuario_fake(db: DBManager) -> int:
    # nombre tipo userabcde
    nombre = "user" + "".join(random.choices(string.ascii_lowercase, k=5))
    email = nombre + "@fake.com"
    password = "1234"

    # Registrar usuario (si por alguna razón se repite el email, lo reintenta)
    registrado = db.registrar_usuario(nombre, email, password)
    if not registrado:
        # si ya existía, solo intentamos login
        print(f"El usuario {email} ya existía, se reutiliza.")
    # Recuperar el usuario para obtener id_usuario
    usuario = db.validar_login(email, password)
    if not usuario:
        raise RuntimeError(f"No se pudo recuperar el usuario {email} después de registrarlo.")

    print(f"[USUARIO FAKE] id={usuario['id_usuario']} | email={email}")
    return usuario["id_usuario"]


# --------------------------------------------------------
# 2. Simular un intento y guardarlo en la tabla intentos
# --------------------------------------------------------
def simular_intento(db: DBManager, id_usuario: int, tipo: str, cantidad_preguntas: int):
    # Cargar banco de preguntas
    df = pd.read_csv(ARCHIVO_PREGUNTAS, encoding="latin1").fillna("")

    ids_disponibles = df["ID"].tolist()
    if cantidad_preguntas > len(ids_disponibles):
        raise ValueError("cantidad_preguntas mayor al número de preguntas disponibles")

    ids_seleccionados = random.sample(ids_disponibles, cantidad_preguntas)

    errores = 0

    for id_preg in ids_seleccionados:
        correcta = df.loc[df["ID"] == id_preg, "respuesta"].values[0]

        # 70% probabilidad de acertar, 30% de fallar
        if random.random() <= 0.7:
            respuesta_usuario = correcta
        else:
            opciones = ["a", "b", "c", "d"]
            if correcta in opciones:
                opciones.remove(correcta)
            respuesta_usuario = random.choice(opciones)

        if respuesta_usuario != correcta:
            errores += 1

    # Cálculo de calificación (ajusta si tu lógica es distinta)
    puntos = 5 if tipo == "practica" else 2.5
    total = cantidad_preguntas
    puntaje = (total - errores) * puntos
    porcentaje = (puntaje / (total * puntos)) * 100
    aprobado = 1 if porcentaje >= 75 else 0

    # Aquí se llama EXACTAMENTE a tu registrar_intento
    db.registrar_intento(id_usuario, tipo, porcentaje, aprobado)

    print(
        f"[INTENTO] user={id_usuario} | tipo={tipo} | "
        f"preguntas={total} | errores={errores} | "
        f"calif={porcentaje:.2f}% | aprobado={aprobado}"
    )


# --------------------------------------------------------
# 3. Generar muchos exámenes fake respetando los límites
# --------------------------------------------------------
def main():
    db = DBManager()

    for _ in range(NUM_USUARIOS_FAKE):
        # Crear usuario nuevo
        id_usuario = generar_usuario_fake(db)

        # --------- Modo práctica (máx 6 intentos por usuario) ----------
        intentos_previos_practica = db.contar_intentos(id_usuario, "practica")
        restantes_practica = max(0, LIMITE_PRACTICA - intentos_previos_practica)

        for _ in range(restantes_practica):
            simular_intento(db, id_usuario, "practica", cantidad_preguntas=20)  # ajusta 20 si usas otro valor

        # --------- Modo final (máx 3 intentos por usuario) ----------
        intentos_previos_final = db.contar_intentos(id_usuario, "final")
        restantes_final = max(0, LIMITE_FINAL - intentos_previos_final)

        for _ in range(restantes_final):
            simular_intento(db, id_usuario, "final", cantidad_preguntas=40)  # ajusta 40 si usas otro valor

    print(f"\n✔ Listo: se generaron intentos fake para {NUM_USUARIOS_FAKE} usuarios (respetando 6 práctica / 3 final).")


if __name__ == "__main__":
    main()
