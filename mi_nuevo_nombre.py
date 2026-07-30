import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración inicial de la página web
st.set_page_config(page_title="Simulador Financiero Pro", layout="wide")

st.title("🚀 Simulador Visual de Retiro e Interés Compuesto")
st.write("Calcula tu ruta hacia la libertad financiera con desglose de procedimiento.")

# --- CREACIÓN DE LAS DOS COLUMNAS ---
col1, col2 = st.columns([1, 1.2]) # La columna 2 es un poco más ancha para los visuales

with col1:
    st.header("🎛️ Panel de Control")
    st.write("Modifica tus variables financieras:")
    
    # Inputs del usuario
    capital_inicial = st.number_input("Capital Inicial ($)", min_value=0, value=1000, step=100)
    ahorro_mensual = st.number_input("Ahorro Mensual ($)", min_value=0, value=200, step=50)
    anios = st.slider("Años de inversión", min_value=1, max_value=40, value=20)
    tasa_interes = st.slider("Tasa de interés anual (%)", min_value=1, max_value=20, value=8)
    
    # Botón disparador del cálculo
    calcular = st.button("🔮 Calcular Mi Ruta Financiera", use_container_width=True)

with col2:
    st.header("🎯 Resultados Visuales")
    
    if calcular:
        # --- CÁLCULOS MATEMÁTICOS SIMPLES (Ejemplo base) ---
        tasa_decimal = tasa_interes / 100
        # Fórmula base de interés compuesto simulada para el año final
                # --- 1. CÁLCULO MATEMÁTICO AVANZADO CON PANDAS ---
        tasa_decimal = tasa_interes / 100
        inflacion_estimada = 0.045 # Supongamos un 4.5% de inflación promedio anual
        
        datos_anios = []
        saldo_actual = capital_inicial
        
        for anio in range(1, anios + 1):
            # El interés se aplica al saldo del año anterior
            interes_ganado = saldo_actual * tasa_decimal
            saldo_actual += interes_ganado + (ahorro_mensual * 12)
            
            # Cálculo del impacto de la inflación (Rendimiento Real)
            rendimiento_real = tasa_decimal - inflacion_estimada
            
            # Guardamos los datos de cada año
            datos_anios.append({
                "Año": f"Año {anio}",
                "Saldo Total ($)": round(saldo_actual, 2),
                "Rendimiento Real (%)": round(rendimiento_real * 100, 2)
            })
        
        # Convertimos la lista en un DataFrame de Pandas
        df_financiero = pd.DataFrame(datos_anios)
        
        # --- 2. MOSTRAR MÉTRICA PRINCIPAL ---
        st.metric(
            label="Dinero Total Acumulado", 
            value=f"${saldo_actual:,.2f}", 
            delta=f"+{tasa_interes}% Interés Anual"
        )
        
        # --- 3. CREACIÓN DEL MAPA DE CALOR CON PLOTLY ---
        st.subheader("🔥 Mapa de Calor: ¿Tu dinero está seguro?")
        st.write("Si el rendimiento es menor a la inflación, tu dinero pierde valor (Zona Roja).")
        
        # Creamos una matriz visual basada en el Rendimiento Real
        # Usamos una escala de color que va de Rojo (Peligro) a Verde (Ganancia)
        fig_heatmap = px.density_heatmap(
            df_financiero,
            x="Año",
            y=["Rendimiento Real (%)"],
            z="Rendimiento Real (%)",
            color_continuous_scale=["#FF4B4B", "#F0F2F6", "#00F5A0"], # Rojo -> Gris -> Verde brillante
            text_auto=True
        )
        
        # Ajustes visuales para que se adapte perfectamente a Streamlit
        fig_heatmap.update_layout(
            height=200, 
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False # Ocultamos la barra lateral de escala para limpiar la pantalla
        )
        
        # Renderizamos el mapa de calor interactivo de Plotly en Streamlit
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # --- 4. PROCEDIMIENTO MATEMÁTICO EN LATEX ---
        st.subheader("📝 Procedimiento Matemático")
        st.latex(rf"V_f = {capital_inicial} \times (1 + {tasa_decimal})^{{{anios}}} + \sum_{{t=1}}^{{{anios}}} \text{{Ahorro}} \times (1 + {tasa_decimal})^t")

        total_acumulado = capital_inicial * ((1 + tasa_decimal) ** anios)
        
        # 1. Métricas de Impacto Visual
        st.metric(label="Dinero Total Acumulado", value=f"${total_acumulado:,.2f}", delta=f"+{tasa_interes}% anual")
        
        # 2. Demostración del Procedimiento en LaTeX
        st.subheader("📝 Procedimiento Matemático")
        st.write("Sustitución de tus datos reales en la fórmula de interés compuesto:")
        st.latex(rf"V_f = {capital_inicial} \times (1 + {tasa_decimal})^{{{anios}}}")
        
    else:
        st.info("Configura tus datos a la izquierda y presiona el botón para ver la magia.")

# --- FILA INFERIOR DE ANCHO COMPLETO ---
st.divider() # Línea divisoria visual

st.header("👑 Zona Premium y Opciones Avanzadas")
with st.expander("🔓 Desbloquear Simulación de Impuestos e Inflación Real"):
    st.write("Esta opción te permite calcular cuánto dinero devorará la inflación de tu país año con año.")
    st.warning("Función Premium: Integra aquí tu pasarela de pago para monetizar tu app.")
