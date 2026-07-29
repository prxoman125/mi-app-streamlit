import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Simulador de Mira Láser", layout="centered")

st.title("🎯 Simulador de Inclinación de Mira Telescópica")
st.write(
    "El cañón láser está fijo y apunta horizontalmente en línea recta hacia el centro de la diana. "
    "Calculamos el ángulo que debe tener la mira para cruzarse exactamente en el objetivo."
)

# --- PANEL DE CONTROL (Parámetros modificables) ---
st.sidebar.header("Configuración del Sistema")

distancia = st.sidebar.slider(
    "Distancia horizontal a la diana (metros):", 
    min_value=1.0, max_value=50.0, value=10.0, step=0.5
)

altura_mira = st.sidebar.slider(
    "Altura de la mira respecto al láser (cm):", 
    min_value=-20.0, max_value=20.0, value=5.0, step=0.5
)

# --- CÁLCULOS TRIGONOMÉTRICOS ---
# Convertimos la altura de la mira de centímetros a metros para homogenizar unidades
h_metros = altura_mira / 100.0
d_metros = distancia

# Cálculo del ángulo usando el arco tangente: theta = arctan(opuesto / adyacente)
angulo_rad = np.arctan(h_metros / d_metros)
angulo_deg = np.degrees(angulo_rad)

# --- PRESENTACIÓN DE RESULTADOS ---
st.subheader("📊 Resultados del Cálculo")

col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="Ángulo de la Mira (Grados)", 
        value=f"{angulo_deg:.4f}°"
    )
with col2:
    if altura_mira > 0:
        st.info("🟢 La mira debe apuntar hacia **abajo** (Ángulo de depresión).")
    elif altura_mira < 0:
        st.info("🔵 La mira debe apuntar hacia **arriba** (Ángulo de elevación).")
    else:
        st.info("🟡 La mira está alineada con el láser. Ángulo: 0°.")

# --- GRÁFICA INTERACTIVA (Matplotlib) ---
st.subheader("👁️ Visualización del Sistema")

fig, ax = plt.subplots(figsize=(10, 4))

# Dibujar la línea del láser (Siempre recta y horizontal hacia el centro en Y=0)
ax.plot([0, d_metros], [0, 0], color="red", linestyle="--", linewidth=2, label="Rayo Láser (Fijo)")

# Dibujar la línea de visión de la mira (Desde (0, h) hasta (d, 0))
ax.plot([0, d_metros], [h_metros, 0], color="blue", linestyle="-", linewidth=2, label="Línea de Visión de la Mira")

# Dibujar componentes (Cañón, Mira y Diana)
ax.scatter(0, 0, color="black", s=100, zorder=5, label="Cañón Láser")
ax.scatter(0, h_metros, color="blue", s=100, zorder=5, label="Mira")
ax.scatter(d_metros, 0, color="darkred", s=150, marker="X", zorder=5, label="Centro de la Diana")

# Configuración estética de la gráfica
ax.set_xlabel("Distancia Horizontal (metros)")
ax.set_ylabel("Altura Vertical (metros)")
ax.set_title(f"Alineación de Objetivos (Ángulo de la mira: {angulo_deg:.3f}°)")
ax.legend(loc="upper right")
ax.grid(True, linestyle=":", alpha=0.6)

# Ajustar límites dinámicamente para que se aprecie el ángulo
ax.set_ylim(min(-0.05, h_metros - 0.05), max(0.05, h_metros + 0.05))

# Renderizar en la pantalla de Streamlit
st.pyplot(fig)
