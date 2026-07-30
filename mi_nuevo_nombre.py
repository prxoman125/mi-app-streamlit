import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Calculador Balístico 3D", layout="wide")

st.title("🚀 Calculador Balístico Pro y Simulador de Trayectorias 3D")
st.markdown("""
Esta aplicación resuelve las **ecuaciones diferenciales de movimiento con resistencia aerodinámica del aire y viento lateral**. 
¡Ideal para estudiar física avanzada, balística deportiva o programación de videojuegos!
""")

# 2. BARRA LATERAL - ENTRADA DE DATOS (INPUTS)
st.sidebar.header("🔧 Parámetros del Disparo")

# Datos del proyectil
v0 = st.sidebar.slider("Velocidad Inicial (m/s)", min_value=100, max_value=1200, value=800, step=50, 
                       help="Velocidad a la que sale la bala del cañón.")
angulo_deg = st.sidebar.slider("Ángulo de Elevación (grados)", min_value=0.0, max_value=85.0, value=15.0, step=0.5)

# Datos del entorno
v_viento = st.sidebar.slider("Viento Lateral (m/s)", min_value=-30, max_value=30, value=10, step=1,
                             help="Valores positivos empujan a la derecha, negativos a la izquierda.")

# Selector de gravedad (¡Para darle variedad técnica!)
entorno = st.sidebar.selectbox("Entorno / Gravedad", 
                               ["Tierra (9.81 m/s²)", "Marte (3.71 m/s²)", "Luna (1.62 m/s²)"])
if "Tierra" in entorno:
    g = 9.81
elif "Marte" in entorno:
    g = 3.71
else:
    g = 1.62

# Configuración avanzada de la bala (Física real)
st.sidebar.subheader("⚙️ Propiedades Aerodinámicas Avanzadas")
peso_gramos = st.sidebar.number_input("Masa de la bala (Gramos)", min_value=1.0, max_value=500.0, value=15.0)
m = peso_gramos / 1000.0 # Convertir a kg para las fórmulas
Cd = st.sidebar.slider("Coeficiente de Arrastre (Cd)", min_value=0.1, max_value=0.9, value=0.3, step=0.05,
                       help="Qué tan aerodinámica es la bala. Menor número significa más aerodinámica.")
diametro_mm = st.sidebar.slider("Calibre / Diámetro (mm)", min_value=4.0, max_value=20.0, value=7.62, step=0.1)
radio_m = (diametro_mm / 2.0) / 1000.0
A = np.pi * (radio_m ** 2) # Área frontal
rho = 1.225 # Densidad del aire estándar en kg/m³

# 3. EL MOTOR MATEMÁTICO (CÁLCULOS DIFÍCILES)
# Ecuaciones diferenciales de movimiento en 3D
def modelo_balistico(t, variables, m, Cd, A, rho, g, v_viento):
    x, y, z, vx, vy, vz = variables
    
    # Velocidad total actual de la bala
    v = np.sqrt(vx**2 + vy**2 + vz**2)
    
    # Fuerza de resistencia del aire (Frenado)
    factor_arrastre = 0.5 * rho * Cd * A / m
    
    # Aceleraciones en cada eje
    ax = -factor_arrastre * v * vx
    ay = -g - (factor_arrastre * v * vy)
    az = factor_arrastre * (v_viento - vz) # El viento empuja lateralmente
    
    return [vx, vy, vz, ax, ay, az]

# Condiciones iniciales del disparo
angulo_rad = np.radians(angulo_deg)
vx0 = v0 * np.cos(angulo_rad)
vy0 = v0 * np.sin(angulo_rad)
vz0 = 0.0 # Sale alineada en el eje Z

condiciones_iniciales = [0.0, 0.0, 0.0, vx0, vy0, vz0] # [x, y, z, vx, vy, vz]

# Evento para detener la simulación cuando la bala toque el suelo (y = 0)
def bala_toca_suelo(t, variables, *args):
    return variables[1] # Monitorea la variable 'y' (altura)
bala_toca_suelo.terminal = True
bala_toca_suelo.direction = -1

# Resolver numéricamente las ecuaciones paso a paso en el tiempo (máximo 200 segundos)
solucion = solve_ivp(
    modelo_balistico, 
    t_span=(0, 200), 
    y0=condiciones_iniciales, 
    args=(m, Cd, A, rho, g, v_viento),
    events=bala_toca_suelo,
    max_step=0.01 # Precisión milimétrica
)

# Extraer los datos de la trayectoria calculada
x_vals = solucion.y[0]
y_vals = solucion.y[1]
z_vals = solucion.y[2]
tiempos = solucion.t

# Asegurarse de que el último punto sea exactamente el suelo
if y_vals[-1] < 0:
    y_vals[-1] = 0

# 4. MOSTRAR RESULTADOS PRINCIPALES (MÉTRICAS)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🎯 Alcance Máximo (Destino)", value=f"{x_vals[-1]:.2f} metros")
with col2:
    st.metric(label="🌪️ Desviación Lateral (Eje Z)", value=f"{z_vals[-1]:.2f} metros")
with col3:
    st.metric(label="⏱️ Tiempo de Vuelo Total", value=f"{tiempos[-1]:.2f} segundos")

# 5. RENDERIZAR GRÁFICO INTERACTIVO 3D
st.subheader("📊 Visualización de la Trayectoria en 3D")

fig = go.Figure()

# Línea de la trayectoria de la bala
fig.add_trace(go.Scatter3d(
    x=x_vals, y=z_vals, z=y_vals, # Plotly usa Z para la altura por defecto, por eso invertimos los ejes visualmente
    mode='lines',
    line=dict(color='red', width=4),
    name='Trayectoria de la Bala'
))

# Punto de impacto en el destino
fig.add_trace(go.Scatter3d(
    x=[x_vals[-1]], y=[z_vals[-1]], z=[y_vals[-1]],
    mode='markers',
    marker=dict(size=6, color='black', symbol='diamond'),
    name='Punto de Impacto'
))

# Configuración del diseño del gráfico (Ejes, títulos, rotación)
fig.update_layout(
    scene=dict(
        xaxis_title='Distancia (Metros)',
        yaxis_title='Desviación Viento (Metros)',
        zaxis_title='Altura (Metros)',
        aspectmode='data' # Mantiene la proporción física real de los ejes
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    height=600,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

st.plotly_chart(fig, use_container_width=True)

# 6. EXPLICACIÓN CIENTÍFICA / APRENDIZAJE
st.info("""
💡 **¿Qué hace difícil a este cálculo?** Si el aire no existiera, la bala viajaría en una parábola perfecta simétrica. 
Sin embargo, debido al **arrastre aerodinámico ($Cd$)**, la bala pierde velocidad rápidamente a medida que avanza. 
Notarás en el gráfico que la curva de caída al final de la trayectoria es mucho más inclinada que al inicio.
""")
