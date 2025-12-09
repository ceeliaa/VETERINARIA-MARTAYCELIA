import sys
import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

from src.database.db import DataBaseConnector
from src.modulos.saldo import Saldo


# --------------------------------------------------
# CONFIGURACIÓN PÁGINA
# --------------------------------------------------
st.set_page_config(page_title="Saldo", page_icon="💰")


# --------------------------------------------------
# ESTILOS
# --------------------------------------------------
st.markdown("""
<style>
    .main { background-color: #FFF9FB; }
    h1 { color:#4A4A4A !important; text-align:center !important; font-weight:700 !important; }

    div.stButton > button {
        background-color:#FFB7CE!important;
        color:black!important;
        border-radius:12px!important;
        border:none!important;
        padding:10px 20px!important;
        font-size:16px!important;
        font-weight:600!important;
    }
    div.stButton > button:hover {
        background-color:#FFC7DA!important;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius:10px!important;
        border:2px solid #FFB7CE!important;
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
            border-radius:14px;
            border:2px solid #FFB6C9;
            margin-top:25px;
            margin-bottom:20px;
            font-weight:600;
            font-size:20px;">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# CONEXIÓN A LA BD
# --------------------------------------------------
db = DataBaseConnector(password="12345678")
saldo = Saldo(db)


# --------------------------------------------------
# TÍTULO
# --------------------------------------------------
st.markdown("""
<h1>💰 Gestión del Saldo de la Clínica</h1>
<hr style='margin-top:5px; margin-bottom:20px;'>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SALDO ACTUAL
# --------------------------------------------------
pink_box("💵 Saldo actual")

saldo_actual = saldo.consultar_saldo()
st.metric("Saldo disponible", f"{saldo_actual:.2f} €")


# ==================================================
# 1️⃣ COBRAR A UN CLIENTE
# ==================================================
pink_box("🧾 Cobrar a un cliente")

clientes = db.ejecutar_query("SELECT id, nombre, apellidos FROM clientes ORDER BY nombre ASC")
dic_clientes = {f"{c['id']} - {c['nombre']} {c['apellidos']}": c for c in clientes}

cliente_sel = st.selectbox("Selecciona el cliente", list(dic_clientes.keys()))
cliente_obj = dic_clientes[cliente_sel]

monto_cobrar = st.number_input("Cantidad a cobrar (€)", min_value=0.0, step=1.0, format="%.2f")

if st.button("Cobrar"):
    try:
        nuevo_saldo = saldo.cobrar_consulta(
            monto=float(monto_cobrar),
            servicio="Servicio veterinario",
            cliente=f"{cliente_obj['nombre']} {cliente_obj['apellidos']}"
        )
        st.success(f"Cobro registrado. Nuevo saldo: {nuevo_saldo:.2f} €")
        st.rerun()
    except Exception as e:
        st.error(str(e))


# ==================================================
# 2️⃣ PAGAR A UN EMPLEADO
# ==================================================
pink_box("👨🏻‍⚕️ Pagar a un empleado")

empleados = db.ejecutar_query("SELECT id, nombre, apellidos FROM empleados ORDER BY nombre ASC")
dic_empleados = {f"{e['id']} - {e['nombre']} {e['apellidos']}": e for e in empleados}

empleado_sel = st.selectbox("Selecciona el empleado", list(dic_empleados.keys()))
empleado_obj = dic_empleados[empleado_sel]

monto_pago = st.number_input("Cantidad a pagar (€)", min_value=0.0, step=1.0, format="%.2f")

if st.button("Pagar"):
    try:
        nuevo_saldo = saldo.pagar_empleado(
            monto=float(monto_pago),
            empleado=f"{empleado_obj['nombre']} {empleado_obj['apellidos']}"
        )
        st.success(f"Pago registrado. Nuevo saldo: {nuevo_saldo:.2f} €")
        st.rerun()
    except Exception as e:
        st.error(str(e))


# ==================================================
# 3️⃣ HISTORIAL DE OPERACIONES
# ==================================================
pink_box("📚 Historial de Operaciones")

historial = saldo.obtener_historial()

if historial:
    st.dataframe(historial, use_container_width=True)
else:
    st.info("No hay operaciones registradas.")


# ==================================================
# 4️⃣ GRÁFICO — INGRESOS VS GASTOS
# ==================================================
pink_box("📊 Ingresos vs Gastos del Mes")

stats = saldo.obtener_estadisticas_mes()

df_stats = pd.DataFrame({
    "Tipo": ["Ingresos", "Gastos"],
    "Cantidad": [stats["ingresos"], stats["gastos"]]
})

fig = px.bar(
    df_stats,
    x="Tipo",
    y="Cantidad",
    color="Tipo",
    color_discrete_sequence=["#FF7FA6", "#FFC2D1"],
    text="Cantidad"
)

fig.update_layout(yaxis_title="€")
st.plotly_chart(fig, use_container_width=True)
