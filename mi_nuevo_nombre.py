import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Calculador Óptico de Mira", layout="wide")

st.title("🎯 Calculador de Ángulo de Mira y Trayectoria Láser")
st.markdown("""
Este software calcula el **ángulo de inclinación exacto de una mira telescópica/óptica** montada sobre un eje láser horizontal.
Modifica los parámetros en la barra lateral para ver cómo cambian los ángulos y las trayectorias en tiempo real.
""")

# 2. BARRA LATERAL - ENTRADA DE DATOS (INPUTS)
st.sidebar.header("🎛️ Configuración del Sistema")

# Distancia (de 1 a 1000 metros)
distancia_m = st.sidebar.slider("📏 Distancia a la Diana (Metros)", min_value=1.0, max_value=1000.0, value=50.0, step=0.5)

# Altura del Láser (de 25 cm a 50 cm)
altura_laser_cm = st.sidebar.slider("📐 Altura del Láser desde el suelo (cm)", min_value=25.0, max_value=50.0, value=25.0, step=0.5)

# Altura de la Mira sobre el Láser (de 1 cm a 5 cm)
altura_mira_cm = st.sidebar.slider("👁️ Altura de la Mira sobre el Láser (cm)", min_value=1.0, max_value=5.0, value=3.0, step=0.1)

# Tamaño de la Diana (Diámetro de 20 cm a 30 cm)
diametro_diana_cm = st.sidebar.slider("🎯 Diámetro de la Diana (cm)", min_value=20.0, max_value=30.0, value=20.0, step=1.0)

# Punto de impacto deseado (Desviación respecto al centro)
radio_maximo = diametro_diana_cm / 2.0
st.sidebar.subheader("🎯 Objetivo de Apuntado")
desviacion_cm = st.sidebar.slider("Ajustar Punto de Impacto (cm respecto al centro)", 
                                  min_value=-float(radio_maximo), 
                                  max_value=float(radio_maximo), 
                                  value=0.0, 
                                  step=0.5,
                                  help="0.0 es el centro. Valores positivos son más arriba, negativos más abajo.")

# 3. CONVERSIÓN DE UNIDADES A METROS
distancia = distancia_m
h_laser = altura_laser_cm / 100.0
h_mira_absolute = (altura_laser_cm + altura_mira_cm) / 100.0
radio_diana = radio_maximo / 100.0
desviacion_objetivo = desviacion_cm / 100.0

# El centro de la diana siempre está a la altura del láser
h_centro_diana = h_laser 
h_punto_impacto = h_centro_diana + desviacion_objetivo

# 4. CÁLCULO TRIGONOMÉTRICO
angulo_centro_rad = np.arctan((h_mira_absolute - h_centro_diana) / distancia)
angulo_centro_deg = np.degrees(angulo_centro_rad)

angulo_variable_rad = np.arctan((h_mira_absolute - h_punto_impacto) / distancia)
angulo_variable_deg = np.degrees(angulo_variable_rad)

moa_centro = angulo_centro_deg * 60
moa_variable = angulo_variable_deg * 60

# 5. DESPLEGAR MÉTRICAS
st.subheader("📊 Ángulos de Ajuste Calculados")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📐 Inclinación al Centro de la Diana", 
        value=f"{angulo_centro_deg:.4f}°", 
        delta=f"{moa_centro:.2f} MOA",
        delta_color="off"
    )
with col2:
    st.metric(
        label="🎯 Inclinación al Objetivo Ajustado", 
        value=f"{angulo_variable_deg:.4f}°",
        delta=f"{moa_variable:.2f} MOA",
        delta_color="off"
    )
with col3:
    posicion_texto = "Centro" if desviacion_cm == 0 else ("Arriba" if desviacion_cm > 0 else "Abajo")
    st.metric(label="📍 Estado del Impacto", value=f"{abs(desviacion_cm)} cm hacia {posicion_texto}")

# 6. GENERACIÓN DEL GRÁFICO INTERACTIVO (Trayectorias)
st.subheader("📉 Simulación Visual de las Líneas de Visión (Vista Lateral)")

# Creamos todos los trazos (data) de forma independiente
trazos = []

# Línea del Suelo (Fijada a altura 0)
trazos.append(go.Scatter(
    x=[0.0, distancia], y=[0.0, 0.0],
    mode='lines', name='Suelo', line=dict(color='green', width=2, dash='dash')
))

# Línea del Láser (Eje Horizontal) con los argumentos explícitos x e y bien definidos
trazos.append(go.Scatter(
    x=[0.0, distancia], y=[float(h_laser), float(h_centro_diana)],
    mode='lines', name='Rayo Láser (Eje Horizontal)', line=dict(color='red', width=3)
))

# Línea de la Mira apuntando al objetivo elegido
trazos.append(go.Scatter(
    x=[0.0, distancia], y=[float(h_mira_absolute), float(h_punto_impacto)],
    mode='lines', name='Línea de Visión de la Mira', line=dict(color='blue', width=2, dash='dot')
))

# Cuerpo vertical de la diana
y_diana_superior = h_centro_diana + radio_diana
y_diana_inferior = h_centro_diana - radio_diana
trazos.append(go.Scatter(
    x=[distancia, distancia], y=[float(y_diana_inferior), float(y_diana_superior)],
    mode='lines', name='Cuerpo de la Diana', line=dict(color='black', width=6)
))

# Anillos/Sucesiones de la diana (Cada 5 cm de división)
divisiones = np.arange(-radio_diana, radio_diana + 0.01, 0.05)
for div in divisiones:
    trazos.append(go.Scatter(
        x=[distancia, distancia], y=[float(h_centro_diana + div), float(h_centro_diana + div)],
        mode='markers', marker=dict(size=6, color='gray'), showlegend=False
    ))

# Punto de impacto exacto
trazos.append(go.Scatter(
    x=[distancia], y=[float(h_punto_impacto)],
    mode='markers', marker=dict(size=14, color='gold', symbol='star'), name='Punto de Apuntado'
))

# DEFINICIÓN DIRECTA DEL DISEÑO (Sin usar update_layout posterior para evitar problemas de compatibilidad)
diseno_grafico = go.Layout(
    xaxis=dict(title="Distancia Horizontal (Metros)"),
    yaxis=dict(title="Altura desde el Suelo (Metros)"),
    hovermode="closest",
    height=500,
    legend=dict(orient="h", yanchor="bottom", y=1.12, xanchor="right", x=1)
)

# Inicializamos la figura con los componentes ya estructurados de raíz
fig = go.Figure(data=trazos, layout=diseno_grafico)

st.plotly_chart(fig, use_container_width=True)

# 7. NOTAS TÉCNICAS
st.info(f"""
💡 **Análisis Geométrico:** 
* La mira física se encuentra actualmente a una altura absoluta de **{altura_laser_cm + altura_mira_cm} cm** respecto al suelo.
* Para compensar la altura de montaje, la mira debe inclinarse hacia abajo un ángulo de **{angulo_variable_deg:.4f} grados** para intersectar tu objetivo a una distancia de **{distancia_m} metros**.
""")
