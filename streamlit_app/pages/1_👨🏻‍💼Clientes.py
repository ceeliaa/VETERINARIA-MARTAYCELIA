import sys
import os

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#os.path.abspath(__file__) → Obtiene la ruta absoluta del archivo
#os.path.dirname(ruta) → Obtiene la carpeta que contiene el archivo
#Por lo tanto, llamando 3 veces añadimos la carpeta raíz del proyecto al path

sys.path.append(ROOT_DIR)
#Agregamos la carpeta raiz ROOT_DIR al path, de esta forma Python busca módulos dentro de la carpeta raiz del proyecto

import streamlit as st #se usa para crear aplicaciones web interactivas en Python
import pandas as pd #para manejo de datos en Python (tablas, CSV, Excel, etc.)
import plotly.express as px #crear gráficos interactivos facilmente
from src.database.db import DataBaseConnector
#Tenemos que importar la clase DataBaseConnector del dp.py para poder conectarse a la base de datos y ejecutar consultas


# --------------------------------------------------
# CONFIGURACIÓN PÁGINA
# --------------------------------------------------

#Comenzamos indicando como sera el titulo de la pestaña del navegador
st.set_page_config(page_title="Clientes", page_icon="🧍‍♂️")


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
    <h1>🧍‍♂️ Gestión de Clientes</h1>
    <hr style='margin-top:5px; margin-bottom:20px;'>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FUNCIONES AUXILIARES
# --------------------------------------------------
#Estas funciones estan creadas de tal forma que se puedan llevar como "querys" o consultas a la base de datos de MySQL

#Devuelve los datos como una lista de diccionarios de los clientes registrados en la base de datos de forma ascendente según su id
def obtener_clientes():
    query = """
        SELECT id, nombre, apellidos, dni, telefono, correo, fecha_registro
        FROM clientes
        ORDER BY id ASC
    """
    return db.ejecutar_query(query)

#Añadimos un cliente a la base de datos junto a cuando se incluyo en esta misma (lo necesitaremos más tarde)
#con fetch=False indicamos que no esperamos resultados, solo queremos que se ejecute la acción
def insertar_cliente(nombre, apellidos, dni, telefono, correo):
    query = """
        INSERT INTO clientes (nombre, apellidos, dni, telefono, correo, fecha_registro)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """
    db.ejecutar_query(query, (nombre, apellidos, dni, telefono, correo), fetch=False)

#A partir de la clave id modificamos información de un cliente de la base de datos
def actualizar_cliente(cliente_id, nombre, apellidos, dni, telefono, correo):
    query = """
        UPDATE clientes
        SET nombre=%s, apellidos=%s, dni=%s, telefono=%s, correo=%s
        WHERE id=%s
    """
    db.ejecutar_query(query, (nombre, apellidos, dni, telefono, correo, cliente_id), fetch=False)

#A partir de un id eliminar un cliente
def eliminar_cliente(cliente_id):
    query = "DELETE FROM clientes WHERE id=%s"
    db.ejecutar_query(query, (cliente_id,), fetch=False)



#PARTE MÁS VISUAL DEL TRABAJO (despues del titulo)

# --------------------------------------------------
# 1. TABLA con la LISTA de CLIENTES
# --------------------------------------------------

pink_box("📋 Lista de Clientes")#usamos el componente pink_box() que hemos definido anteriormente

#guardamos en clientes el conjunto de diccionarios de nuestros usuarios y creamos un dataframe
clientes = obtener_clientes()
st.dataframe(clientes, use_container_width=True)


# --------------------------------------------------
# 2. cuadro para AÑADIR CLIENTE
# --------------------------------------------------

pink_box("➕ Añadir Cliente")

#Creamos un formulario de 2 columnas (efecto visual, nada más) con los pares que se deben de rellenar para guardar al clietne en la BBDD
with st.form("form_anadir_cliente"):

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")
        dni = st.text_input("DNI")

    with col2:
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo electrónico")

    #Cuando se rellenen todos los datos necesarios, se le da al boton "Añadir Cliente" y con la información recogida se llama a la función auxiliar insertar_cliente()
    if st.form_submit_button("Añadir Cliente"):
        try:
            insertar_cliente(nombre, apellidos, dni, telefono, correo)
            st.success("Cliente añadido correctamente 🩷")
            st.rerun() #Recargamos la página para actualizar la lista y por tanto los gráficos
        except Exception as e:#En caso de error:
            st.error(f"Error al añadir cliente: {e}")



# --------------------------------------------------
# 3. TABLA para poder MODIFICAR CLIENTE
# --------------------------------------------------

pink_box("✏️ Editar Cliente")

#Permite seleccionar un cliente de la lista para editarlo.

