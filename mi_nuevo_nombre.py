import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y CONSTANTES
# ---------------------------------------------------------
st.set_page_config(page_title="Software Modular: Topografia & Ciencias", layout="wide")

# ---------------------------------------------------------
# INYECCIÓN DE CSS MONOCROMÁTICO (NEGROS Y GRISES OSCUROS)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 1. Fondo principal y tipografía general */
    .stApp {
        background-color: #050505 !important;
        color: #D4D4D4 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* 2. Estilo de Encabezados */
    h1, h2, h3, h4, h5, h6, .stHeader {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

    /* 3. Tarjetas de Métricas (st.metric) */
    [data-testid="stMetric"] {
        background-color: #121212 !important;
        border: 1px solid #262626 !important;
        padding: 16px !important;
        border-radius: 6px !important;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #8C8C8C !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* 4. Inputs, Selectbox y Sliders */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stNumberInput input {
        background-color: #121212 !important;
        border: 1px solid #262626 !important;
        color: #FFFFFF !important;
        border-radius: 4px !important;
    }
    div[data-baseweb="select"]:hover > div,
    div[data-baseweb="input"]:hover > div {
        border-color: #404040 !important;
    }

    /* 5. Cuadros de Información (st.info, st.warning) */
    div[data-testid="stNotification"] {
        background-color: #171717 !important;
        border: 1px solid #262626 !important;
        color: #A3A3A3 !important;
        border-radius: 4px !important;
    }

    /* 6. Editor de Datos (st.data_editor) */
    div[data-testid="stDataEditor"] {
        background-color: #121212 !important;
        border: 1px solid #262626 !important;
        border-radius: 6px !important;
        padding: 4px;
    }

    /* 7. Línea divisoria (st.divider) */
    hr {
        border-color: #262626 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Constantes Físicas para el Motor de Ciencias
G_CONST = 6.67430e-11   # Constante de gravitación universal (m^3 kg^-1 s^-2)
M_SOLAR = 1.98847e30   # Masa del Sol en kg (para escala de sliders)

# Diccionario de Materiales para Ingeniería Civil
PROPIEDADES_MATERIALES = {
    "Tierra común / Arena": {"esponjamiento": 1.25, "talud_opt": 35.0},
    "Arcilla blanda": {"esponjamiento": 1.30, "talud_opt": 40.0},
    "Roca fragmentada / Volada": {"esponjamiento": 1.50, "talud_opt": 45.0},
    "Grava": {"esponjamiento": 1.15, "talud_opt": 38.0}
}

# ---------------------------------------------------------
# 2. ESTRUCTURA PRINCIPAL (3 COLUMNAS: [1, 2, 1])
# ---------------------------------------------------------
col_izq, col_central, col_der = st.columns([1, 2, 1])

# =========================================================
# COLUMNA IZQUIERDA: SELECTOR Y PARÁMETROS DE ENTRADA
# =========================================================
with col_izq:
    st.header("Configuracion")
    
    mercado = st.selectbox(
        "Selecciona el Mercado:",
        ["Ingeniería Civil (Topografía)", "Ciencias (Geofísica/Astrofísica)"]
    )
    
    st.divider()

    if mercado == "Ingeniería Civil (Topografía)":
        st.subheader("Geometria del Terreno")
        cota_corte = st.slider("Cota de Plano de Corte (m)", min_value=-2.0, max_value=5.0, value=1.0, step=0.1)

        st.subheader("Propiedades Fisicas del Suelo")
        tipo_material = st.selectbox("Tipo de Material", list(PROPIEDADES_MATERIALES.keys()))
        
        # Factor de esponjamiento automático
        factor_esponjamiento = PROPIEDADES_MATERIALES[tipo_material]["esponjamiento"]
        st.info(f"**Factor de Esponjamiento (Auto):** {factor_esponjamiento:.2f}")

        talud_reposo = st.number_input(
            "Talud de Reposo / Angulo (°)", 
            min_value=10.0, max_value=80.0, 
            value=PROPIEDADES_MATERIALES[tipo_material]["talud_opt"], step=1.0
        )
        
        factor_compactacion = st.number_input(
            "Factor de Compactacion", 
            min_value=0.50, max_value=1.00, value=0.85, step=0.01
        )

        st.subheader("Costos y Logistica")
        costo_corte_m3 = st.number_input("Costo Excavacion/Corte ($/m³)", min_value=0.0, value=12.5, step=0.5)
        costo_relleno_m3 = st.number_input("Costo Relleno ($/m³)", min_value=0.0, value=18.0, step=0.5)
        capacidad_camion_m3 = st.number_input("Capacidad Camion de Volteo (m³)", min_value=1.0, value=14.0, step=1.0)

    else:  # Modo Ciencias (Geofísica/Astrofísica)
        st.subheader("Parametros Astrofisicos")
        
        # Sliders y controles solicitados
        M_input = st.slider("Masa del Cuerpo Central (M)", min_value=1.0, max_value=100.0, value=5.0, step=0.5)
        R_km = st.slider("Radio del Cuerpo (R) [km]", min_value=1000, max_value=70000, value=10000, step=1000)
        
        tipo_campo = st.selectbox(
            "Tipo de Campo",
            ["Campo Gravitatorio Masivo", "Anomalía Geofísica Subterránea"]
        )

        # Conversiones físicas para cálculos reales
        M_kg = M_input * M_SOLAR
        R_m = R_km * 1000.0
        
        # Variables calculadas vinculadas
        gravedad = (G_CONST * M_kg) / (R_m**2)
        v_escape_ms = np.sqrt((2 * G_CONST * M_kg) / R_m)
        v_escape_kms = v_escape_ms / 1000.0

# =========================================================
# COLUMNA DERECHA: EDITOR DE DATOS DINÁMICO
# =========================================================
with col_der:
    st.header("Coordenadas")
    
    if mercado == "Ingeniería Civil (Topografía)":
        if "df_civil" not in st.session_state:
            st.session_state.df_civil = pd.DataFrame({'X': [0.0, 2.0, -1.5], 'Y': [0.0, -1.0, 2.0]})
        
        st.write("Puntos de Interes / Sondeos:")
        df_input = st.data_editor(st.session_state.df_civil, num_rows="dynamic", key="editor_civil")
    else:
        if "df_ciencias" not in st.session_state:
            st.session_state.df_ciencias = pd.DataFrame({'X': [1.0, -2.0, 3.0], 'Y': [1.0, 2.0, -1.0]})
        
        st.write("Posicion de Cuerpos / Particulas:")
        df_input = st.data_editor(st.session_state.df_ciencias, num_rows="dynamic", key="editor_ciencias")

# =========================================================
# COLUMNA CENTRAL: GRÁFICA 3D Y MÉTRICAS INFERIORES
# =========================================================
with col_central:
    st.header("Visualizacion y Analisis 3D")
    
    # Malla matemática base
    x = np.linspace(-5, 5, 60)
    y = np.linspace(-5, 5, 60)
    X, Y = np.meshgrid(x, y)

    fig = go.Figure()

    if mercado == "Ingeniería Civil (Topografía)":
        # Ecuación de superficie de terreno
        Z = 3 * np.exp(-(X**2 + Y**2)/6) + 1.5 * np.cos(X/1.5) * np.sin(Y/1.5)
        
        # Cálculos de Volúmenes y Costos
        diff = Z - cota_corte
        dx, dy = x[1] - x[0], y[1] - y[0]
        area_celda = dx * dy
        
        vol_corte_bancal = np.sum(diff[diff > 0]) * area_celda
        vol_relleno_bancal = np.sum(-diff[diff < 0]) * area_celda
        
        vol_corte_suelto = vol_corte_bancal * factor_esponjamiento
        costo_total_obra = (vol_corte_bancal * costo_corte_m3) + (vol_relleno_bancal * costo_relleno_m3)
        viajes_camion = int(np.ceil(vol_corte_suelto / capacidad_camion_m3)) if capacidad_camion_m3 > 0 else 0

        # Renders 3D
        fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Earth", name="Terreno"))
        Z_plano = np.full_like(Z, cota_corte)
        fig.add_trace(go.Surface(
            z=Z_plano, x=X, y=Y, 
            colorscale=[[0, 'rgba(255,0,0,0.5)'], [1, 'rgba(255,0,0,0.5)']], 
            showscale=False, name="Plano de Corte"
        ))

        # Control de errores al graficar puntos
        try:
            if not df_input.empty and 'X' in df_input.columns and 'Y' in df_input.columns:
                px = pd.to_numeric(df_input['X'], errors='coerce').dropna().values
                py = pd.to_numeric(df_input['Y'], errors='coerce').dropna().values
                pz = 3 * np.exp(-(px**2 + py**2)/6) + 1.5 * np.cos(px/1.5) * np.sin(py/1.5)
                
                fig.add_trace(go.Scatter3d(
                    x=px, y=py, z=pz, mode='markers',
                    marker=dict(size=6, color='red', symbol='diamond'), name='Sondeos'
                ))
        except Exception:
            st.warning("Revisa las coordenadas ingresadas en la tabla de la derecha.")

        fig.update_layout(
            scene=dict(xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Elevación (m)", aspectratio=dict(x=1, y=1, z=0.6)),
            margin=dict(l=0, r=0, b=0, t=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Métricas Inferiores - Topografía
        m1, m2, m3 = st.columns(3)
        m1.metric("Volumen Corte (Suelto)", f"{vol_corte_suelto:.2f} m³")
        m2.metric("Costo Total Estimado", f"${costo_total_obra:,.2f}")
        m3.metric("Viajes de Camión", f"{viajes_camion} viajes")

    else:  # Renderizado para Ciencias (Geofísica/Astrofísica)
        # Embudo Gravitatorio / Potencial
        r = np.sqrt(X**2 + Y**2) + 0.5
        Z = - (G_CONST * M_kg) / (r * 1e8)

        fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", name="Embudo Gravitatorio"))

        # Control de errores al graficar partículas
        try:
            if not df_input.empty and 'X' in df_input.columns and 'Y' in df_input.columns:
                px = pd.to_numeric(df_input['X'], errors='coerce').dropna().values
                py = pd.to_numeric(df_input['Y'], errors='coerce').dropna().values
                pr = np.sqrt(px**2 + py**2) + 0.5
                pz = - (G_CONST * M_kg) / (pr * 1e8)
                
                fig.add_trace(go.Scatter3d(
                    x=px, y=py, z=pz, mode='markers',
                    marker=dict(size=7, color='yellow', symbol='circle'), name='Partículas'
                ))
        except Exception:
            st.warning("Revisa las coordenadas de las partículas en la tabla de la derecha.")

        fig.update_layout(
            scene=dict(xaxis_title="X (UA)", yaxis_title="Y (UA)", zaxis_title="Potencial (Φ)", aspectratio=dict(x=1, y=1, z=0.6)),
            margin=dict(l=0, r=0, b=0, t=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- MÉTRICAS INFERIORES SOLICITADAS PARA CIENCIAS ---
        m1, m2, m3 = st.columns(3)
        
        m1.metric(
            label="Gravedad Superficial", 
            value=f"{gravedad:.2f} m/s²"
        )
        
        m2.metric(
            label="Velocidad de Escape", 
            value=f"{v_escape_kms:.2f} km/s"
        )
        
        estado_sistema = "Gravedad Extrema" if gravedad > 50 else "Campo Estable"
        m3.metric(
            label="Estado del Sistema", 
            value=estado_sistema
        )
