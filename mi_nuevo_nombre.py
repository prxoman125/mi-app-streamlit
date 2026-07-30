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

# --- INYECCIÓN DE CSS PARA DISEÑO INTEGRAL DE ALTA GAMA CON DEGRADADO REAL ---
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
        /* CORRECCIÓN: Fondo degradado azul marino/zafiro institucional puro para la columna de entrada */
        div[data-testid="column"] {
            background: linear-gradient(180deg, #0D1B3E 0%, #070F26 100%) !important;
            border: 1px solid #1E3A8A !important;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 229, 255, 0.05);
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

# --- REINGENIERÍA: FIJACIÓN ESTABLE DEL ESTADO DE MEMORIA (SESSION STATE) ---
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

# Normalización automática si se altera el idioma del sistema con datos en memoria
if st.session_state.idioma_previo != idioma and not st.session_state.df_financiero.empty:
    st.session_state.idioma_previo = idioma
    st.session_state.df_financiero.columns = [t["col_anio"], t["col_saldo"], t["col_rend"]]

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

# --- COLUMNA 1: PANEL DE CONTROL DE ALTA GAMA (CON LA CORRECCIÓN DEL HISTORIAL DEL BOTÓN) ---
with col1:
    st.header(t["p_control"])
    st.write(t["p_desc"])
    
    capital_inicial = st.number_input(t["cap_init"], min_value=0, value=10000, step=500)
    ahorro_mensual = st.number_input(t["ahorro"], min_value=0, value=500, step=50)
    anios = st.number_input(t["horizonte"], min_value=1, max_value=50, value=20, step=1)
    tasa_interes = st.number_input(t["tasa"], min_value=0, max_value=50, value=12, step=1)
    
    st.write("") 
    calcular = st.button(t["ejecutar"], use_container_width=True)

    # El botón ahora escribe datos fijos en la memoria de persistencia de Streamlit
    if calcular:
        tasa_decimal = tasa_interes / 100
        inflacion_decimal = inflacion_premium / 100
        
        datos_anios = []
        saldo_actual = capital_inicial
Usa el código con precaución.st.session_state.total_invertido_global = capital_inicial + (ahorro_mensual * 12 * anios)for anio in range(1, anios + 1):interes_ganado = saldo_actual * tasa_decimalsaldo_actual += interes_ganado + (ahorro_mensual * 12)rendimiento_real = tasa_interes - (inflacion_decimal * 100)datos_anios.append({t["col_anio"]: f"{t['col_anio']} {anio}",t["col_saldo"]: round(saldo_actual, 2),t["col_rend"]: round(rendimiento_real, 2)})st.session_state.df_financiero = pd.DataFrame(datos_anios)st.session_state.saldo_final_global = saldo_actualst.session_state.calculado = True--- COLUMNA 2: RESULTADOS ANALÍTICOS (LEIDOS DESDE EL ESTADO PERSISTENTE) ---with col2:st.header(t["res_analiticos"])if st.session_state.calculado:df_financiero = st.session_state.df_financierosaldo_final_global = st.session_state.saldo_final_globaltotal_invertido_global = st.session_state.total_invertido_globaltasa_decimal = tasa_interes / 100if usuario_pago and impuesto_premium > 0:ganancia_bruta = max(0.0, saldo_final_global - total_invertido_global)retencion_impuestos = ganancia_bruta * (impuesto_premium / 100)saldo_mostrar = saldo_final_global - retencion_impuestoselse:saldo_mostrar = saldo_final_globalst.metric(label=t["cap_neto"],value=f"${saldo_mostrar:,.2f}",delta=f"+{tasa_interes}% {t['retorno_bruto']}")st.subheader(t["auditoria"])st.write(f"{t['desglose_infla']} {inflacion_premium}%:")def color_semaforo(val):if val > 0:color = '#0D2B45'texto = '#00E5FF'else:color = '#3A151D'texto = '#FF6B6B'return f'background-color: {color}; color: {texto}; font-weight: bold;'columna_rendimiento = t["col_rend"]df_estilizado = df_financiero.style.map(color_semaforo, subset=[columna_rendimiento]) .format({t["col_saldo"]: "${:,.2f}", columna_rendimiento: "{:+.2f}%"})st.dataframe(df_estilizado, use_container_width=True, hide_index=True)st.subheader(t["proc_mat"])st.latex(rf"V_f = {capital_inicial} \times (1 + {tasa_decimal})^{{{anios}}} + \sum_{{t=1}}^{{{anios}}} ({ahorro_mensual} \times 12) \times (1 + {tasa_decimal})^t")else:st.info(t["info_init"])4. FILA INFERIOR DE ANCHO COMPLETO: PROTOCOLO INSTITUCIONALst.divider()st.header(t["mod_avanzados"])if not usuario_pago:st.info(t["aviso_premium"])st.button(t["btn_premium"], use_container_width=True)else:if st.session_state.calculado and not st.session_state.df_financiero.empty:p_col1, p_col2 = st.columns(2)with p_col1:st.subheader(t["sim_montecarlo"])st.write(t["desc_montecarlo"])simulaciones = 500resultados_finales = []rendimientos_simulados = np.random.normal(loc=tasa_interes / 100,scale=volatilidad_premium / 100,size=(simulaciones, anios))for sim in range(simulaciones):saldo_sim = capital_inicialfor anio in range(anios):r = rendimientos_simulados[sim, anio]saldo_sim = (saldo_sim * (1 + r)) + (ahorro_mensual * 12)resultados_finales.append(saldo_sim)df_simulaciones = pd.DataFrame({"Resultados": resultados_finales})fig_hist = px.histogram(df_simulaciones,x="Resultados",nbins=30,color_discrete_sequence=['#1E3A8A'])fig_hist.update_layout(height=250,margin=dict(l=10, r=10, t=10, b=10),plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#E2E8F0"),dragmode=False)st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})st.subheader(t["e_sharpe"])tasa_libre_riesgo = 0.04exceso_retorno = (tasa_interes / 100) - tasa_libre_riesgosharpe_ratio = exceso_retorno / (volatilidad_premium / 100) if volatilidad_premium > 0 else 0if sharpe_ratio >= 1:st.success(f"Sharpe Ratio: {sharpe_ratio:.2f} ({t['sharpe_ok']})")else:st.warning(f"Sharpe Ratio: {sharpe_ratio:.2f} ({t['sharpe_no']})")with p_col2:st.subheader(t["gestion_preserv"])retiro_anual_seguro = st.session_state.saldo_final_global * 0.04retiro_mensual_seguro = retiro_anual_seguro / 12st.info(f"{t['retiro_sug']} ${retiro_mensual_seguro:,.2f} {t['sin_amortizar']}")st.subheader(t["costo_oport"])capital_devaluado = capital_inicialfor _ in range(anios):capital_devaluado = capital_devaluado * (1 - (inflacion_premium/100))perdida_oportunidad = st.session_state.saldo_final_global - capital_devaluadost.error(f"{t['perdida_patr']} ${perdida_oportunidad:,.2f}")st.subheader(t["export_corp"])csv_data = st.session_state.df_financiero.to_csv(index=False).encode('utf-8')st.download_button(label=t["btn_csv"],data=csv_data,file_name="quantum_capital_report.csv",mime="text/csv",use_container_width=True)else:st.info(t["info_premium"])
