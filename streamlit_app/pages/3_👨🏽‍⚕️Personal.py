import sys
import os
import pandas as pd
import plotly.express as px

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
"""
os.path.abspath(__file__) → Obtiene la ruta absoluta del archivo
os.path.dirname(ruta) → Obtiene la carpeta que contiene el archivo
Por lo tanto, llamando 3 veces añadimos la carpeta raíz del proyecto al path
"""
sys.path.append(ROOT_DIR)
#Agregamos la carpeta raiz ROOT_DIR al path, de esta forma Python busca módulos dentro de la carpeta raiz del proyecto

import streamlit as st#se usa para crear aplicaciones web interactivas en Python
from src.database.db import DataBaseConnector
#Tenemos que importar la clase DataBaseConnector del dp.py para poder conectarse a la base de datos y ejecutar consultas


# --------------------------------------------------
# CONFIGURACIÓN PÁGINA
# --------------------------------------------------

#Comenzamos indicando como sera el titulo de la pestaña del navegador
st.set_page_config(page_title="Personal", page_icon="👨🏽‍⚕️")

# --------------------------------------------------
# ESTILOS (CSS)
# --------------------------------------------------

#Nosotras hemos decidido definir la apariencia de esta pestaña mediante el uso de css
#Seguimos un protocolo de estilo para que nuestra página tenga un diseño parecido
st.markdown("""
<style>

    .main {
        background-color: #FFF9FB;
    }

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
        color: black !important;
    }

    /* Inputs redondeados y en rosa */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #FFB7CE !important;
    }

</style>
""", unsafe_allow_html=True)
#Con esta última linea permitimos al programa de python entender html y css



# --------------------------------------------------
# PINK BOX COMPONENT
# --------------------------------------------------
#Usando la misma de idea de antes, generamos un div rosa con borde redondeado, sombra y padding (diseño de la página)
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
# CONEXIÓN A BBDD
# --------------------------------------------------
#Creamos el objeto db usando la clase DaraBaseConnector que hemos importado antes
#Necesitamos hacer esto para poder usar, consultar o modificar la base de datos más tarde
db = DataBaseConnector(password="12345678")

# --------------------------------------------------
# TÍTULO PRINCIPAL
# --------------------------------------------------

#Titulo principal de la página de Gestión de Personal
st.markdown("""
    <h1>👨🏽‍⚕️ Gestión del Personal de la Clínica</h1>
    <hr style='margin-top:5px; margin-bottom:20px;'>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FUNCIONES AUXILIARES
# --------------------------------------------------
#Estas funciones estan creadas de tal forma que se puedan llevar como "querys" o consultas a la base de datos de MySQL

#Devuelve los datos como una lista de diccionarios de los empleados registrados en la base de datos de forma ascendente según su id
def obtener_empleados():
    query = "SELECT * FROM empleados ORDER BY id ASC"
    return db.ejecutar_query(query)

#Añadimos un empleado a la base de datos junto a cuando se incluyo en esta misma (lo necesitaremos más tarde)
#con fetch=False indicamos que no esperamos resultados, solo queremos que se ejecute la acción
def insertar_empleado(nombre, apellidos, puesto, telefono):
    query = """
        INSERT INTO empleados (nombre, apellidos, puesto, telefono)
        VALUES (%s, %s, %s, %s)
    """
    db.ejecutar_query(query, (nombre, apellidos, puesto, telefono), fetch=False)
    
#A partir de la clave id modificamos información de un empleado de la base de datos
def actualizar_empleado(empleado_id, nombre, apellidos, puesto, telefono):
    query = """
        UPDATE empleados
        SET nombre=%s, apellidos=%s, puesto=%s, telefono=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (nombre, apellidos, puesto, telefono, empleado_id), fetch=False)

#A partir de un id eliminar un cliente
def eliminar_empleado(empleado_id):
    query = "DELETE FROM empleados WHERE id=%s"
    db.ejecutar_query(query, (empleado_id,), fetch=False)


"""
PARTE MÁS VISUAL DEL TRABAJO (despues del titulo)
"""

# --------------------------------------------------
# 1. TABLA con LISTA DEL PERSONAL
# --------------------------------------------------

empleados = obtener_empleados()
#guardamos en clientes el conjunto de diccionarios de nuestros usuarios y creamos un dataframe

