import os
import sys

# --- TRUCO SÚPER FÁCIL: Auto-instalar Plotly si no existe ---
try:
    import plotly
except ImportError:
    # Si la aplicación no encuentra Plotly, ella misma se lo ordena a internet
    os.system(f"{sys.executable} -m pip install plotly")
    import plotly

import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Configuración inicial de la ventana de la aplicación
st.set_page_config(page_title="Mira Láser Interactiva", layout="centered")

st.title("🎯 Alineador Geométrico de Mira Telescópica")
st.write("Ajusta la altura de la mira o de la diana usando los controles inferiores para calcular el ángulo exacto.")

# --- CONTROLES DE INTERFAZ ---
col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    y_mira = st.slider(
        "🎛️ Altura de la Mira (cm):", 
        min_value=-15.0, max_value=15.0, value=5.0, step=0.5
    )

with col_ctrl2:
    y_diana = st.slider(
        "🎛️ Altura de la Diana (cm):", 
        min_value=-15.0, max_value=15.0, value=0.0, step=0.5
    )

# Distancia horizontal fija en metros (equivale a 1000 cm)
distancia_fija_m = 10.0 

# --- CÁLCULO TRIGONOMÉTRICO ---
# Cateto opuesto: Diferencia de altura expresada en metros
altura_relativa_m = (y_mira - y_diana) / 100.0
angulo_rad = np.arctan(altura_relativa_m / distancia_fija_m)
angulo_deg = np.degrees(angulo_rad)

# --- PANEL DE RESULTADOS ---
st.subheader("📐 Ángulo Calculado")
st.metric(label="Inclinación requerida en la Mira", value=f"{angulo_deg:.4f}°")

# --- CONSTRUCCIÓN DEL GRÁFICO INTERACTIVO (PLOTLY) ---
fig = go.Figure()

# 1. DISEÑO DE LA MIRA TELESCÓPICA (Ubicada en X = 0)
fig.add_shape(type="circle", x0=-0.3, y0=y_mira-1.5, x1=0.3, y1=y_mira+1.5, line=dict(color="RoyalBlue", width=4))
fig.add_shape(type="line", x0=-0.6, y0=y_mira, x1=0.6, y1=y_mira, line=dict(color="RoyalBlue", width=2))
fig.add_shape(type="line", x0=0, y0=y_mira-1.8, x1=0, y1=y_mira+1.8, line=dict(color="RoyalBlue", width=2))

# 2. DISEÑO DE LA DIANA DE TIRO (Ubicada en X = 10 metros)
fig.add_shape(type="circle", x0=9.6, y0=y_diana-2.5, x1=10.4, y1=y_diana+2.5, line=dict(color="Crimson", width=3))
fig.add_shape(type="circle", x0=9.8, y0=y_diana-1.2, x1=10.2, y1=y_diana+1.2, line=dict(color="Crimson", width=2))
fig.add_shape(type="circle", x0=9.93, y0=y_diana-0.2, x1=10.07, y1=y_diana+0.2, fillcolor="Crimson", line=dict(color="Crimson"))

# 3. VÍAS DE PROYECCIÓN
fig.add_shape(type="line", x0=0, y0=y_diana, x1=10, y1=y_diana, line=dict(color="Red", width=3, dash="dash"))
fig.add_shape(type="line", x0=0, y0=y_mira, x1=10, y1=y_diana, line=dict(color="DarkCyan", width=2))

# --- AJUSTES ESTÉTICOS DEL ESCENARIO ---
fig.update_layout(
    xaxis=dict(range=[-1, 11], title="Distancia Horizontal (Metros)", fixedrange=True),
    yaxis=dict(range=[-18, 18], title="Altura Vertical (Centímetros)", fixedrange=True),
    height=450,
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10)
)

# Renderizar gráfico en pantalla
st.plotly_chart(fig, use_container_width=True)

# Mensaje inteligente de guía
if y_mira > y_diana:
    st.info(f"💡 Apunta la mira hacia **abajo** un total de {abs(angulo_deg):.4f}° para interceptar el punto del láser.")
elif y_mira < y_diana:
    st.info(f"💡 Apunta la mira hacia **arriba** un total de {abs(angulo_deg):.4f}° para interceptar el punto del láser.")
else:
    st.success("🎯 Sistema perfectamente paralelo. Ángulo de inclinación: 0°.")
