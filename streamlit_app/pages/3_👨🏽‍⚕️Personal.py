import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar
import streamlit as st
from src.database.db import DataBaseConnector


# --------------------------------------------------
# CONFIGURACIÓN RUTA PROYECTO
# --------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)


# --------------------------------------------------
# CONFIGURACIÓN PÁGINA
# --------------------------------------------------
st.set_page_config(page_title="Personal", page_icon="👨🏽‍⚕️")


# --------------------------------------------------
# ESTILOS CSS
# --------------------------------------------------
st.markdown("""
<style>
    .main { background-color: #FFF9FB; }

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
    }

    /* Inputs bonitos */
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
# COMPONENTE PINK BOX
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
            box-shadow:0 4px 12px rgba(255,182,201,0.4);
            font-weight:600;
            font-size:20px;
            margin-top:20px;
            margin-bottom:20px;">
            {title}
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# CONEXIÓN A BBDD
# --------------------------------------------------
db = DataBaseConnector(password="12345678")


# --------------------------------------------------
# FUNCIONES BBDD
# --------------------------------------------------
def obtener_empleados():
    return db.ejecutar_query("SELECT * FROM empleados ORDER BY id ASC")

def insertar_empleado(nombre, apellidos, puesto, telefono):
    query = """
        INSERT INTO empleados (nombre, apellidos, puesto, telefono)
        VALUES (%s, %s, %s, %s)
    """
    db.ejecutar_query(query, (nombre, apellidos, puesto, telefono), fetch=False)

def actualizar_empleado(id_, nombre, apellidos, puesto, telefono):
    query = """
        UPDATE empleados SET nombre=%s, apellidos=%s, puesto=%s, telefono=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (nombre, apellidos, puesto, telefono, id_), fetch=False)

def eliminar_empleado(id_):
    db.ejecutar_query("DELETE FROM empleados WHERE id=%s", (id_,), fetch=False)

def obtener_citas():
    query = """
        SELECT c.id, c.fecha, c.motivo,
               m.nombre AS mascota,
               e.nombre AS empleado
        FROM citas c
        JOIN mascotas m ON c.mascota_id = m.id
        JOIN empleados e ON c.empleado_id = e.id
        ORDER BY c.fecha ASC
    """
    return db.ejecutar_query(query)


# --------------------------------------------------
# TÍTULO
# --------------------------------------------------
st.markdown("""
    <h1>👨🏽‍⚕️ Gestión del Personal de la Clínica</h1>
    <hr style='margin-top:5px; margin-bottom:20px;'>
""", unsafe_allow_html=True)



# --------------------------------------------------
# 1. LISTA DEL PERSONAL
# --------------------------------------------------
empleados = obtener_empleados()

pink_box("📋 Lista del Personal")
st.dataframe(empleados, use_container_width=True)


# --------------------------------------------------
# 2. GRÁFICO EMPLEADOS POR PUESTO
# --------------------------------------------------
pink_box("📊 Distribución del Personal por Puesto")

if empleados:
    df_empleados = pd.DataFrame(empleados)
    conteo = df_empleados["puesto"].value_counts().reset_index()
    conteo.columns = ["Puesto", "Cantidad"]

    fig_puestos = px.bar(
        conteo,
        x="Puesto",
        y="Cantidad",
        color="Cantidad",
        text="Cantidad",
        color_continuous_scale=px.colors.sequential.Pinkyl,
        title="Cantidad de empleados por puesto"
    )
    
    fig_puestos.update_layout(xaxis_tickangle=45, showlegend=False)
    st.plotly_chart(fig_puestos, use_container_width=True)


# --------------------------------------------------
# 3. AÑADIR EMPLEADO
# --------------------------------------------------
pink_box("➕ Añadir Personal")

puestos_posibles = [
    "Veterinario", "Veterinaria", "Auxiliar", "Asistente",
    "Recepción", "Peluquero Canino"
]

with st.form("form_add"):
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")
    with col2:
        puesto = st.selectbox("Puesto", puestos_posibles)
        telefono = st.text_input("Teléfono")
    
    if st.form_submit_button("Añadir"):
        if nombre and apellidos and telefono:
            insertar_empleado(nombre, apellidos, puesto, telefono)
            st.success("Empleado añadido correctamente 🩷")
            st.rerun()
        else:
            st.warning("Completa todos los campos.")


