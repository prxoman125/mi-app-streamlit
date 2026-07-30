import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Configuración inicial
st.set_page_config(page_title="Calculadora de Mira y Láser", layout="wide")

# CSS para fijar la barra lateral al 25% y bloquear el botón de colapsar
st.markdown(
    """
    <style>
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    [data-testid="stSidebar"] {
        width: 25vw !important;
        min-width: 25vw !important;
        max-width: 25vw !important;
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- BARRA LATERAL (25% ANCHO) ---
st.sidebar.header("⚙️ Configuración")

# Punto Fijo: Diana / Láser
altura_laser = st.sidebar.number_input(
    "Altura del Láser / Diana (m):", value=5.0, step=0.5, disabled=True
)

st.sidebar.subheader("Ajustes de la Mira")
distancia_mira = st.sidebar.number_input(
    "Distancia horizontal a la Diana (m):", min_value=0.1, value=10.0, step=0.5
)
altura_mira = st.sidebar.number_input(
    "Altura de la Mira (m):", min_value=0.0, value=2.0, step=0.5
)

# --- CÁLCULOS MATEMÁTICOS (NumPy & Math) ---
diferencia_altura = altura_laser - altura_mira

# Cálculo del ángulo usando trigonometría
angulo_rad = math.atan2(diferencia_altura, distancia_mira)
angulo_grados = math.degrees(angulo_rad)

# --- PANTALLA PRINCIPAL (75% RESTANTE) ---
st.title("🎯 Calculadora de Ángulo de Inclinación")
st.caption(
    "El láser está fijo en la diana. Ajusta la mira en el menú izquierdo para ver el ángulo necesario para apuntar al centro."
)

st.markdown("---")

# Métrica del resultado en columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Diferencia de Altura", value=f"{diferencia_altura:+.2f} m"
    )

with col2:
    st.metric(
        label="Ángulo de Inclinación", value=f"{angulo_grados:+.2f}°"
    )

with col3:
    if angulo_grados > 0:
        st.metric("Orientación", "Inclinar hacia ARRIBA ⬆️")
    elif angulo_grados < 0:
        st.metric("Orientación", "Inclinar hacia ABAJO ⬇️")
    else:
        st.metric("Orientación", "Totalmente NIVELADO ➡️")

st.markdown("---")

# --- GRÁFICO INTERACTIVO (Plotly) ---
st.subheader("📐 Representación Visual del Disparo")

# Crear la figura interactiva de Plotly
fig = go.Figure()

# 1. Línea de referencia horizontal (piso/suelo)
fig.add_trace(
    go.Scatter(
        x=[0, distancia_mira + 2],
        y=[0, 0],
        mode="lines",
        name="Suelo",
        line=dict(color="gray", dash="dash"),
    )
)

# 2. Línea horizontal de referencia para la mira
fig.add_trace(
    go.Scatter(
        x=[0, distancia_mira],
        y=[altura_mira, altura_mira],
        mode="lines",
        name="Nivel Cero de Mira",
        line=dict(color="lightgray", dash="dot"),
    )
)

# 3. Línea de Visión (Desde la Mira hasta el Láser)
fig.add_trace(
    go.Scatter(
        x=[0, distancia_mira],
        y=[altura_mira, altura_laser],
        mode="lines+markers",
        name=f"Trayectoria ({angulo_grados:.2f}°)",
        line=dict(color="#10b981", width=3),
    )
)

# 4. Punto: Mira
fig.add_trace(
    go.Scatter(
        x=[0],
        y=[altura_mira],
        mode="markers+text",
        name="Mira",
        text=["Mira"],
        textposition="top center",
        marker=dict(size=14, color="#3b82f6", symbol="square"),
    )
)

# 5. Punto: Láser / Diana Fijo
fig.add_trace(
    go.Scatter(
        x=[distancia_mira],
        y=[altura_laser],
        mode="markers+text",
        name="Centro Diana (Láser Fijo)",
        text=["Láser / Diana"],
        textposition="top center",
        marker=dict(size=16, color="#ef4444", symbol="circle-cross"),
    )
)

# Ajustes de diseño de la gráfica
fig.update_layout(
    xaxis_title="Distancia Horizontal (metros)",
    yaxis_title="Altura (metros)",
    height=450,
    margin=dict(l=20, r=20, t=30, b=20),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
)

# Mostrar en Streamlit usando Plotly
st.plotly_chart(fig, use_container_width=True)
