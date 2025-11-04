from db_manager import DBManager
from cuestionario import Cuestionario


def main():
    nombre = input("Ingresa tu nombre: ")
    db = DBManager()  # <- aquí se llama el constructor que crea self.conn
    usuario_id = db.registrar_usuario(nombre)
    print(f"ID del usuario: {usuario_id}")

    modo = input("Selecciona modo: (1) Práctica (2) Examen Final): ")
    if modo == "1":
        tipo, cantidad, limite = "practica", 20, 6
    elif modo == "2":
        tipo, cantidad, limite = "final", 40, 3
    else:
        print("Modo no válido.")
        return

    intentos = db.contar_intentos(usuario_id, tipo)
    if intentos >= limite:
        print(f"Ya alcanzaste el máximo de {limite} intentos para el modo {tipo}.")
        return

    cuestionario = Cuestionario(r"C:\Users\julio\OneDrive\Escritorio\7 semestre\Simulacion\Simulacion_Manejo\preguntas_manejo.csv", db)
    cuestionario.iniciar(usuario_id, tipo, cantidad)

if __name__ == "__main__":
    main()
