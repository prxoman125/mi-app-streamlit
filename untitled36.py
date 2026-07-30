import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuracion inicial de la ventana de la aplicacion
st.set_page_config(page_title="Mira Laser Interactiva", layout="wide")

st.title("Alineador Geometrico de Mira Telescopica")
st.write("Ajusta la altura de la mira, la desviacion en la diana y la distancia para calcular el angulo exacto.")

# --- 1. CAPTURA DE CONTROLES EN COLUMNAS ---
col_izq, col_grafica, col_der = st.columns([1, 3, 1])

# Control de la Mira (Izquierda)
with col_izq:
    st.subheader("Mira")
    y_mira = st.slider(
        "Altura de la Mira (cm):", 
        min_value=1.0, max_value=5.0, value=5.0, step=0.5
    )

# Control de la Diana (Derecha)
with col_der:
    st.subheader("Diana")
    y_diana = st.slider(
        "Punto de apunte en Diana (cm):", 
        min_value=-10.0, max_value=10.0, value=0.0, step=0.5
    )

# Control de Distancia (Abajo de la grafica)
with col_grafica:
    st.subheader("Visualizacion del Sistema")
    distancia_m = st.slider(
        "Distancia entre la mira y la diana (metros):",
        min_value=1.0, max_value=100.0, value=10.0, step=1.0
    )

y_laser_fijo = 0.0  # El laser esta fijo en el centro de la diana (0 cm)

# --- 2. CONSTRUCCION DE LA GRAFICA INTERACTIVA CON PLOTLY ---
fig = go.Figure()

# Linea y marcadores del Laser
fig.add_trace(go.Scatter(
    x=[0, distancia_m],
    y=[y_laser_fijo, y_laser_fijo],
    mode='lines+markers',
    name='Laser (Fijo en 0 cm)',
    line=dict(color='#e74c3c', width=3),
    marker=dict(
        symbol=['circle', 'diamond'], # Circulo al inicio, Diamante en la diana
        size=12
    )
))

# Linea y marcadores de la Linea de Vision
fig.add_trace(go.Scatter(
    x=[0, distancia_m],
    y=[y_mira, y_diana],
    mode='lines+markers',
    name='Linea de Vision',
    line=dict(color='#2980b9', width=3),
    marker=dict(
        symbol=['cross', 'triangle-down'], # Cruz en la mira, Triangulo en la diana
        size=12
    )
))

# Configuracion de ejes y estetica
fig.update_layout(
    xaxis_title="Distancia (m)",
    yaxis_title="Altura (cm)",
    yaxis=dict(range=[-12, 12]),
    xaxis=dict(range=[0, distancia_m]),
    height=400,
    margin=dict(l=20, r=20, t=30, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Dibujar la grafica en la columna central
with col_grafica:
    st.plotly_chart(fig, use_container_width=True)

# --- 3. CALCULO TRIGONOMETRICO ---
altura_relativa_m = (y_mira - y_diana) / 100.0
angulo_rad = np.arctan(altura_relativa_m / distancia_m)
angulo_deg = np.degrees(angulo_rad)

st.divider()

# --- 4. PANEL DE RESULTADOS Y MENSAJE DE GUIA ---
col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    st.metric(label="Inclinacion requerida en la Mira", value=f"{angulo_deg:.4f}°")

with col_res2:
    if y_mira > y_diana:
        st.info(f"Apunta la mira hacia abajo un total de {abs(angulo_deg):.4f}° para dar en el punto objetivo.")
    elif y_mira < y_diana:
        st.info(f"Apunta la mira hacia arriba un total de {abs(angulo_deg):.4f}° para dar en el punto objetivo.")
    else:
        st.success("Sistema perfectamente paralelo. Angulo de inclinacion: 0°.")
