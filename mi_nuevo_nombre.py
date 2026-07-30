import streamlit as st

# Configuración de la página en modo ancho
st.set_page_config(page_title="Calculadora Inmobiliaria", layout="wide")

# --- BARRA LATERAL: ENTRADAS DE DATOS ---
st.sidebar.header("⚙️ Ingreso de Datos")

st.sidebar.subheader("Inversión")
precio_compra = st.sidebar.number_input(
    "Precio de compra ($):", min_value=0.0, value=100000.0, step=1000.0
)
costo_remodelacion = st.sidebar.number_input(
    "Costo de remodelación ($):", min_value=0.0, value=15000.0, step=500.0
)

st.sidebar.subheader("Flujo Mensual")
renta_mensual = st.sidebar.number_input(
    "Renta mensual ($):", min_value=0.0, value=1200.0, step=50.0
)
gastos_fijos = st.sidebar.number_input(
    "Gastos fijos mensuales ($):", min_value=0.0, value=200.0, step=20.0
)


# --- CÁLCULOS MATEMÁTICOS ---
inversion_total = precio_compra + costo_remodelacion
ingreso_neto_anual = (renta_mensual - gastos_fijos) * 12

if inversion_total > 0:
    cap_rate = (ingreso_neto_anual / inversion_total) * 100
else:
    cap_rate = 0.0


# --- PANTALLA PRINCIPAL: RESULTADOS EN FIJA ---
st.title("🏢 Análisis de Inversión y Cap Rate")
st.caption("Modifica las cifras en el menú de la izquierda para ver la actualización automática.")

st.markdown("---")

# Visualización limpia en 3 columnas arriba
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Inversión Total", 
        value=f"${inversion_total:,.2f}"
    )

with col2:
    st.metric(
        label="Ingreso Neto Anual", 
        value=f"${ingreso_neto_anual:,.2f}"
    )

with col3:
    st.metric(
        label="Cap Rate", 
        value=f"{cap_rate:.2f}%"
    )

st.markdown("---")

# Retroalimentación rápida según el resultado
if cap_rate >= 8.0:
    st.success(f"🔥 **Excelente rendimiento:** Un Cap Rate del **{cap_rate:.2f}%** es una métrica muy atractiva.")
elif cap_rate >= 5.0:
    st.warning(f"⚖️ **Rendimiento moderado:** Un Cap Rate del **{cap_rate:.2f}%** está en el promedio de mercado.")
else:
    st.error(f"⚠️ **Rendimiento bajo:** Un Cap Rate del **{cap_rate:.2f}%** podría requerir ajustar el precio o subir rentas.")
