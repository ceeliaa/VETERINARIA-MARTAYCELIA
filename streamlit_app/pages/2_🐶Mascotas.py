import sys
import os

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector

st.set_page_config(page_title="Mascotas", page_icon="🐶")

# Inicializar conexión con la BBDD
db = DataBaseConnector(password="1234")

st.title("🐶 Gestión de Mascotas")


# 1. FUNCIONES AUXILIARES


def obtener_mascotas():
    query = """
        SELECT m.id, m.nombre, m.especie, m.raza, c.nombre AS dueño, c.id AS cliente_id 
        FROM mascotas m
        JOIN clientes c ON m.cliente_id = c.id
        ORDER BY m.id ASC
    """
    return db.ejecutar_query(query)

def obtener_clientes():
    query = "SELECT id, nombre, apellidos FROM clientes ORDER BY nombre ASC"
    return db.ejecutar_query(query)

def insertar_mascota(nombre, especie, raza, cliente_id):
    query = """
        INSERT INTO mascotas (nombre, especie, raza, cliente_id)
        VALUES (%s, %s, %s, %s)
    """
    db.ejecutar_query(query, (nombre, especie, raza, cliente_id), fetch=False)

def actualizar_mascota(mascota_id, nombre, especie, raza, cliente_id):
    query = """
        UPDATE mascotas
        SET nombre=%s, especie=%s, raza=%s, cliente_id=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (nombre, especie, raza, cliente_id, mascota_id), fetch=False)

def eliminar_mascota(mascota_id):
    query = "DELETE FROM mascotas WHERE id=%s"
    db.ejecutar_query(query, (mascota_id,), fetch=False)



# 2. LISTADO DE MASCOTAS

st.subheader("📋 Lista de Mascotas")

mascotas = obtener_mascotas()
st.dataframe(mascotas, use_container_width=True)


# 3. AÑADIR NUEVA MASCOTA

st.subheader("➕ Añadir Mascota")

clientes = obtener_clientes()
dic_clientes = {f"{c['id']} - {c['nombre']} {c['apellidos']}": c['id'] for c in clientes}

with st.form("form_anadir_mascota"):
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre de la mascota")
        especie = st.selectbox("Especie", ["Perro", "Gato", "Conejo", "Tortuga", "Hámster", "Hurón"])

    with col2:
        raza = st.text_input("Raza")
        cliente_seleccionado = st.selectbox("Dueño", list(dic_clientes.keys()))

    submitted = st.form_submit_button("Añadir")

    if submitted:
        try:
            insertar_mascota(
                nombre,
                especie,
                raza,
                dic_clientes[cliente_seleccionado]
            )
            st.success("Mascota añadida correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al añadir mascota: {e}")


# 4. EDITAR MASCOTA

st.subheader("✏️ Editar Mascota")

# Crear mapa id → mascota
mapa_mascotas = {f"{m['id']} - {m['nombre']} ({m['especie']})": m for m in mascotas}

mascota_key = st.selectbox("Selecciona una mascota", list(mapa_mascotas.keys()))
mascota_sel = mapa_mascotas[mascota_key]

with st.form("form_editar_mascota"):
    col1, col2 = st.columns(2)

    with col1:
        nuevo_nombre = st.text_input("Nombre", mascota_sel["nombre"])
        nueva_especie = st.selectbox("Especie", ["Perro", "Gato", "Conejo", "Tortuga", "Hámster", "Hurón"], index=["Perro", "Gato", "Conejo", "Tortuga", "Hámster", "Hurón"].index(mascota_sel["especie"]))

    with col2:
        nueva_raza = st.text_input("Raza", mascota_sel["raza"])
        nuevo_duenio = st.selectbox("Dueño", list(dic_clientes.keys()))

    submitted_edit = st.form_submit_button("Guardar cambios")

    if submitted_edit:
        try:
            actualizar_mascota(
                mascota_sel["id"],
                nuevo_nombre,
                nueva_especie,
                nueva_raza,
                dic_clientes[nuevo_duenio],
            )
            st.success("Mascota actualizada correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al actualizar mascota: {e}")


# 5. ELIMINAR MASCOTA

st.subheader("🗑️ Eliminar Mascota")

if st.button("Eliminar mascota seleccionada"):
    try:
        eliminar_mascota(mascota_sel["id"])
        st.success("Mascota eliminada correctamente.")
        st.rerun()
    except Exception as e:
        st.error(f"Error al eliminar mascota: {e}")
