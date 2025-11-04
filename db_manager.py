import mysql.connector
from datetime import datetime

class DBManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",          # usuario por defecto en XAMPP
            password="",          # vacío si no configuraste contraseña
            database="simulador_manejo"  # nombre de tu BD
        )
        print("✅ Conexión a la base de datos establecida correctamente.")

    # --------------------------------------------------------
    # Registrar o recuperar usuario
    # --------------------------------------------------------
    def registrar_usuario(self, nombre):
        cur = self.conn.cursor()

        # Buscar si el usuario ya existe
        cur.execute("SELECT id_usuario FROM usuarios WHERE nombre = %s", (nombre,))
        result = cur.fetchone()

        if result:
            user_id = result[0]
            print(f"Usuario existente con ID {user_id}")
        else:
            # Generar correo único para evitar duplicados
            email = f"{nombre.lower()}@simulacion.com"
            cur.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, "")
            )
            self.conn.commit()
            user_id = cur.lastrowid
            print(f"Nuevo usuario registrado con ID {user_id}")

        cur.close()
        return user_id

    # --------------------------------------------------------
    # Contar intentos previos de un usuario
    # --------------------------------------------------------
    def contar_intentos(self, id_usuario, tipo):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM intentos WHERE id_usuario = %s AND tipo = %s", (id_usuario, tipo))
        total = cur.fetchone()[0]
        cur.close()
        return total

    # --------------------------------------------------------
    # Registrar un nuevo intento
    # --------------------------------------------------------
    def registrar_intento(self, id_usuario, tipo, calificacion, aprobado):
        cur = self.conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO intentos (id_usuario, tipo, fecha, calificacion, aprobado)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_usuario, tipo, fecha, calificacion, aprobado))
        self.conn.commit()
        cur.close()
