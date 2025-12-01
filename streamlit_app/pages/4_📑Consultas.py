import sys
import os

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector

st.set_page_config(page_title="Consultas", page_icon="📑")

# Inicializar conexión
db = DataBaseConnector(password="1234")

st.title("📑 Gestión de las Consultas de la Clínica")

# 1. FUNCIONES AUXILIARES

#obtenemos las consultas por la fecha y la hora en orden descendente
def obtener_consultas():
    query = "SELECT * FROM consultas ORDER BY fecha DESC, hora DESC"
    return db.ejecutar_query(query)

def obtener_mascotas():
    query = "SELECT id, nombre FROM mascotas ORDER BY nombre ASC"
    return db.ejecutar_query(query)

def insertar_consulta(fecha, hora, veterinario, motivo, id_mascota):
    query = """
        INSERT INTO consultas (fecha, hora, veterinario, motivo, id_mascota, consulta_realizada, diagnostico)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    db.ejecutar_query(query, (fecha, hora, veterinario, motivo, id_mascota, False, ""), fetch=False)

def actualizar_consulta(consulta_id, fecha, hora, veterinario, motivo, id_mascota):
    query = """
        UPDATE consultas
        SET fecha=%s, hora=%s, veterinario=%s, motivo=%s, id_mascota=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (fecha, hora, veterinario, motivo, id_mascota, consulta_id), fetch=False)

def confirmar_realizacion_consulta(consulta_id):
    query = """
        UPDATE consultas
        SET consulta_realizada=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (True, consulta_id), fetch=False)

def registrar_diagnostico_consulta(consulta_id, diagnostico):
    query = """
        UPDATE consultas
        SET diagnostico=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (diagnostico, consulta_id), fetch=False)

def eliminar_consulta(consulta_id):
    query = "DELETE FROM consultas WHERE id=%s"
    db.ejecutar_query(query, (consulta_id,), fetch=False)


# 2. LISTADO DE CONSULTAS

st.subheader("📋 Lista de Consultas")

consultas = obtener_consultas()
st.dataframe(consultas, use_container_width=True)


# 3. AÑADIR NUEVA CONSULTA

st.subheader("➕ Añadir Consulta")

mascotas = obtener_mascotas()
veterinarios_posibles = [
    "Dr. García Pérez",
    "Dra. Martínez López",
    "Dr. Rodríguez Sánchez",
    "Dra. López Fernández",
]

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

with st.form("form_anadir_consulta"):
    col1, col2 = st.columns(2)

    with col1:
        fecha = st.date_input("Fecha")
        hora = st.time_input("Hora")
        veterinario = st.selectbox("Veterinario", veterinarios_posibles)

    with col2:
        motivo = st.selectbox("Motivo", motivos_posibles)
        # Crear selector de mascotas
        lista_mascotas = {f"{m['id']} - {m['nombre']}": m['id'] for m in mascotas}
        mascota_key = st.selectbox("Mascota", list(lista_mascotas.keys()))
        id_mascota = lista_mascotas[mascota_key]

    submitted = st.form_submit_button("Añadir Consulta")

    if submitted:
        if fecha and hora and veterinario and motivo and id_mascota:
            try:
                insertar_consulta(str(fecha), str(hora), veterinario, motivo, id_mascota)
                st.success("Consulta añadida correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al añadir consulta: {e}")
        else:
            st.warning("Completa todos los campos.")


# 4. EDITAR CONSULTA

st.subheader("✏️ Editar Consulta")

if len(consultas) > 0:
    # Crear selector
    lista_consultas = {
        f"{c['id']} - {c['fecha']} {c['hora']} - {c['veterinario']}": c for c in consultas
    }

    consulta_key = st.selectbox("Selecciona consulta", list(lista_consultas.keys()))
    consulta_sel = lista_consultas[consulta_key]

    with st.form("form_editar_consulta"):
        col1, col2 = st.columns(2)

        with col1:
            nueva_fecha = st.date_input("Fecha", value=consulta_sel["fecha"])
            nueva_hora = st.time_input("Hora", value=consulta_sel["hora"])
            nuevo_veterinario = st.selectbox("Veterinario", veterinarios_posibles, 
                                            index=veterinarios_posibles.index(consulta_sel["veterinario"]) if consulta_sel["veterinario"] in veterinarios_posibles else 0)

        with col2:
            nuevo_motivo = st.selectbox("Motivo", motivos_posibles,
                                       index=motivos_posibles.index(consulta_sel["motivo"]) if consulta_sel["motivo"] in motivos_posibles else 0)
            lista_mascotas = {f"{m['id']} - {m['nombre']}": m['id'] for m in mascotas}
            mascota_key_edit = st.selectbox("Mascota", list(lista_mascotas.keys()),
                                           index=list(lista_mascotas.values()).index(consulta_sel["id_mascota"]) if consulta_sel["id_mascota"] in lista_mascotas.values() else 0)
            nuevo_id_mascota = lista_mascotas[mascota_key_edit]

        submitted_edit = st.form_submit_button("Guardar cambios")

        if submitted_edit:
            try:
                actualizar_consulta(
                    consulta_sel["id"],
                    str(nueva_fecha),
                    str(nueva_hora),
                    nuevo_veterinario,
                    nuevo_motivo,
                    nuevo_id_mascota
                )
                st.success("Consulta actualizada correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al actualizar consulta: {e}")

    # 5. CONFIRMAR REALIZACIÓN Y REGISTRAR DIAGNÓSTICO

    st.subheader("✅ Confirmar Realización y Diagnóstico")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Estado:** {'Realizada ✅' if consulta_sel.get('consulta_realizada', False) else 'Pendiente ⏳'}")
        
        if not consulta_sel.get('consulta_realizada', False):
            if st.button("Marcar como Realizada"):
                try:
                    confirmar_realizacion_consulta(consulta_sel["id"])
                    st.success("Consulta marcada como realizada.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    with col2:
        with st.form("form_diagnostico"):
            diagnostico_actual = consulta_sel.get('diagnostico', '')
            nuevo_diagnostico = st.text_area("Diagnóstico", value=diagnostico_actual)
            
            submitted_diagnostico = st.form_submit_button("Guardar Diagnóstico")
            
            if submitted_diagnostico:
                try:
                    registrar_diagnostico_consulta(consulta_sel["id"], nuevo_diagnostico)
                    st.success("Diagnóstico registrado correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    # 6. ELIMINAR CONSULTA

    st.subheader("🗑️ Eliminar Consulta")

    if st.button("Eliminar consulta seleccionada"):
        try:
            eliminar_consulta(consulta_sel["id"])
            st.success("Consulta eliminada correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al eliminar consulta: {e}")
else:
    st.info("No hay consultas registradas.")
