# app.py
from flask import Flask, request, render_template, redirect
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# Configuración de la conexión a PostgreSQL
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="todo_db",
            user="postgres",  # Cambia esto según tu usuario
            password="tu_password"  # Cambia esto según tu contraseña
        )
        return connection
    except Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None

# Crear la tabla si no existe
def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    description VARCHAR(200) NOT NULL,
                    completed BOOLEAN DEFAULT FALSE
                )
            """)
            conn.commit()
        except Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            cursor.close()
            conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            return render_template('index.html', tasks=tasks)
        except Error as e:
            print(f"Error al obtener tareas: {e}")
            return "Error al cargar las tareas"
        finally:
            cursor.close()
            conn.close()
    return "No se pudo conectar a la base de datos"

@app.route('/add', methods=['POST'])
def add_task():
    description = request.form['description']
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (description) VALUES (%s)",
                (description,)
            )
            conn.commit()
        except Error as e:
            print(f"Error al agregar tarea: {e}")
        finally:
            cursor.close()
            conn.close()
    return redirect('/')  # Ahora redirect está definido

if __name__ == '__main__':
    init_db()
    app.run(debug=True)