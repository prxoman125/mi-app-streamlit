import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

st.set_page_config(page_title="Simulador de Colimación Óptica Avanzado", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #0e0f1d;
            border-right: 1px solid #23264d;
        }

        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #00d2ff !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-top: 15px !important;
            margin-bottom: 8px !important;
            border-bottom: 1px solid #1f2242;
            padding-bottom: 4px;
        }

        div.stButton > button {
            background: linear-gradient(135deg, #1f2242 0%, #2b2f5c 100%) !important;
            color: #00d2ff !important;
            border: 1px solid #00d2ff !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            background: #00d2ff !important;
            color: #0e0f1d !important;
            box-shadow: 0px 0px 10px rgba(0, 210, 255, 0.4);
        }

        div.btn-confirm-yes > div.stButton > button {
            background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%) !important;
            color: #52b788 !important;
            border: 1px solid #52b788 !important;
        }

        div.btn-confirm-cancel > div.stButton > button {
            background: linear-gradient(135deg, #4a0e17 0%, #780016 100%) !important;
            color: #ff4d6d !important;
            border: 1px solid #ff4d6d !important;
        }

        @keyframes glowBlue {
            0% { box-shadow: 0 0 35px 12px rgba(0, 210, 255, 0.85); border-color: #00d2ff; }
            100% { box-shadow: 0 0 0px 0px rgba(0, 210, 255, 0); border-color: transparent; }
        }

        .glow-box {
            animation: glowBlue 1s ease-out forwards;
            border-radius: 12px;
            border: 2px solid #00d2ff;
            padding: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# --- TRADUCCIONES E IDIOMA ---
TEXTS = {
    "ES": {
        "title": "Simulador Avanzado de Alineación y Colimación Óptica 3D",
        "profile_select": "Perfil de Aplicación / Profesión",
        "profile_placeholder": "-- Seleccione una Profesión / Carrera --",
        "unit_select": "Sistema de Unidades",
        "metric": "Métrico (cm, metros)",
        "imperial": "Imperial (pulgadas, yardas)",
        "params": "Parámetros de Entrada",
        "h_mira": "Línea de colimación vertical (Y)",
        "z_mira": "Offset horizontal inicial (Z)",
        "h_extra": "Desviación objetivo vertical (Y)",
        "z_extra": "Desviación objetivo horizontal (Z)",
        "dist_input": "Distancia al objetivo",
        "ref_angle_y": "Inclinación vertical ref. (°)",
        "ref_angle_z": "Inclinación horizontal ref. (°)",
        "divergence_input": "Divergencia del haz (mrad)",
        "waist_input": "Radio inicial del haz (mm)",
        "reset_btn": "Reiniciar Valores",
        "save_btn": "💾 Registrar Medición",
        "history_title": "Historial de Registros Guardados",
        "clear_history": "Borrar Historial",
        "confirm_clear_msg": "¿Deseas borrar todo el historial?",
        "confirm_yes": "✔ Sí, Borrar",
        "confirm_cancel": "✖ Cancelar",
        "empty_history": "No hay registros en el historial.",
        "select_prompt": "⚠️ Seleccione un perfil profesional para iniciar.",
        "record_saved": "✅ Medición registrada con éxito.",
        "graph_profile": "Perfil Lateral (Eje Y-X)",
        "graph_target": "Vista de Diana / Receptor (Eje Y-Z)",
    },
    "EN": {
        "title": "3D Advanced Optical Alignment & Collimation Simulator",
        "profile_select": "Application Profile / Profession",
        "profile_placeholder": "-- Select a Profession / Career --",
        "unit_select": "Unit System",
        "metric": "Metric (cm, meters)",
        "imperial": "Imperial (inches, yards)",
        "params": "Input Parameters",
        "h_mira": "Vertical Collimation Line (Y)",
        "z_mira": "Initial Horizontal Offset (Z)",
        "h_extra": "Vertical Target Offset (Y)",
        "z_extra": "Horizontal Target Offset (Z)",
        "dist_input": "Distance to Target",
        "ref_angle_y": "Ref Vertical Inclination (°)",
        "ref_angle_z": "Ref Horizontal Inclination (°)",
        "divergence_input": "Beam Divergence (mrad)",
        "waist_input": "Initial Beam Radius (mm)",
        "reset_btn": "Reset Values",
        "save_btn": "💾 Save Measurement",
        "history_title": "Saved Records History",
        "clear_history": "Clear History",
        "confirm_clear_msg": "Clear all history?",
        "confirm_yes": "✔ Yes, Clear",
        "confirm_cancel": "✖ Cancel",
        "empty_history": "No saved records yet.",
        "select_prompt": "⚠️ Select a profile to start.",
        "record_saved": "✅ Measurement saved successfully.",
        "graph_profile": "Side Profile (Y-X Axis)",
        "graph_target": "Target View (Y-Z Axis)",
    }
}

st.sidebar.header("Configuración / Settings")
lang = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
lang_code = "ES" if lang == "Español" else "EN"
txt = TEXTS[lang_code]

profiles_options = [txt["profile_placeholder"], "Industrial / Robótica", "Topografía / Ingeniería Civil", "Telecomunicaciones Satelitales", "Óptica Quirúrgica / Médica", "Defensa y Aeroespacial"]
profile = st.sidebar.selectbox(txt["profile_select"], profiles_options, index=0)

if "unit_choice" not in st.session_state:
    st.session_state["unit_choice"] = txt["metric"]

unit_sys = st.sidebar.radio(txt["unit_select"], [txt["metric"], txt["imperial"]], key="unit_choice")
is_metric = (unit_sys == txt["metric"])

# --- INICIALIZACIÓN DE VARIABLES EN SESSION STATE ---
for key in ["h_mira_val", "z_mira_val", "h_extra_val", "z_extra_val", "dist_val", "ref_angle_y_val", "ref_angle_z_val", "div_val", "waist_val"]:
    if key not in st.session_state:
        st.session_state[key] = 0.0 if "angle" not in key and "div" not in key and "waist" not in key else 1.0

if "history" not in st.session_state:
    st.session_state["history"] = []
if "confirm_clear" not in st.session_state:
    st.session_state["confirm_clear"] = False

def reset_inputs_to_zero():
    st.session_state["h_mira_val"] = 0.0
    st.session_state["z_mira_val"] = 0.0
    st.session_state["h_extra_val"] = 0.0
    st.session_state["z_extra_val"] = 0.0
    st.session_state["dist_val"] = 10.0
    st.session_state["ref_angle_y_val"] = 0.0
    st.session_state["ref_angle_z_val"] = 0.0

st.sidebar.header(txt["params"])
h_unit, d_unit = (txt["metric"].split()[1][1:3], "m") if is_metric else ("in", "yd")

H_mira = st.sidebar.number_input(f"{txt['h_mira']} ({h_unit})", value=st.session_state["h_mira_val"], key="h_mira_val")
Z_mira = st.sidebar.number_input(f"{txt['z_mira']} ({h_unit})", value=st.session_state["z_mira_val"], key="z_mira_val")
H_extra = st.sidebar.number_input(f"{txt['h_extra']} ({h_unit})", value=st.session_state["h_extra_val"], key="h_extra_val")
Z_extra = st.sidebar.number_input(f"{txt['z_extra']} ({h_unit})", value=st.session_state["z_extra_val"], key="z_extra_val")
D_val = st.sidebar.number_input(f"{txt['dist_input']} ({d_unit})", min_value=0.1, value=max(1.0, st.session_state["dist_val"]), key="dist_val")

st.sidebar.markdown("---")
ref_angle_y = st.sidebar.number_input(txt['ref_angle_y'], value=st.session_state["ref_angle_y_val"], format="%.2f", key="ref_angle_y_val")
ref_angle_z = st.sidebar.number_input(txt['ref_angle_z'], value=st.session_state["ref_angle_z_val"], format="%.2f", key="ref_angle_z_val")
divergence_mrad = st.sidebar.number_input(txt['divergence_input'], min_value=0.1, value=1.5, step=0.1, key="div_val")
waist_mm = st.sidebar.number_input(txt['waist_input'], min_value=0.1, value=2.0, step=0.1, key="waist_val")

save_clicked = st.sidebar.button(txt["save_btn"], use_container_width=True)
st.sidebar.button(txt["reset_btn"], on_click=reset_inputs_to_zero, use_container_width=True)

if profile == txt["profile_placeholder"]:
    st.warning(txt["select_prompt"])
    st.stop()

# --- CONVERSIÓN DE UNIDADES A CM ---
D_cm = D_val * 100 if is_metric else D_val * 91.44
H_mira_cm = H_mira if is_metric else H_mira * 2.54
Z_mira_cm = Z_mira if is_metric else Z_mira * 2.54
H_extra_cm = H_extra if is_metric else H_extra * 2.54
Z_extra_cm = Z_extra if is_metric else Z_extra * 2.54

# --- CÁLCULOS 3D Y DIVERGENCIA ---
rad_y, rad_z = math.radians(ref_angle_y), math.radians(ref_angle_z)
y_target = D_cm * math.tan(rad_y) + H_extra_cm
z_target = D_cm * math.tan(rad_z) + Z_extra_cm

diff_y_cm = y_target - H_mira_cm
diff_z_cm = z_target - Z_mira_cm

angle_y_deg = math.degrees(math.atan2(diff_y_cm, D_cm))
angle_z_deg = math.degrees(math.atan2(diff_z_cm, D_cm))
total_angular_dev_deg = math.sqrt(angle_y_deg**2 + angle_z_deg**2)

# Divergencia del haz Gaussiano: W(d) = W0 + d * tan(theta/2)
waist_cm = waist_mm / 10.0
beam_radius_cm = waist_cm + (D_cm * math.tan(math.radians(divergence_mrad / 1000.0 * 180 / math.pi)))

# --- VISUALIZACIÓN GRÁFICA (Doble Panel) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
fig.patch.set_facecolor('#0b0c1b')

# Gráfica 1: Perfil Lateral (X vs Y)
ax1.set_facecolor('#0b0c1b')
ax1.plot([0, D_cm], [0, y_target], '#ff4444', linestyle='--', label='Ref Laser')
ax1.plot([0, D_cm], [H_mira_cm, y_target], '#00d2ff', label='Sensor Axis')
ax1.scatter(D_cm, y_target, color='#33ff77', s=100, zorder=5, label='Target Point')
ax1.set_title(txt["graph_profile"], color='white')
ax1.grid(True, alpha=0.2, color='cyan')
ax1.tick_params(colors='white')
ax1.legend(facecolor='#12132c', labelcolor='white')

# Gráfica 2: Vista de Diana Frontal (Z vs Y)
ax2.set_facecolor('#0b0c1b')
circle_target = plt.Circle((0, 0), radius=beam_radius_cm*2, color='#ffcc00', fill=False, linestyle=':', label='Target Area')
circle_beam = plt.Circle((diff_z_cm, diff_y_cm), radius=beam_radius_cm, color='#00d2ff', alpha=0.4, label='Beam Spot')
ax2.add_patch(circle_target)
ax2.add_patch(circle_beam)
ax2.scatter(0, 0, color='#ff4444', marker='+', s=150, label='Center Ref')
ax2.scatter(diff_z_cm, diff_y_cm, color='#33ff77', marker='x', s=100, label='Beam Center')

limit = max(abs(diff_z_cm), abs(diff_y_cm), beam_radius_cm * 3, 5.0)
ax2.set_xlim(-limit, limit)
ax2.set_ylim(-limit, limit)
ax2.set_aspect('equal')
ax2.set_title(txt["graph_target"], color='white')
ax2.grid(True, alpha=0.2, color='cyan')
ax2.tick_params(colors='white')
ax2.legend(facecolor='#12132c', labelcolor='white', loc='upper right')

st.markdown('<div class="glow-box">', unsafe_allow_html=True)
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

# --- MÉTRICAS Y RESULTADOS ---
st.markdown(f"""
    <div style="display: flex; justify-content: space-around; background-color: #12132c; border: 1px solid #333566; padding: 15px; border-radius: 8px; margin-top: 15px;">
        <div style="text-align: center;">
            <span style="color: #a0a5c0; font-size: 11px;">AJUSTE VERTICAL (EJE Y)</span><br>
            <span style="color: #00d2ff; font-size: 16px; font-weight: bold;">{angle_y_deg:.4f}° ({angle_y_deg*60:.1f} MOA)</span>
        </div>
        <div style="text-align: center;">
            <span style="color: #a0a5c0; font-size: 11px;">AJUSTE HORIZONTAL (EJE Z)</span><br>
            <span style="color: #00d2ff; font-size: 16px; font-weight: bold;">{angle_z_deg:.4f}° ({angle_z_deg*60:.1f} MOA)</span>
        </div>
        <div style="text-align: center;">
            <span style="color: #a0a5c0; font-size: 11px;">DESVIACIÓN TOTAL COMBINADA</span><br>
            <span style="color: #33ff77; font-size: 16px; font-weight: bold;">{total_angular_dev_deg:.4f}°</span>
        </div>
        <div style="text-align: center;">
            <span style="color: #a0a5c0; font-size: 11px;">DIÁMETRO DEL SPOT EN DESTINO</span><br>
            <span style="color: #ff77ff; font-size: 16px; font-weight: bold;">{(beam_radius_cm*2):.2f} cm</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- HISTORIAL DE REGISTROS ---
if save_clicked:
    st.session_state["history"].append({
        "Perfil": profile,
        "Distancia": f"{D_val} {d_unit}",
        "Ángulo Y (Vertical)": f"{angle_y_deg:.4f}°",
        "Ángulo Z (Horizontal)": f"{angle_z_deg:.4f}°",
        "Diámetro Spot": f"{(beam_radius_cm*2):.2f} cm"
    })
    st.sidebar.success(txt["record_saved"])

st.markdown("---")
st.subheader(txt["history_title"])

if st.session_state["history"]:
    st.dataframe(pd.DataFrame(st.session_state["history"]), use_container_width=True)
else:
    st.info(txt["empty_history"])
