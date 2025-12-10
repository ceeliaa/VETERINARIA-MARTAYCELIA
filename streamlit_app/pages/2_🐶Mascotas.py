import sys
import os
import pandas as pd
import plotly.express as px

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector


# --------------------------------------------------
# CONFIGURACIÓN PÁGINA
# --------------------------------------------------

st.set_page_config(page_title="Mascotas", page_icon="🐶")

# --------------------------------------------------
# ESTILOS (CSS)
# --------------------------------------------------

st.markdown("""
<style>

    .main {
        background-color: #FFF9FB;
    }

    h1 {
        color: #4A4A4A !important;
        text-align: center !important;
        font-weight: 700 !important;
    }

    h2, h3, h4 {
        color: #4A4A4A !important;
        font-weight: 600 !important;
    }

    div.stButton > button {
        background-color: #FFB7CE !important;
        color: black !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    div.stButton > button:hover {
        background-color: #FFC7DA !important;
        color: black !important;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #FFB7CE !important;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PINK BOX COMPONENT
# --------------------------------------------------

def pink_box(title):
    st.markdown(
        f"""
        <div style="
            background-color:#FFE6EB;
            padding:18px;
            padding-left:25px;
            border-radius:14px;
            border:2px solid #FFB6C9;
            box-shadow:0 4px 12px rgba(255, 182, 201, 0.4);
            font-weight:600;
            font-size:20px;
            margin-top:20px;
            margin-bottom:20px;">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# CONEXIÓN A BBDD
# --------------------------------------------------

db = DataBaseConnector(password="12345678")


# --------------------------------------------------
# TÍTULO PRINCIPAL
# --------------------------------------------------

st.markdown("""
    <h1>🐶 Gestión de Mascotas</h1>
    <hr style='margin-top:5px; margin-bottom:20px;'>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FUNCIONES AUXILIARES
# --------------------------------------------------

def obtener_mascotas():
    query = """
        SELECT 
            m.id AS id_mascota,
            m.nombre AS nombre_mascota,
            m.especie,
            m.raza,
            m.sexo,
            m.edad,
            m.estado_salud,
            c.dni AS dni_cliente,
            c.nombre AS dueño,
            c.apellidos AS apellidos_dueño,
            m.cliente_id
        FROM mascotas m
        JOIN clientes c ON m.cliente_id = c.id
        ORDER BY m.id ASC
    """
    return db.ejecutar_query(query)


def obtener_clientes():
    query = "SELECT id, nombre, apellidos FROM clientes ORDER BY nombre ASC"
    return db.ejecutar_query(query)


def insertar_mascota(nombre, especie, raza, sexo, edad, estado_salud, cliente_id):
    query = """
        INSERT INTO mascotas (nombre, especie, raza, sexo, edad, estado_salud, cliente_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    db.ejecutar_query(query, (nombre, especie, raza, sexo, edad, estado_salud, cliente_id), fetch=False)


def actualizar_mascota(mascota_id, nombre, especie, raza, sexo, edad, estado_salud, cliente_id):
    query = """
        UPDATE mascotas
        SET nombre=%s, especie=%s, raza=%s, sexo=%s, edad=%s, estado_salud=%s, cliente_id=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (nombre, especie, raza, sexo, edad, estado_salud, cliente_id, mascota_id), fetch=False)


def eliminar_mascota(mascota_id):
    query = "DELETE FROM mascotas WHERE id=%s"
    db.ejecutar_query(query, (mascota_id,), fetch=False)


# --------------------------------------------------
# 1. LISTA DE MASCOTAS
# --------------------------------------------------

pink_box("📋 Lista de Mascotas")

mascotas = obtener_mascotas()
st.dataframe(mascotas, use_container_width=True)


# --------------------------------------------------
# 2. GRÁFICO — Mascotas por especie
# --------------------------------------------------

pink_box("📊 Distribución de Mascotas por Especie")

if mascotas:
    df = pd.DataFrame(mascotas)

    conteo = df["especie"].value_counts().reset_index()
    conteo.columns = ["Especie", "Cantidad"]

    fig = px.pie(
        conteo,
        names="Especie",
        values="Cantidad",
        title="Mascotas por especie",
        color_discrete_sequence=px.colors.sequential.Pinkyl
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay mascotas registradas para generar gráficos.")



# --------------------------------------------------
# 3. AÑADIR MASCOTA
# --------------------------------------------------

pink_box("➕ Añadir Mascota")

clientes = obtener_clientes()
dic_clientes = {f"{c['id']} - {c['nombre']} {c['apellidos']}": c['id'] for c in clientes}

with st.form("form_anadir_mascota"):

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre de la mascota")
        especie = st.selectbox("Especie", ["Perro", "Gato", "Conejo", "Tortuga", "Hámster", "Hurón"])
        sexo = st.selectbox("Sexo", ["Macho", "Hembra"])
        edad = st.number_input("Edad", min_value=0, max_value=40, step=1)

    with col2:
        raza = st.text_input("Raza")
        estado_salud = st.selectbox("Estado de salud", ["Sano", "En tratamiento", "Crónico"])
        cliente_sel = st.selectbox("Dueño", list(dic_clientes.keys()))

    if st.form_submit_button("Añadir Mascota"):
        try:
            insertar_mascota(nombre, especie, raza, sexo, edad, estado_salud, dic_clientes[cliente_sel])
            st.success("Mascota añadida correctamente 🩷")
            st.rerun()
        except Exception as e:
            st.error(f"Error al añadir mascota: {e}")



# --------------------------------------------------
# 4. EDITAR MASCOTA
# --------------------------------------------------

pink_box("✏️ Editar Mascota")

mapa_mascotas = {
    f"{m['id_mascota']} - {m['nombre_mascota']} ({m['especie']})": m
    for m in mascotas
}

mascota_key = st.selectbox("Selecciona una mascota", list(mapa_mascotas.keys()))
mascota_sel = mapa_mascotas[mascota_key]

with st.form("form_editar_mascota"):

    col1, col2 = st.columns(2)

    with col1:
        nuevo_nombre = st.text_input("Nombre", mascota_sel["nombre_mascota"])
        nueva_especie = st.selectbox("Especie",
            ["Perro", "Gato", "Conejo", "Tortuga", "Hámster", "Hurón"],
            index=["Perro", "Gato", "Conejo", "Tortuga", "Hámster", "Hurón"].index(mascota_sel["especie"])
        )
        nuevo_sexo = st.selectbox("Sexo", ["Macho", "Hembra"], index=0 if mascota_sel["sexo"] == "Macho" else 1)
        nueva_edad = st.number_input("Edad", value=mascota_sel["edad"], min_value=0, max_value=40)

    with col2:
        nueva_raza = st.text_input("Raza", mascota_sel["raza"])
        nuevo_estado = st.selectbox("Estado de salud", ["Sano", "En tratamiento", "Crónico"])
        nuevo_duenio = st.selectbox("Dueño", list(dic_clientes.keys()))

    if st.form_submit_button("Guardar cambios"):
        try:
            actualizar_mascota(
                mascota_sel["id_mascota"],
                nuevo_nombre,
                nueva_especie,
                nueva_raza,
                nuevo_sexo,
                nueva_edad,
                nuevo_estado,
                dic_clientes[nuevo_duenio]
            )
            st.success("Mascota actualizada correctamente 💚")
            st.rerun()
        except Exception as e:
            st.error(f"Error al actualizar mascota: {e}")



# --------------------------------------------------
# 5. ELIMINAR MASCOTA
# --------------------------------------------------

pink_box("🗑️ Eliminar Mascota")

if st.button("Eliminar mascota seleccionada"):
    try:
        eliminar_mascota(mascota_sel["id_mascota"])
        st.success("Mascota eliminada correctamente ❌")
        st.rerun()
    except Exception as e:
        st.error(f"Error al eliminar mascota: {e}")
