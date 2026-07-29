import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Mira Interactiva", layout="centered")

st.title("🎯 Alineación de Mira Arrastrable")
st.write("👉 **Instrucciones:** Haz clic en el centro de la **mira** (azul) o de la **diana** (roja) y **arrástralos verticalmente**. El sistema calculará el ángulo al instante.")

# 1. Inicializar las posiciones en el estado de Streamlit si no existen
if "y_mira" not in st.session_state:
    st.session_state.y_mira = 4.0      # Altura inicial de la mira (en cm)
if "y_diana" not in st.session_state:
    st.session_state.y_diana = 0.0    # La diana empieza en el centro horizontal

distancia_fija = 10.0 # Distancia fija a la diana en metros (1000 cm)

# 2. Capturar el movimiento del ratón desde el gráfico Plotly
if "valores_grafico" in st.session_state and st.session_state.valores_grafico:
    relayout_data = st.session_state.valores_grafico.get("relayout", {})
    
    # Detectar si el usuario arrastró la Mira (Punto índice 0 en los datos)
    if "shapes[0].y0" in relayout_data:
        st.session_state.y_mira = relayout_data["shapes[0].y0"]
    # Detectar si el usuario arrastró la Diana (Punto índice 1 en los datos)
    elif "shapes[5].y0" in relayout_data: # Ajustado al índice base del centro de la diana
        st.session_state.y_diana = relayout_data["shapes[5].y0"]

# --- CÁLCULOS TRIGONOMÉTRICOS ---
# Cateto opuesto = Diferencia de altura entre la mira y la diana (en metros)
altura_relativa_m = (st.session_state.y_mira - st.session_state.y_diana) / 100.0
angulo_rad = np.arctan(altura_relativa_m / distancia_fija)
angulo_deg = np.degrees(angulo_rad)

# Mostrar el ángulo calculado en grande
st.metric(label="📐 Ángulo requerido en la Mira", value=f"{angulo_deg:.4f}°")

# 3. CONSTRUCCIÓN DEL GRÁFICO INTERACTIVO (Plotly)
fig = go.Figure()

# --- DISEÑO DE LA MIRA TELESCÓPICA (Posición X = 0) ---
y_m = st.session_state.y_mira
# Círculo exterior de la mira
fig.add_shape(type="circle", x0=-0.3, y0=y_m-1, x1=0.3, y1=y_m+1, line=dict(color="Blue", width=3))
# Cruz interna de la mira (Retícula)
fig.add_shape(type="line", x0=-0.5, y0=y_m, x1=0.5, y1=y_m, line=dict(color="Blue", width=2))
fig.add_shape(type="line", x0=0, y0=y_m-1.2, x1=0, y1=y_m+1.2, line=dict(color="Blue", width=2))

# --- DISEÑO DE LA DIANA (Posición X = 10 metros) ---
y_d = st.session_state.y_diana
# Anillos de la diana
fig.add_shape(type="circle", x0=9.7, y0=y_d-1.5, x1=10.3, y1=y_d+1.5, line=dict(color="Red", width=2))
fig.add_shape(type="circle", x0=9.85, y0=y_d-0.7, x1=10.15, y1=y_d+0.7, line=dict(color="Red", width=2))
# Centro de la diana (Punto de impacto del láser)
fig.add_shape(type="circle", x0=9.95, y0=y_d-0.15, x1=10.05, y1=y_d+0.15, fillcolor="Red", line=dict(color="Red"))

# --- LÍNEAS DE PROYECTO ---
# Láser recto apuntando siempre al centro de la diana (Desde X=0, Y=y_d hasta X=10, Y=y_d)
fig.add_shape(type="line", x0=0, y0=y_d, x1=10, y1=y_d, line=dict(color="Red", width=2, dash="dash"))

# Línea de visión desde la Mira hasta la Diana
fig.add_shape(type="line", x0=0, y0=y_m, x1=10, y1=y_d, line=dict(color="Cyan", width=2))

# Configuración visual del escenario
fig.update_layout(
    xaxis=dict(range=[-1, 11], title="Distancia Horizontal (Metros)", fixedrange=True),
    yaxis=dict(range=[-7, 7], title="Altura (Centímetros)", fixedrange=True),
    height=450,
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    # ACTIVAR EL MODO EDICIÓN: Esto permite arrastrar las formas con el ratón
    config={"editable": True, "displayModeBar": False}
)

# Renderizar el gráfico asignándole una clave para guardar su estado en Streamlit
st.plotly_chart(fig, use_container_width=True, key="valores_grafico")

# Texto Informativo Dinámico
if y_m > y_d:
    st.info(f"💡 Al estar la mira por encima del objetivo, debes inclinarla hacia **abajo** un ángulo de {abs(angulo_deg):.4f}°.")
elif y_m < y_d:
    st.info(f"💡 Al estar la mira por debajo del objetivo, debes inclinarla hacia **arriba** un ángulo de {abs(angulo_deg):.4f}°.")
else:
    st.success("🎯 Perfectamente alineados en paralelo (0°).")
