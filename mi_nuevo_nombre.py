import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.integrate import solve_ivp

# Configuración de página ancha para aprovechar mejor las 3 columnas
st.set_page_config(layout="wide")

st.title("Estructura de 3 Columnas en Streamlit")

# Inicializar el historial en la sesión si no existe
if "historial" not in st.session_state:
    st.session_state.historial = []

# Crear las 3 columnas
col_izquierda, col_centro, col_derecha = st.columns([1, 2, 1])

# --- COLUMNA 1: Ajuste de datos ---
with col_izquierda:
    st.subheader("⚙️ Ajustes")

    # Parámetros simples (ejemplo: Ecuación diferencial de enfriamiento/decaimiento)
    k = st.slider(
        "Constante de decaimiento (k)",
        min_value=0.1,
        max_value=2.0,
        value=0.5,
        step=0.1,
    )
    y0 = st.number_input(
        "Valor inicial (y0)", min_value=1.0, max_value=100.0, value=10.0
    )

    # Botón para guardar la configuración actual
    if st.button("Guardar Configuración"):
        st.session_state.historial.append({"k": k, "y0": y0})
        st.success("¡Guardado!")

# --- CÁLCULOS (scipy + numpy) ---
# Definimos una EDO simple: dy/dt = -k * y
def edo(t, y, k):
    return -k * y


t_eval = np.linspace(0, 10, 100)
solucion = solve_ivp(edo, [0, 10], [y0], args=(k,), t_eval=t_eval)

# --- COLUMNA 2: Gráfica ---
with col_centro:
    st.subheader("📈 Gráfica")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=solucion.t,
            y=solucion.y[0],
            mode="lines",
            name=f"k={k}, y0={y0}",
            line=dict(color="royalblue", width=3),
        )
    )

    fig.update_layout(
        title="Resultado de solve_ivp",
        xaxis_title="Tiempo (t)",
        yaxis_title="Valor (y)",
        margin=dict(l=20, r=20, t=40, b=20),
    )

    st.plotly_chart(fig, use_container_width=True)

# --- COLUMNA 3: Guardar/Historial ---
with col_derecha:
    st.subheader("💾 Datos Guardados")

    if st.session_state.historial:
        for i, registro in enumerate(st.session_state.historial, 1):
            st.write(f"**Registro {i}:** k = {registro['k']}, y0 = {registro['y0']}")

        if st.button("Limpiar Historial"):
            st.session_state.historial = []
            st.rerun()
    else:
        st.info("No hay datos guardados aún.")
