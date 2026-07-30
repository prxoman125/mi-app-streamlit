import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Simulador Financiero Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TÍTULO DE LA APLICACIÓN ---
st.title("Simulador Visual de Retiro e Interés Compuesto")
st.write("Calcula tu ruta hacia la libertad financiera con un desglose de procedimiento paso a paso.")
st.divider()

# 2. CREACIÓN DE LA ESTRUCTURA DE DOS COLUMNAS
col1, col2 = st.columns([1, 1.2])

# Variables globales inicializadas para control de estado
df_financiero = pd.DataFrame()
saldo_final_global = 0.0
total_invertido_global = 0.0

# --- COLUMNA 1: PANEL DE CONTROL (ENTRADAS DE DATOS) ---
with col1:
    st.header("Panel de Control")
    st.write("Modifica tus variables financieras en tiempo real:")
    
    capital_inicial = st.number_input("Capital Inicial ($)", min_value=0, value=5000, step=500)
    ahorro_mensual = st.number_input("Ahorro Mensual ($)", min_value=0, value=300, step=50)
    anios = st.slider("Plazo de la Inversión (Años)", min_value=1, max_value=40, value=15)
    tasa_interes = st.slider("Tasa de Interés Anual Esperada (%)", min_value=1, max_value=25, value=10)
    
    st.write("") 
    calcular = st.button("Calcular Mi Ruta Financiera", use_container_width=True)

# 3. FILA INFERIOR (DECLARACIÓN DE CONTROLES PREMIUM PARA SU USO PREVIO)
with st.sidebar:
    st.header("Licencia del Software")
    usuario_pago = st.toggle("Activar Licencia Premium")
    
    if usuario_pago:
        st.success("Acceso Premium Concedido.")
        st.subheader("Ajustes Macroeconómicos")
        inflacion_premium = st.slider("Inflación Estimada (%)", min_value=0.0, max_value=15.0, value=4.5, step=0.5)
        impuesto_premium = st.slider("Impuesto sobre Ganancias (%)", min_value=0, max_value=35, value=10)
        volatilidad_premium = st.slider("Volatilidad del Mercado / Riesgo (%)", min_value=1, max_value=20, value=5)
    else:
        st.warning("Licencia Gratuita Activa.")
        inflacion_premium = 4.5  
        impuesto_premium = 0     
        volatilidad_premium = 0  

# --- COLUMNA 2: RESULTADOS VISUALES (MAGIA DE DATOS) ---
with col2:
    st.header("Resultados Visuales")
    
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
            label="Dinero Total Acumulado (Neto Estimado)", 
            value=f"${saldo_final_global:,.2f}", 
            delta=f"+{tasa_interes}% Rendimiento Anual Bruto"
        )
        
        st.subheader("Diagnóstico de Poder Adquisitivo")
        st.write(f"Análisis del impacto de la inflación ({inflacion_premium}% configurada) en tus rendimientos:")

        def color_semaforo(val):
            if val > 0:
                color = '#355749' 
                texto = '#32CD32' 
            else:
                color = '#4A1515'  
                texto = '#FF4500' 
            return f'background-color: {color}; color: {texto}; font-weight: bold;'

        df_estilizado = df_financiero.style.map(color_semaforo, subset=['Rendimiento Real (%)']) \
                                           .format({"Saldo Total ($)": "${:,.2f}", "Rendimiento Real (%)": "{:+.2f}%"})

        st.dataframe(df_estilizado, use_container_width=True, hide_index=True)
        
        st.subheader("Procedimiento Matemático Base")
        st.latex(rf"V_f = {capital_inicial} \times (1 + {tasa_decimal})^{{{anios}}} + \sum_{{t=1}}^{{{anios}}} ({ahorro_mensual} \times 12) \times (1 + {tasa_decimal})^t")
        
    else:
        st.info("Modifica los valores en el Panel de Control izquierdo y presiona el botón para calcular tu proyección.")

# 4. FILA INFERIOR DE ANCHO COMPLETO (HERRAMIENTAS AVANZADAS DESBLOQUEABLES)
st.divider()
st.header("Herramientas Avanzadas de Grado Profesional")

if not usuario_pago:
    st.info("Las funciones de simulación estocástica, análisis de riesgo institucional y exportación ejecutiva están reservadas para usuarios Premium.")
    st.button("Adquirir Acceso Premium por $9.99 USD", use_container_width=True)
else:
    if not df_financiero.empty:
        p_col1, p_col2 = st.columns(2)
        
        with p_col1:
            st.subheader("Simulación de Riesgo de Mercado (Montecarlo)")
            st.write("Análisis estocástico de 500 escenarios independientes:")
            
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
            
            fig_hist = px.histogram(
                df_simulaciones, 
                x="Resultados", 
                nbins=30,
                labels={"Resultados": "Capital Final Posible ($)"},
                color_discrete_sequence=['#355749']
            )
            
            # CONFIGURACIÓN PARA ELIMINAR EL ZOOM MOLESTO Y LA CRUZ
            fig_hist.update_layout(
                height=250, 
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor="rgba(0,0,0,0)",
                dragmode=False # Desactiva el arrastre para hacer zoom por completo
            )
            
            # Se renderiza el gráfico ocultando la barra flotante de herramientas de Plotly
            st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
            
        with p_col2:
            st.subheader("Sostenibilidad de Jubilación")
            st.write("Cálculo de la tasa de retiro seguro aplicando la regla institucional del 4% ajustada:")
            
            retiro_anual_seguro = saldo_final_global * 0.04
            retiro_mensual_seguro = retiro_anual_seguro / 12
            
            st.info(f"Basado en tu capital neto final, puedes retirar con seguridad un estimado de **${retiro_mensual_seguro:,.2f} al mes** durante tu jubilación sin extinguir el fondo.")
            
            st.subheader("Exportación de Datos Ejecutiva")
            csv_data = df_financiero.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descargar Reporte Completo de Datos (.CSV)",
                data=csv_data,
                file_name="reporte_avanzado_libertad_financiera.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.subheader("Desglose del Impacto Fiscal Real")
            ganancia_neta_calculada = max(0.0, (saldo_final_global + (total_invertido_global * (impuesto_premium/100) if impuesto_premium > 0 else 0)) - total_invertido_global)
            impuesto_cobrado = ganancia_neta_calculada * (impuesto_premium / 100)
            st.error(f"Retención fiscal por plusvalía de capital: ${impuesto_cobrado:,.2f}")
    else:
        st.info("Por favor, ejecuta un cálculo válido en el Panel de Control superior para activar las herramientas estocásticas premium.")
