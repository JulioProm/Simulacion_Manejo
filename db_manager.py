import mysql.connector
from datetime import datetime

class DBManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="",          
            database="simulador_manejo"
        )
        print("Conexión a la base de datos establecida correctamente.")

    # --------------------------------------------------------
    # Registrar o recuperar usuario
    # --------------------------------------------------------
    def registrar_usuario(self, nombre, email, password):
        cur = self.conn.cursor()

        cur.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
        result = cur.fetchone()

        if result:
            print("El usuario ya existe.")
            cur.close()
            return False
        else:
            cur.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, password)
            )
            self.conn.commit()
            print(f"Usuario '{nombre}' registrado correctamente.")
            cur.close()
            return True

    # --------------------------------------------------------
    # Validar login
    # --------------------------------------------------------
    def validar_login(self, email, password):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        return user

    # --------------------------------------------------------
    # Contar intentos previos
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

        # Determinar id_simulador según el tipo
        if tipo == "practica":
            id_simulador = 1
        elif tipo == "final":
            id_simulador = 2
        else:
            id_simulador = None

        if id_simulador is None:
            print(" Tipo de simulador no válido.")
            cur.close()
            return

        cur.execute("""
            INSERT INTO intentos (id_usuario, tipo, id_simulador, fecha, calificacion, aprobado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, tipo, id_simulador, fecha, calificacion, aprobado))

        self.conn.commit()
        cur.close()

