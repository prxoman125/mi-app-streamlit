import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Calculador Balistico Avanzado", layout="wide")

# Estilo CSS institucional de alta visibilidad (Fondos limpios, textos oscuros y acentos morados elegantes)
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    h1, h2, h3, p, label {
        color: #1A0D2E !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    div[data-testid="stSidebar"] {
        background-color: #F4F0FA;
        border-right: 2px solid #D1C4E9;
    }
    div[data-testid="stMetric"] {
        background-color: #FDFBFF;
        border-left: 5px solid #4A148C;
        padding: 10px 15px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] {
        color: #4A148C !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Calculador de Trayectorias Balisticas")
st.markdown("""
Sistema de analisis geometrico y balistico con resistencia aerodinamica. 
El software procesa los datos en tiempo real de forma dinamica y fluida sin parpadeos de pantalla.
""")

# 2. SECCIÓN PRINCIPAL ENVOLVIENDO LOS CONTROLES Y GRÁFICAS EN UN FRAGMENTO (ELIMINA EL PARPADEO)
@st.fragment
def renderizar_simulador():
    # CORRECCIÓN DEFINITIVA: Se especifican las proporciones exactas de las columnas (1 parte controles, 3 partes gráficas)
    col_controles, col_graficas = st.columns([1, 3])
    
    with col_controles:
        st.subheader("Parametros de Configuracion")
        
        # Parámetros de Distancia y Geometría
        distancia_m = st.slider("Distancia a la Diana (metros)", min_value=1.0, max_value=1000.0, value=300.0, step=5.0)
        altura_laser_cm = st.slider("Altura del Canon desde el suelo (cm)", min_value=25.0, max_value=50.0, value=25.0, step=0.5)
        altura_mira_cm = st.slider("Altura de la Mira sobre el Laser (cm)", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
        diametro_diana_cm = st.slider("Diametro de la Diana (cm)", min_value=20.0, max_value=30.0, value=20.0, step=1.0)
        
        # Parámetros del Proyectil y Clima (Física)
        st.markdown("---")
        st.markdown("**Condiciones de Entorno**")
        v0 = st.slider("Velocidad Inicial del Proyectil (m/s)", min_value=100, max_value=1200, value=800, step=50)
        v_viento = st.slider("Velocidad del Viento Lateral (m/s)", min_value=-20, max_value=20, value=8, step=1, 
                             help="Valores positivos empujan a la derecha, valores negativos a la izquierda.")
        
        # Filtro de visibilidad solicitado por el cliente (Uso de segmented_control para máxima compatibilidad)
        st.markdown("---")
        st.markdown("**Seleccion de Vista**")
        vista_seleccionada = st.segmented_control(
            "Elige el plano grafico a desplegar:",
            options=["Vista Lateral", "Vista Superior (Desde Arriba)"],
            default="Vista Lateral"
        )
        
        st.markdown("---")
        st.markdown("**Capas Visuales**")
        visibilidad = st.segmented_control(
            "Filtrar trazos en el mapa:",
            options=["Mostrar Todo", "Ocultar Bala", "Ocultar Apunte"],
            default="Mostrar Todo"
        )

    # 3. CONVERSIÓN DE UNIDADES A METROS
    distancia = distancia_m
    h_laser = altura_laser_cm / 100.0
    h_mira_absolute = (altura_laser_cm + altura_mira_cm) / 100.0
    radio_diana = (diametro_diana_cm / 2.0) / 100.0
    h_centro_diana = h_laser 

    # 4. CÁLCULO TRIGONOMÉTRICO DE INCLINACIÓN DE LA MIRA
    angulo_mira_rad = np.arctan((h_mira_absolute - h_centro_diana) / distancia)
    angulo_mira_deg = np.degrees(angulo_mira_rad)
    moa_mira = angulo_mira_deg * 60

    # 5. MOTOR DE CÁLCULO FÍSICO (Ecuaciones Diferenciales Balísticas)
    m = 0.015       
    Cd = 0.3        
    A = 0.000045    
    rho = 1.225     
    g = 9.81        

    def modelo_balistico(t, variables):
        x, y, z, vx, vy, vz = variables
        v = np.sqrt(vx**2 + vy**2 + vz**2)
        factor_arrastre = 0.5 * rho * Cd * A / m
        
        ax = -factor_arrastre * v * vx
        ay = -g - (factor_arrastre * v * vy)
        az = factor_arrastre * (v_viento - vz)
        return [vx, vy, vz, ax, ay, az]

    vx0 = v0 * np.cos(angulo_mira_rad)
    vy0 = v0 * np.sin(angulo_mira_rad)
    
    condiciones_iniciales = [0.0, h_laser, 0.0, vx0, vy0, 0.0]

    def cruza_diana(t, variables):
        return distancia - variables[0]
    cruza_diana.terminal = True

    solucion = solve_ivp(modelo_balistico, t_span=(0, 5), y0=condiciones_iniciales, events=cruza_diana, max_step=0.01)
    
    x_vals = solucion.y[0]
    y_vals = solucion.y[1] 
    z_vals = solucion.y[2] 

    ver_bala = visibilidad in ["Mostrar Todo", "Ocultar Apunte"]
    ver_mira = visibilidad in ["Mostrar Todo", "Ocultar Bala"]

    # PALETA DE COLORES PROFESIONALES DE ALTA VISIBILIDAD
    color_eje_referencia = "#E0E0E0"  
    color_mira_linea = "#424242"      
    color_bala_linea = "#9C27B0"      
    color_diana_solido = "#311B92"    

    with col_graficas:
        # INDICADORES TÉCNICOS INTEGRALES DE LA MIRA Y EL IMPACTO
        metric1, metric2, metric3 = st.columns(3)
        with metric1:
            st.metric("Inclinacion Necesaria de la Mira", f"{angulo_mira_deg:.4f}°", f"{moa_mira:.2f} MOA")
        with metric2:
            st.metric("Caida Real del Proyectil", f"{(y_vals[-1]*100):.2f} cm del suelo")
        with metric3:
            st.metric("Desviacion por Fuerza de Viento", f"{(z_vals[-1]*100):.2f} cm")

        # -----------------------------------------------------------------
        # RENDERIZADO DINÁMICO DE LAS GRÁFICAS SEGÚN LA VISTA SELECCIONADA
        # -----------------------------------------------------------------
        if vista_seleccionada == "Vista Superior (Desde Arriba)":
            st.subheader("Grafica Cenital: Desviacion por Resistencia del Aire")
            fig_superior = go.Figure()

            # Centro de la diana ideal sin viento
            fig_superior.add_trace(go.Scatter(x=[0.0, distancia], y=[0.0, 0.0], mode='lines', name='Eje Central Cero', line=dict(color=color_eje_referencia, width=1.5, dash='dash')))

            # Desviación de la bala por viento
            if ver_bala:
                fig_superior.add_trace(go.Scatter(x=x_vals, y=z_vals, mode='lines', name='Desviacion Proyectil', line=dict(color=color_bala_linea, width=3)))

            # Línea de la mira superior
            if ver_mira:
                fig_superior.add_trace(go.Scatter(x=[0.0, distancia], y=[0.0, 0.0], mode='lines', name='Linea de la Mira', line=dict(color=color_mira_linea, width=2, dash='dot')))

            # Ancho de la diana
            fig_superior.add_trace(go.Scatter(x=[distancia, distancia], y=[-radio_diana, radio_diana], mode='lines', name='Ancho Diana', line=dict(color=color_diana_solido, width=6)))
            
            # Punto final de impacto
            if ver_bala:
                fig_superior.add_trace(go.Scatter(x=[distancia], y=[z_vals[-1]], mode='markers', marker=dict(size=12, color=color_diana_solido, symbol='diamond'), name='Impacto Real'))

            fig_superior.update_layout(hovermode="closest", height=450, dragmode="pan", margin=dict(t=10, b=10))
            fig_superior.update_xaxes(title_text="Distancia Horizontal (Metros)", fixedrange=False)
            fig_superior.update_yaxes(title_text="Desviacion Izquierda / Derecha (Metros)", fixedrange=True)

            st.plotly_chart(fig_superior, use_container_width=True, config={"displayModeBar": False})

        else:
            # Por defecto o si selecciona Vista Lateral
            st.subheader("Grafica de Perfil: Elevacion y Caida")
            fig_lateral = go.Figure()

            # Suelo de referencia
            fig_lateral.add_trace(go.Scatter(x=[0.0, distancia], y=[0.0, 0.0], mode='lines', name='Suelo', line=dict(color=color_eje_referencia, width=2, dash='dash')))
            
            # Línea de la mira (Eje recto visual de apuntado)
            if ver_mira:
                fig_lateral.add_trace(go.Scatter(x=[0.0, distancia], y=[h_mira_absolute, h_centro_diana], mode='lines', name='Linea de la Mira', line=dict(color=color_mira_linea, width=2, dash='dot')))
            
            # Trayectoria de la bala
            if ver_bala:
                fig_lateral.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Trayectoria Proyectil', line=dict(color=color_bala_linea, width=3)))

            # Cuerpo Diana Vertical
            fig_lateral.add_trace(go.Scatter(x=[distancia, distancia], y=[h_centro_diana - radio_diana, h_centro_diana + radio_diana], mode='lines', name='Diana', line=dict(color=color_diana_solido, width=6)))

            fig_lateral.update_layout(hovermode="closest", height=450, dragmode="pan", margin=dict(t=10, b=10))
            fig_lateral.update_xaxes(title_text="Distancia Horizontal (Metros)", fixedrange=False)
            fig_lateral.update_yaxes(title_text="Altura (Metros)", fixedrange=True)

            st.plotly_chart(fig_lateral, use_container_width=True, config={"displayModeBar": False})

# Ejecutamos la aplicación integrada
renderizar_simulador()
