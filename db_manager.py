import mysql.connector
from datetime import datetime

class DBManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
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

    # --------------------------------------------------------
    # Obtener usuario por id (NUEVO)
    # --------------------------------------------------------
    def obtener_usuario(self, id_usuario):   # <-- CAMBIO NUEVO MÉTODO
        """
        Regresa el registro completo del usuario como diccionario
        para poder reenviarlo a MenuModo.
        """
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        user = cur.fetchone()
        cur.close()
        return user

    def obtener_estadisticas_dashboard(self):
        cur = self.conn.cursor()
        
        # Total por tipo
        cur.execute("SELECT COUNT(*) FROM intentos WHERE tipo='practica'")
        total_practica = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM intentos WHERE tipo='final'")
        total_final = cur.fetchone()[0]

        # Aprobados
        cur.execute("SELECT COUNT(*) FROM intentos WHERE tipo='practica' AND aprobado=1")
        aprob_practica = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM intentos WHERE tipo='final' AND aprobado=1")
        aprob_final = cur.fetchone()[0]

        # Promedio general
        cur.execute("SELECT AVG(calificacion) FROM intentos")
        promedio = cur.fetchone()[0] or 0

        cur.close()

        return {
            "total_practica": total_practica,
            "total_final": total_final,
            "aprob_practica": aprob_practica,
            "aprob_final": aprob_final,
            "promedio_global": promedio
    }
