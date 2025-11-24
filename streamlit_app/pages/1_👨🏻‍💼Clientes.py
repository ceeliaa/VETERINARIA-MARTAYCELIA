import sys
import os

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector

st.set_page_config(page_title="Clientes", page_icon="👨🏻‍💼")

# Inicializamos la conexión con la base de datos  
db = DataBaseConnector(password="1234")  # si tu contraseña es otra, cámbiala

st.title("👨🏻‍💼 Gestión de Clientes")



# 1. FUNCIONES AUXILIARES

#Obtenemos los clientes y las mascotas de la base de datos
def obtener_clientes():
    query = "SELECT * FROM clientes ORDER BY id ASC"
    return db.ejecutar_query(query)

def obtener_mascotas_de_cliente(cliente_id):
    query = "SELECT * FROM mascotas WHERE cliente_id = %s"
    return db.ejecutar_query(query, (cliente_id,))

def insertar_cliente(nombre, apellidos, dni, telefono, correo):
    query = """
        INSERT INTO clientes (nombre, apellidos, dni, telefono, correo)
        VALUES (%s, %s, %s, %s, %s)
    """
    db.ejecutar_query(query, (nombre, apellidos, dni, telefono, correo), fetch=False)

def eliminar_cliente(cliente_id):
    query = "DELETE FROM clientes WHERE id = %s"
    db.ejecutar_query(query, (cliente_id,), fetch=False)

def actualizar_cliente(cliente_id, nombre, apellidos, dni, telefono, correo):
    query = """
        UPDATE clientes
        SET nombre=%s, apellidos=%s, dni=%s, telefono=%s, correo=%s
        WHERE id = %s
    """
    db.ejecutar_query(query, (nombre, apellidos, dni, telefono, correo, cliente_id), fetch=False)
    # todos llevan lo de fetch=False menos  los que necesito que me devuelvan algún dato



# 2. LISTADO DE CLIENTES

st.subheader("📋 Lista de Clientes")

clientes = obtener_clientes()
st.dataframe(clientes, use_container_width=True)


# 3. AÑADIR NUEVO CLIENTE

st.subheader("➕ Añadir Cliente")

with st.form("form_anadir_cliente"):
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")
        dni = st.text_input("DNI")

    with col2:
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo")

    submitted = st.form_submit_button("Añadir")

    if submitted:
        if nombre and apellidos and dni and telefono and correo:
            try:
                insertar_cliente(nombre, apellidos, dni, telefono, correo)
                st.success("Cliente añadido correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al añadir: {e}")
        else:
            st.warning("Completa todos los campos.")


# 4. EDITAR CLIENTE

st.subheader("✏️ Editar Cliente")

lista_nombres = {f"{c['id']} - {c['nombre']} {c['apellidos']}": c for c in clientes}
select_cliente = st.selectbox("Selecciona un cliente", list(lista_nombres.keys()))

cliente_seleccionado = lista_nombres[select_cliente]

with st.form("form_editar_cliente"):
    col1, col2 = st.columns(2)

    with col1:
        nuevo_nombre = st.text_input("Nombre", cliente_seleccionado["nombre"])
        nuevos_apellidos = st.text_input("Apellidos", cliente_seleccionado["apellidos"])
        nuevo_dni = st.text_input("DNI", cliente_seleccionado["dni"])

    with col2:
        nuevo_telefono = st.text_input("Teléfono", cliente_seleccionado["telefono"])
        nuevo_correo = st.text_input("Correo", cliente_seleccionado["correo"])

    submitted_edit = st.form_submit_button("Guardar Cambios")

    if submitted_edit:
        try:
            actualizar_cliente(
                cliente_seleccionado["id"],
                nuevo_nombre,
                nuevos_apellidos,
                nuevo_dni,
                nuevo_telefono,
                nuevo_correo,
            )
            st.success("Cliente actualizado correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al editar: {e}")


# 5. VER MASCOTAS DEL CLIENTE

st.subheader("🐾 Mascotas del Cliente")

cliente_id = cliente_seleccionado["id"]
mascotas = obtener_mascotas_de_cliente(cliente_id)

if mascotas:
    st.table(mascotas)
else:
    st.info("Este cliente no tiene mascotas registradas.")


# 6. ELIMINAR CLIENTE

st.subheader("🗑️ Eliminar Cliente")

if st.button("Eliminar cliente seleccionado"):
    try:
        eliminar_cliente(cliente_seleccionado["id"])
        st.success("Cliente eliminado correctamente.")
        st.rerun()
    except Exception as e:
        st.error(f"Error al eliminar: {e}")
