import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

# 1. Configuración de página con Estética Profesional
st.set_page_config(page_title="Professional IVP Dashboard", layout="wide")

# CSS para suavizar la interfaz de Streamlit
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    div[data-testid="stMetricValue"] { color: #38bdf8; }
    .stButton>button { 
        width: 100%; border-radius: 10px; background-color: #1e293b; 
        color: #38bdf8; border: 1px solid #38bdf833;
    }
    .stButton>button:hover { border-color: #38bdf8; color: #f8fafc; }
    </style>
    """, unsafe_allow_stdio=True)

# 2. Lógica de Negocio (EDO)
def model(t, y, k):
    return -k * y

# 3. Inicialización de estado
if "history" not in st.session_state:
    st.session_state.history = []

# 4. Arquitectura 1-2-1
col_adj, col_plot, col_data = st.columns([1, 2.2, 0.8], gap="large")

# --- COLUMNA IZQUIERDA: Ajustes Minimalistas ---
with col_adj:
    st.markdown("### ⚙️ Parámetros")
    k_val = st.select_slider("Constante K", options=np.round(np.arange(0.1, 2.1, 0.1), 1), value=0.5)
    y0_val = st.number_input("Valor Inicial (Y0)", 1, 100, 50)
    
    st.markdown("---")
    if st.button("📌 Guardar Snapshot"):
        st.session_state.history.append({"K": k_val, "Y0": y0_val})

# --- COLUMNA CENTRAL: Visualización Premium ---
with col_plot:
    sol = solve_ivp(model, [0, 10], [y0_val], args=(k_val,), t_eval=np.linspace(0, 10, 200))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sol.t, y=sol.y[0],
        mode='lines',
        line=dict(color='#38bdf8', width=4),
        fill='tozeroy',
        fillcolor='rgba(56, 189, 248, 0.1)',
        name='Simulación'
    ))

    # Ajustes estéticos para que la gráfica sea "cómoda"
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(showgrid=False, title="Tiempo (s)"),
        yaxis=dict(showgrid=True, gridcolor="#334155", title="Magnitud"),
        hovermode="x unified",
        dragmode=False # Evita mover la gráfica por accidente
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False})

# --- COLUMNA DERECHA: Historial Limpio ---
with col_data:
    st.markdown("### 🕒 Historial")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Simulación #{len(st.session_state.history)-i}"):
                st.write(f"**K:** {item['K']}")
                st.write(f"**Y0:** {item['Y0']}")
        if st.button("🗑️ Limpiar"):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("No hay registros guardados.")

¡Tu presentación y el código están listos! He optimizado la gráfica para que sea estéticamente placentera y la estructura de columnas para que se sienta espaciosa. ¿Te gustaría ajustar algún color o detalle específico?
