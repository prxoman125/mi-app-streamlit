import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

# Configuración de la página
st.set_page_config(
    page_title="Simulación de Estadística y Probabilidad",
    page_icon="🎲",
    layout="wide"
)

# Título y descripción
st.title("🎲 Simulación del Teorema del Límite Central")
st.markdown("""
Esta aplicación demuestra cómo la distribución de las **medias muestrales** se aproxima a una **distribución normal** a medida que aumenta el tamaño de la muestra, independientemente de la forma de la población original.
""")

st.sidebar.header("⚙️ Parámetros de la Simulación")

# 1. Selección de la distribución poblacional
distribucion = st.sidebar.selectbox(
    "Selecciona la Distribución Original:",
    ("Uniforme", "Exponencial", "Bernoulli (Moneda)")
)

# 2. Selección de parámetros numéricos
num_simulaciones = st.sidebar.slider("Número de Simulaciones (Muestras):", 100, 10000, 2000, step=100)
tamano_muestra = st.sidebar.slider("Tamaño de cada Muestra (n):", 1, 500, 30, step=1)

# Generación de datos según la distribución seleccionada
np.random.seed(42)  # Semilla para reproducibilidad

if distribucion == "Uniforme":
    poblacion = np.random.uniform(low=0, high=10, size=(num_simulaciones, tamano_muestra))
elif distribucion == "Exponencial":
    poblacion = np.random.exponential(scale=2.0, size=(num_simulaciones, tamano_muestra))
else:  # Bernoulli
    poblacion = np.random.binomial(n=1, p=0.5, size=(num_simulaciones, tamano_muestra))

# Cálculo de medias por muestra utilizando NumPy
medias_muestrales = np.mean(poblacion, axis=1)

# Creación de DataFrame con Pandas
df_medias = pd.DataFrame({'Media Muestral': medias_muestrales})

# Layout de columnas para visualización
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Distribución de las Medias Muestrales")
    
    # Gráfico interactivo con Plotly
    fig = px.histogram(
        df_medias, 
        x='Media Muestral', 
        nbins=40, 
        title="Histrograma de Medias Muestrales",
        color_discrete_sequence=['#636EFA'],
        marginal="box", # Añade un diagrama de caja superior
        opacity=0.75
    )
    
    # Línea vertical para la media global
    media_global = df_medias['Media Muestral'].mean()
    fig.add_vline(x=media_global, line_dash="dash", line_color="red", annotation_text=f"Media: {media_global:.2f}")
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📈 Resumen Estadístico")
    
    # Métricas clave
    st.metric(label="Media de las Medias", value=f"{df_medias['Media Muestral'].mean():.4f}")
    st.metric(label="Desviación Estándar (Error Estándar)", value=f"{df_medias['Media Muestral'].std():.4f}")
    st.metric(label="Varianza", value=f"{df_medias['Media Muestral'].var():.4f}")
    
    st.markdown("---")
    st.write("**Vista previa de los datos simulados (Pandas DataFrame):**")
    st.dataframe(df_medias.head(10), use_container_width=True)

# Sección informativa adicional
st.info("""
💡 **Observación:** Intenta aumentar el **Tamaño de cada Muestra (n)** en la barra lateral. 
Verás cómo el histograma se vuelve cada vez más simétrico y acampanado (distribución normal), sin importar si empezaste con una distribución uniforme o exponencial.
""")
