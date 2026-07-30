import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera instrucción)
st.set_page_config(
    page_title="Simulador Financiero Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TÍTULO DE LA APLICACIÓN ---
st.title("🚀 Simulador Visual de Retiro e Interés Compuesto")
st.write("Calcula tu ruta hacia la libertad financiera con un desglose de procedimiento paso a paso.")
st.divider()

# 2. CREACIÓN DE LA ESTRUCTURA DE DOS COLUMNAS
col1, col2 = st.columns([1, 1.2])

# --- COLUMNA 1: PANEL DE CONTROL (ENTRADAS DE DATOS) ---
with col1:
    st.header("🎛️ Panel de Control")
    st.write("Modifica tus variables financieras en tiempo real:")
    
    # Inputs numéricos y sliders interactivos
    capital_inicial = st.number_input("Capital Inicial ($)", min_value=0, value=5000, step=500)
    ahorro_mensual = st.number_input("Ahorro Mensual ($)", min_value=0, value=300, step=50)
    anios = st.slider("Plazo de la Inversión (Años)", min_value=1, max_value=40, value=15)
    tasa_interes = st.slider("Tasa de Interés Anual Esperada (%)", min_value=1, max_value=25, value=10)
    
    st.write("") 
    calcular = st.button("🔮 Calcular Mi Ruta Financiera", use_container_width=True)

# --- COLUMNA 2: RESULTADOS VISUALES (MAGIA DE DATOS) ---
with col2:
    st.header("🎯 Resultados Visuales")
    
    if calcular:
        # --- CÁLCULOS MATEMÁTICOS CON PANDAS Y NUMPY ---
        tasa_decimal = tasa_interes / 100
        inflacion_estimada = 0.045 # Supongamos un 4.5% de inflación promedio anual fija
        
        datos_anios = []
        saldo_actual = capital_inicial
        
        for anio in range(1, anios + 1):
            interes_ganado = saldo_actual * tasa_decimal
            saldo_actual += interes_ganado + (ahorro_mensual * 12)
            
            # Cálculo del Rendimiento Real contra la inflación
            rendimiento_real = tasa_interes - (inflacion_estimada * 100)
            
            datos_anios.append({
                "Año": f"Año {anio}",
                "Saldo Total ($)": round(saldo_actual, 2),
                "Rendimiento Real (%)": round(rendimiento_real, 2)
            })
        
        df_financiero = pd.DataFrame(datos_anios)
        
        # --- EXHIBICIÓN DE MÉTRICAS CLAVE ---
        st.metric(
            label="Dinero Total Acumulado al Final del Plazo", 
            value=f"${saldo_actual:,.2f}", 
            delta=f"+{tasa_interes}% Rendimiento Anual Bruto"
        )
        
        # --- TABLA DE SEMÁFORO INTELIGENTE (COLORES SUAVES/MATE) ---
        st.subheader("🛡️ Diagnóstico de Poder Adquisitivo")
        st.write("Análisis del impacto de la inflación (4.5% promedio) en tus rendimientos:")

        # Función modificada con tonos opacos/pastel para evitar colores chillones
        def color_semaforo(val):
            if val > 0:
                color = '#E2F0D9'  # Verde menta/oliva muy suave (mate)
                texto = '#385723'  # Verde pino oscuro para el texto
            else:
                color = '#FCE4D6'  # Rojo salmón/arena muy suave (mate)
                texto = '#C65911'  # Café/óxido oscuro para el texto
            return f'background-color: {color}; color: {texto}; font-weight: bold;'

        # Aplicamos la función de estilo a la columna correspondiente
        df_estilizado = df_financiero.style.map(color_semaforo, subset=['Rendimiento Real (%)']) \
                                           .format({"Saldo Total ($)": "${:,.2f}", "Rendimiento Real (%)": "{:+.2f}%"})

        # Renderizamos la tabla con los nuevos colores ejecutivos
        st.dataframe(df_estilizado, use_container_width=True, hide_index=True)
        
        # --- PROCEDIMIENTO MATEMÁTICO DETALLADO EN LATEX ---
        st.subheader("📝 Procedimiento Matemático")
        st.write("Sustitución de tus variables reales dentro del modelo matemático financiero:")
        
        st.latex(rf"V_f = {capital_inicial} \times (1 + {tasa_decimal})^{{{anios}}} + \sum_{{t=1}}^{{{anios}}} ({ahorro_mensual} \times 12) \times (1 + {tasa_decimal})^t")
        st.caption("Fórmula que integra el interés compuesto del capital inicial más las anualidades del ahorro mensual acumulado.")
        
    else:
        st.info("💡 Modifica los valores en el Panel de Control izquierdo y presiona el botón para calcular tu proyección.")

# 3. FILA INFERIOR DE ANCHO COMPLETO (SISTEMA DE MONETIZACIÓN)
st.divider()
st.header("👑 Zona Premium y Herramientas Avanzadas")

with st.expander("🔓 Desbloquear Simulación de Impuestos y Reportes PDF"):
    st.write("Lleva tu estrategia financiera al siguiente nivel con cálculos avanzados adaptados a la ley fiscal de tu país.")
    st.button("💳 Adquirir Acceso Premium (Descargar Reporte Completo en PDF)", use_container_width=True)
    st.caption("Esta sección es ideal para integrar pasarelas de pago como Stripe para cobrar por los reportes desglosados.")
