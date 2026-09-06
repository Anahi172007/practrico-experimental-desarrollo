from flask import Flask, render_template, redirect, url_for, flash
from forms.servicio_form import ServicioForm
import sqlite3
import os


# ==========================================
# CONFIGURACIÓN DE FLASK
# ==========================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-granix"


# ==========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

DATABASE = os.path.join(DATA_DIR, "servicios.db")


# ==========================================
# CONEXIÓN A LA BASE DE DATOS
# ==========================================

def conectar_db():

    # Crear carpeta data si no existe
    os.makedirs(DATA_DIR, exist_ok=True)

    # Conectar a SQLite
    conn = sqlite3.connect(DATABASE)

    # Permitir acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# CREAR BASE DE DATOS Y TABLA
# ==========================================

def crear_base_datos():

    # Crear carpeta data
    os.makedirs(DATA_DIR, exist_ok=True)

    # Conectar a la base de datos
    conn = conectar_db()

    # Crear tabla servicios
    conn.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            disponible INTEGER NOT NULL DEFAULT 1
        )
    """)

    # Guardar cambios
    conn.commit()

    # Cerrar conexión
    conn.close()


# ==========================================
# PÁGINA DE INICIO
# ==========================================

@app.route("/")
def inicio():

    # Nombre del sistema
    nombre_sistema = "Sistema de Registro de Servicios"

    # Crear formulario
    form = ServicioForm()

    # Mostrar index.html y enviar el formulario
    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema,
        form=form
    )


# ==========================================
# MOSTRAR SERVICIOS
# ==========================================

@app.route("/servicios")
def servicios_page():

    # Conectar a SQLite
    conn = conectar_db()

    # Consultar servicios
    servicios = conn.execute("""
        SELECT
            id,
            nombre,
            precio,
            descripcion,
            categoria,
            disponible
        FROM servicios
        ORDER BY id DESC
    """).fetchall()

    # Cerrar conexión
    conn.close()

    # Mostrar servicios.html
    return render_template(
        "servicios.html",
        servicios=servicios
    )


# ==========================================
# REGISTRAR SERVICIO
# ==========================================

@app.route("/registrar", methods=["GET", "POST"])
def registrar_servicio():

    # Crear formulario
    form = ServicioForm()

    # Validar formulario
    if form.validate_on_submit():

        # Obtener datos
        nombre = form.nombre.data
        precio = form.precio.data
        descripcion = form.descripcion.data
        categoria = form.categoria.data

        # Conectar a SQLite
        conn = conectar_db()

        try:

            # Insertar servicio
            conn.execute("""
                INSERT INTO servicios
                (
                    nombre,
                    precio,
                    descripcion,
                    categoria,
                    disponible
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                nombre,
                precio,
                descripcion,
                categoria,
                1
            ))

            # Guardar cambios
            conn.commit()

        finally:

            # Cerrar conexión
            conn.close()

        # Mensaje de confirmación
        flash(
            "Servicio registrado correctamente.",
            "success"
        )

        # Ir a Servicios
        return redirect(
            url_for("servicios_page")
        )

    # Si hay errores, mostrar formulario
    return render_template(
        "formulario_servicio.html",
        form=form
    )


# ==========================================
# INICIAR APLICACIÓN
# ==========================================

if __name__ == "__main__":

    # Crear base de datos y tabla
    crear_base_datos()

    # Ejecutar Flask
    app.run(debug=True)