# --------------------------------------------------
# 4. EDITAR EMPLEADO
# --------------------------------------------------
pink_box("✏️ Editar Personal")

if empleados:
    empleado_map = {
        f"{e['id']} - {e['nombre']} {e['apellidos']} ({e['puesto']})": e
        for e in empleados
    }

    selected_key = st.selectbox("Selecciona un empleado", list(empleado_map.keys()))
    empleado_sel = empleado_map[selected_key]

    with st.form("form_edit"):
        col1, col2 = st.columns(2)

        with col1:
            new_nombre = st.text_input("Nombre", empleado_sel["nombre"])
            new_apellidos = st.text_input("Apellidos", empleado_sel["apellidos"])

        with col2:
            new_puesto = st.selectbox(
                "Puesto", puestos_posibles,
                index=puestos_posibles.index(empleado_sel["puesto"])
            )
            new_telefono = st.text_input("Teléfono", empleado_sel["telefono"])

        if st.form_submit_button("Guardar cambios"):
            actualizar_empleado(
                empleado_sel["id"], new_nombre, new_apellidos,
                new_puesto, new_telefono
            )
            st.success("Empleado actualizado correctamente 💚")
            st.rerun()


# --------------------------------------------------
# 5. ELIMINAR EMPLEADO
# --------------------------------------------------
pink_box("🗑️ Eliminar Personal")

if empleados:
    if st.button("Eliminar empleado seleccionado"):
        eliminar_empleado(empleado_sel["id"])
        st.success("Empleado eliminado correctamente ❌")
        st.rerun()


# --------------------------------------------------
# 6. CALENDARIO MENSUAL INTERACTIVO
# --------------------------------------------------

def mostrar_calendario_mensual(df, year, month):
    cal = calendar.monthcalendar(year, month)

    # Preparar datos
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["day"] = df["fecha"].dt.day
    df["hora"] = df["fecha"].dt.strftime("%H:%M")

    eventos = df.groupby("day").apply(
        lambda x: "<br>".join(
            f"<b>{row['hora']}</b> — {row['mascota']} ({row['empleado']})<br>{row['motivo']}"
            for _, row in x.iterrows()
        )
    ).to_dict()

    # Crear lista plana
    celdas = []
    for semana in cal:
        for dia in semana:
            if dia == 0:
                celdas.append("")
            elif dia in eventos:
                celdas.append(f"<b>{dia}</b><br><br>{eventos[dia]}")
            else:
                celdas.append(f"<b>{dia}</b>")

    # Crear figura
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
            fill_color="#FFB7CE",
            align="center",
            font=dict(size=14)
        ),
        cells=dict(
            values=[celdas[i::7] for i in range(7)],
            fill_color="#FFE6EB",
            align="left",
            height=120,
            font=dict(color="#4A4A4A", size=12),
        )
    )])

    fig.update_layout(width=1000, height=900)
    return fig


# CALENDARIO INTERACTIVO
pink_box("📆 Calendario Mensual de Citas")

citas = obtener_citas()

if citas:
    df_citas = pd.DataFrame(citas)

    # Estado inicial
    if "cal_year" not in st.session_state:
        st.session_state.cal_year = datetime.now().year
    if "cal_month" not in st.session_state:
        st.session_state.cal_month = datetime.now().month

    colA, colB, colC = st.columns([2, 3, 2])

    with colA:
        if st.button("← Mes anterior"):
            if st.session_state.cal_month == 1:
                st.session_state.cal_month = 12
                st.session_state.cal_year -= 1
            else:
                st.session_state.cal_month -= 1

    with colC:
        if st.button("Mes siguiente →"):
            if st.session_state.cal_month == 12:
                st.session_state.cal_month = 1
                st.session_state.cal_year += 1
            else:
                st.session_state.cal_month += 1

    year = st.session_state.cal_year
    month = st.session_state.cal_month

    st.markdown(
        f"<h3 style='text-align:center;'>📅 {calendar.month_name[month]} {year}</h3>",
        unsafe_allow_html=True,
    )

    fig_calendar = mostrar_calendario_mensual(df_citas, year, month)
    st.plotly_chart(fig_calendar, use_container_width=True)

else:
    st.info("No hay citas registradas.")
