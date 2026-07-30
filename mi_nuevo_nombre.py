import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="App Modular Math & Topo", layout="wide")

# ---------------------------------------------------------
# DICCIONARIO DE MATERIALES Y PROPIEDADES FÍSICAS
# ---------------------------------------------------------
PROPIEDADES_MATERIALES = {
    "Tierra común / Arena": {"esponjamiento": 1.25, "talud_opt": 35},
    "Arcilla blanda": {"esponjamiento": 1.30, "talud_opt": 40},
    "Roca fragmentada / Volada": {"esponjamiento": 1.50, "talud_opt": 45},
    "Grava": {"esponjamiento": 1.15, "talud_opt": 38}
}

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
        st.subheader("📏 Geometría del Terreno")
        cota_corte = st.slider("Cota de Plano de Corte (m)", min_value=-2.0, max_value=5.0, value=1.0, step=0.1)

        st.subheader("🧱 Propiedades Físicas del Suelo")
        
        tipo_material = st.selectbox("Tipo de Material", list(PROPIEDADES_MATERIALES.keys()))
        
        # Factor de esponjamiento automático según el material elegido
        factor_esponjamiento = PROPIEDADES_MATERIALES[tipo_material]["esponjamiento"]
        st.info(f"**Factor de Esponjamiento (Auto):** {factor_esponjamiento:.2f}")

        talud_reposo = st.number_input(
            "Talud de Reposo / Ángulo de Inclinación (°)", 
            min_value=10.0, max_value=80.0, 
            value=float(PROPIEDADES_MATERIALES[tipo_material]["talud_opt"]), step=1.0
        )
        
        factor_compactacion = st.number_input(
            "Factor de Compactación", 
            min_value=0.50, max_value=1.00, value=0.85, step=0.01,
            help="Relación de volumen compactado frente a volumen natural bancal."
        )

        st.subheader("💰 Costos y Logística")
        costo_corte_m3 = st.number_input("Costo Excavación/Corte ($/m³)", min_value=0.0, value=12.5, step=0.5)
        costo_relleno_m3 = st.number_input("Costo Relleno ($/m³)", min_value=0.0, value=18.0, step=0.5)
        capacidad_camion_m3 = st.number_input("Capacidad Camión de Volteo (m³)", min_value=1.0, value=14.0, step=1.0)

    else:
        st.subheader("Parámetros Gravitatorios")
        masa = st.slider("Masa Central (M)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)

# =========================================================
# COLUMNA DERECHA: EDITOR DE DATOS DINÁMICO
# =========================================================
with col_right:
    st.header("📍 Coordenadas")
    
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
        # Ecuación de relieve (superficie del terreno)
        Z = 3 * np.exp(-(X**2 + Y**2)/6) + 1.5 * np.cos(X/1.5) * np.sin(Y/1.5)
        
        # Cálculos Geométricos Básicos (Bancal/Natural)
        diff = Z - cota_corte
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        area_celda = dx * dy
        
        vol_corte_bancal = np.sum(diff[diff > 0]) * area_celda
        vol_relleno_bancal = np.sum(-diff[diff < 0]) * area_celda
        
        # Ajuste por propiedades físicas del suelo
        vol_corte_suelto = vol_corte_bancal * factor_esponjamiento  # Volumen a transportar
        vol_relleno_compactado = vol_relleno_bancal / factor_compactacion # Volumen requerido
        
        # Costos y Transporte
        costo_total_corte = vol_corte_bancal * costo_corte_m3
        costo_total_relleno = vol_relleno_bancal * costo_relleno_m3
        costo_total_obra = costo_total_corte + costo_total_relleno
        
        viajes_camion = int(np.ceil(vol_corte_suelto / capacidad_camion_m3)) if capacidad_camion_m3 > 0 else 0

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
                pz = 3 * np.exp(-(px**2 + py**2)/6) + 1.5 * np.cos(px/1.5) * np.sin(py/1.5)
                
                fig.add_trace(go.Scatter3d(
                    x=px, y=py, z=pz,
                    mode='markers',
                    marker=dict(size=6, color='red', symbol='diamond'),
                    name='Sondeos'
                ))
        except Exception as e:
            st.warning("Error al procesar los puntos ingresados. Revisa que las columnas 'X' e 'Y' contengan valores válidos.")

        # Diseño del gráfico
        fig.update_layout(
            scene=dict(
                xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Elevación (m)",
                aspectratio=dict(x=1, y=1, z=0.6)
            ),
            margin=dict(l=0, r=0, b=0, t=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Despliegue de Métricas Principales (3 Métricas requeridas)
        m1, m2, m3 = st.columns(3)
        m1.metric("Volumen Corte (Suelto)", f"{vol_corte_suelto:.2f} m³", help=f"Bancal: {vol_corte_bancal:.2f} m³")
        m2.metric("Costo Total Estimado", f"${costo_total_obra:,.2f}")
        m3.metric("Viajes de Camión", f"{viajes_camion} viajes", help=f"Basado en {capacidad_camion_m3} m³ por viaje")

    else: # Mercado: Ciencias (Geofísica/Astrofísica)
        G = 1.0
        r = np.sqrt(X**2 + Y**2) + 0.5
        Z = - (G * masa) / r
        
        fuerza_max = (G * masa) / (0.5**2)
        fuerza_media = np.mean((G * masa) / (r**2))
        potencial_min = np.min(Z)

        # Visualización 3D
        fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", name="Pozo Gravitatorio"))

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
