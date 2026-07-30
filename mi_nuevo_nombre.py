import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Quantum Capital Suite", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INYECCIÓN DE CSS PARA DISEÑO INTEGRAL DE ALTA GAMA CON DEGRADADO ---
st.markdown("""
    <style>
        /* Fondo general oscuro de alta gama */
        .stApp {
            background-color: #0A1128;
            color: #E2E8F0;
        }
        /* Color unificado para todos los encabezados */
        h1, h2, h3 {
            color: #00E5FF !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
        }
        /* Estilizado técnico de bloques de métricas */
        div[data-testid="stMetric"] {
            background-color: #101F42;
            border: 1px solid #1E3A8A;
            border-radius: 8px;
            padding: 15px;
        }
        /* CAMBIO: Fondo degradado azul oscuro para la columna izquierda (col1) */
        div[data-testid="column"]:nth-of-type(1) {
            background: linear-gradient(135deg, #0A1432 0%, #12255C 100%);
            border: 1px solid #1E3A8A;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 229, 255, 0.05);
        }
        /* Ajuste para que los inputs numéricos combinen con el fondo oscuro */
        input {
            background-color: #101F42 !important;
            color: #E2E8F0 !important;
            border: 1px solid #1E3A8A !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DINÁMICO DE IDIOMAS (DICCIONARIO DE TRADUCCIÓN) ---
idioma = st.selectbox("Language / Idioma", ["Español", "English"])

t = {
    "Español": {
        "titulo": "Quantum Capital Suite",
        "subtitulo": "Plataforma analítica e industrial para la proyección de activos e interés compuesto.",
        "p_control": "Parámetros de Inversión",
        "p_desc": "Configure los vectores financieros de entrada manualmente:",
        "cap_init": "Capital Inicial ($)",
        "ahorro": "Ahorro Mensual Recurrente ($)",
        "horizonte": "Horizonte Temporal (Años)",
        "tasa": "Tasa de Retorno Anual Esperada (%)",
        "ejecutar": "Ejecutar Análisis Financiero",
        "licencia": "Licencia del Entorno",
        "lic_inst": "Activar Licencia Institucional",
        "lic_ok": "Acceso Premium Concedido.",
        "lic_no": "Licencia Gratuita Restringida.",
        "v_macro": "Variables Macroeconómicas",
        "inflacion": "Tasa de Inflación Proyectada (%)",
        "impuesto": "Tasa Impositiva sobre Rendimientos (%)",
        "volatilidad": "Volatilidad de Activos / Desviación (%)",
        "res_analiticos": "Métricas de Rendimiento",
        "cap_neto": "Capital Neto Estimado al Cierre del Horizonte",
        "retorno_bruto": "Retorno Bruto Compuesto",
        "auditoria": "Auditoría de Poder Adquisitivo",
        "desglose_infla": "Desglose anual indexado a una inflación estimada del",
        "proc_mat": "Procedimiento Matemático Estándar",
        "info_init": "Especifique los parámetros numéricos en el panel izquierdo y presione el botón de ejecución.",
        "mod_avanzados": "Módulos Analíticos Avanzados (Licencia Institucional)",
        "aviso_premium": "Los modelos estocásticos, análisis de riesgo de volatilidad y la evaluación Sharpe están reservados para el entorno de pago.",
        "btn_premium": "Adquirir Licencia Institucional por $19.99 USD",
        "sim_montecarlo": "Simulación Estocástica de Mercado (Montecarlo)",
        "desc_montecarlo": "Generación de 500 trayectorias probabilísticas con volatilidad matemática:",
        "e_sharpe": "Evaluación de Eficiencia (Índice de Sharpe)",
        "sharpe_ok": "Estrategia óptima respecto al riesgo asumido.",
        "sharpe_no": "Rendimiento ajustado al riesgo subóptimo.",
        "gestion_preserv": "Gestión de Preservación de Fondos",
        "retiro_sug": "Retiro mensual institucional sugerido:",
        "sin_amortizar": "sin amortizar el capital base.",
        "costo_oport": "Costo de Oportunidad por Capital Ocioso",
        "perdida_patr": "Pérdida patrimonial si el capital inicial se mantiene ocioso frente a la inflación:",
        "export_corp": "Exportación Corporativa de Datos",
        "btn_csv": "Descargar Reporte Ejecutivo (.CSV)",
        "info_premium": "Inicie el cálculo superior para habilitar el motor de análisis estocástico institucional.",
        "col_anio": "Año",
        "col_saldo": "Saldo Total ($)",
        "col_rend": "Rendimiento Real (%)"
    },
    "English": {
        "titulo": "Quantum Capital Suite",
        "subtitulo": "Analytical and industrial platform for asset projection and compound interest.",
        "p_control": "Investment Parameters",
        "p_desc": "Configure the input financial vectors manually:",
        "cap_init": "Initial Capital ($)",
        "ahorro": "Recurring Monthly Savings ($)",
        "horizonte": "Time Horizon (Years)",
        "tasa": "Expected Annual Return Rate (%)",
        "ejecutar": "Execute Financial Analysis",
        "licencia": "Environment License",
        "lic_inst": "Activate Institutional License",
        "lic_ok": "Premium Access Granted.",
        "lic_no": "Restricted Free License.",
        "v_macro": "Macroeconomic Variables",
        "inflacion": "Projected Inflation Rate (%)",
        "impuesto": "Tax Rate on Returns (%)",
        "volatilidad": "Asset Volatility / Deviation (%)",
        "res_analiticos": "Performance Metrics",
        "cap_neto": "Estimated Net Capital at Horizon Close",
        "retorno_bruto": "Compound Gross Return",
        "auditoria": "Purchasing Power Audit",
        "desglose_infla": "Annual breakdown indexed to an estimated inflation of",
        "proc_mat": "Standard Mathematical Procedure",
        "info_init": "Specify the numerical parameters in the left panel and press the execute button.",
        "mod_avanzados": "Advanced Analytical Modules (Institutional License)",
        "aviso_premium": "Stochastic models, volatility risk analysis, and Sharpe evaluation are reserved for the paid environment.",
        "btn_premium": "Acquire Institutional License for $19.99 USD",
        "sim_montecarlo": "Stochastic Market Simulation (Monte Carlo)",
        "desc_montecarlo": "Generation of 500 probabilistic trajectories with mathematical volatility:",
        "e_sharpe": "Efficiency Evaluation (Sharpe Ratio)",
        "sharpe_ok": "Optimal strategy relative to the risk assumed.",
        "sharpe_no": "Suboptimal risk-adjusted performance.",
        "gestion_preserv": "Fund Preservation Management",
        "retiro_sug": "Suggested institutional monthly withdrawal:",
        "sin_amortizar": "without amortizing the core capital.",
        "costo_oport": "Opportunity Cost of Idle Capital",
        "perdida_patr": "Wealth loss if initial capital remains idle against inflation:",
        "export_corp": "Corporate Data Export",
        "btn_csv": "Download Executive Report (.CSV)",
        "info_premium": "Start the calculation above to enable the institutional stochastic analysis engine.",
        "col_anio": "Year",
        "col_saldo": "Total Balance ($)",
        "col_rend": "Real Return (%)"
    }
}[idioma]

# --- INICIALIZACIÓN ESTABLE DEL ESTADO DE MEMORIA (SESSION STATE) ---
if "calculado" not in st.session_state:
    st.session_state.calculado = False
if "df_financiero" not in st.session_state:
    st.session_state.df_financiero = pd.DataFrame()
if "saldo_final_global" not in st.session_state:
    st.session_state.saldo_final_global = 0.0
if "total_invertido_global" not in st.session_state:
    st.session_state.total_invertido_global = 0.0
if "idioma_previo" not in st.session_state:
    st.session_state.idioma_previo = idioma

# Si el usuario cambia el idioma, recalculamos las columnas del DataFrame de memoria para evitar errores de visualización
if st.session_state.idioma_previo != idioma and not st.session_state.df_financiero.empty:
    st.session_state.idioma_previo = idioma
    # Forzamos una actualización de las etiquetas de las columnas basándonos en el nuevo idioma seleccionado
    columnas_antiguas = st.session_state.df_financiero.columns.tolist()
    nuevas_columnas = [t["col_anio"], t["col_saldo"], t["col_rend"]]
    st.session_state.df_financiero.columns = nuevas_columnas

# --- ENCABEZADO CORPORATIVO ---
st.title(t["titulo"])
st.write(t["subtitulo"])
st.divider()

# 2. CREACIÓN DE LA ESTRUCTURA DE DOS COLUMNAS
col1, col2 = st.columns([1, 1.2])

# --- CONTROL DE LICENCIA (UBICADO EN EL SIDEBAR) ---
with st.sidebar:
    st.header(t["licencia"])
    usuario_pago = st.toggle(t["lic_inst"])
    st.divider()
    
    if usuario_pago:
        st.success(t["lic_ok"])
        st.subheader(t["v_macro"])
        inflacion_premium = st.number_input(t["inflacion"], min_value=0.0, max_value=30.0, value=4.0, step=0.1)
        impuesto_premium = st.number_input(t["impuesto"], min_value=0, max_value=50, value=15, step=1)
        volatilidad_premium = st.number_input(t["volatilidad"], min_value=0, max_value=50, value=8, step=1)
    else:
        st.warning(t["lic_no"])
        inflacion_premium = 4.0  
        impuesto_premium = 0     
        volatilidad_premium = 0  

# --- COLUMNA 1: PANEL DE CONTROL DE ALTA GAMA (ENTRADAS MANUALES CON DEGRADADO CSS) ---
with col1:
    st.header(t["p_control"])
    st.write(t["p_desc"])
    
    capital_inicial = st.number_input(t["cap_init"], min_value=0, value=10000, step=500)
    ahorro_mensual = st.number_input(t["ahorro"], min_value=0, value=500, step=50)
    anios = st.number_input(t["horizonte"], min_value=1, max_value=50, value=20, step=1)
    tasa_interes = st.number_input(t["tasa"], min_value=0, max_value=50, value=12, step=1)
    
    st.write("") 
    calcular = st.button(t["ejecutar"], use_container_width=True)

