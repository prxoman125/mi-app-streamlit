import streamlit as st
import pandas as pd
import numpy as np

# Configuracion inicial de la ventana de la aplicacion
st.set_page_config(page_title="Mira Laser Interactiva", layout="wide")

st.title("Alineador Geometrico de Mira Telescopica")
st.write("Ajusta la altura de la mira, la desviacion en la diana y la distancia para calcular el angulo exacto.")

# --- 1. CAPTURA DE CONTROLES (PRIMERO DEFINIMOS TODOS LOS SLIDERS) ---
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

# Control de Distancia (Abajo en la columna central)
with col_grafica:
    st.subheader("Visualizacion del Sistema")
    distancia_m = st.slider(
        "Distancia entre la mira y la diana (metros):",
        min_value=1.0, max_value=100.0, value=10.0, step=1.0
    )

# --- 2. PREPARACION DE DATOS ---
y_laser_fijo = 0.0  # El laser esta fijo en el centro de la diana (0 cm)

chart_data_long = pd.DataFrame([
    {'Distancia': 0.0, 'Altura': y_laser_fijo, 'Elemento': 'Laser', 'Icono': 'circle'},
    {'Distancia': distancia_m, 'Altura': y_laser_fijo, 'Elemento': 'Laser', 'Icono': 'diamond'},
    {'Distancia': 0.0, 'Altura': y_mira, 'Elemento': 'Linea de Vision', 'Icono': 'cross'},
    {'Distancia': distancia_m, 'Altura': y_diana, 'Elemento': 'Linea de Vision', 'Icono': 'triangle-down'}
])

# --- 3. DEFINICION Y RENDERIZADO DEL GRAFICO ---
vega_lite_spec = {
    "width": "container",
    "height": 400,
    "data": {"values": chart_data_long.to_dict('records')},
    "encoding": {
        "x": {
            "field": "Distancia", 
            "type": "quantitative", 
            "title": "Distancia (m)",
            "scale": {"domain": [0, distancia_m]}
        },
        "y": {
            "field": "Altura", 
            "type": "quantitative", 
            "title": "Altura (cm)",
            "scale": {"domain": [-12, 12]}
        },
        "color": {
            "field": "Elemento", 
            "type": "nominal", 
            "scale": {"domain": ["Laser", "Linea de Vision"], "range": ["#e74c3c", "#2980b9"]}
        }
    },
    "layer": [
        {
            "mark": {"type": "line", "strokeWidth": 3}
        },
        {
            "mark": {"type": "point", "size": 150, "filled": True},
            "encoding": {
                "shape": {"field": "Icono", "type": "nominal", "scale": None}
            }
        }
    ]
}

# Renders de la gráfica dentro de la columna central con una clave fija
with col_grafica:
    st.vega_lite_chart(vega_lite_spec, use_container_width=True, key="grafica_laser")

# --- 4. CALCULO TRIGONOMETRICO ---
altura_relativa_m = (y_mira - y_diana) / 100.0
angulo_rad = np.arctan(altura_relativa_m / distancia_m)
angulo_deg = np.degrees(angulo_rad)

st.divider()

# --- 5. PANEL DE RESULTADOS Y MENSAJE DE GUIA ---
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