pink_box("📋 Lista del Personal")#usamos el componente pink_box() que hemos definido anteriormente

st.dataframe(empleados, use_container_width=True)


# --------------------------------------------------
# GRÁFICO: Distribución de Personal por Puesto
# --------------------------------------------------

pink_box("📊 Distribución del Personal por Puesto")

if empleados:
    df_empleados = pd.DataFrame(empleados)

    # Contar cuántas personas hay por puesto
    conteo_puestos = df_empleados["puesto"].value_counts().reset_index()
    conteo_puestos.columns = ["Puesto", "Cantidad"]

    fig_puestos = px.bar(
        conteo_puestos,
        x="Puesto",
        y="Cantidad",
        title="Cantidad de empleados por puesto",
        color="Cantidad",
        color_continuous_scale=px.colors.sequential.Pinkyl,
        text="Cantidad"
    )

    fig_puestos.update_layout(
        xaxis_title="Puesto",
        yaxis_title="Número de empleados",
        xaxis_tickangle=45,
        showlegend=False
    )

    st.plotly_chart(fig_puestos, use_container_width=True)

else:
    st.info("No hay empleados registrados para generar gráficos.")




# --------------------------------------------------
# 2. cuadro para AÑADIR PERSONAL
# --------------------------------------------------

pink_box("➕ Añadir Personal")

puestos_posibles = [ #Es importar que hay una lista de posibles puestos que puede realizar un empleado
    "Veterinario",
    "Veterinaria",
    "Auxiliar",
    "Asistente",
    "Recepción",
    "Peluquero Canino",
]

with st.form("form_anadir_empleado"):

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")

    with col2:
        puesto = st.selectbox("Puesto", puestos_posibles)
        telefono = st.text_input("Teléfono")

    if st.form_submit_button("Añadir"):
        if nombre and apellidos and puesto and telefono:
            try:
                insertar_empleado(nombre, apellidos, puesto, telefono)
                st.success("Empleado añadido correctamente 🩷")
                st.rerun()
            except Exception as e:
                st.error(f"Error al añadir empleado: {e}")
        else:
            st.warning("Completa todos los campos.")



# --------------------------------------------------
# 3. TABLA para poder MODIFICAR CLIENTE
# --------------------------------------------------

pink_box("✏️ Editar Personal")

if len(empleados) > 0:

    lista_empleados = {
        f"{e['id']} - {e['nombre']} {e['apellidos']} ({e['puesto']})": e
        for e in empleados
    }

    empleado_key = st.selectbox("Selecciona empleado", list(lista_empleados.keys()))
    empleado_sel = lista_empleados[empleado_key]

    with st.form("form_editar_empleado"):
        col1, col2 = st.columns(2)

        with col1:
            nuevo_nombre = st.text_input("Nombre", empleado_sel["nombre"])
            nuevos_apellidos = st.text_input("Apellidos", empleado_sel["apellidos"])

        with col2:
            nuevo_puesto = st.selectbox("Puesto", puestos_posibles,
                                        index=puestos_posibles.index(empleado_sel["puesto"]))
            nuevo_telefono = st.text_input("Teléfono", empleado_sel["telefono"])

        if st.form_submit_button("Guardar cambios"):
            try:
                actualizar_empleado(
                    empleado_sel["id"],
                    nuevo_nombre,
                    nuevos_apellidos,
                    nuevo_puesto,
                    nuevo_telefono
                )
                st.success("Empleado actualizado correctamente 💚")
                st.rerun()
            except Exception as e:
                st.error(f"Error al actualizar empleado: {e}")

else:
    st.info("No hay empleados registrados.")



# --------------------------------------------------
# 4. ELIMINAR PERSONAL
# --------------------------------------------------

pink_box("🗑️ Eliminar Personal")

#Se permite eliminar el empleado que haya sido seleccionado
if len(empleados) > 0:
    if st.button("Eliminar empleado seleccionado"):
        try:
            eliminar_empleado(empleado_sel["id"])
            st.success("Empleado eliminado correctamente ❌")
            st.rerun() #Refrescar la página para tener los nuevos valores
        except Exception as e:
            st.error(f"Error al eliminar empleado: {e}")
else:
    st.info("No hay empleados para eliminar.")
