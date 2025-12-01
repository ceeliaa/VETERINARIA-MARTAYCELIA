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
