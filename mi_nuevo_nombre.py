import streamlit as st
import numpy as np
import math
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from scipy import stats
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sistema de Metrología y Colimación Óptica", layout="wide")

# --- BASE DE DATOS SQLITE ---
DB_NAME = "metrologia_avanzada.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mediciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            perfil TEXT,
            distancia REAL,
            h_emisor REAL,
            dy_target REAL,
            angulo REAL,
            mrad REAL,
            incertidumbre REAL,
            tolerancia REAL,
            estado TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_record(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO mediciones (fecha, perfil, distancia, h_emisor, dy_target, angulo, mrad, incertidumbre, tolerancia, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data['perfil'], data['dist'], data['h_e'], 
          data['dy'], data['ang'], data['mrad'], data['incert'], data['tol'], data['status']))
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM mediciones ORDER BY id DESC", conn)
    conn.close()
    return df

init_db()

# --- ESTILOS CSS (TEMÁTICA MONOCROMÁTICA INDUSTRIAL) ---
st.markdown("""
    <style>
        .stApp { background-color: #000000 !important; color: #e0e0e0 !important; }
        [data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 1px solid #262626 !important; }
        
        /* Estilos para las Pestañas (st.tabs) */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #000000; }
        .stTabs [data-baseweb="tab"] {
            background-color: #121212 !important;
            border: 1px solid #262626 !important;
            color: #888888 !important;
            border-radius: 6px 6px 0px 0px !important;
            padding: 10px 20px !important;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* Badge de Tolerancia */
        .status-badge {
            padding: 14px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            font-size: 15px;
            margin-bottom: 20px;
            border: 1px solid #333;
            letter-spacing: 0.5px;
        }

        div.stButton > button {
            background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%) !important;
            color: #ffffff !important;
            border: 1px solid #444444 !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover { 
            background: #ffffff !important; 
            color: #000000 !important; 
            border-color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- PANEL LATERAL (SIDEBAR) ---
st.sidebar.title("🛠️ Configuración Metrológica")

lang = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
is_es = lang == "Español"

# Nomenclaturas técnicas dinámicas
L_H_EMISOR = "Altura del Emisor (H_emisor)" if is_es else "Emitter Height (H_emitter)"
L_DY_TARGET = "Desplazamiento Objetivo (Δy_target)" if is_es else "Target Offset (Δy_target)"
L_DIST = "Distancia de Trabajo (D)" if is_es else "Working Distance (D)"
L_TOL = "Límite de Tolerancia (mrad)" if is_es else "Tolerance Limit (mrad)"

st.sidebar.header("📊 Geometría de Estación")
perfil = st.sidebar.selectbox("Perfil de Aplicación", ["Industrial", "Topografía", "Aeroespacial", "Investigación", "Robótica"])
dist_val = st.sidebar.number_input(f"{L_DIST} (m)", 0.0, 2000.0, 100.0, step=1.0, help="Distancia horizontal entre el emisor láser y el plano del objetivo.")
h_emisor = st.sidebar.number_input(f"{L_H_EMISOR} (cm)", -100.0, 100.0, 0.0, step=0.1, help="Altura inicial de origen de la línea de colimación.")
dy_target = st.sidebar.number_input(f"{L_DY_TARGET} (cm)", -100.0, 100.0, 0.0, step=0.1, help="Desviación o desplazamiento requerido sobre el objetivo.")
tol_limit = st.sidebar.slider(L_TOL, 0.0, 10.0, 1.5, step=0.1, help="Límite máximo de ajuste angular permitido en mrad.")

st.sidebar.header("🌡️ Condiciones Ambientales")
temp = st.sidebar.number_input("Temperatura (°C)", -20.0, 50.0, 20.0, help="Afecta el índice de refracción atmosférico.")
pres = st.sidebar.number_input("Presión (hPa)", 800.0, 1100.0, 1013.25, help="Presión atmosférica local.")
div_mrad = st.sidebar.number_input("Divergencia Haz (mrad)", 0.01, 5.0, 1.0, help="Apertura del haz para cálculo del diámetro de impacto.")

# --- CÁLCULOS TÉCNICOS Y FÍSICOS ---
D_cm = dist_val * 100.0
diferencia_altura_cm = dy_target - h_emisor

if D_cm > 0:
    angulo_rad = math.atan(diferencia_altura_cm / D_cm)
else:
    angulo_rad = 0.0

angulo_deg = math.degrees(angulo_rad)
mrad = angulo_rad * 1000.0
moa = angulo_deg * 60.0

# Incertidumbre Combinada (SciPy / Propagación de Errores)
sigma_h = 0.02  # Incertidumbre instrumental en altura (cm)
sigma_d = 0.5   # Incertidumbre en distancia (cm)
if D_cm > 0:
    sigma_angle_rad = math.sqrt((sigma_h / D_cm)**2 + (diferencia_altura_cm * sigma_d / (D_cm**2 + diferencia_altura_cm**2))**2)
    confianza_95_mrad = sigma_angle_rad * 1000.0 * stats.norm.ppf(0.975)
else:
    confianza_95_mrad = 0.0

# Tamaño del Spot
div_rad = div_mrad / 1000.0
spot_diameter_cm = 0.2 + (2.0 * dist_val * math.tan(div_rad / 2.0) * 100.0)

# Verificación de Tolerancia
is_within_tol = abs(mrad) <= tol_limit
status_text = "DENTRO DE TOLERANCIA" if is_within_tol else "FUERA DE TOLERANCIA / REQUIERE CALIBRACIÓN"
status_color = "#1f3a1f" if is_within_tol else "#3a1f1f"
text_color = "#a3dda3" if is_within_tol else "#dda3a3"

# --- ENCABEZADO Y BADGE DE TOLERANCIA ---
st.markdown(f"""
    <div style="background: #121212; padding: 18px 25px; border-radius: 10px; border: 1px solid #262626; margin-bottom: 15px;">
        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Optical Metrology System v2.0</h1>
        <p style="color: #888888; margin: 0; font-size: 13px;">Sistema de Monitoreo Óptico, Colimación y Análisis Metrológico</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="status-badge" style="background-color: {status_color}; color: {text_color}; border-color: {text_color};">
        STATUS: {status_text} | Error Actual: {abs(mrad):.3f} mrad | Límite Máximo: {tol_limit:.3f} mrad
    </div>
""", unsafe_allow_html=True)

# --- PESTAÑAS PRINCIPALES ---
tab_sim, tab_trend, tab_data = st.tabs(["📐 Simulación 3D/2D", "📈 Análisis de Tendencia", "🗄️ Registros & Base de Datos"])

# --- PESTAÑA 1: SIMULACIÓN ---
with tab_sim:
    col_graph, col_metrics = st.columns([1.8, 1.0])
    
    with col_graph:
        fig3d = go.Figure()

        # Eje de referencia cero
        fig3d.add_trace(go.Scatter3d(
            x=[0, D_cm], y=[0, 0], z=[0, 0],
            mode='lines', name="Eje de Referencia",
            line=dict(color='#FF0055', width=4, dash='dash')
        ))

        # Haz corregido
        fig3d.add_trace(go.Scatter3d(
            x=[0, D_cm], y=[0, 0], z=[h_emisor, dy_target],
            mode='lines+markers', name=f"Haz Ajustado (α = {angulo_deg:.4f}°)",
            line=dict(color='#00F0FF', width=7),
            marker=dict(size=4, color='#00F0FF')
        ))

        fig3d.update_layout(
            title=dict(text=f"<b>Visualización 3D del Haz</b> | Distancia: {dist_val:.1f} m", font=dict(color="#ffffff", size=13)),
            paper_bgcolor='#000000', plot_bgcolor='#000000',
            height=460, margin=dict(l=0, r=0, t=30, b=0),
            scene=dict(
                xaxis=dict(title='Distancia (cm)', backgroundcolor="#000000", gridcolor="#222222", tickfont=dict(color="#888888")),
                yaxis=dict(title='Lateral (cm)', backgroundcolor="#000000", gridcolor="#222222", tickfont=dict(color="#888888")),
                zaxis=dict(title='Elevación (cm)', backgroundcolor="#000000", gridcolor="#222222", tickfont=dict(color="#888888")),
                camera=dict(eye=dict(x=1.5, y=-1.3, z=0.6))
            ),
            legend=dict(orientation="h", y=0.01, font=dict(color="white", size=10), bgcolor="rgba(18, 18, 18, 0.8)")
        )
        st.plotly_chart(fig3d, use_container_width=True, key="grafica_3d_v2")

    with col_metrics:
        st.markdown("### 📋 Métricas de Colimación")
        st.metric("Ángulo de Corrección (α)", f"{angulo_deg:.4f}°")
        st.metric("Ajuste Angular (mrad / MOA)", f"{mrad:.3f} mrad | {moa:.2f} MOA")
        st.metric("Incertidumbre Combinada (u_c)", f"±{confianza_95_mrad:.3f} mrad (95% IC)")
        st.metric("Diámetro del Haz (Spot Ø)", f"{spot_diameter_cm:.2f} cm")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 REGISTRAR EN BASE DE DATOS", use_container_width=True):
            save_record({
                'perfil': perfil, 'dist': dist_val, 'h_e': h_emisor, 
                'dy': dy_target, 'ang': angulo_deg, 'mrad': mrad, 
                'incert': confianza_95_mrad, 'tol': tol_limit, 'status': status_text
            })
            st.success("✅ Registro guardado permanentemente en SQLite.")

# --- PESTAÑA 2: ANÁLISIS DE TENDENCIAS ---
with tab_trend:
    st.subheader("📈 Estabilidad Histórica del Haz")
    df_history = load_data()
    
    if not df_history.empty:
        fig_trend = go.Figure()
        
        # Línea de tendencia de error mrad
        fig_trend.add_trace(go.Scatter(
            x=df_history['fecha'], y=df_history['mrad'], 
            mode='lines+markers', name='Error Angular (mrad)',
            line=dict(color='#00F0FF', width=2),
            marker=dict(size=6, color='#ffffff')
        ))
        
        # Líneas de tolerancia
        fig_trend.add_hline(y=tol_limit, line_dash="dash", line_color="#ff4d6d", annotation_text="Límite Tol. (+)")
        fig_trend.add_hline(y=-tol_limit, line_dash="dash", line_color="#ff4d6d", annotation_text="Límite Tol. (-)")
        
        fig_trend.update_layout(
            title="Variación del Error Angular en las Últimas Mediciones",
            paper_bgcolor='#000000', plot_bgcolor='#000000',
            font=dict(color='#888888'),
            height=420,
            xaxis=dict(showgrid=False, title="Fecha / Hora"),
            yaxis=dict(showgrid=True, gridcolor='#222222', title="Ajuste (mrad)")
        )
        st.plotly_chart(fig_trend, use_container_width=True, key="grafica_tendencias")
    else:
        st.info("No hay datos suficientes guardados para generar gráficos de tendencia.")

# --- PESTAÑA 3: GESTIÓN DE DATOS ---
with tab_data:
    st.subheader("🗄️ Historial Metrológico Almacenado")
    df_display = load_data()
    
    if not df_display.empty:
        search = st.text_input("🔍 Filtrar historial por Perfil o Estado:")
        if search:
            df_display = df_display[
                df_display['perfil'].str.contains(search, case=False) | 
                df_display['estado'].str.contains(search, case=False)
            ]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        col_csv, col_del = st.columns(2)
        with col_csv:
            csv_data = df_display.to_csv(index=False).encode('utf-8')
            st.download_button("📥 DESCARGAR REGISTROS (CSV)", csv_data, "registros_metrologia.csv", "text/csv", use_container_width=True)
            
        with col_del:
            if st.button("🗑️ VACIAR BASE DE DATOS", use_container_width=True):
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("DELETE FROM mediciones")
                conn.commit()
                conn.close()
                st.rerun()
    else:
        st.info("La base de datos SQLite no contiene registros guardados.")
