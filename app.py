# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, flash
from forms.servicio_form import ServicioForm
import psycopg2
from psycopg2.extras import RealDictCursor


# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-granix"


# ==========================================================
# CONEXIÓN A POSTGRESQL
# ==========================================================

def get_db_connection():

    return psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="registro_servicios",
        user="postgres",
        password="Jose21"
    )


# ==========================================================
# OBTENER CATEGORÍAS
# ==========================================================

def obtener_categorias():

    conn = None
    cur = None

    try:

        conn = get_db_connection()

        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT
                id,
                nombre
            FROM categorias
            ORDER BY nombre ASC
        """)

        categorias = cur.fetchall()

        print("==========================================")
        print("CATEGORÍAS ENCONTRADAS:")
        print(categorias)
        print("==========================================")

        return categorias

    except psycopg2.Error as e:

        print("ERROR AL OBTENER CATEGORÍAS:")
        print(e)

        return []

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():

    return redirect(url_for("index"))


# ==========================================================
# FORMULARIO DE REGISTRO
# ==========================================================

@app.route("/registro", methods=["GET"])
def index():

    form = ServicioForm()

    categorias = obtener_categorias()

    form.categoria_id.choices = [
        (
            categoria["id"],
            categoria["nombre"]
        )
        for categoria in categorias
    ]

    if not categorias:

        flash(
            "No se encontraron categorías en la base de datos.",
            "warning"
        )

    return render_template(
        "index.html",
        form=form
    )


# ==========================================================
# REGISTRAR SERVICIO
# ==========================================================

@app.route("/registrar-servicio", methods=["POST"])
def registrar_servicio():

    form = ServicioForm()

    categorias = obtener_categorias()

    form.categoria_id.choices = [
        (
            categoria["id"],
            categoria["nombre"]
        )
        for categoria in categorias
    ]

    if not form.validate_on_submit():

        print("ERRORES DEL FORMULARIO:")
        print(form.errors)

        flash(
            "Revisa los datos ingresados.",
            "warning"
        )

        return render_template(
            "index.html",
            form=form
        )

    conn = None
    cur = None

    try:

        nombre = form.nombre.data
        precio = form.precio.data
        descripcion = form.descripcion.data
        disponible = form.disponible.data
        categoria_id = form.categoria_id.data

        conn = get_db_connection()

        cur = conn.cursor()

        cur.execute("""
            INSERT INTO servicios
            (
                nombre,
                precio,
                descripcion,
                disponible,
                categoria_id
            )
            VALUES
            (%s, %s, %s, %s, %s)
        """, (
            nombre,
            precio,
            descripcion,
            disponible,
            categoria_id
        ))

        conn.commit()

        flash(
            "Servicio registrado correctamente.",
            "success"
        )

        return redirect(url_for("servicios_page"))

    except psycopg2.Error as e:

        if conn:
            conn.rollback()

        print("ERROR DE POSTGRESQL:")
        print(e)

        flash(
            "Error al guardar el servicio.",
            "danger"
        )

        return redirect(url_for("index"))

    except Exception as e:

        if conn:
            conn.rollback()

        print("ERROR DE LA APLICACIÓN:")
        print(e)

        flash(
            "Ocurrió un error al registrar el servicio.",
            "danger"
        )

        return redirect(url_for("index"))

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()


# ==========================================================
# LISTAR SERVICIOS
# ==========================================================

@app.route("/servicios")
def servicios_page():

    conn = None
    cur = None

    try:

        conn = get_db_connection()

        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT
                s.id,
                s.nombre,
                s.precio,
                s.descripcion,
                s.disponible,
                s.categoria_id,
                c.nombre AS categoria
            FROM servicios AS s
            LEFT JOIN categorias AS c
                ON s.categoria_id = c.id
            ORDER BY s.id DESC
        """)

        servicios = cur.fetchall()

        return render_template(
            "servicios.html",
            servicios=servicios
        )

    except psycopg2.Error as e:

        print("ERROR DE POSTGRESQL:")
        print(e)

        flash(
            "No se pudieron cargar los servicios.",
            "danger"
        )

        return redirect(url_for("index"))

    except Exception as e:

        print("ERROR:")
        print(e)

        flash(
            "Ocurrió un error al cargar los servicios.",
            "danger"
        )

        return redirect(url_for("index"))

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()


# ==========================================================
# PRUEBA DE CONEXIÓN
# ==========================================================

@app.route("/probar-conexion")
def probar_conexion():

    conn = None
    cur = None

    try:

        conn = get_db_connection()

        cur = conn.cursor()

        cur.execute("SELECT current_database();")

        base_datos = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM categorias;
        """)

        cantidad_categorias = cur.fetchone()[0]

        return f"""
        <h1>Conexión correcta</h1>

        <p><strong>Base de datos:</strong>
        {base_datos}</p>

        <p><strong>Cantidad de categorías:</strong>
        {cantidad_categorias}</p>
        """

    except Exception as e:

        return f"""
        <h1>Error de conexión</h1>

        <p>{e}</p>
        """

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()


# ==========================================================
# EJECUTAR FLASK
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )