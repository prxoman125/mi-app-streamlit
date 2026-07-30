from taipy.gui import Gui
import numpy as np
import plotly.graph_objects as go

# 1. Variables iniciales que controlan la física
v0_fps = 2700       # Velocidad de la bala
viento_mph = 10     # Viento lateral
distancia_max = 800 # Distancia del disparo en metros

# 2. El motor matemático rápido
def calcular_trayectoria(v0_fps, viento_mph, dist_max):
    # Física básica de gravedad y resistencia al viento
    x = np.arange(0, dist_max + 10, 20)
    factor_caida = 3000 / v0_fps
    y = -((x / 50) ** 2) * factor_caida     # Caída vertical (cm)
    z = -((x / 100) ** 2) * (viento_mph / 5) # Desvío por viento (cm)
    return x, y, z

# 3. Función de actualización del gráfico
def generar_figura(v0_fps, viento_mph, dist_max):
    x, y, z = calcular_trayectoria(v0_fps, viento_mph, dist_max)
    
    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=z, z=y, 
        mode='lines', 
        line=dict(color='#FF4B4B', width=5)
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis_title="Distancia (m)", 
            yaxis_title="Viento (cm)", 
            zaxis_title="Caída (cm)"
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        template="plotly_dark"
    )
    return fig

# Generar la figura inicial
grafico_3d = generar_figura(v0_fps, viento_mph, distancia_max)

def actualizar(state):
    state.grafico_3d = generar_figura(state.v0_fps, state.viento_mph, state.distancia_max)

# 4. Diseño de la interfaz gráfica
pantalla = """
# 🎯 Simulador de Trayectoria 3D

<|layout|columns=1 2|
### 🛠️ Controles de Simulación
* **Velocidad (FPS):**
<|{v0_fps}|slider|min=1500|max=4000|on_change=actualizar|>

* **Viento Lateral (MPH):**
<|{viento_mph}|slider|min=0|max=30|on_change=actualizar|>

* **Distancia Máxima (Metros):**
<|{distancia_max}|slider|min=100|max=1500|step=100|on_change=actualizar|>

### 📊 Gráfico 3D Interactivo
<|{grafico_3d}|chart|>
|>
"""

if __name__ == "__main__":
    Gui(page=pantalla).run(dark_mode=True, notebook=-1, width="100%", height="600px")