#Creamos un diccionario que mapea un string a cada cliente de esta forma: id - nombre apellidos
mapa_clientes = {f"{c['id']} - {c['nombre']} {c['apellidos']}": c for c in clientes}

#Con las claves de nuestro diccionaro creamos una lista que introducimos en un selectbox para que se puedan visualizar y buscar el cliente concreto
cliente_key = st.selectbox("Selecciona un cliente", list(mapa_clientes.keys()))
cliente_sel = mapa_clientes[cliente_key]#Guardamos el cliente seleccionado

#En estas 2 columnas mostramos los datos ACTUALES del cliente seleccionado
with st.form("form_editar_cliente"):

    col1, col2 = st.columns(2)

    with col1:
        nuevo_nombre = st.text_input("Nombre", cliente_sel["nombre"])
        nuevos_apellidos = st.text_input("Apellidos", cliente_sel["apellidos"])
        nuevo_dni = st.text_input("DNI", cliente_sel["dni"])

    with col2:
        nuevo_telefono = st.text_input("Teléfono", cliente_sel["telefono"])
        nuevo_correo = st.text_input("Correo", cliente_sel["correo"])

    if st.form_submit_button("Guardar Cambios"):
        #Tras darle al boton "Guardar Cambios" llamamos a la función actualizar_cliente() y asi de esta forma guardar los nuevos valores
        try:
            actualizar_cliente(
                cliente_sel["id"],
                nuevo_nombre,
                nuevos_apellidos,
                nuevo_dni,
                nuevo_telefono,
                nuevo_correo
            )
            st.success("Cliente actualizado correctamente 💚")
            st.rerun() #Refrescamos como antes
        except Exception as e:#Mensaje de error tras caso de fallo
            st.error(f"Error al actualizar cliente: {e}")



# --------------------------------------------------
# 4. ELIMINAR CLIENTE
# --------------------------------------------------

pink_box("🗑️ Eliminar Cliente")

#Se permite eliminar el cliente que haya sido seleccionado
if st.button("Eliminar cliente seleccionado"):
    try:
        eliminar_cliente(cliente_sel["id"])
        st.success("Cliente eliminado correctamente ❌")
        st.rerun()#Refrescar la página
    except Exception as e:#Control de errores
        st.error(f"Error al eliminar cliente: {e}")



# --------------------------------------------------
# 5. GRÁFICO DE BARRAS de Mascotas por Cliente
# --------------------------------------------------

pink_box("📊 Número de Mascotas por Cliente")

query_mascotas = """
    SELECT 
        c.id,
        CONCAT(c.nombre, ' ', c.apellidos) AS cliente,
        COUNT(m.id) AS num_mascotas
    FROM clientes c
    LEFT JOIN mascotas m ON c.id = m.cliente_id
    GROUP BY c.id, c.nombre, c.apellidos
    ORDER BY num_mascotas DESC;
"""


datos_mascotas = db.ejecutar_query(query_mascotas)
df_mascotas = pd.DataFrame(datos_mascotas)

# 🟢 Conversión clave: asegurar que num_mascotas es entero
df_mascotas["num_mascotas"] = df_mascotas["num_mascotas"].astype(int)

# Crear gráfico
fig1 = px.bar(
    df_mascotas,
    x="cliente",
    y="num_mascotas",
    color="num_mascotas",
    color_continuous_scale=px.colors.sequential.Pinkyl,
    text="num_mascotas",
    title="Mascotas por Cliente"
)


fig1.update_traces(textposition="outside")
fig1.update_layout(xaxis_title="Cliente", yaxis_title="Número de Mascotas")

st.plotly_chart(fig1, use_container_width=True)



# --------------------------------------------------
# 6. GRÁFICO sobre los CLIENTES añadidos por MES
# --------------------------------------------------

pink_box("📈 Clientes Nuevos por Mes")

query_clientes_mes = """
    SELECT DATE_FORMAT(fecha_registro, '%Y-%m') AS mes,
           COUNT(*) AS cantidad
    FROM clientes
    GROUP BY mes
    ORDER BY mes;
"""
#Ejecutamos la query donde se agrupan por mes los clientes añadidos por entonces
#Cabe recalcar que como se creo la base de datos en diciembre y los primeros añadidos han sido por ese entonces, solo habra valores en ese mes por ahora
datos_clientes_mes = db.ejecutar_query(query_clientes_mes)
df_mes = pd.DataFrame(datos_clientes_mes)

#Creamos un gráfico de linea interactivo que muestre la evolución mensual de clientes
fig2 = px.line(
    df_mes,
    x="mes",
    y="cantidad",
    markers=True, #markers=True añade puntos sobre la línea
    title="Clientes añadidos por mes"
)

fig2.update_layout(xaxis_title="Mes", yaxis_title="Clientes nuevos")
st.plotly_chart(fig2, use_container_width=True)
