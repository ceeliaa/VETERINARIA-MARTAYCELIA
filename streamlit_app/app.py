"""
PÁGINA DE INICIO DE NUESTRA APP
"""

import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="Vet",
    page_icon="🐒",
)

# --------------------------
# CSS GLOBAL — FONDO ROSA
# --------------------------
st.markdown(
    """
    <style>

    /* Fondo general como en el resto de la app */
    .main {
        background-color: #FFF9FB !important;
    }

    /* Ajuste del contenedor principal */
    .home-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1400px !important;
    }

    /* Imagen más grande y redondeada */
    .home-logo img {
        width: 100% !important;
        max-width: 330px !important;
        margin-top: 50px !important;
        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# CONTENIDO ENVUELTO EN CONTENEDOR
# --------------------------
st.markdown('<div class="home-container">', unsafe_allow_html=True)

# --------------------------
# Cargar imagen del logo
# --------------------------
logo_path = os.path.join("streamlit_app", "logo_vet.png")

try:
    logo = Image.open(logo_path)
except:
    st.warning("⚠️ No se encontró la imagen del logo. Revisa la ruta.")
    logo = None

# ----------------------------------
# DISEÑO EN DOS COLUMNAS
# ----------------------------------

# Texto más ancho que la imagen
col1, col2 = st.columns([4, 3])   # Puedes probar también [1.6, 1] o [2, 1]


with col1:
    st.markdown(
        """
        # Bienvenido a la clínica veterinaria! 🐾🐶🩺  

        Este sistema ha sido diseñado para facilitar tu trabajo diario, permitiéndote gestionar fácilmente los datos de clientes, mascotas, citas y tratamientos de forma rápida, segura y organizada.

        Desde aquí podrás:

        ⭐️ **Consultar y actualizar** la información de los pacientes.  
        ⭐️ **Registrar nuevas visitas**, vacunas o tratamientos.  
        ⭐️ **Gestionar citas**, historiales clínicos y comunicación con los dueños.  
        ⭐️ **Acceder a informes y estadísticas** para optimizar la atención y el funcionamiento de la clínica.  

        Nuestro objetivo es ayudarte a ahorrar tiempo, reducir errores y ofrecer un servicio de calidad a cada mascota que atendemos.  

        Gracias por formar parte del equipo y por cuidar cada día de nuestros pacientes con tanta dedicación 🩷
        """,
        unsafe_allow_html=True
    )

with col2:
    st.write("")  
    st.write("")  
    if logo:
        st.image(logo, use_container_width=True, output_format="PNG")
    else:
        st.info("Aquí aparecerá el logo.")

st.markdown("</div>", unsafe_allow_html=True)
