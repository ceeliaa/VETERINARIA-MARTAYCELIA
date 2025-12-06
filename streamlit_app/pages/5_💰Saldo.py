import sys
import os

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector

st.set_page_config(page_title="Saldo", page_icon="💰") #Cambiar el icono que eso ns hacerlo

# Inicializar conexión
db = DataBaseConnector(password="1234")

st.title("💰 Gestión del Saldo de la Clínica")

# 1. FUNCIONES AUXILIARES

def consultar_saldo():
    query = "SELECT saldo_final FROM saldo"
    return db.ejecutar_query(query)

def consultar_historial_operaciones():
    query = "SELECT operaciones FROM saldo"
    return db.ejecutar_query(query)



# 2. CONSULTAR SALDO ACTUAL

st.subheader("💰 Saldo actual")

saldo = consultar_saldo()
st.dataframe(saldo, use_container_width=True)


# 3. CONSULTAR HISTORIAL DE OPERACIONES

st.subheader("💰 Lista de Operaciones")

operaciones_saldo = consultar_historial_operaciones()
st.dataframe(operaciones_saldo, use_container_width=True)




