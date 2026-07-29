import streamlit as st
import pandas as pd
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

# --- CONSTRUCCIÓN DEL GRÁFICO CON EL SISTEMA NATIVO DE STREAMLIT ---
st.subheader("👁️ Visualización del Sistema")

# Creamos los puntos de las líneas utilizando tablas de datos (DataFrames)
# Línea del Láser (Línea recta horizontal en la altura de la diana)
laser_data = pd.DataFrame({
    'Distancia (m)': [0, distancia_fija_m],
    'Láser': [y_diana, y_diana]
}).set_index('Distancia (m)')

# Línea de Visión de la Mira (Une la mira con la diana)
vision_data = pd.DataFrame({
    'Distancia (m)': [0, distancia_fija_m],
    'Línea de Visión': [y_mira, y_diana]
}).set_index('Distancia (m)')

# Unimos ambas líneas en una sola tabla para graficarlas juntas
chart_data = pd.concat([laser_data, vision_data], axis=1)

# Desplegamos el gráfico nativo. Este gráfico ya incluye de forma automática:
# - Ajuste de colores claro/oscuro del sistema.
# - Botón de pantalla completa nativo en la esquina superior derecha.
st.line_chart(chart_data, y_label="Altura (cm)", height=400)

# Mensaje inteligente de guía
if y_mira > y_diana:
    st.info(f"💡 Apunta la mira hacia **abajo** un total de {abs(angulo_deg):.4f}° para interceptar el punto del láser.")
elif y_mira < y_diana:
    st.info(f"💡 Apunta la mira hacia **arriba** un total de {abs(angulo_deg):.4f}° para interceptar el punto del láser.")
else:
    st.success("🎯 Sistema perfectamente paralelo. Ángulo de inclinación: 0°.")
