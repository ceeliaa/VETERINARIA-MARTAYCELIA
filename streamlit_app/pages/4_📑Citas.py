import sys
import os

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector

st.set_page_config(page_title="Consultas", page_icon="📑")

# Inicializar conexión
db = DataBaseConnector(password="12345678")

st.title("📑 Gestión de Citas de la Clínica")

# 1. FUNCIONES AUXILIARES 

def obtener_citas():
    query = "SELECT * FROM citas ORDER BY fecha DESC"
    return db.ejecutar_query(query)

def obtener_mascotas():
    query = "SELECT id, nombre FROM mascotas ORDER BY nombre ASC"
    return db.ejecutar_query(query)

def obtener_empleados():
    query = "SELECT id, nombre, apellidos FROM empleados ORDER BY nombre ASC"
    return db.ejecutar_query(query)

def insertar_cita(fecha, motivo, mascota_id, empleado_id, estado):
    query = """
        INSERT INTO citas (fecha, motivo, mascota_id, empleado_id, estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    db.ejecutar_query(query, (fecha, motivo, mascota_id, empleado_id, estado), fetch=False)

def actualizar_cita(cita_id, fecha, motivo, mascota_id, empleado_id, estado):
    query = """
        UPDATE citas
        SET fecha=%s, motivo=%s, mascota_id=%s, empleado_id=%s, estado=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (fecha, motivo, mascota_id, empleado_id, estado, cita_id), fetch=False)

def eliminar_cita(cita_id):
    query = "DELETE FROM citas WHERE id=%s"
    db.ejecutar_query(query, (cita_id,), fetch=False)

# 2. LISTADO DE CITAS

st.subheader("📋 Lista de Citas")

citas = obtener_citas()
st.dataframe(citas, use_container_width=True)

# 3. AÑADIR NUEVA CITA

st.subheader("➕ Añadir Cita")

mascotas = obtener_mascotas()
empleados = obtener_empleados()

motivos_posibles = [
    "Vacunación",
    "Revisión general",
    "Desparasitación",
    "Consulta dermatológica",
    "Consulta digestiva",
    "Urgencia",
    "Cirugía",
    "Control post-operatorio",
    "Otro"
]

estados_posibles = ["Pendiente", "Realizada", "Cancelada"]

with st.form("form_anadir_cita"):

    col1, col2 = st.columns(2)

    with col1:
        fecha = st.datetime_input("Fecha y hora")
        motivo = st.selectbox("Motivo", motivos_posibles)

    with col2:
        mascota_dict = {f"{m['id']} - {m['nombre']}": m["id"] for m in mascotas}
        mascota_key = st.selectbox("Mascota", list(mascota_dict.keys()))
        mascota_id = mascota_dict[mascota_key]

        empleado_dict = {f"{e['id']} - {e['nombre']} {e['apellidos']}": e["id"] for e in empleados}
        empleado_key = st.selectbox("Veterinario", list(empleado_dict.keys()))
        empleado_id = empleado_dict[empleado_key]

        estado = st.selectbox("Estado", estados_posibles)

    submitted = st.form_submit_button("Añadir Cita")

    if submitted:
        try:
            insertar_cita(str(fecha), motivo, mascota_id, empleado_id, estado)
            st.success("Cita añadida correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al añadir cita: {e}")

# 4. EDITAR CITA

st.subheader("✏️ Editar Cita")

if len(citas) > 0:
    lista_citas = {
        f"{c['id']} - {c['fecha']} - {c['motivo']}": c for c in citas
    }

    cita_key = st.selectbox("Selecciona una cita", list(lista_citas.keys()))
    cita_sel = lista_citas[cita_key]

    with st.form("form_editar_cita"):
        col1, col2 = st.columns(2)

        with col1:
            nueva_fecha = st.datetime_input("Fecha y hora", value=cita_sel["fecha"])
            nuevo_motivo = st.selectbox("Motivo", motivos_posibles,
                                        index=motivos_posibles.index(cita_sel["motivo"]) if cita_sel["motivo"] in motivos_posibles else 0)

        with col2:
            mascota_id_old = cita_sel["mascota_id"]
            mascota_key_edit = list(mascota_dict.values()).index(mascota_id_old)
            nueva_mascota_id = st.selectbox("Mascota", list(mascota_dict.keys()), index=mascota_key_edit)
            nueva_mascota_id = mascota_dict[nueva_mascota_id]

            empleado_id_old = cita_sel["empleado_id"]
            empleado_key_edit = list(empleado_dict.values()).index(empleado_id_old)
            nuevo_empleado_id = st.selectbox("Veterinario", list(empleado_dict.keys()), index=empleado_key_edit)
            nuevo_empleado_id = empleado_dict[nuevo_empleado_id]

            nuevo_estado = st.selectbox("Estado", estados_posibles,
                                        index=estados_posibles.index(cita_sel["estado"]))

        submitted_edit = st.form_submit_button("Guardar cambios")

        if submitted_edit:
            try:
                actualizar_cita(
                    cita_sel["id"], str(nueva_fecha), nuevo_motivo,
                    nueva_mascota_id, nuevo_empleado_id, nuevo_estado
                )
                st.success("Cita actualizada correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al actualizar cita: {e}")

# 5. ELIMINAR CITA

    st.subheader("🗑️ Eliminar Cita")

    if st.button("Eliminar cita seleccionada"):
        try:
            eliminar_cita(cita_sel["id"])
            st.success("Cita eliminada correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al eliminar cita: {e}")

else:
    st.info("No hay citas registradas.")


