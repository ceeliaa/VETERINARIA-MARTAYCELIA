import sys
import os
import streamlit as st

# Añadimos la ruta raíz para que Python encuentre src/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

from src.database.sqlalchemy_connector import SessionLocal
from src.database.orm.cliente_orm import ClienteORM
from src.database.orm.mascota_orm import MascotaORM

st.set_page_config(page_title="Clientes", page_icon="👨🏻‍💼")


st.markdown("""
    <h1 style='text-align: center; color: #4A4A4A;'>
        👨🏻‍💼 Gestión de Clientes
    </h1>
    <hr style='margin-top:10px; margin-bottom:20px;'>
""", unsafe_allow_html=True)

# 1. Inicializar sesión con la bbdd
# 
db = SessionLocal()


# 2. Funciones ORM (así funcionan con SQLAlchemy)
def obtener_clientes():
    return db.query(ClienteORM).order_by(ClienteORM.id.asc()).all()

def obtener_mascotas_de_cliente(cliente_id):
    return db.query(MascotaORM).filter(MascotaORM.cliente_id == cliente_id).all()

def insertar_cliente(nombre, apellidos, dni, telefono, correo):
    nuevo = ClienteORM(
        nombre=nombre,
        apellidos=apellidos,
        dni=dni,
        telefono=telefono,
        correo=correo
    )
    db.add(nuevo)
    db.commit()

def actualizar_cliente(cliente_id, nombre, apellidos, dni, telefono, correo):
    cliente = db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
    if cliente:
        cliente.nombre = nombre
        cliente.apellidos = apellidos
        cliente.dni = dni
        cliente.telefono = telefono
        cliente.correo = correo
        db.commit()

def eliminar_cliente(cliente_id):
    cliente = db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
    if cliente:
        db.delete(cliente)
        db.commit()


# 3. Mostrar clientes
clientes = obtener_clientes()
st.subheader("📋 Lista de Clientes")

if clientes:
    st.dataframe(
        [{"ID": c.id, "Nombre": c.nombre, "Apellidos": c.apellidos,
          "DNI": c.dni, "Teléfono": c.telefono, "Correo": c.correo}
         for c in clientes],
        use_container_width=True,
    )
else:
    st.info("No hay clientes en la base de datos.")


# 4. Añadir Cliente
st.subheader("➕ Añadir Cliente")

with st.form("form_anadir_cliente"):
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")
        dni = st.text_input("DNI")

    with col2:
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo")

    submitted = st.form_submit_button("Añadir")

    if submitted:
        if nombre and apellidos and dni and telefono and correo:
            try:
                insertar_cliente(nombre, apellidos, dni, telefono, correo)
                st.success("Cliente añadido correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al añadir: {e}")
        else:
            st.warning("Completa todos los campos.")


# 5. Editar Cliente
st.subheader("✏️ Editar Cliente")

if not clientes:
    st.warning("No hay clientes para editar.")
else:
    opciones = {f"{c.id} - {c.nombre} {c.apellidos}": c for c in clientes}

    seleccion = st.selectbox("Selecciona un cliente", list(opciones.keys()))
    cliente_sel = opciones[seleccion]

    with st.form("form_editar_cliente"):
        col1, col2 = st.columns(2)

        with col1:
            nuevo_nombre = st.text_input("Nombre", cliente_sel.nombre)
            nuevos_apellidos = st.text_input("Apellidos", cliente_sel.apellidos)
            nuevo_dni = st.text_input("DNI", cliente_sel.dni)

        with col2:
            nuevo_telefono = st.text_input("Teléfono", cliente_sel.telefono)
            nuevo_correo = st.text_input("Correo", cliente_sel.correo)

        submitted_edit = st.form_submit_button("Guardar Cambios")

        if submitted_edit:
            try:
                actualizar_cliente(
                    cliente_sel.id,
                    nuevo_nombre,
                    nuevos_apellidos,
                    nuevo_dni,
                    nuevo_telefono,
                    nuevo_correo,
                )
                st.success("Cliente actualizado correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al editar: {e}")


# 6. Ver Mascotas del Cliente
st.subheader("🐾 Mascotas del Cliente")

if clientes:
    mascotas = obtener_mascotas_de_cliente(cliente_sel.id)

    if mascotas:
        st.table(
            [{
                "ID": m.id,
                "Nombre": m.nombre,
                "Especie": m.especie,
                "Raza": m.raza,
                "Sexo": m.sexo,
                "Edad": m.edad,
                "Estado": m.estado_salud
            } for m in mascotas]
        )
    else:
        st.info("Este cliente no tiene mascotas registradas.")


# 7. Eliminar Cliente

st.subheader("🗑️ Eliminar Cliente")

if clientes:
    if st.button("Eliminar cliente seleccionado"):
        try:
            eliminar_cliente(cliente_sel.id)
            st.success("Cliente eliminado correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al eliminar: {e}")
