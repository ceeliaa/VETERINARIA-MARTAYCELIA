"""
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
    query = "SELECT s.operaciones FROM saldo"
    return db.ejecutar_query(query)



# 2. CONSULTAR SALDO ACTUAL

st.subheader("💰 Saldo actual")

saldo = consultar_saldo()
st.dataframe(saldo, use_container_width=True)


# 3. CONSULTAR HISTORIAL DE OPERACIONES

st.subheader("💰 Lista de Operaciones")

operaciones_saldo = consultar_historial_operaciones()
st.dataframe(operaciones_saldo, use_container_width=True)
"""
#Comprobar que queremos hacer esto asi
import sys
import os

# Añadimos la carpeta raíz del proyecto al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import streamlit as st
from src.database.db import DataBaseConnector
from src.modulos.saldo import Saldo

st.set_page_config(page_title="Saldo", page_icon="💰")

# Inicializar conexión y clase Saldo
db = DataBaseConnector(password="1234")
saldo_manager = Saldo(db)

st.title("💰 Gestión del Saldo de la Clínica")


# ============================================
# FUNCIONES AUXILIARES PARA SERVICIOS
# ============================================

def obtener_servicios():
    """Obtiene todos los servicios disponibles"""
    query = "SELECT * FROM servicios ORDER BY nombre ASC"
    return db.ejecutar_query(query)

def agregar_servicio(nombre, precio):
    """Agrega un nuevo servicio"""
    query = "INSERT INTO servicios (nombre, precio) VALUES (%s, %s)"
    db.ejecutar_query(query, (nombre, precio), fetch=False)

def actualizar_servicio(servicio_id, nombre, precio):
    """Actualiza un servicio existente"""
    query = "UPDATE servicios SET nombre=%s, precio=%s WHERE id=%s"
    db.ejecutar_query(query, (nombre, precio, servicio_id), fetch=False)

def eliminar_servicio(servicio_id):
    """Elimina un servicio"""
    query = "DELETE FROM servicios WHERE id=%s"
    db.ejecutar_query(query, (servicio_id,), fetch=False)


# ============================================
# 1. MOSTRAR SALDO ACTUAL Y ESTADÍSTICAS
# ============================================

st.subheader("💵 Saldo Actual")

saldo_actual = saldo_manager.consultar_saldo()
estadisticas = saldo_manager.obtener_estadisticas_mes()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Saldo Disponible", f"€{saldo_actual:,.2f}")
with col2:
    st.metric("Ingresos del Mes", f"€{estadisticas['ingresos']:,.2f}")
with col3:
    st.metric("Gastos del Mes", f"€{estadisticas['gastos']:,.2f}")

st.divider()


# ============================================
# 2. REGISTRAR CONSULTA/SERVICIO (INGRESO)
# ============================================

st.subheader("🩺 Registrar Consulta o Servicio")

servicios = obtener_servicios()

