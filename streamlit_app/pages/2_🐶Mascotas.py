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

st.set_page_config(page_title="Mascotas", page_icon="🐶")


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

    /* Inputs y selects */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
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
# CONEXIÓN A LA BBDD
# --------------------------------------------------
#Creamos el objeto db usando la clase DaraBaseConnector que hemos importado antes
#Necesitamos hacer esto para poder usar, consultar o modificar la base de datos más tarde
db = DataBaseConnector(password="12345678")

# --------------------------------------------------
# TÍTULO PRINCIPAL
# --------------------------------------------------
#Titulo principal de la página de Gestión de Clientes
st.markdown("""
    <h1>🐶 Gestión de Mascotas</h1>
    <hr style='margin-top:5px; margin-bottom:20px;'>
""", unsafe_allow_html=True)



# --------------------------------------------------
# FUNCIONES AUXILIARES
# --------------------------------------------------
#Estas funciones estan creadas de tal forma que se puedan llevar como "querys" o consultas a la base de datos de MySQL

#Devuelve los datos como una lista de diccionarios de las mascotas registradas en la base de datos de forma ascendente según su id
def obtener_mascotas():
    query = """
        SELECT m.id, m.nombre, m.especie, m.raza,
               c.nombre AS dueño, c.apellidos AS apellidos_dueño, c.id AS cliente_id
        FROM mascotas m
        JOIN clientes c ON m.cliente_id = c.id
        ORDER BY m.id ASC
    """
    return db.ejecutar_query(query)

#Tambien necesitaremos más tarde obtener los clientes
def obtener_clientes():
    query = "SELECT id, nombre, apellidos FROM clientes ORDER BY nombre ASC"
    return db.ejecutar_query(query)

#Añadimos una mascota a la base de datos junto a cuando se incluyo en esta misma (lo necesitaremos más tarde)
#con fetch=False indicamos que no esperamos resultados, solo queremos que se ejecute la acción
def insertar_mascota(nombre, especie, raza, cliente_id):
    query = """
        INSERT INTO mascotas (nombre, especie, raza, cliente_id)
        VALUES (%s, %s, %s, %s)
    """
    db.ejecutar_query(query, (nombre, especie, raza, cliente_id), fetch=False)

#A partir de la clave id modificamos información de una mascota de la base de datos
def actualizar_mascota(mascota_id, nombre, especie, raza, cliente_id):
    query = """
        UPDATE mascotas
        SET nombre=%s, especie=%s, raza=%s, cliente_id=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (nombre, especie, raza, cliente_id, mascota_id), fetch=False)

#A partir de un id eliminar una mascota
def eliminar_mascota(mascota_id):
    query = "DELETE FROM mascotas WHERE id=%s"
    db.ejecutar_query(query, (mascota_id,), fetch=False)


"""
PARTE MÁS VISUAL DEL TRABAJO (despues del titulo)
"""
# --------------------------------------------------
# 1. TABLA con la LISTA de MASCOTAS
# --------------------------------------------------

pink_box("📋 Lista de Mascotas")#usamos el componente pink_box() que hemos definido anteriormente

#guardamos en mascotas el conjunto de diccionarios de nuestras mascotas y creamos un dataframe
mascotas = obtener_mascotas()
st.dataframe(mascotas, use_container_width=True)


# --------------------------------------------------
# DIAGRAMA de VENN sobre MASCOTAS por especie
# --------------------------------------------------

pink_box("📊 Distribución de Mascotas por Especie")

if mascotas: #En caso de que haya mascotas if TRUE
    df_mascotas = pd.DataFrame(mascotas)

    #Contamos cuantos animales hay por especie, y los distribuimos 
    conteo_especies = df_mascotas['especie'].value_counts().reset_index()
    conteo_especies.columns = ["Especie", "Cantidad"]

    #Creamos nuestro diagrama circular
    fig_especies = px.pie(
        conteo_especies,
        names="Especie",
        values="Cantidad",
        title="Mascotas por especie",
        color_discrete_sequence=px.colors.sequential.Pinkyl
    )

    fig_especies.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig_especies, use_container_width=True)

else:
    #En caso de FALSE no hay mascotas y no se podría generar un gráfico
    st.info("No hay mascotas registradas para generar gráficos.")




# --------------------------------------------------
# 2. cuadro para AÑADIR MASCOTA
# --------------------------------------------------

pink_box("➕ Añadir Mascota")

clientes = obtener_clientes() #La mascota SIEMPRE tiene que estar relacionada con una máscota
#Por ello, necesitamos llamar a obtener_clientes
dic_clientes = {f"{c['id']} - {c['nombre']} {c['apellidos']}": c['id'] for c in clientes}

#Creamos un formulario de 2 columnas (efecto visual, nada más) con los pares que se deben de rellenar para guardar a la mascota en la BBDD
with st.form("form_anadir_mascota"):

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre de la mascota")
        especie = st.selectbox("Especie", ["Perro", "Gato", "Conejo", "Tortuga", "Hámster", "Hurón"])

    with col2:
        raza = st.text_input("Raza")
        cliente_seleccionado = st.selectbox("Dueño", list(dic_clientes.keys()))

    if st.form_submit_button("Añadir Mascota"):
        try:
            insertar_mascota(nombre, especie, raza, dic_clientes[cliente_seleccionado])
            st.success("Mascota añadida correctamente 🩷")
            st.rerun()
        except Exception as e:
            st.error(f"Error al añadir mascota: {e}")



# --------------------------------------------------
# 3. TABLA para poder MODIFICAR MASCOTA
# --------------------------------------------------

pink_box("✏️ Editar Mascota")

"""
Crea un diccionario que mapea un string descriptivo a cada mascota (id - nombre especie).

