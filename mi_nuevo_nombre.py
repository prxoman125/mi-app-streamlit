import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Terminal Financiera de Alta Gama", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INYECCIÓN DE CSS PARA DISEÑO PREMIUM DE ALTA GAMA ---
# Estiliza el fondo de la app, fuentes tipográficas y limpia los bordes de los contenedores
st.markdown("""
    <style>
        /* Estilo para el fondo general y fuentes */
        .stApp {
            background-color: #0A1128;
            color: #E2E8F0;
        }
        /* Estilizado de títulos y headers */
        h1, h2, h3 {
            color: #00E5FF !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
        }
        /* Refinamiento de los bloques de métricas */
        div[data-testid="stMetric"] {
            background-color: #101F42;
            border: 1px solid #1E3A8A;
            border-radius: 8px;
            padding: 15px;
        }
        /* Estilos personalizados para los expanders */
        .conda-env {
            border: 1px solid #1E3A8A !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO CORPORATIVO ---
st.title("Quantum Capital Suite")
st.write("Plataforma analítica e industrial para la proyección de activos e interés compuesto.")
st.divider()

# 2. CREACIÓN DE LA ESTRUCTURA DE DOS COLUMNAS
col1, col2 = st.columns([1, 1.2])

# Variables globales inicializadas para control de estado
df_financiero = pd.DataFrame()
saldo_final_global = 0.0
total_invertido_global = 0.0

# --- COLUMNA 1: PANEL DE CONTROL DE ALTA GAMA ---
with col1:
    st.header("Parámetros de Inversión")
    st.write("Configure los vectores financieros de entrada:")
    
    capital_inicial = st.number_input("Capital Inicial ($)", min_value=0, value=10000, step=1000)
    ahorro_mensual = st.number_input("Ahorro Mensual Recurrente ($)", min_value=0, value=500, step=100)
    anios = st.slider("Horizonte Temporal (Años)", min_value=1, max_value=40, value=20)
    tasa_interes = st.slider("Tasa de Retorno Anual Esperada (%)", min_value=1, max_value=25, value=12)
    
    st.write("") 
    calcular = st.button("Ejecutar Análisis Financiero", use_container_width=True)

# 3. CONTROL DE LICENCIA Y PARÁMETROS MACROECONÓMICOS (SIDEBAR AZUL)
with st.sidebar:
    st.header("Licencia y Entorno")
    usuario_pago = st.toggle("Activar Licencia Institucional")
    st.divider()
    
    if usuario_pago:
        st.success("Acceso Premium Concedido.")
        st.subheader("Variables Macroeconómicas")
        inflacion_premium = st.slider("Tasa de Inflación Proyectada (%)", min_value=0.0, max_value=15.0, value=4.0, step=0.5)
        impuesto_premium = st.slider("Tasa Impositiva sobre Rendimientos (%)", min_value=0, max_value=35, value=15)
        volatilidad_premium = st.slider("Volatilidad de Activos / Desviación (%)", min_value=1, max_value=25, value=8)
    else:
        st.warning("Licencia Gratuita Restringida.")
        inflacion_premium = 4.0  
        impuesto_premium = 0     
        volatilidad_premium = 0  

# --- COLUMNA 2: RESULTADOS ANALÍTICOS ---
with col2:
    st.header("Métricas de Rendimiento")
    
    if calcular:
        tasa_decimal = tasa_interes / 100
        inflacion_decimal = inflacion_premium / 100
        
        datos_anios = []
        saldo_actual = capital_inicial
        total_invertido_global = capital_inicial + (ahorro_mensual * 12 * anios)
        
        for anio in range(1, anios + 1):
            interes_ganado = saldo_actual * tasa_decimal
            saldo_actual += interes_ganado + (ahorro_mensual * 12)
            rendimiento_real = tasa_interes - (inflacion_decimal * 100)
            
            datos_anios.append({
                "Año": f"Año {anio}",
                "Saldo Total ($)": round(saldo_actual, 2),
                "Rendimiento Real (%)": round(rendimiento_real, 2)
            })
        
        df_financiero = pd.DataFrame(datos_anios)
        saldo_final_global = saldo_actual
        
        if usuario_pago and impuesto_premium > 0:
            ganancia_bruta = max(0.0, saldo_final_global - total_invertido_global)
            retencion_impuestos = ganancia_bruta * (impuesto_premium / 100)
            saldo_final_global -= retencion_impuestos
            
        st.metric(
            label="Capital Neto Estimado al Cierre del Horizonte", 
            value=f"${saldo_final_global:,.2f}", 
            delta=f"+{tasa_interes}% Retorno Bruto Compuesto"
        )
        
        st.subheader("Auditoría de Poder Adquisitivo")
        st.write(f"Desglose anual indexado a una inflación estimada del {inflacion_premium}%:")

        # Ajuste de color del semáforo a una gama azul-marino oscura sofisticada para Dark Mode
        def color_semaforo(val):
            if val > 0:
                color = '#0D2B45' # Azul marino oscuro de alta gama
                texto = '#00E5FF' # Cyan neón para texto legible
            else:
                color = '#3A151D' # Rojo vino apagado institucional
                texto = '#FF6B6B' # Coral suave para alertas
            return f'background-color: {color}; color: {texto}; font-weight: bold;'

        df_estilizado = df_financiero.style.map(color_semaforo, subset=['Rendimiento Real (%)']) \
                                           .format({"Saldo Total ($)": "${:,.2f}", "Rendimiento Real (%)": "{:+.2f}%"})

        st.dataframe(df_estilizado, use_container_width=True, hide_index=True)
        
        st.subheader("Procedimiento Matemático Estándar")
        st.latex(rf"V_f = {capital_inicial} \times (1 + {tasa_decimal})^{{{anios}}} + \sum_{{t=1}}^{{{anios}}} ({ahorro_mensual} \times 12) \times (1 + {tasa_decimal})^t")
        
    else:
        st.info("Especifique los parámetros numéricos en el panel izquierdo y presione el botón de ejecución.")

# 4. FILA INFERIOR DE ANCHO COMPLETO: PROTOCOLO INSTITUCIONAL
st.divider()
st.header("Módulos Analíticos Avanzados (Licencia Institucional)")

if not usuario_pago:
    st.info("Los modelos estocásticos, análisis de riesgo de volatilidad y la evaluación Sharpe están reservados para el entorno de pago.")
    st.button("Adquirir Licencia Institucional por $19.99 USD", use_container_width=True)
else:
    if not df_financiero.empty:
        p_col1, p_col2 = st.columns(2)
        
        with p_col1:
            st.subheader("Simulación Estocástica de Mercado (Montecarlo)")
            st.write("Generación de 500 trayectorias probabilísticas con volatilidad matemática:")
            
            simulaciones = 500
            resultados_finales = []
            
            rendimientos_simulados = np.random.normal(
                loc=tasa_interes / 100, 
                scale=volatilidad_premium / 100, 
                size=(simulaciones, anios)
            )
            
            for sim in range(simulaciones):
                saldo_sim = capital_inicial
                for anio in range(anios):
                    r = rendimientos_simulados[sim, anio]
                    saldo_sim = (saldo_sim * (1 + r)) + (ahorro_mensual * 12)
                resultados_finales.append(saldo_sim)
                
            df_simulaciones = pd.DataFrame({"Resultados": resultados_finales})
            
            # Gráfico con escala cromática azul profundo institucional
            fig_hist = px.histogram(
                df_simulaciones, 
                x="Resultados", 
                nbins=30,
                labels={"Resultados": "Capital de Destino Posible ($)"},
                color_discrete_sequence=['#1E3A8A'] # Azul Cobalto Corporativo
            )
            
            fig_hist.update_layout(
                height=250, 
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E2E8F0"),
                dragmode=False
            )
            st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
            
            # --- NUEVA FUNCIÓN PREMIUM 1: ÍNDICE DE SHARPE ---
            st.subheader("Evaluación de Eficiencia (Índice de Sharpe)")
            tasa_libre_riesgo = 0.04 # 4% retorno base asegurado (ej. bonos de gobierno)
            exceso_retorno = (tasa_interes / 100) - tasa_libre_riesgo
            sharpe_ratio = exceso_retorno / (volatilidad_premium / 100) if volatilidad_premium > 0 else 0
            
            if sharpe_ratio >= 1:
                st.success(f"Ratio de Sharpe: {sharpe_ratio:.2f} (Estrategia óptima respecto al riesgo asumido).")
            else:
                st.warning(f"Ratio de Sharpe: {sharpe_ratio:.2f} (Rendimiento ajustado al riesgo subóptimo).")
            
        with p_col2:
            st.subheader("Gestión de Preservación de Fondos")
            
            # Regla institucional del 4%
            retiro_anual_seguro = saldo_final_global * 0.04
            retiro_mensual_seguro = retiro_anual_seguro / 12
            st.info(f"Retiro mensual institucional sugerido: ${retiro_mensual_seguro:,.2f} sin amortizar el capital base.")
            
            # --- NUEVA FUNCIÓN PREMIUM 2: COSTO DE OPORTUNIDAD ---
            st.subheader("Costo de Oportunidad por Capital Ocioso")
            # Calcula cuánto valdría el dinero invertido vs guardado debajo del colchón perdiendo 4% anual
            capital_devaluado = capital_inicial
            for _ in range(anios):
                capital_devaluado = capital_devaluado * (1 - (inflacion_premium/100))
                
            perdida_oportunidad = saldo_final_global - capital_devaluado
            st.error(f"Pérdida patrimonial si el capital inicial se mantiene ocioso frente a la inflación: ${perdida_oportunidad:,.2f}")
            
            st.subheader("Exportación Corporativa de Datos")
            csv_data = df_financiero.to_csv(index=False).encode('utf-8')