with st.form("form_registrar_consulta"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Crear diccionario de servicios
        if servicios:
            dict_servicios = {f"{s['nombre']} - €{s['precio']}": s for s in servicios}
            servicio_seleccionado = st.selectbox(
                "Servicio Prestado", 
                list(dict_servicios.keys())
            )
        else:
            st.warning("⚠️ No hay servicios registrados. Ve a 'Gestión de Servicios' para añadir.")
            servicio_seleccionado = None
    
    with col2:
        cliente_nombre = st.text_input("Cliente (opcional)")
        notas_consulta = st.text_input("Notas adicionales (opcional)")
    
    submitted_consulta = st.form_submit_button("✅ Registrar Ingreso")
    
    if submitted_consulta:
        if not servicios:
            st.error("❌ Primero debes crear servicios en la sección correspondiente.")
        else:
            try:
                servicio = dict_servicios[servicio_seleccionado]
                
                # Usar la clase Saldo para registrar
                concepto_completo = servicio['nombre']
                if notas_consulta:
                    concepto_completo += f" - {notas_consulta}"
                
                nuevo_saldo = saldo_manager.cobrar_consulta(
                    float(servicio['precio']), 
                    concepto_completo,
                    cliente_nombre if cliente_nombre else None
                )
                
                st.success(f"✅ Ingreso registrado. Nuevo saldo: €{nuevo_saldo:,.2f}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error al registrar: {e}")

st.divider()


# ============================================
# 3. REGISTRAR GASTO
# ============================================

st.subheader("💸 Registrar Gasto")

tipo_gasto_seleccionado = st.radio(
    "Tipo de Gasto",
    ["Nómina Empleado", "Facturas Proveedores", "Otro Gasto"],
    horizontal=True
)

# Formulario de Nómina Empleado
if tipo_gasto_seleccionado == "Nómina Empleado":
    with st.form("form_nomina"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_empleado = st.text_input("Nombre del Empleado")
        with col2:
            monto_nomina = st.number_input("Monto (€)", min_value=0.01, step=0.01)
        
        submitted_nomina = st.form_submit_button("➖ Pagar Nómina")
        
        if submitted_nomina:
            if not nombre_empleado:
                st.warning("⚠️ Debes indicar el nombre del empleado.")
            else:
                try:
                    nuevo_saldo = saldo_manager.pagar_empleado(monto_nomina, nombre_empleado)
                    st.success(f"✅ Nómina pagada. Nuevo saldo: €{nuevo_saldo:,.2f}")
                    st.rerun()
                except ValueError as ve:
                    st.error(f"❌ {ve}")
                except Exception as e:
                    st.error(f"❌ Error al registrar: {e}")

# Formulario de Facturas
elif tipo_gasto_seleccionado == "Facturas Proveedores":
    with st.form("form_facturas"):
        col1, col2 = st.columns(2)
        
        with col1:
            proveedor = st.text_input("Proveedor")
            descripcion_factura = st.text_input("Descripción")
        with col2:
            monto_factura = st.number_input("Monto (€)", min_value=0.01, step=0.01)
        
        submitted_factura = st.form_submit_button("➖ Pagar Factura")
        
        if submitted_factura:
            try:
                nuevo_saldo = saldo_manager.pagar_facturas(
                    monto_factura,
                    proveedor if proveedor else None,
                    descripcion_factura if descripcion_factura else None
                )
                st.success(f"✅ Factura pagada. Nuevo saldo: €{nuevo_saldo:,.2f}")
                st.rerun()
            except ValueError as ve:
                st.error(f"❌ {ve}")
            except Exception as e:
                st.error(f"❌ Error al registrar: {e}")

# Formulario de Otro Gasto
else:
    with st.form("form_otro_gasto"):
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_gasto = st.selectbox(
                "Categoría",
                ["Material Médico", "Mantenimiento", "Servicios", "Marketing", "Otros"]
            )
            descripcion_gasto = st.text_input("Descripción del gasto")
        
        with col2:
            monto_gasto = st.number_input("Monto (€)", min_value=0.01, step=0.01)
        
        submitted_gasto = st.form_submit_button("➖ Registrar Gasto")
        
        if submitted_gasto:
            if not descripcion_gasto:
                st.warning("⚠️ Debes indicar una descripción del gasto.")
            else:
                try:
                    nuevo_saldo = saldo_manager.registrar_gasto(
                        monto_gasto,
                        tipo_gasto,
                        descripcion_gasto
                    )
                    st.success(f"✅ Gasto registrado. Nuevo saldo: €{nuevo_saldo:,.2f}")
                    st.rerun()
                except ValueError as ve:
                    st.error(f"❌ {ve}")
                except Exception as e:
                    st.error(f"❌ Error al registrar: {e}")

st.divider()


# ============================================
# 4. GESTIÓN DE SERVICIOS Y PRECIOS
# ============================================

st.subheader("⚙️ Gestión de Servicios y Precios")

tab1, tab2, tab3 = st.tabs(["📋 Ver Servicios", "➕ Añadir Servicio", "✏️ Editar/Eliminar"])

with tab1:
    if servicios:
        st.dataframe(servicios, use_container_width=True)
    else:
        st.info("ℹ️ No hay servicios registrados.")

with tab2:
    with st.form("form_anadir_servicio"):
        col1, col2 = st.columns(2)
        with col1:
            nombre_servicio = st.text_input("Nombre del Servicio")
        with col2:
            precio_servicio = st.number_input("Precio (€)", min_value=0.01, step=0.01, value=30.00)
        
        submitted_servicio = st.form_submit_button("Añadir Servicio")
        
        if submitted_servicio:
            if nombre_servicio:
                try:
                    agregar_servicio(nombre_servicio, precio_servicio)
                    st.success("✅ Servicio añadido correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Completa todos los campos.")

with tab3:
    if servicios:
        dict_servicios_edit = {f"{s['id']} - {s['nombre']}": s for s in servicios}
        servicio_edit = st.selectbox("Selecciona un servicio", list(dict_servicios_edit.keys()))
        servicio_seleccionado_edit = dict_servicios_edit[servicio_edit]
        
        with st.form("form_editar_servicio"):
            col1, col2 = st.columns(2)
            with col1:
                nuevo_nombre = st.text_input("Nombre", servicio_seleccionado_edit['nombre'])
            with col2:
                nuevo_precio = st.number_input(
                    "Precio (€)", 
                    value=float(servicio_seleccionado_edit['precio']), 
                    min_value=0.01, 
                    step=0.01
                )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submitted_edit = st.form_submit_button("💾 Guardar Cambios")
            with col_btn2:
                submitted_delete = st.form_submit_button("🗑️ Eliminar", type="secondary")
            
            if submitted_edit:
                try:
                    actualizar_servicio(servicio_seleccionado_edit['id'], nuevo_nombre, nuevo_precio)
                    st.success("✅ Servicio actualizado correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            
            if submitted_delete:
                try:
                    eliminar_servicio(servicio_seleccionado_edit['id'])
                    st.success("✅ Servicio eliminado correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    else:
        st.info("ℹ️ No hay servicios para editar.")

st.divider()


# ============================================
# 5. HISTORIAL DE OPERACIONES
# ============================================

st.subheader("📊 Historial de Operaciones")

# Filtros
col1, col2, col3 = st.columns(3)
with col1:
    filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos", "INGRESO", "GASTO"])
with col2:
    limite_registros = st.selectbox("Mostrar", [20, 50, 100, "Todos"])
with col3:
    st.write("")  # Espaciador

# Obtener historial con filtros
tipo_filtro = None if filtro_tipo == "Todos" else filtro_tipo
limite = None if limite_registros == "Todos" else int(limite_registros)

historial = saldo_manager.obtener_historial(limite=limite, tipo_operacion=tipo_filtro)

if historial:
    st.dataframe(historial, use_container_width=True)
    
    # Resumen del historial mostrado
    total_ingresos = sum(float(op['monto']) for op in historial if op['tipo_operacion'] == 'INGRESO')
    total_gastos = sum(float(op['monto']) for op in historial if op['tipo_operacion'] == 'GASTO')
    
    st.markdown("---")
    st.subheader("📈 Resumen del Historial")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Ingresos", f"€{total_ingresos:,.2f}")
    with col2:
        st.metric("Total Gastos", f"€{total_gastos:,.2f}")
    with col3:
        balance = total_ingresos - total_gastos
        st.metric("Balance", f"€{balance:,.2f}", delta=balance)
else:
    st.info("ℹ️ No hay operaciones registradas.")