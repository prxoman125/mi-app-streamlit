import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y CONSTANTES
# ---------------------------------------------------------
st.set_page_config(page_title="Software Modular: Topografia & Ciencias", layout="wide")

# ---------------------------------------------------------
# INYECCIÓN DE CSS ENTERPRISE (HIGH-END DARK UI)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 1. Fondo principal y tipografía general estilo Enterprise */
    .stApp {
        background-color: #090A0F !important;
        color: #C5C9D3 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Ocultar barra superior por defecto de Streamlit */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* 2. Estilo de Encabezados */
    h1, h2, h3 {
        color: #F0F2F5 !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0.8rem !important;
    }
    
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.25rem !important; }
    h3 { font-size: 1rem !important; }

    /* 3. Tarjetas de Métricas Ejecutivas */
    [data-testid="stMetric"] {
        background-color: #12151E !important;
        border: 1px solid #232836 !important;
        border-top: 2px solid #3B4254 !important;
        padding: 18px 20px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }
    [data-testid="stMetricLabel"] {
        color: #7A8499 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* 4. Inputs, Selectbox y Sliders */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stNumberInput input {
        background-color: #12151E !important;
        border: 1px solid #232836 !important;
        color: #F0F2F5 !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease;
    }
    
    div[data-baseweb="select"]:hover > div,
    div[data-baseweb="input"]:hover > div {
        border-color: #3B4254 !important;
    }

    /* Labels de los controles */
    .stSelectbox label, .stSlider label, .stNumberInput label {
        color: #9DA5B4 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* 5. Cuadros de Información */
    div[data-testid="stNotification"] {
        background-color: #12151E !important;
        border: 1px solid #232836 !important;
        border-left: 3px solid #5A657D !important;
        color: #C5C9D3 !important;
        border-radius: 6px !important;
    }

    /* 6. Editor de Datos */
    div[data-testid="stDataEditor"] {
        background-color: #12151E !important;
        border: 1px solid #232836 !important;
        border-radius: 8px !important;
        padding: 6px;
    }

    /* 7. Separadores visuales */
    hr {
        border-color: #1D222E !important;
        margin: 1.5rem 0 !important;
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

# Configuración del maquetado base para Plotly 3D (para encajar impecable en el tema oscuro)
PLOTLY_LAYOUT_BASE = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, b=0, t=10),
    font=dict(family="Inter, sans-serif", color="#7A8499", size=11)
)

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

        # Renders 3D (Colores mantenidos)
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
            **PLOTLY_LAYOUT_BASE,
            scene=dict(
                xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Elevación (m)",
                aspectratio=dict(x=1, y=1, z=0.6),
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#232836", showbackground=True),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#232836", showbackground=True),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#232836", showbackground=True)
            )
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

        # Renders 3D (Colores mantenidos)
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
            **PLOTLY_LAYOUT_BASE,
            scene=dict(
                xaxis_title="X (UA)", yaxis_title="Y (UA)", zaxis_title="Potencial (Φ)",
                aspectratio=dict(x=1, y=1, z=0.6),
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#232836", showbackground=True),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#232836", showbackground=True),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#232836", showbackground=True)
            )
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- MÉTRICAS INFERIORES PARA CIENCIAS ---
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
