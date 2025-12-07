import sys
import os

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector

st.set_page_config(page_title="Personal", page_icon="👨🏽‍⚕️")

# Inicializar conexión
db = DataBaseConnector(password="12345678")

st.markdown("""
    <h1 style='text-align: center; color: #4A4A4A;'>
        👨🏽‍⚕️ Gestión del Personal de la Clínica
    </h1>
    <hr style='margin-top:10px; margin-bottom:20px;'>
""", unsafe_allow_html=True)



# 1. FUNCIONES AUXILIARES

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


# 2. LISTADO DE EMPLEADOS

st.subheader("📋 Lista del Personal")

empleados = obtener_empleados()
st.dataframe(empleados, use_container_width=True)


# 3. AÑADIR NUEVO EMPLEADO

st.subheader("➕ Añadir Personal")

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

    submitted = st.form_submit_button("Añadir")

    if submitted:
        if nombre and apellidos and puesto and telefono:
            try:
                insertar_empleado(nombre, apellidos, puesto, telefono)
                st.success("Empleado añadido correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al añadir empleado: {e}")
        else:
            st.warning("Completa todos los campos.")


# 4. EDITAR EMPLEADO

st.subheader("✏️ Editar Personal")

# Crear selector
lista_empleados = {
    f"{e['id']} - {e['nombre']} {e['apellidos']} ({e['puesto']})": e for e in empleados
}

empleado_key = st.selectbox("Selecciona empleado", list(lista_empleados.keys()))
empleado_sel = lista_empleados[empleado_key]

with st.form("form_editar_empleado"):
    col1, col2 = st.columns(2)

    with col1:
        nuevo_nombre = st.text_input("Nombre", empleado_sel["nombre"])
        nuevos_apellidos = st.text_input("Apellidos", empleado_sel["apellidos"])

    with col2:
        nuevo_puesto = st.selectbox("Puesto", puestos_posibles, index=puestos_posibles.index(empleado_sel["puesto"]))
        nuevo_telefono = st.text_input("Teléfono", empleado_sel["telefono"])

    submitted_edit = st.form_submit_button("Guardar cambios")

    if submitted_edit:
        try:
            actualizar_empleado(
                empleado_sel["id"],
                nuevo_nombre,
                nuevos_apellidos,
                nuevo_puesto,
                nuevo_telefono
            )
            st.success("Empleado actualizado correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al actualizar empleado: {e}")


# 5. ELIMINAR EMPLEADO

st.subheader("🗑️ Eliminar Personal")

if st.button("Eliminar empleado seleccionado"):
    try:
        eliminar_empleado(empleado_sel["id"])
        st.success("Empleado eliminado correctamente.")
        st.rerun()
    except Exception as e:
        st.error(f"Error al eliminar empleado: {e}")
