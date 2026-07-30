import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="App Modular Math & Topo", layout="wide")

# ---------------------------------------------------------
# ESTRUCTURA PRINCIPAL (3 COLUMNAS: [1, 2, 1])
# ---------------------------------------------------------
col_left, col_center, col_right = st.columns([1, 2, 1])

# =========================================================
# COLUMNA IZQUIERDA: SELECTOR Y PARÁMETROS
# =========================================================
with col_left:
    st.header("⚙️ Configuración")
    
    mercado = st.selectbox(
        "Selecciona el Mercado:",
        ["Ingeniería Civil (Topografía)", "Ciencias (Geofísica/Astrofísica)"]
    )
    
    st.divider()

    # Parámetros según el mercado
    if mercado == "Ingeniería Civil (Topografía)":
        st.subheader("Parámetros de Terreno")
        cota_corte = st.slider("Cota de Plano de Corte (m)", min_value=-2.0, max_value=5.0, value=1.0, step=0.1)
    else:
        st.subheader("Parámetros Gravitatorios")
        masa = st.slider("Masa Central (M)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)

# =========================================================
# COLUMNA DERECHA: EDITOR DE DATOS DINÁMICO
# =========================================================
with col_right:
    st.header("📍 Coordenadas")
    
    # Inicialización de estado para la tabla si no existe
    if mercado == "Ingeniería Civil (Topografía)":
        if "df_civil" not in st.session_state:
            st.session_state.df_civil = pd.DataFrame({'X': [0.0, 2.0, -1.5], 'Y': [0.0, -1.0, 2.0]})
        
        st.write("Puntos de Interés / Sondeos:")
        df_input = st.data_editor(st.session_state.df_civil, num_rows="dynamic", key="editor_civil")
    else:
        if "df_ciencias" not in st.session_state:
            st.session_state.df_ciencias = pd.DataFrame({'X': [1.0, -2.0, 3.0], 'Y': [1.0, 2.0, -1.0]})
        
        st.write("Posición de Cuerpos / Partículas:")
        df_input = st.data_editor(st.session_state.df_ciencias, num_rows="dynamic", key="editor_ciencias")

# =========================================================
# COLUMNA CENTRAL: CÁLCULOS, GRÁFICA 3D Y MÉTRICAS
# =========================================================
with col_center:
    st.header("📊 Visualización y Análisis 3D")
    
    # Malla base para cálculos 3D
    x = np.linspace(-5, 5, 60)
    y = np.linspace(-5, 5, 60)
    X, Y = np.meshgrid(x, y)

    fig = go.Figure()

    if mercado == "Ingeniería Civil (Topografía)":
        # Ecuación de relieve (combinación de funciones gaussianas)
        Z = 3 * np.exp(-(X**2 + Y**2)/6) + 1.5 * np.cos(X/1.5) * np.sin(Y/1.5)
        
        # Cálculos de volumen (Corte y Relleno)
        # Diferencia respecto a la cota de corte
        diff = Z - cota_corte
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        area_celda = dx * dy
        
        vol_corte = np.sum(diff[diff > 0]) * area_celda
        vol_relleno = np.sum(-diff[diff < 0]) * area_celda
        vol_neto = vol_corte - vol_relleno

        # Superficie del terreno
        fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Earth", name="Terreno"))
        
        # Plano de corte horizontal
        Z_plano = np.full_like(Z, cota_corte)
        fig.add_trace(go.Surface(
            z=Z_plano, x=X, y=Y, 
            colorscale=[[0, 'rgba(255,0,0,0.5)'], [1, 'rgba(255,0,0,0.5)']], 
            showscale=False, name="Plano de Corte"
        ))

        # Control de errores y visualización de puntos de la tabla
        try:
            if not df_input.empty and 'X' in df_input.columns and 'Y' in df_input.columns:
                px = df_input['X'].dropna().values
                py = df_input['Y'].dropna().values
                # Interpola la Z del terreno en las posiciones (X, Y) ingresadas
                pz = 3 * np.exp(-(px**2 + py**2)/6) + 1.5 * np.cos(px/1.5) * np.sin(py/1.5)
                
                fig.add_trace(go.Scatter3d(
                    x=px, y=py, z=pz,
                    mode='markers',
                    marker=dict(size=6, color='red', symbol='diamond'),
                    name='Sondeos'
                ))
        except Exception as e:
            st.warning("Error al procesar los puntos ingresados. Revisa que las columnas 'X' e 'Y' contengan valores numéricos válidos.")

        # Diseño del gráfico
        fig.update_layout(
            scene=dict(
                xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Elevación (m)",
                aspectratio=dict(x=1, y=1, z=0.6)
            ),
            margin=dict(l=0, r=0, b=0, t=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Despliegue de 3 Métricas
        m1, m2, m3 = st.columns(3)
        m1.metric("Volumen Corte", f"{vol_corte:.2f} m³")
        m2.metric("Volumen Relleno", f"{vol_relleno:.2f} m³")
        m3.metric("Balance Neto", f"{vol_neto:.2f} m³", delta=f"{vol_neto:.2f}")

    else: # Mercado: Ciencias (Geofísica/Astrofísica)
        # Embudo gravitatorio: Potencial V(r) ~ -G*M / sqrt(r^2 + epsilon)
        G = 1.0
        r = np.sqrt(X**2 + Y**2) + 0.5  # Modificador suavizado para evitar singularidad en origin
        Z = - (G * masa) / r
        
        # Magnitud del campo de aceleración (fuerza por unidad de masa)
        # F = G*M / r^2
        fuerza_max = (G * masa) / (0.5**2)
        fuerza_media = np.mean((G * masa) / (r**2))
        potencial_min = np.min(Z)

        # Visualización 3D
        fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", name="Pozo Gravitatorio"))

        # Control de errores y visualización de partículas
        try:
            if not df_input.empty and 'X' in df_input.columns and 'Y' in df_input.columns:
                px = df_input['X'].dropna().values
                py = df_input['Y'].dropna().values
                pr = np.sqrt(px**2 + py**2) + 0.5
                pz = - (G * masa) / pr
                
                fig.add_trace(go.Scatter3d(
                    x=px, y=py, z=pz,
                    mode='markers+text',
                    marker=dict(size=7, color='yellow', symbol='circle'),
                    name='Partículas'
                ))
        except Exception as e:
            st.warning("Error al procesar las partículas. Asegúrate de ingresar coordenadas X e Y válidas.")

        # Diseño del gráfico
        fig.update_layout(
            scene=dict(
                xaxis_title="X (UA)", yaxis_title="Y (UA)", zaxis_title="Potencial (Φ)",
                aspectratio=dict(x=1, y=1, z=0.6)
            ),
            margin=dict(l=0, r=0, b=0, t=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Despliegue de 3 Métricas
        m1, m2, m3 = st.columns(3)
        m1.metric("Potencial Mínimo", f"{potencial_min:.2f} J/kg")
        m2.metric("Fuerza Máx. Central", f"{fuerza_max:.2f} N/kg")
        m3.metric("Fuerza Promedio", f"{fuerza_media:.2f} N/kg")
