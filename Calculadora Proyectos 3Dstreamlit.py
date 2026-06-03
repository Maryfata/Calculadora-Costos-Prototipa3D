import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Prototipa3D - Calculadora", page_icon="🖨️")
st.title("🖨️ Calculadora de Costos Prototipa3D")

# --- VARIABLES CONFIGURABLES (Sidebar) ---
st.sidebar.header("Configuración")
PRECIO_KWH = st.sidebar.number_input("Precio kWh ($)", value=2.30)
PRECIO_GRAMO = st.sidebar.number_input("Precio por gramo ($)", value=0.23)
DEPRECIACION_HORA = st.sidebar.number_input("Depreciación/h ($)", value=2.00)
TASA_FALLO = st.sidebar.slider("Tasa de fallo (%)", 0, 50, 15) / 100
COSTO_MANTENIMIENTO_HORA = st.sidebar.number_input("Mantenimiento/h ($)", value=0.50)

# --- INPUTS PRINCIPALES ---
col1, col2 = st.columns(2)
with col1:
    horas = st.number_input("Horas de impresión", value=1.0)
    watts_impresora = st.number_input("Watts impresora", value=150.0)
with col2:
    gramos_usados = st.number_input("Gramos usados", value=10.0)
    horas_diseno = st.number_input("Horas diseño PC", value=1.0)

complejidad = st.selectbox("Complejidad de la pieza (limpieza/soportes):", [1, 2, 3], format_func=lambda x: f"{x} - {'Baja' if x==1 else 'Media' if x==2 else 'Alta'}")

# --- MÓDULOS OPCIONALES ---
costo_packaging = st.number_input("Costo empaque ($)", value=0.0)
costo_traslado = st.number_input("Costo traslado ($)", value=0.0)
es_urgente = st.checkbox("¿Es un pedido urgente?")

# --- CÁLCULOS ---
factor_post_proc = 1 + (complejidad * 0.1)
costo_energia = (((watts_impresora / 1000) * horas) + ((95 / 1000) * horas_diseno)) * PRECIO_KWH
costo_material = gramos_usados * PRECIO_GRAMO
costo_maquina = horas * (DEPRECIACION_HORA + COSTO_MANTENIMIENTO_HORA)
costo_tiempo = (horas_diseno * 10) * factor_post_proc
costo_logistica = costo_packaging + costo_traslado

costo_base = (costo_energia + costo_material + costo_maquina + costo_tiempo + costo_logistica)
costo_total = costo_base * (1 + TASA_FALLO)

precio_estudiante = costo_total * 1.25
precio_publico = costo_total * 1.60

if es_urgente:
    precio_estudiante *= 1.5
    precio_publico *= 1.5

# --- IMPUESTOS Y PAGOS ---
usa_iva = st.checkbox("¿El cliente requiere factura (IVA 16%)?")
usa_tarjeta = st.checkbox("¿El cliente paga con tarjeta (Comisión 3.5%)?")

def calcular_final(precio):
    if usa_iva: precio += (precio * 0.16)
    if usa_tarjeta: precio += (precio * 0.035)
    return precio

# --- RESULTADOS ---
st.divider()
st.subheader("Desglose Técnico")
st.write(f"Precio solo luz y material: ${costo_energia + costo_material:.2f} MXN")
st.write(f"Precio máquina y mantenimiento: ${costo_maquina + costo_tiempo:.2f} MXN")
st.caption("Nota: El costo total incluye un margen para imprevistos y fallos, así como los costos logísticos si se aplican.")

st.divider()
st.subheader("Reporte Final PROTOTIPA3D")
st.write(f"**Costo operativo total:** ${costo_total:.2f} MXN")
st.metric("Precio para Estudiante", f"${calcular_final(precio_estudiante):.2f} MXN")
st.metric("Precio Público General", f"${calcular_final(precio_publico):.2f} MXN")