import math
import matplotlib.pyplot as plt
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Cálculo de Inclinación de Mira", layout="wide")

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
st.sidebar.header("🎯 Parámetros del Sistema")

# Posición fija del centro de la diana / láser
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

# --- CÁLCULOS MATEMÁTICOS ---
diferencia_altura = altura_laser - altura_mira

# Ángulo en radianes y conversión a grados
angulo_rad = math.atan2(diferencia_altura, distancia_mira)
angulo_grados = math.degrees(angulo_rad)

# --- PANTALLA PRINCIPAL (75% RESTANTE) ---
st.title("🎯 Calculadora de Ángulo para Mira de Caza/Tiro")
st.caption(
    "El láser está fijo en el centro de la diana. Ajusta la posición de la mira para obtener el ángulo de inclinación."
)

st.markdown("---")

# Métricas principales arriba
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Diferencia de Altura", f"{diferencia_altura:+.2f} m")

with col2:
    st.metric("Ángulo de Inclinación", f"{angulo_grados:+.2f}°")

with col3:
    if angulo_grados > 0:
        st.metric("Orientación", "Inclinado hacia ARRIBA ⬆️")
    elif angulo_grados < 0:
        st.metric("Orientación", "Inclinado hacia ABAJO ⬇️")
    else:
        st.metric("Orientación", "Completamente NIVELADO ➡️")

st.markdown("---")

# --- GRÁFICO VISUAL (SIMULACIÓN) ---
st.subheader("📐 Simulación Visual")

fig, ax = plt.subplots(figsize=(8, 3.5))

# Dibujar la línea de suelo
ax.axhline(0, color="gray", linestyle="--", alpha=0.5)

# Dibujar Diana y Láser (Fijo en x=distancia_mira, y=altura_laser)
ax.plot(
    distancia_mira,
    altura_laser,
    "ro",
    markersize=12,
    label="Centro Diana / Láser",
)
ax.annotate(
    " Diana (Láser Fijo)",
    (distancia_mira, altura_laser),
    textcoords="offset points",
    xytext=(10, -5),
)

# Dibujar la Mira (en x=0, y=altura_mira)
ax.plot(0, altura_mira, "bs", markersize=10, label="Mira")
ax.annotate(
    " Mira", (0, altura_mira), textcoords="offset points", xytext=(-35, -5)
)

# Línea de visión de la Mira al Láser
ax.plot(
    [0, distancia_mira],
    [altura_mira, altura_laser],
    "g--",
    linewidth=2,
    label=f"Línea de Visión ({angulo_grados:.2f}°)",
)

# Línea horizontal de referencia para la mira
ax.plot([0, distancia_mira], [altura_mira, altura_mira], "k:", alpha=0.4)

# Configuración del gráfico
ax.set_xlim(-1, distancia_mira + 2)
ax.set_ylim(-1, max(altura_laser, altura_mira) + 2)
ax.set_xlabel("Distancia Horizontal (m)")
ax.set_ylabel("Altura (m)")
ax.legend(loc="upper left")
ax.grid(True, linestyle=":", alpha=0.6)

# Mostrar en Streamlit
st.pyplot(fig)
