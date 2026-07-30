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
st.title("🚀 Simulador Visual de Retiro e Interés Compuesto")
st.write("Calcula tu ruta hacia la libertad financiera con un desglose de procedimiento paso a paso.")
st.divider()

# 2. CREACIÓN DE LA ESTRUCTURA DE DOS COLUMNAS
col1, col2 = st.columns([1, 1.2])

# --- COLUMNA 1: PANEL DE CONTROL (ENTRADAS DE DATOS) ---
with col1:
    st.header("🎛️ Panel de Control")
    st.write("Modifica tus variables financieras en tiempo real:")
    
    capital_inicial = st.number_input("Capital Inicial ($)", min_value=0, value=5000, step=500)
    ahorro_mensual = st.number_input("Ahorro Mensual ($)", min_value=0, value=300, step=50)
    anios = st.slider("Plazo de la Inversión (Años)", min_value=1, max_value=40, value=15)
    tasa_interes = st.slider("Tasa de Interés Anual Esperada (%)", min_value=1, max_value=25, value=10)
    
    st.write("") 
    calcular = st.button("🔮 Calcular Mi Ruta Financiera", use_container_width=True)

# Variables globales para compartir datos entre secciones
df_financiero = pd.DataFrame()
saldo_final_global = 0.0

# --- COLUMNA 2: RESULTADOS VISUALES (MAGIA DE DATOS) ---
with col2:
    st.header("🎯 Resultados Visuales")
    
    if calcular:
        tasa_decimal = tasa_interes / 100
        inflacion_estimada = 0.045 # 4.5% básica
        
        datos_anios = []
        saldo_actual = capital_inicial
        
        for anio in range(1, anios + 1):
            interes_ganado = saldo_actual * tasa_decimal
            saldo_actual += interes_ganado + (ahorro_mensual * 12)
            rendimiento_real = tasa_interes - (inflacion_estimada * 100)
            
            datos_anios.append({
                "Año": f"Año {anio}",
                "Saldo Total ($)": round(saldo_actual, 2),
                "Rendimiento Real (%)": round(rendimiento_real, 2)
            })
        
        df_financiero = pd.DataFrame(datos_anios)
        saldo_final_global = saldo_actual
        
        st.metric(
            label="Dinero Total Acumulado al Final del Plazo", 
            value=f"${saldo_actual:,.2f}", 
            delta=f"+{tasa_interes}% Rendimiento Anual Bruto"
        )
        
        st.subheader("🛡️ Diagnóstico de Poder Adquisitivo")
        st.write("Análisis del impacto de la inflación (4.5% promedio) en tus rendimientos:")

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
        
        st.subheader("📝 Procedimiento Matemático")
        st.latex(rf"V_f = {capital_inicial} \times (1 + {tasa_decimal})^{{{anios}}} + \sum_{{t=1}}^{{{anios}}} ({ahorro_mensual} \times 12) \times (1 + {tasa_decimal})^t")
        st.caption("Fórmula que integra el interés compuesto del capital inicial más las anualidades del ahorro mensual acumulado.")
        
    else:
        st.info("💡 Modifica los valores en el Panel de Control izquierdo y presiona el botón para calcular tu proyección.")

# 3. FILA INFERIOR DE ANCHO COMPLETO (SISTEMA DE MONETIZACIÓN PREMIUM)
st.divider()
st.header("👑 Zona Premium y Herramientas Avanzadas")

with st.expander("🔓 CONFIGURACIÓN PREMIUM: Impuestos, Inflación Dinámica y Exportación"):
    st.write("Simula cómo interactúa tu dinero con las leyes fiscales y la macroeconomía real.")
    
    # Interruptor de simulación de pago (Simula si el usuario ya pagó con Stripe)
    usuario_pago = st.toggle("Simular Licencia Premium Activada (Simulación de Pago con Stripe)")
    
    if not usuario_pago:
        st.warning("⚠️ Las herramientas de abajo están bloqueadas. Activa el interruptor de arriba para simular la compra del software.")
        st.button("💳 Adquirir Acceso Premium por $9.99 USD", use_container_width=True)
    else:
        st.success("✅ ¡Acceso Premium Concedido! Herramientas de grado profesional desbloqueadas.")
        
        # Grid premium de controles avanzados
        p_col1, p_col2 = st.columns(2)
        
        with p_col1:
            st.subheader("📊 Ajustes Macroeconómicos")
            inflacion_premium = st.slider("Ajustar Inflación del País (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.5)
            impuesto_premium = st.slider("Impuesto sobre Ganancias / ISR (%)", min_value=0, max_value=35, value=10)
        
        with p_col2:
            st.subheader("📥 Exportación Ejecutiva")
            st.write("Descarga los resultados en limpio para utilizarlos en Excel o reportes universitarios:")
            
            # Verificación de que existan datos calculados antes de descargar
            if not df_financiero.empty:
                # Conversión del DataFrame de Pandas a formato CSV en memoria
                csv_data = df_financiero.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Descargar Reporte de Datos (.CSV)",
                    data=csv_data,
                    file_name="reporte_libertad_financiera.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("Primero debes presionar 'Calcular Mi Ruta Financiera' arriba para generar el archivo.")

        # --- CÁLCULO DE IMPACTO FISCAL PREMIUM ---
        if not df_financiero.empty:
            st.subheader("📉 Impacto Fiscal Neto (Tu dinero real después de impuestos)")
            
            # Lógica matemática premium: calcular ganancia real y restarle el impuesto
            total_invertido = capital_inicial + (ahorro_mensual * 12 * anios)
            ganancia_bruta = max(0.0, saldo_final_global - total_invertido)
            retencion_impuestos =  ganancia_bruta * (impuesto_premium / 100)
            saldo_neto_real = saldo_final_global - retencion_impuestos
            
            st.error(f"⚠️ El gobierno retendrá **${retencion_impuestos:,.2f}** por concepto de impuestos sobre tus ganancias.")
            st.success(f"💰 Tu Capital Neto Real disponible para el retiro es de: **${saldo_neto_real:,.2f}**")
