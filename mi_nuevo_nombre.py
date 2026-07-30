import streamlit as st

# Configuración inicial en modo ancho
st.set_page_config(page_title="Calculadora Inmobiliaria", layout="wide")

# --- CSS PERSONALIZADO PARA FIJAR EL ANCHO AL 25% Y BLOQUEAR EL DESLIZAMIENTO ---
st.markdown(
    """
    <style>
    /* Ocultar el botón de colapsar/deslizar la barra lateral */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    
    /* Fijar la barra lateral al 25% del ancho de pantalla */
    [data-testid="stSidebar"] {
        width: 25vw !important;
        min-width: 25vw !important;
        max-width: 25vw !important;
    }
    
    /* Asegurar que el contenido principal ocupe el resto del espacio */
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- BARRA LATERAL (25% FIJO) ---
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


# --- ÁREA PRINCIPAL (75% RESTANTE) ---
st.title("🏢 Análisis de Inversión y Cap Rate")
st.caption("Los datos cambian automáticamente al modificar la barra izquierda.")

st.markdown("---")

# Muestra los 3 resultados principales alineados horizontalmente
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

# Diagnóstico de la inversión
if cap_rate >= 8.0:
    st.success(f"🔥 **Excelente rendimiento:** Un Cap Rate del **{cap_rate:.2f}%** es una métrica muy atractiva.")
elif cap_rate >= 5.0:
    st.warning(f"⚖️ **Rendimiento moderado:** Un Cap Rate del **{cap_rate:.2f}%** está en el promedio de mercado.")
else:
    st.error(f"⚠️ **Rendimiento bajo:** Un Cap Rate del **{cap_rate:.2f}%** podría requerir ajustar el precio o subir rentas.")
