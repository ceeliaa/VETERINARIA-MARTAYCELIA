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

st.set_page_config(page_title="Citas", page_icon="📑")


# --------------------------------------------------
# ESTILOS (CSS)
# --------------------------------------------------

st.markdown("""
<style>

    .main {
        background-color: #F7F7F7;
    }

    h1 {
        color: #444444 !important;
        text-align: center !important;
        font-weight: 700 !important;
    }

    h2, h3, h4 {
        color: #444444 !important;
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
        background-color: #A7D8FF !important;
        color: black !important;
    }

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
# PINK BOX COMPONENT — RECUADRO DECORATIVO
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
# CONEXIÓN A LA BASE DE DATOS
# --------------------------------------------------

db = DataBaseConnector(password="12345678")



# --------------------------------------------------
# TÍTULO PRINCIPAL
# --------------------------------------------------

st.markdown("""
    <h1>📑 Gestión de Citas de la Clínica</h1>
    <hr style='margin-top:5px; margin-bottom:20px;'>
""", unsafe_allow_html=True)



# --------------------------------------------------
# FUNCIONES AUXILIARES
# --------------------------------------------------

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



# --------------------------------------------------
# 1. LISTA DE CITAS
# --------------------------------------------------

citas = obtener_citas()

pink_box("📋 Lista de Citas")

st.dataframe(citas, use_container_width=True)



# --------------------------------------------------
# 2. AÑADIR UNA NUEVA CITA
# --------------------------------------------------

mascotas = obtener_mascotas()
empleados = obtener_empleados()

motivos_posibles = [
    "Vacunación",
    "Vacuna antirrábica",
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

pink_box("➕ Añadir Cita 🐶💉")

with st.form("form_anadir_cita"):

    col1, col2 = st.columns(2)

    with col1:
        fecha = st.date_input("Fecha")
        hora = st.time_input("Hora")
        motivo = st.selectbox("Motivo", motivos_posibles)

    with col2:
        mascota_dict = {f"{m['id']} - {m['nombre']}": m["id"] for m in mascotas}
        mascota_sel = st.selectbox("Mascota", list(mascota_dict.keys()))
        mascota_id = mascota_dict[mascota_sel]

        empleado_dict = {f"{e['id']} - {e['nombre']} {e['apellidos']}": e["id"] for e in empleados}
        empleado_sel = st.selectbox("Veterinario", list(empleado_dict.keys()))
        empleado_id = empleado_dict[empleado_sel]

        estado = st.selectbox("Estado", estados_posibles)

    if st.form_submit_button("Añadir Cita"):
        fecha_completa = f"{fecha} {hora}"
        try:
            insertar_cita(fecha_completa, motivo, mascota_id, empleado_id, estado)
            st.success("Cita añadida correctamente 🩷")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")



# --------------------------------------------------
# 3. EDITAR CITA
# --------------------------------------------------

pink_box("✏️ Editar Cita")

if len(citas) > 0:

    lista_citas = {
        f"{c['id']} - {c['fecha']} - {c['motivo']}": c for c in citas
    }

    cita_key = st.selectbox("Selecciona una cita", list(lista_citas.keys()))
    cita_sel = lista_citas[cita_key]

    with st.form("form_editar_cita"):

        col1, col2 = st.columns(2)

        with col1:
            fecha_original = str(cita_sel["fecha"]).split(" ")[0]
            hora_original = str(cita_sel["fecha"]).split(" ")[1]

            nueva_fecha = st.date_input("Fecha", value=fecha_original)
            nueva_hora = st.time_input("Hora", value=hora_original)
            motivo_actual = cita_sel["motivo"]
            index_motivo = motivos_posibles.index(motivo_actual) if motivo_actual in motivos_posibles else 0

            nuevo_motivo = st.selectbox("Motivo", motivos_posibles, index=index_motivo)


        with col2:
            mascota_dict = {f"{m['id']} - {m['nombre']}": m["id"] for m in mascotas}
            mascota_edit = st.selectbox("Mascota", list(mascota_dict.keys()))
            nueva_mascota_id = mascota_dict[mascota_edit]

            empleado_dict = {f"{e['id']} - {e['nombre']} {e['apellidos']}": e["id"] for e in empleados}
            empleado_edit = st.selectbox("Veterinario", list(empleado_dict.keys()))
            nuevo_empleado_id = empleado_dict[empleado_edit]

            nuevo_estado = st.selectbox("Estado", estados_posibles,
                                        index=estados_posibles.index(cita_sel["estado"]))

        if st.form_submit_button("Guardar cambios"):
            nueva_fecha_completa = f"{nueva_fecha} {nueva_hora}"
            try:
                actualizar_cita(
                    cita_sel["id"], nueva_fecha_completa, nuevo_motivo,
                    nueva_mascota_id, nuevo_empleado_id, nuevo_estado
                )
                st.success("Cita actualizada correctamente 💚")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

else:
    st.info("No hay citas registradas.")



# --------------------------------------------------
# 4. ELIMINAR CITA
# --------------------------------------------------

pink_box("🗑️ Eliminar Cita")

if len(citas) > 0:
    if st.button("Eliminar cita seleccionada"):
        try:
            eliminar_cita(cita_sel["id"])
            st.success("Cita eliminada correctamente ❌")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("No hay citas para eliminar.")
