import sys
import os

# Añadir root del proyecto al PATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector

# Configuración de página
st.set_page_config(page_title="Saldo", page_icon="💰")

# Conexión con contraseña correcta
db = DataBaseConnector(password="12345678")


st.markdown("""
    <h1 style='text-align: center; color: #4A4A4A;'>
        💰 Gestión del Saldo de la Clínica
    </h1>
    <hr style='margin-top:10px; margin-bottom:20px;'>
""", unsafe_allow_html=True)


# 1. FUNCIONES AUXILIARES

def consultar_saldo():
    query = "SELECT cantidad FROM saldo WHERE id = 1"
    result = db.ejecutar_query(query, fetch=True)
    if result:
        return result[0][0]
    return 0


def actualizar_saldo(nueva_cantidad):
    query = "UPDATE saldo SET cantidad = %s WHERE id = 1"
    db.ejecutar_query(query, (nueva_cantidad,), fetch=False)


# 2. MOSTRAR SALDO ACTUAL

st.subheader("💰 Saldo actual")

saldo_actual = consultar_saldo()
st.metric("Saldo disponible", f"{saldo_actual:.2f} €")


# 3. OPERACIONES MANUALES (COBRAR / PAGAR)

st.subheader("💵 Cobrar a un cliente")

monto_cobrar = st.number_input("Cantidad a cobrar (€)", min_value=0.0, step=1.0)

if st.button("Cobrar"):
    nuevo_saldo = saldo_actual + monto_cobrar
    actualizar_saldo(nuevo_saldo)
    st.success("💵 Cobro registrado correctamente.")
    st.rerun()


st.subheader("👨‍⚕️ Pagar a un empleado")

monto_pagar = st.number_input("Cantidad a pagar (€)", min_value=0.0, step=1.0)

if st.button("Pagar"):
    nuevo_saldo = saldo_actual - monto_pagar
    actualizar_saldo(nuevo_saldo)
    st.success("👨‍⚕️ Pago registrado correctamente.")
    st.rerun()