Permite seleccionar un cliente de la lista para editarlo.
"""
#Creamos un diccionario que mapea un string a cada mascota de esta forma: id - nombre especie
mapa_mascotas = {f"{m['id']} - {m['nombre']} ({m['especie']})": m for m in mascotas}

#Con las claves de nuestro diccionaro creamos una lista que introducimos en un selectbox para que se puedan visualizar y buscar la mascota concreta
mascota_key = st.selectbox("Selecciona una mascota", list(mapa_mascotas.keys()))
mascota_sel = mapa_mascotas[mascota_key]

#En estas 2 columnas mostramos los datos ACTUALES de la mascota seleccionado
with st.form("form_editar_mascota"):

    col1, col2 = st.columns(2)

    with col1:
        nuevo_nombre = st.text_input("Nombre", mascota_sel["nombre"])
        nueva_especie = st.selectbox(
            "Especie",
            ["Perro", "Gato", "Conejo", "Tortuga", "Hámster", "Hurón"],
            index=["Perro", "Gato", "Conejo", "Tortuga", "Hámster", "Hurón"].index(mascota_sel["especie"])
        )

    with col2:
        nueva_raza = st.text_input("Raza", mascota_sel["raza"])
        nuevo_duenio = st.selectbox("Dueño", list(dic_clientes.keys()))
        
    #Tras darle al boton "Guardar Cambios" llamamos a la función actualizar_mascota() y asi de esta forma guardar los nuevos valores
    if st.form_submit_button("Guardar cambios"):
        try:
            actualizar_mascota(
                mascota_sel["id"],
                nuevo_nombre,
                nueva_especie,
                nueva_raza,
                dic_clientes[nuevo_duenio]
            )
            st.success("Mascota actualizada correctamente 💚")
            st.rerun()
        except Exception as e:
            st.error(f"Error al actualizar mascota: {e}")



# --------------------------------------------------
# 4. ELIMINAR MASCOTA
# --------------------------------------------------

pink_box("🗑️ Eliminar Mascota")

#Se permite eliminar la mascota que haya sido seleccionada

if st.button("Eliminar mascota seleccionada"):
    try:
        eliminar_mascota(mascota_sel["id"])
        st.success("Mascota eliminada correctamente ❌")
        st.rerun()#Refrescar la página
    except Exception as e:#Control de errores
        st.error(f"Error al eliminar mascota: {e}")
