import streamlit as st
import pandas as pd
import numpy as np

# Configuracion inicial de la ventana de la aplicacion
st.set_page_config(page_title="Mira Laser Interactiva", layout="wide")

st.title("Alineador Geometrico de Mira Telescopica")
st.write("Ajusta la altura de la mira, la desviacion en la diana y la distancia para calcular el angulo exacto.")

# --- ESTRUCTURA EN 3 COLUMNAS: [Izquierda, Centro (Grafica), Derecha] ---
col_izq, col_grafica, col_der = st.columns([1, 3, 1])

# 1. Columna Izquierda: Control de la Mira (1 cm a 5 cm)
with col_izq:
    st.subheader("Mira")
    y_mira = st.slider(
        "Altura de la Mira (cm):", 
        min_value=1.0, max_value=5.0, value=5.0, step=0.5
    )

# 2. Columna Derecha: Punto de Apunte en la Diana (-10 cm a 10 cm)
with col_der:
    st.subheader("Diana")
    y_diana = st.slider(
        "Punto de apunte en Diana (cm):", 
        min_value=-10.0, max_value=10.0, value=0.0, step=0.5
    )

# 3. Columna Central: Grafica y Control de Distancia
with col_grafica:
    st.subheader("Visualizacion del Sistema")
    
    # Barra deslizable de distancia (abajo de la grafica / espacio de visualizacion)
    distancia_m = st.slider(
        "Distancia entre la mira y la diana (metros):",
        min_value=1.0, max_value=100.0, value=10.0, step=1.0
    )

    y_laser_fijo = 0.0  # El laser esta fijo en el centro de la diana (0 cm)

    # --- PREPARACION DE DATOS EN FORMATO LARGO ---
    # Creamos registros específicos para los puntos de origen (0m) y destino (distancia_m)
    chart_data_long = pd.DataFrame([
        {'Distancia': 0.0, 'Altura': y_laser_fijo, 'Elemento': 'Laser', 'Icono': 'circle'},
        {'Distancia': distancia_m, 'Altura': y_laser_fijo, 'Elemento': 'Laser', 'Icono': 'diamond'}, # Diamante para el laser en diana
        {'Distancia': 0.0, 'Altura': y_mira, 'Elemento': 'Linea de Vision', 'Icono': 'cross'},       # Cruz/Reticula para la mira
        {'Distancia': distancia_m, 'Altura': y_diana, 'Elemento': 'Linea de Vision', 'Icono': 'triangle-down'} # Triangulo en destino
    ])

    # --- DEFINICION DEL GRAFICO VEGA-LITE ---
    vega_lite_spec = {
        "width": "container",
        "height": 400,
        "data": {"values": chart_data_long.to_dict('records')},
        "encoding": {
            "x": {
                "field": "Distancia", 
                "type": "quantitative", 
                "title": "Distancia (m)",
                "scale": {"domain": [0, distancia_m]} # Mantiene la escala del eje X sincronizada
            },
            "y": {
                "field": "Altura", 
                "type": "quantitative", 
                "title": "Altura (cm)",
                "scale": {"domain": [-12, 12]} # Rango fijo en Y para evitar saltos bruscos
            },
            "color": {
                "field": "Elemento", 
                "type": "nominal", 
                "scale": {"domain": ["Laser", "Linea de Vision"], "range": ["#e74c3c", "#2980b9"]}
            }
        },
        "layer": [
            # Capa 1: Lineas de trayectoria
            {
                "mark": {"type": "line", "strokeWidth": 3}
            },
            # Capa 2: Iconos/Simbolos diferenciados en cada extremo
            {
                "mark": {"type": "point", "size": 150, "filled": True},
                "encoding": {
                    "shape": {"field": "Icono", "type": "nominal", "scale": None}
                }
            }
        ]
    }

    # Renderizado interactivo usando una clave dinamica para forzar la actualizacion
    st.vega_lite_chart(vega_lite_spec, use_container_width=True, key=f"chart_{y_mira}_{y_diana}_{distancia_m}")


# --- CALCULO TRIGONOMETRICO ---
altura_relativa_m = (y_mira - y_diana) / 100.0
angulo_rad = np.arctan(altura_relativa_m / distancia_m)
angulo_deg = np.degrees(angulo_rad)

st.divider()

# --- PANEL DE RESULTADOS Y MENSAJE DE GUIA ---
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
