import sys
import os

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector


# --------------------------------------------------
# CONFIGURACIÓN PÁGINA
# --------------------------------------------------

st.set_page_config(page_title="Personal", page_icon="👨🏽‍⚕️")


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

    /* Inputs redondeados y en rosa */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #FFB7CE !important;
    }

</style>
""", unsafe_allow_html=True)



# --------------------------------------------------
# RECUADRO ROSA (pink_box)
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
    <h1>👨🏽‍⚕️ Gestión del Personal de la Clínica</h1>
    <hr style='margin-top:5px; margin-bottom:20px;'>
""", unsafe_allow_html=True)



# --------------------------------------------------
# FUNCIONES AUXILIARES
# --------------------------------------------------

def obtener_empleados():
    query = "SELECT * FROM empleados ORDER BY id ASC"
    return db.ejecutar_query(query)

def insertar_empleado(nombre, apellidos, puesto, telefono):
    query = """
        INSERT INTO empleados (nombre, apellidos, puesto, telefono)
        VALUES (%s, %s, %s, %s)
    """
    db.ejecutar_query(query, (nombre, apellidos, puesto, telefono), fetch=False)

def actualizar_empleado(empleado_id, nombre, apellidos, puesto, telefono):
    query = """
        UPDATE empleados
        SET nombre=%s, apellidos=%s, puesto=%s, telefono=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (nombre, apellidos, puesto, telefono, empleado_id), fetch=False)

def eliminar_empleado(empleado_id):
    query = "DELETE FROM empleados WHERE id=%s"
    db.ejecutar_query(query, (empleado_id,), fetch=False)



# --------------------------------------------------
# 1. LISTA DEL PERSONAL
# --------------------------------------------------

empleados = obtener_empleados()

pink_box("📋 Lista del Personal")

st.dataframe(empleados, use_container_width=True)



# --------------------------------------------------
# 2. AÑADIR PERSONAL
# --------------------------------------------------

pink_box("➕ Añadir Personal")

puestos_posibles = [
    "Veterinario",
    "Veterinaria",
    "Auxiliar",
    "Asistente",
    "Recepción",
    "Peluquero Canino",
]

with st.form("form_anadir_empleado"):

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")

    with col2:
        puesto = st.selectbox("Puesto", puestos_posibles)
        telefono = st.text_input("Teléfono")

    if st.form_submit_button("Añadir"):
        if nombre and apellidos and puesto and telefono:
            try:
                insertar_empleado(nombre, apellidos, puesto, telefono)
                st.success("Empleado añadido correctamente 🩷")
                st.rerun()
            except Exception as e:
                st.error(f"Error al añadir empleado: {e}")
        else:
            st.warning("Completa todos los campos.")



# --------------------------------------------------
# 3. EDITAR PERSONAL
# --------------------------------------------------

pink_box("✏️ Editar Personal")

if len(empleados) > 0:

    lista_empleados = {
        f"{e['id']} - {e['nombre']} {e['apellidos']} ({e['puesto']})": e
        for e in empleados
    }

    empleado_key = st.selectbox("Selecciona empleado", list(lista_empleados.keys()))
    empleado_sel = lista_empleados[empleado_key]

    with st.form("form_editar_empleado"):
        col1, col2 = st.columns(2)

        with col1:
            nuevo_nombre = st.text_input("Nombre", empleado_sel["nombre"])
            nuevos_apellidos = st.text_input("Apellidos", empleado_sel["apellidos"])

        with col2:
            nuevo_puesto = st.selectbox("Puesto", puestos_posibles,
                                        index=puestos_posibles.index(empleado_sel["puesto"]))
            nuevo_telefono = st.text_input("Teléfono", empleado_sel["telefono"])

        if st.form_submit_button("Guardar cambios"):
            try:
                actualizar_empleado(
                    empleado_sel["id"],
                    nuevo_nombre,
                    nuevos_apellidos,
                    nuevo_puesto,
                    nuevo_telefono
                )
                st.success("Empleado actualizado correctamente 💚")
                st.rerun()
            except Exception as e:
                st.error(f"Error al actualizar empleado: {e}")

else:
    st.info("No hay empleados registrados.")



# --------------------------------------------------
# 4. ELIMINAR PERSONAL
# --------------------------------------------------

pink_box("🗑️ Eliminar Personal")

if len(empleados) > 0:
    if st.button("Eliminar empleado seleccionado"):
        try:
            eliminar_empleado(empleado_sel["id"])
            st.success("Empleado eliminado correctamente ❌")
            st.rerun()
        except Exception as e:
            st.error(f"Error al eliminar empleado: {e}")
else:
    st.info("No hay empleados para eliminar.")
