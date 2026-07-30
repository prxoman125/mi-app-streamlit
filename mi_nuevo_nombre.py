import streamlit as st

# Configuración del título y descripción
st.title("🏢 Calculadora de Inversión Inmobiliaria y Cap Rate")
st.write("Ingresa los datos del inmueble para calcular la inversión total, el ingreso neto anual y el retorno de inversión (Cap Rate).")

st.markdown("---")

# --- SECCIÓN 1: INVERSIÓN TOTAL ---
st.header("1. Inversión Total")
col1, col2 = st.columns(2)

with col1:
    precio_compra = st.number_input("Precio de compra ($):", min_value=0.0, value=100000.0, step=1000.0)
with col2:
    costo_remodelacion = st.number_input("Costo de remodelación ($):", min_value=0.0, value=15000.0, step=500.0)

# Cálculo: Inversión Total
inversion_total = precio_compra + costo_remodelacion

st.info(f"**Inversión Total:** ${inversion_total:,.2f}")

st.markdown("---")

# --- SECCIÓN 2: INGRESOS Y GASTOS ---
st.header("2. Ingreso Neto Anual")
col3, col4 = st.columns(2)

with col3:
    renta_mensual = st.number_input("Renta mensual estimada ($):", min_value=0.0, value=1200.0, step=50.0)
with col4:
    gastos_fijos_mensuales = st.number_input("Gastos fijos mensuales ($):", min_value=0.0, value=200.0, step=20.0)

# Cálculo: Ingreso Neto Anual = (renta mensual - gastos fijos) * 12
ingreso_neto_mensual = renta_mensual - gastos_fijos_mensuales
ingreso_neto_anual = ingreso_neto_mensual * 12

st.info(f"**Ingreso Neto Anual:** ${ingreso_neto_anual:,.2f}")

st.markdown("---")

# --- SECCIÓN 3: RESULTADO CAP RATE ---
st.header("3. Cap Rate (Tasa de Capitalización)")

if st.button("Calcular Cap Rate", type="primary"):
    if inversion_total > 0:
        # Cálculo: Cap Rate = (ingreso neto anual / inversion total) * 100
        cap_rate = (ingreso_neto_anual / inversion_total) * 100
        
        # Mostrar el resultado principal destacado
        st.metric(label="Cap Rate Estimado", value=f"{cap_rate:.2f}%")
        
        # Mensaje de retroalimentación según el resultado
        if cap_rate >= 8.0:
            st.success(f"¡Excelente retorno! El Cap Rate es del **{cap_rate:.2f}%**.")
        elif cap_rate >= 5.0:
            st.warning(f"Retorno moderado. El Cap Rate es del **{cap_rate:.2f}%**.")
        else:
            st.error(f"Retorno bajo. El Cap Rate es del **{cap_rate:.2f}%**.")
    else:
        st.error("La inversión total debe ser mayor a cero para poder calcular el Cap Rate.")
