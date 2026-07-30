import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuracion inicial de la ventana
st.set_page_config(page_title="Mira Laser Interactiva", layout="wide")

st.title("Alineador Geometrico de Mira Telescopica")

# --- 1. CAPTURA DE CONTROLES EN COLUMNAS ---
col_izq, col_grafica, col_der = st.columns([1, 3, 1])

with col_izq:
    st.write("Mira")
    y_mira = st.slider(
        "Altura Mira (cm):", 
        min_value=1.0, max_value=5.0, value=5.0, step=0.5,
        label_visibility="collapsed" # Limpieza visual
    )
    st.caption(f"Mira: {y_mira} cm")

with col_der:
    st.write("Diana")
    y_diana = st.slider(
        "Apunte Diana (cm):", 
        min_value=-10.0, max_value=10.0, value=0.0, step=0.5,
        label_visibility="collapsed"
    )
    st.caption(f"Diana: {y_diana} cm")

with col_grafica:
    # El slider de distancia se coloca arriba de la grafica para mejor control
    distancia_m = st.slider(
        "Distancia (m):",
        min_value=1.0, max_value=100.0, value=10.0, step=1.0
    )

y_laser_fijo = 0.0

# --- 2. CONSTRUCCION DE LA GRAFICA (LIMPIA Y CON CUADRICULA) ---
fig = go.Figure()

# Linea del Laser
fig.add_trace(go.Scatter(
    x=[0, distancia_m],
    y=[y_laser_fijo, y_laser_fijo],
    mode='lines+markers',
    name='Laser',
    line=dict(color='#e74c3c', width=3),
    marker=dict(symbol=['circle', 'diamond'], size=14),
    hoverinfo='skip' # Quita etiquetas molestas
))

# Linea de Vision
fig.add_trace(go.Scatter(
    x=[0, distancia_m],
    y=[y_mira, y_diana],
    mode='lines+markers',
    name='Vision',
    line=dict(color='#2980b9', width=3),
    marker=dict(symbol=['cross', 'triangle-down'], size=14),
    hoverinfo='skip'
))

# Estetica tecnica: Cuadrícula y limpieza de funciones
fig.update_layout(
    xaxis=dict(
        range=[0, distancia_m],
        showgrid=True, # Activa cuadricula
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='black'
    ),
    yaxis=dict(
        range=[-12, 12],
        showgrid=True, # Activa cuadricula
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='black'
    ),
    height=450,
    margin=dict(l=40, r=40, t=10, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False, # Quita la leyenda para ganar espacio
    dragmode=False    # Desactiva el zoom con el raton
)

with col_grafica:
    # CONFIG: displayModeBar=False quita todos los botones de la grafica
    # staticPlot=True haria que no se pueda mover nada, pero preferimos que sea interactiva sin estorbos
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 3. CALCULO Y RESULTADOS ---
altura_relativa_m = (y_mira - y_diana) / 100.0
angulo_rad = np.arctan(altura_relativa_m / distancia_m)
angulo_deg = np.degrees(angulo_rad)

st.divider()

col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    st.metric(label="Angulo requerido", value=f"{angulo_deg:.4f}°")

with col_res2:
    if y_mira > y_diana:
        st.info(f"Apunta hacia abajo {abs(angulo_deg):.4f}°")
    elif y_mira < y_diana:
        st.info(f"Apunta hacia arriba {abs(angulo_deg):.4f}°")
    else:
        st.success("Sistema paralelo: 0°")
