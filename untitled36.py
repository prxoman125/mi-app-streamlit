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

    # --- PREPARACION DE DATOS PARA EL GRAFICO (Formato Largo para Vega-Lite) ---
    # Vega-Lite prefiere datos en formato "largo" (long format) para capas complejas.
    chart_data_long = pd.DataFrame({
        'Distancia (m)': [0.0, distancia_m, 0.0, distancia_m],
        'Altura (cm)': [y_laser_fijo, y_laser_fijo, y_mira, y_diana],
        'Tipo': ['Laser (Fijo en 0 cm)', 'Laser (Fijo en 0 cm)', 'Linea de Vision', 'Linea de Vision'],
        # Definimos que simbolo queremos en cada punto extremo
        'Simbolo': ['square', 'square', 'circle', 'circle'] 
    })

    # --- DEFINICION DEL GRAFICO VEGA-LITE (Capas) ---
    vega_lite_spec = {
        "width": "container", # Ocupa todo el ancho disponible
        "height": 400,
        "data": {"values": chart_data_long.to_dict('records')},
        "encoding": {
            "x": {"field": "Distancia (m)", "type": "quantitative", "title": "Distancia (m)"},
            "y": {"field": "Altura (cm)", "type": "quantitative", "title": "Altura (cm)"},
            "color": {
                "field": "Tipo", 
                "type": "nominal", 
                "legend": {"title": "Elemento"},
                # Definimos colores explicitos para que coincidan con los simbolos
                "scale": {"domain": ["Laser (Fijo en 0 cm)", "Linea de Vision"], "range": ["#1f77b4", "#ff7f0e"]}
            }
        },
        "layer": [
            # Capa 1: Las Lineas
            {
                "mark": {"type": "line", "interpolate": "linear"},
                "encoding": {
                    "strokeWidth": {"value": 2}
                }
            },
            # Capa 2: Los Simbolos en los extremos
            {
                "mark": {"type": "point", "size": 100, "filled": True}, # Puntos rellenos y mas grandes
                "encoding": {
                    # Usamos el campo 'Simbolo' definido en el DataFrame
                    "shape": {"field": "Simbolo", "type": "nominal", "scale": None} 
                }
            }
        ]
    }

    # Renderizamos el grafico usando la definicion Vega-Lite
    st.vega_lite_chart(vega_lite_spec, use_container_width=True)


# --- CALCULO TRIGONOMETRICO ---
# Cateto opuesto: Diferencia entre la altura de la mira y el punto objetivo en la diana (convertido a metros)
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
