import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Calculador Balistico Avanzado", layout="wide")

st.title("Calculador de Trayectorias Balisticas con Doble Vista")
st.markdown("""
Sistema de calculo avanzado con resistencia aerodinamica y desviacion por viento. 
Al modificar los controles de la izquierda, las graficas se actualizaran de inmediato sin parpadear.
""")

# 2. SECCIÓN PRINCIPAL ENVOLVIENDO LOS CONTROLES Y GRÁFICAS EN UN FRAGMENTO (ELIMINA EL PARPADEO)
@st.fragment
def renderizar_simulador():
    # Creamos dos columnas: una estrecha para controles y una ancha para las gráficas
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
        st.markdown("**Condiciones Balisticas de Entorno**")
        v0 = st.slider("Velocidad Inicial del Proyectil (m/s)", min_value=100, max_value=1200, value=800, step=50)
        v_viento = st.slider("Velocidad del Viento Lateral (m/s)", min_value=-20, max_value=20, value=8, step=1, 
                             help="Valores positivos empujan a la derecha, valores negativos a la izquierda.")
        
        # Filtro visual solicitado: Mostrar/Ocultar trayectos de forma interactiva sin recargar
        st.markdown("---")
        st.markdown("**Capas Visuales de la Grafica**")
        visibilidad = st.pills(
            "Selecciona los elementos a desplegar en el mapa:",
            ["Mostrar Todo", "Ocultar Bala (Solo Apunte)", "Ocultar Apunte (Solo Bala)"],
            selection_mode="single",
            default="Mostrar Todo"
        )

    # 3. CONVERSIÓN DE UNIDADES Y MOTOR DE CÁLCULO FÍSICO
    distancia = distancia_m
    h_laser = altura_laser_cm / 100.0
    h_mira_absolute = (altura_laser_cm + altura_mira_cm) / 100.0
    radio_diana = (diametro_diana_cm / 2.0) / 100.0
    
    # Parámetros físicos fijos de la bala (Calibre estándar 7.62mm)
    m = 0.015       # Masa en kg (15 gramos)
    Cd = 0.3        # Coeficiente de arrastre aerodinámico
    A = 0.000045    # Área frontal en m²
    rho = 1.225     # Densidad del aire estándar kg/m³
    g = 9.81        # Gravedad de la Tierra

    # Ecuaciones diferenciales de balística real en 3D (Eje X=Distancia, Eje Y=Altura, Eje Z=Desviación Lateral)
    def modelo_balistico(t, variables):
        x, y, z, vx, vy, vz = variables
        v = np.sqrt(vx**2 + vy**2 + vz**2)
        factor_arrastre = 0.5 * rho * Cd * A / m
        
        ax = -factor_arrastre * v * vx
        ay = -g - (factor_arrastre * v * vy)
        az = factor_arrastre * (v_viento - vz) # El viento empuja el proyectil lateralmente
        return [vx, vy, vz, ax, ay, az]

    # Cálculo del ángulo de sitio inicial para que el proyectil salga apuntando hacia la diana
    # (El láser siempre viaja recto horizontal, la bala sigue la física parabólica)
    angulo_rad = np.arctan((h_mira_absolute - h_laser) / distancia)
    vx0 = v0 * np.cos(angulo_rad)
    vy0 = v0 * np.sin(angulo_rad)
    
    condiciones_iniciales = [0.0, h_laser, 0.0, vx0, vy0, 0.0]

    # Evento de parada cuando cruza la distancia de la diana
    def cruza_diana(t, variables):
        return distancia - variables
    cruza_diana.terminal = True

    # Resolver la trayectoria real en el espacio
    solucion = solve_ivp(modelo_balistico, t_span=(0, 5), y0=condiciones_iniciales, events=cruza_diana, max_step=0.01)
    
    x_vals = solucion.y
    y_vals = solucion.y # Alturas (Vista Lateral)
    z_vals = solucion.y # Desviaciones por viento (Vista Superior)

    # Determinar qué elementos se renderizan según la opción de los botones de visibilidad
    ver_bala = visibilidad in ["Mostrar Todo", "Ocultar Apunte (Solo Bala)"]
    ver_mira = visibilidad in ["Mostrar Todo", "Ocultar Bala (Solo Apunte)"]

    with col_graficas:
        # TABLA DE MÉTRICAS RÁPIDAS
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Caida de la Bala en Destino", f"{(y_vals[-1]*100):.2f} cm del suelo")
        with m2:
            st.metric("Desviacion por Viento Lateral", f"{(z_vals[-1]*100):.2f} cm")

        # -----------------------------------------------------------------
        # GRÁFICA 1: VISTA LATERAL (Distancia vs Altura)
        # -----------------------------------------------------------------
        st.subheader("Vista Lateral (Perfil de Elevacion)")
        fig_lateral = go.Figure()

        # Suelo
        fig_lateral.add_trace(go.Scatter(x=[0.0, distancia], y=[0.0, 0.0], mode='lines', name='Suelo', line=dict(color='green', width=2, dash='dash')))
        
        # Línea Láser / Apunte de la mira (Eje recto de referencia)
        if ver_mira:
            fig_lateral.add_trace(go.Scatter(x=[0.0, distancia], y=[h_mira_absolute, h_laser], mode='lines', name='Linea de la Mira', line=dict(color='blue', width=2, dash='dot')))
        
        # Trayectoria Real de la Bala cayendo por gravedad y aire
        if ver_bala:
            fig_lateral.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Trayectoria Proyectil', line=dict(color='red', width=3)))

        # Cuerpo Diana Lateral
        fig_lateral.add_trace(go.Scatter(x=[distancia, distancia], y=[h_laser - radio_diana, h_laser + radio_diana], mode='lines', name='Diana', line=dict(color='black', width=6)))

        fig_lateral.update_layout(hovermode="closest", height=320, dragmode="pan", margin=dict(t=10, b=10))
        fig_lateral.update_xaxes(title_text="Distancia Horizontal (Metros)", fixedrange=False)
        fig_lateral.update_yaxes(title_text="Altura (Metros)", fixedrange=True)

        st.plotly_chart(fig_lateral, use_container_width=True, config={"displayModeBar": False})

        # -----------------------------------------------------------------
        # GRÁFICA 2: VISTA DESDE ARRIBA (Distancia vs Desviación Z)
        # -----------------------------------------------------------------
        st.subheader("Vista Superior (Desviacion por Resistencia del Aire)")
        fig_superior = go.Figure()

        # Línea de Centro Cero (Trayectoria ideal sin viento)
        fig_superior.add_trace(go.Scatter(x=[0.0, distancia], y=[0.0, 0.0], mode='lines', name='Eje Central Objetivo', line=dict(color='gray', width=1.5, dash='dash')))

        # Trayectoria de desvío de la bala por empuje del aire
        if ver_bala:
            fig_superior.add_trace(go.Scatter(x=x_vals, y=z_vals, mode='lines', name='Desviacion de Bala', line=dict(color='crimson', width=3)))

        # Línea recta horizontal del Láser (Siempre apunta al centro de la diana a 180° rectos)
        if ver_mira:
            fig_superior.add_trace(go.Scatter(x=[0.0, distancia], y=[0.0, 0.0], mode='lines', name='Linea de Mira (Superior)', line=dict(color='blue', width=2, dash='dot')))

        # Diana vista desde arriba (Ancho representado de forma plana horizontal en destino)
        fig_superior.add_trace(go.Scatter(x=[distancia, distancia], y=[-radio_diana, radio_diana], mode='lines', name='Ancho Diana', line=dict(color='black', width=6)))
        
        # Punto exacto de impacto lateral
        if ver_bala:
            fig_superior.add_trace(go.Scatter(x=[distancia], y=[z_vals[-1]], mode='markers', marker=dict(size=12, color='gold', symbol='diamond'), name='Impacto Real'))

        fig_superior.update_layout(hovermode="closest", height=320, dragmode="pan", margin=dict(t=10, b=10))
        fig_superior.update_xaxes(title_text="Distancia Horizontal (Metros)", fixedrange=False)
        fig_superior.update_yaxes(title_text="Desviacion Izquierda / Derecha (Metros)", fixedrange=True)

        st.plotly_chart(fig_superior, use_container_width=True, config={"displayModeBar": False})

# Ejecutamos la función de fragmento protegida contra parpadeos
renderizar_simulador()
