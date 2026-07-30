import streamlit as st
import numpy as np
import math
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Simulador de Colimación Óptica", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
        /* Fondo y contenedor de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: #0e0f1d;
            border-right: 1px solid #23264d;
        }

        /* Estilo para los títulos de la barra lateral */
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

        /* Rediseño de botones generales */
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

        /* Estilo para los botones + y - de los number_input (Azul claro) */
        button[aria-label="Increase value"], 
        button[aria-label="Decrease value"],
        div[data-baseweb="spinbutton"] button,
        [data-testid="stNumberInputStepDown"],
        [data-testid="stNumberInputStepUp"] {
            color: #00d2ff !important;
            background-color: #161836 !important;
            border-color: #00d2ff !important;
            transition: all 0.2s ease !important;
        }

        button[aria-label="Increase value"]:hover, 
        button[aria-label="Decrease value"]:hover,
        div[data-baseweb="spinbutton"] button:hover,
        [data-testid="stNumberInputStepDown"]:hover,
        [data-testid="stNumberInputStepUp"]:hover {
            background-color: #00d2ff !important;
            color: #0e0f1d !important;
            box-shadow: 0px 0px 8px rgba(0, 210, 255, 0.7) !important;
        }

        /* Botón Verde (Confirmar Borrado) */
        div.btn-confirm-yes > div.stButton > button {
            background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%) !important;
            color: #52b788 !important;
            border: 1px solid #52b788 !important;
        }
        div.btn-confirm-yes > div.stButton > button:hover {
            background: #52b788 !important;
            color: #081c15 !important;
            box-shadow: 0px 0px 10px rgba(82, 183, 136, 0.6);
        }

        /* Botón Rojo (Cancelar Borrado) */
        div.btn-confirm-cancel > div.stButton > button {
            background: linear-gradient(135deg, #4a0e17 0%, #780016 100%) !important;
            color: #ff4d6d !important;
            border: 1px solid #ff4d6d !important;
        }
        div.btn-confirm-cancel > div.stButton > button:hover {
            background: #ff4d6d !important;
            color: #2b0008 !important;
            box-shadow: 0px 0px 10px rgba(255, 77, 109, 0.6);
        }
    </style>
""", unsafe_allow_html=True)

# --- DICCIONARIOS DE TRADUCCIÓN E IDIOMA ---
TEXTS = {
    "ES": {
        "title": "Simulador de Alineación y Colimación Óptica Avanzado",
        "lang_select": "Idioma / Language",
        "unit_select": "Sistema de Unidades / Unit System",
        "metric": "Métrico (cm, metros)",
        "imperial": "Imperial (pulgadas, yardas)",
        "profile_select": "Perfil de Aplicación / Profesión",
        "profile_placeholder": "-- Seleccione una Profesión / Carrera --",
        "p1": "Calibración de brazos robóticos (Rango muy corto)",
        "p2": "Alineación de maquinaria industrial (Rango corto)",
        "p3": "Topografía y construcción civil (Rango medio)",
        "p4": "Alineación de colectores solares / Helióstatos (Rango medio-largo)",
        "p5": "Guiado láser de robótica móvil (Rango largo)",
        "p6": "Guiado de maquinaria de tunelación (Rango largo-extremo)",
        "p7": "Alineación de Puentes Colgantes (Rango Largo)",
        "p8": "Nivelación de Vías de Tren de Alta Velocidad (Rango Medio)",
        "p9": "Montacargas Autónomos en Almacenes 3D (Rango Corto)",
        "p10": "Clasificación de Paquetes por Bandas (Rango Muy Corto)",
        "p11": "Alineación de Antenas Satelitales (Rango Extremo)",
        "p12": "Calibración de Sensores de Aterrizaje (Rango Medio)",
        "p13": "Alineación de Hélices en Torres Eólicas (Rango Corto)",
        "p14": "Inspección Óptica de Cascos de Barcos (Rango Medio)",
        "p15": "Guiado de Perforadoras en Minería (Rango Largo)",
        "p16": "Colimación de Telescopios Astronómicos (Rango Extremo)",
        "p17": "Alineación de Espejos Láser Quirúrgicos (Rango Muy Corto)",
        "p18": "Guiado Optoelectrónico de Misiles Defensivos (Rango Extremo)",
        "p19": "Calibración de Sensores LiDAR Automotrices (Rango Medio)",
        "p20": "Centrado de Turbinas Hidroeléctricas (Rango Corto)",
        "p21": "Inspección de Deformación en Turbinas de Gas (Rango Corto)",
        "p22": "Nivelación de Plataformas Petroleras Offshore (Rango Medio-Largo)",
        "p23": "Alineación de Escáneres LiDAR en Drones (Rango Medio)",
        "p24": "Colimación de Sistemas Ópticos Micro litográficos (Rango Muy Corto)",
        "p25": "Control de Flexión en Estructuras de Estadios (Rango Medio)",

        "params": "Parámetros Geométricos",
        "phys_params": "Óptica & Entorno Físico",
        "reset_btn": "Reiniciar Valores a 0",
        "save_btn": "💾 Registrar Medición",
        "h_mira": "Línea de colimación",
        "h_extra": "Desviación del punto de impacto / Objetivo",
        "dist_input": "Distancia al receptor / Destino",
        "ref_angle_input": "Inclinación eje referencia (°)",
        "laser_div": "Divergencia Láser (mrad)",
        "temp_input": "Temperatura (°C)",
        "press_input": "Presión Atm. (hPa)",
        "earth_curv": "Activar Curvatura Terrestre",
        "cm": "cm",
        "m": "m",
        "in": "pulgadas",
        "yd": "yardas",
        "laser_label": "Eje óptico de referencia",
        "sight_label": "Eje del sensor ajustable",
        "target_center": "Centro del Objetivo",
        "target_point": "Punto Requerido",
        "title_graph": "Distancia",
        "req_angle": "Ángulo Requerido (α)",
        "diff_height": "Diferencia Altura Total",
        "sight_angle": "Ángulo de Inclinación (α)",
        "angular_adj": "Ajuste Angular",
        "direction": "Dirección",
        "direction_up": "Arriba",
        "direction_down": "Abajo",
        "resolution": "Resolución Mecánica",
        "spot_size_lbl": "Diámetro de Haz (Spot)",
        "curv_drop_lbl": "Caída x Curvatura",
        "history_title": "Historial de Registros Guardados",
        "clear_history": "Borrar Historial",
        "confirm_clear_msg": "¿Estás seguro de que deseas borrar todo el historial?",
        "confirm_yes": "✔ Sí, Borrar",
        "confirm_cancel": "✖ Cancelar",
        "empty_history": "No hay registros guardados en el historial.",
        "select_prompt": "⚠️ Por favor, seleccione un Perfil de Aplicación / Profesión en la barra lateral para iniciar la simulación.",
        "record_saved": "✅ Medición registrada en el historial.",
        "target_2d_title": "🎯 Vista Frontal 2D (Retícula / Diana)"
    },
    "EN": {
        "title": "Advanced Optical Alignment & Collimation Simulator",
        "lang_select": "Language / Idioma",
        "unit_select": "Unit System / Sistema de Unidades",
        "metric": "Metric (cm, meters)",
        "imperial": "Imperial (inches, yards)",
        "profile_select": "Application Profile / Profession",
        "profile_placeholder": "-- Select a Profession / Career --",
        "p1": "Robotic Arm Calibration (Very Short Range)",
        "p2": "Industrial Machinery Alignment (Short Range)",
        "p3": "Surveying & Civil Construction (Medium Range)",
        "p4": "Solar Collector / Heliostat Alignment (Medium-Long Range)",
        "p5": "Mobile Robotics Laser Guidance (Long Range)",
        "p6": "Tunneling Machinery Guidance (Long-Extreme Range)",
        "p7": "Suspension Bridge Alignment (Long Range)",
        "p8": "High-Speed Train Track Leveling (Medium Range)",
        "p9": "Autonomous Forklifts in 3D Warehouses (Short Range)",
        "p10": "Belt Package Sorting Systems (Very Short Range)",
        "p11": "Satellite Dish Alignment (Extreme Range)",
        "p12": "Aircraft Landing Sensor Calibration (Medium Range)",
        "p13": "Wind Turbine Blade Alignment (Short Range)",
        "p14": "Ship Hull Optical Inspection (Medium Range)",
        "p15": "Open-Pit Mining Drill Guidance (Long Range)",
        "p16": "Astronomical Telescope Collimation (Extreme Range)",
        "p17": "Surgical Laser Mirror Alignment (Very Short Range)",
        "p18": "Defensive Missile Optoelectronic Guidance (Extreme Range)",
        "p19": "Automotive LiDAR Sensor Calibration (Medium Range)",
        "p20": "Hydroelectric Turbine Centering (Short Range)",
        "p21": "Gas Turbine Strain Inspection (Short Range)",
        "p22": "Offshore Oil Rig Platform Leveling (Medium-Long Range)",
        "p23": "Drone LiDAR Scanner Alignment (Medium Range)",
        "p24": "Microlithographic Optical System Collimation (Very Short Range)",
        "p25": "Stadium Roof Deflection Monitoring (Medium Range)",

        "params": "Geometric Parameters",
        "phys_params": "Optics & Physical Environment",
        "reset_btn": "Reset Values to 0",
        "save_btn": "💾 Save Measurement",
        "h_mira": "Collimation Line",
        "h_extra": "Impact Point Deviation / Target Offset",
        "dist_input": "Distance to Receiver / Destination",
        "ref_angle_input": "Ref. Axis Inclination (°)",
        "laser_div": "Laser Divergence (mrad)",
        "temp_input": "Temperature (°C)",
        "press_input": "Atm. Pressure (hPa)",
        "earth_curv": "Enable Earth Curvature",
        "cm": "cm",
        "m": "m",
        "in": "inches",
        "yd": "yards",
        "laser_label": "Reference Optical Axis",
        "sight_label": "Adjustable Sensor Axis",
        "target_center": "Target Center",
        "target_point": "Required Point",
        "title_graph": "Distance",
        "req_angle": "Required Angle (α)",
        "diff_height": "Total Height Diff.",
        "sight_angle": "Inclination Angle (α)",
        "angular_adj": "Angular Adjustment",
        "direction": "Direction",
        "direction_up": "Up",
        "direction_down": "Down",
        "resolution": "Mechanical Resolution",
        "spot_size_lbl": "Beam Diameter (Spot)",
        "curv_drop_lbl": "Curvature Drop",
        "history_title": "Saved Records History",
        "clear_history": "Clear History",
        "confirm_clear_msg": "Are you sure you want to clear the entire history?",
        "confirm_yes": "✔ Yes, Clear",
        "confirm_cancel": "✖ Cancel",
        "empty_history": "No records saved in history yet.",
        "select_prompt": "⚠️ Please select an Application Profile / Profession in the sidebar to start the simulation.",
        "record_saved": "✅ Measurement saved into history.",
        "target_2d_title": "🎯 2D Front View (Reticle / Target)"
    }
}

# --- SELECCIÓN DE IDIOMA ---
st.sidebar.header("Configuración / Settings")
lang = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
lang_code = "ES" if lang == "Español" else "EN"
txt = TEXTS[lang_code]

# --- MENÚ DESPLEGABLE DE PROFESIONES / CARRERAS ---
st.sidebar.header(txt["profile_select"])
profiles_options = [txt["profile_placeholder"]] + [
    txt["p1"], txt["p2"], txt["p3"], txt["p4"], txt["p5"], txt["p6"],
    txt["p7"], txt["p8"], txt["p9"], txt["p10"], txt["p11"], txt["p12"],
    txt["p13"], txt["p14"], txt["p15"], txt["p16"], txt["p17"], txt["p18"],
    txt["p19"], txt["p20"], txt["p21"], txt["p22"], txt["p23"], txt["p24"], txt["p25"]
]

profile = st.sidebar.selectbox(txt["profile_select"], profiles_options, index=0)

# --- BASE DE DATOS DE PARÁMETROS REALISTAS ---
PROFILE_PRESETS = {
    txt["p1"]:  (True,  1.2,   0.15,  1.5,   0.05, 0.5),
    txt["p2"]:  (True,  2.5,   0.50,  6.0,   0.20, 0.8),
    txt["p3"]:  (False, 4.0,   1.50,  120.0, 1.20, 1.2),
    txt["p4"]:  (True,  12.0,  4.50,  350.0, 2.80, 1.5),
    txt["p5"]:  (True,  8.0,  -2.10,  650.0, -1.50, 1.0),
    txt["p6"]:  (True,  25.0, -8.00,  1200.0, 3.50, 2.0),
    txt["p7"]:  (False, 10.0,  3.20,  850.0, 2.10, 1.4),
    txt["p8"]:  (True,  4.5,   0.80,  180.0, 0.45, 1.0),
    txt["p9"]:  (True,  3.0,   1.20,  18.0,  2.50, 0.6),
    txt["p10"]: (True,  0.5,   0.05,  2.5,   0.10, 0.3),
    txt["p11"]: (True,  35.0,  12.00, 1500.0, 8.50, 0.8),
    txt["p12"]: (False, 5.0,  -1.80,  320.0, -2.10, 1.2),
    txt["p13"]: (True,  5.0,  -1.20,  12.0,  -0.80, 0.9),
    txt["p14"]: (True,  15.0,  2.80,  75.0,  0.90, 1.1),
    txt["p15"]: (False, 6.0,  -2.50,  1100.0,-4.20, 2.5),
    txt["p16"]: (True,  45.0,  15.00, 2000.0, 12.00, 0.2),
    txt["p17"]: (True,  0.2,   0.04,  0.8,   0.05, 0.1),
    txt["p18"]: (True,  50.0, -10.00, 1800.0,-14.00, 0.5),
    txt["p19"]: (True,  6.5,   1.10,  80.0,  1.50, 1.8),
    txt["p20"]: (True,  1.8,  -0.30,  12.0,  -0.40, 0.4),
    txt["p21"]: (True,  0.9,   0.12,  4.5,   0.25, 0.5),
    txt["p22"]: (False, 14.0,  4.50,  650.0, 3.80, 1.3),
    txt["p23"]: (True,  2.8,  -0.50,  45.0,  -1.20, 1.5),
    txt["p24"]: (True,  0.1,   0.01,  0.3,   0.02, 0.05),
    txt["p25"]: (True,  20.0,  4.20,  220.0, 2.90, 1.0),
}

# --- DETECTAR CAMBIO DE PROFESIÓN Y CARGAR CONFIGURACIÓN ---
if "current_profile" not in st.session_state:
    st.session_state["current_profile"] = profile

if profile != st.session_state["current_profile"]:
    st.session_state["current_profile"] = profile
    if profile in PROFILE_PRESETS:
        pref_metric, h_m, h_e, dist, angle, div_mrad = PROFILE_PRESETS[profile]
        st.session_state["unit_choice"] = txt["metric"] if pref_metric else txt["imperial"]
        st.session_state["h_mira_val"] = h_m
        st.session_state["h_extra_val"] = h_e
        st.session_state["dist_val"] = dist
        st.session_state["ref_angle_val"] = angle
        st.session_state["laser_div_val"] = div_mrad
    else:
        st.session_state["h_mira_val"] = 0.0
        st.session_state["h_extra_val"] = 0.0
        st.session_state["dist_val"] = 0.0
        st.session_state["ref_angle_val"] = 0.0
        st.session_state["laser_div_val"] = 1.0

# --- SELECCIÓN DE UNIDADES DE MEDIDA ---
if "unit_choice" not in st.session_state:
    st.session_state["unit_choice"] = txt["metric"]

unit_sys = st.sidebar.radio(txt["unit_select"], [txt["metric"], txt["imperial"]], key="unit_choice")
is_metric = (unit_sys == txt["metric"])

# --- INICIALIZACIÓN DE SESSION STATE ---
if "h_mira_val" not in st.session_state:
    st.session_state["h_mira_val"] = 0.0
if "h_extra_val" not in st.session_state:
    st.session_state["h_extra_val"] = 0.0
if "dist_val" not in st.session_state:
    st.session_state["dist_val"] = 0.0
if "ref_angle_val" not in st.session_state:
    st.session_state["ref_angle_val"] = 0.0
if "laser_div_val" not in st.session_state:
    st.session_state["laser_div_val"] = 1.0
if "temp_val" not in st.session_state:
    st.session_state["temp_val"] = 20.0
if "press_val" not in st.session_state:
    st.session_state["press_val"] = 1013.25
if "earth_curv_val" not in st.session_state:
    st.session_state["earth_curv_val"] = False

if "history" not in st.session_state:
    st.session_state["history"] = []
if "confirm_clear" not in st.session_state:
    st.session_state["confirm_clear"] = False

def reset_inputs_to_zero():
    st.session_state["h_mira_val"] = 0.0
    st.session_state["h_extra_val"] = 0.0
    st.session_state["dist_val"] = 0.0
    st.session_state["ref_angle_val"] = 0.0
    st.session_state["laser_div_val"] = 1.0

st.sidebar.header(txt["params"])

# --- CONTROLES DE ENTRADA GEOMÉTRICOS ---
if is_metric:
    h_unit, d_unit = txt["cm"], txt["m"]
else:
    h_unit, d_unit = txt["in"], txt["yd"]

H_mira = st.sidebar.number_input(f"{txt['h_mira']} ({h_unit})", min_value=-500.0, max_value=500.0, value=st.session_state["h_mira_val"], step=0.1, key="h_mira_val")
H_extra = st.sidebar.number_input(f"{txt['h_extra']} ({h_unit})", min_value=-500.0, max_value=500.0, value=st.session_state["h_extra_val"], step=0.1, key="h_extra_val")
D_val = st.sidebar.number_input(f"{txt['dist_input']} ({d_unit})", min_value=0.0, max_value=2000.0, value=st.session_state["dist_val"], step=1.0, key="dist_val")
ref_angle_deg = st.sidebar.number_input(txt['ref_angle_input'], min_value=-30.00, max_value=30.00, value=st.session_state["ref_angle_val"], step=0.10, format="%.2f", key="ref_angle_val")

# --- CONTROLES DE FÍSICA Y ÓPTICA EN SIDEBAR ---
st.sidebar.header(txt["phys_params"])
laser_div_mrad = st.sidebar.number_input(txt["laser_div"], min_value=0.01, max_value=10.0, value=st.session_state["laser_div_val"], step=0.1, key="laser_div_val")
temp_c = st.sidebar.number_input(txt["temp_input"], min_value=-40.0, max_value=60.0, value=st.session_state["temp_val"], step=1.0, key="temp_val")
press_hpa = st.sidebar.number_input(txt["press_input"], min_value=500.0, max_value=1100.0, value=st.session_state["press_val"], step=10.0, key="press_val")
use_earth_curv = st.sidebar.checkbox(txt["earth_curv"], value=st.session_state["earth_curv_val"], key="earth_curv_val")

save_clicked = st.sidebar.button(txt["save_btn"], use_container_width=True)
st.sidebar.button(txt["reset_btn"], on_click=reset_inputs_to_zero, use_container_width=True)

# Conversión interna a cm y metros
if is_metric:
    D_m = D_val
    D_cm, H_mira_cm, H_extra_cm = D_val * 100, H_mira, H_extra
else:
    D_m = D_val * 0.9144
    D_cm, H_mira_cm, H_extra_cm = D_val * 91.44, H_mira * 2.54, H_extra * 2.54

# --- ENCABEZADO PRINCIPAL ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #12132c 0%, #1d1e3d 100%);
                padding: 10px 25px;
                border-radius: 10px;
                border-left: 5px solid #00d2ff;
                margin-bottom: 20px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.3);">
        <h2 style="color: white; margin: 0; font-size: 24px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; letter-spacing: 1px;">
            {txt['title']}
        </h2>
        <p style="color: #a0a5c0; margin: 0; font-size: 13px; opacity: 0.85;">
            Alineación de precisión óptica & Física Atmosférica | Perfil Activo: <b>{profile if profile != txt['profile_placeholder'] else 'Ninguno'}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

if profile == txt["profile_placeholder"]:
    st.warning(txt["select_prompt"])
    st.stop()

# --- CÁLCULOS DE FÍSICA Y ÓPTICA APLICADA ---
# 1. Curvatura terrestre (caída aparente Dh_curv en cm)
R_earth_m = 6371000.0
k_refraction = 0.14  # Coeficiente estándar de refracción atmosférica
if use_earth_curv and D_m > 0:
    R_eff = R_earth_m / (1 - k_refraction)
    curv_drop_cm = ((D_m ** 2) / (2 * R_eff)) * 100
else:
    curv_drop_cm = 0.0

# 2. Corrección por densidad del aire (Refracción por T y P)
n_air = 1 + (77.6e-6 * press_hpa / (temp_c + 273.15))
refraction_factor = (n_air - 1.00027) * 10.0  # Desviación micro-angular

# 3. Tamaño del Spot Láser (Diámetro en cm)
div_rad = laser_div_mrad / 1000.0
spot_diameter_cm = 0.2 + (2.0 * D_m * math.tan(div_rad / 2.0) * 100.0)
spot_radius_cm = spot_diameter_cm / 2.0

# 4. Trigonometría de alineación principal
ref_angle_rad = math.radians(ref_angle_deg)
y_ref_end = D_cm * math.tan(ref_angle_rad)
y_target_point = y_ref_end + H_extra_cm - curv_drop_cm
diferencia_altura_cm = y_target_point - H_mira_cm

if D_cm > 0:
    angulo_rad = math.atan(diferencia_altura_cm / D_cm)
else:
    angulo_rad = 0.0

angulo_deg = math.degrees(angulo_rad)
moa, mrad = angulo_deg * 60, angulo_rad * 1000
diff_height_display = diferencia_altura_cm if is_metric else diferencia_altura_cm / 2.54
spot_size_display = spot_diameter_cm if is_metric else spot_diameter_cm / 2.54
curv_drop_display = curv_drop_cm if is_metric else curv_drop_cm / 2.54

is_up = (angulo_deg >= 0)
direccion_str = txt["direction_up"] if is_up else txt["direction_down"]

clicks_moa = abs(round(moa * 4))
pulsos_mrad = abs(round(mrad * 10))

# --- REGISTRO MANUAL AL PULSAR EL BOTÓN ---
if save_clicked:
    current_record = {
        "Perfil / Carrera": profile,
        "Distancia": f"{D_val:.1f} {d_unit}",
        "Línea Colimación": f"{H_mira:.2f} {h_unit}",
        "Desviación Impacto": f"{H_extra:.2f} {h_unit}",
        "Spot Size": f"{spot_size_display:.2f} {h_unit}",
        "Ángulo (α)": f"{angulo_deg:.4f}°",
        "MOA": f"{moa:.2f}",
        "mrad": f"{mrad:.2f}",
        "Dirección": direccion_str,
        "Clics (1/4 MOA)": clicks_moa,
        "Pulsos (0.1 mrad)": pulsos_mrad
    }
    st.session_state["history"].append(current_record)
    st.sidebar.success(txt["record_saved"])

# --- DISPOSICIÓN EN COLUMNAS: GRÁFICA 3D Y VISTA 2D DIANA ---
col_3d, col_2d = st.columns([1.75, 1.0])

with col_3d:
    # --- GRÁFICA INTERACTIVA 3D ---
    pos_mira = (0, H_mira_cm)
    pos_impacto_mira = (D_cm, y_target_point)

    fig3d = go.Figure()

    # Plano de suelo Sci-Fi
    grid_x = np.linspace(0, max(D_cm, 10), 10)
    grid_y = np.linspace(-max(abs(H_extra_cm)*1.5, 20), max(abs(H_extra_cm)*1.5, 20), 10)
    gx, gy = np.meshgrid(grid_x, grid_y)
    gz = np.zeros_like(gx)

    fig3d.add_trace(go.Surface(
        x=gx, y=gy, z=gz,
        colorscale=[[0, '#0a0c1b'], [1, '#161936']],
        showscale=False, opacity=0.5, hoverinfo='none'
    ))

    # Eje óptico de referencia (Línea Roja Neón)
    fig3d.add_trace(go.Scatter3d(
        x=[0, D_cm], y=[0, 0], z=[0, y_ref_end],
        mode='lines+markers',
        name=f"{txt['laser_label']} ({ref_angle_deg:.2f}°)",
        line=dict(color='#FF0055', width=7, dash='dash'),
        marker=dict(size=4, color='#FF0055')
    ))

    # Eje del sensor ajustable (Azul Cian Brilliant)
    fig3d.add_trace(go.Scatter3d(
        x=[0, D_cm], y=[0, 0], z=[pos_mira[1], pos_impacto_mira[1]],
        mode='lines+markers',
        name=f"{txt['sight_label']} (α = {angulo_deg:.2f}°)",
        line=dict(color='#00F0FF', width=9),
        marker=dict(size=5, color='#00F0FF')
    ))

    # Puntos clave
    fig3d.add_trace(go.Scatter3d(
        x=[D_cm], y=[0], z=[y_ref_end],
        mode='markers', name=txt["target_center"],
        marker=dict(size=8, color='#FFE600', symbol='circle')
    ))

    fig3d.add_trace(go.Scatter3d(
        x=[D_cm], y=[0], z=[y_target_point],
        mode='markers', name=txt["target_point"],
        marker=dict(size=10, color='#00FF66', symbol='diamond')
    ))

    fig3d.update_layout(
        title=dict(
            text=f"📐 <b>{txt['title_graph']} 3D</b>: {D_val:.1f} {d_unit} | <b>α</b>: {angulo_deg:.4f}°",
            font=dict(color="#00F0FF", size=14)
        ),
        paper_bgcolor='#070814', plot_bgcolor='#070814',
        height=460, margin=dict(l=5, r=5, t=35, b=5),
        scene=dict(
            aspectmode='manual', aspectratio=dict(x=2.0, y=1, z=1.1),
            xaxis=dict(title='Distancia (cm)', backgroundcolor="#070814", gridcolor="#1f244d", tickfont=dict(color="#a0a5c0")),
            yaxis=dict(title='Eje Lateral', backgroundcolor="#070814", gridcolor="#1f244d", tickfont=dict(color="#a0a5c0")),
            zaxis=dict(title='Elevación (cm)', backgroundcolor="#070814", gridcolor="#1f244d", tickfont=dict(color="#a0a5c0")),
            camera=dict(eye=dict(x=1.6, y=-1.4, z=0.6))
        ),
        legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center", font=dict(color="white", size=10), bgcolor="rgba(14, 15, 29, 0.8)")
    )
    st.plotly_chart(fig3d, use_container_width=True, key="grafica_optica_3d")

with col_2d:
    # --- VISTA 2D DE LA DIANA / RETÍCULA (MÓDULO 5) ---
    fig2d = go.Figure()

    # Anillos concéntricos de la diana
    max_radius = max(abs(diferencia_altura_cm) * 1.4, spot_radius_cm * 2.5, 5.0)
    rings = np.linspace(max_radius * 0.2, max_radius, 4)

    for r in reversed(rings):
        fig2d.add_shape(
            type="circle", xref="x", yref="y",
            x0=-r, y0=-r, x1=r, y1=r,
            line=dict(color="#23264d", width=1.5),
            fillcolor="rgba(20, 25, 55, 0.3)"
        )

    # Ejes de la retícula
    fig2d.add_shape(type="line", x0=-max_radius*1.2, y0=0, x1=max_radius*1.2, y1=0, line=dict(color="#00d2ff", width=1, dash="dot"))
    fig2d.add_shape(type="line", x0=0, y0=-max_radius*1.2, x1=0, y1=max_radius*1.2, line=dict(color="#00d2ff", width=1, dash="dot"))

    # Haz Láser Real con Spot Size (Circulo neón traslúcido)
    fig2d.add_shape(
        type="circle", xref="x", yref="y",
        x0=-spot_radius_cm, y0=diferencia_altura_cm - spot_radius_cm,
        x1=spot_radius_cm, y1=diferencia_altura_cm + spot_radius_cm,
        line=dict(color="#00F0FF", width=2),
        fillcolor="rgba(0, 240, 255, 0.35)"
    )

    # Punto de impacto central del sensor
    fig2d.add_trace(go.Scatter(
        x=[0], y=[diferencia_altura_cm],
        mode='markers', name=txt["target_point"],
        marker=dict(size=8, color='#00FF66', symbol='cross')
    ))

    # Centro de la diana (0,0)
    fig2d.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers', name=txt["target_center"],
        marker=dict(size=7, color='#FFE600', symbol='circle')
    ))

    fig2d.update_layout(
        title=dict(text=txt["target_2d_title"], font=dict(color="#00F0FF", size=14)),
        paper_bgcolor='#070814', plot_bgcolor='#070814',
        height=460, margin=dict(l=10, r=10, t=35, b=10),
        xaxis=dict(range=[-max_radius*1.2, max_radius*1.2], showgrid=False, zeroline=False, tickfont=dict(color="#a0a5c0"), title=f"X ({h_unit})"),
        yaxis=dict(range=[-max_radius*1.2, max_radius*1.2], showgrid=False, zeroline=False, tickfont=dict(color="#a0a5c0"), title=f"Y ({h_unit})"),
        scaleanchor="x", scaleratio=1,
        legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center", font=dict(color="white", size=9), bgcolor="rgba(14, 15, 29, 0.8)")
    )
    st.plotly_chart(fig2d, use_container_width=True, key="grafica_diana_2d")

# --- MÉTRICAS EXPANDIDAS CON FÍSICA Y DIVERGENCIA ---
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #12132c; border: 1px solid #333566; padding: 12px 15px; border-radius: 8px; margin-top: 10px; margin-bottom: 25px;">
        <div style="text-align: center; flex: 1;">
            <span style="color: #a0a5c0; font-size: 11px; font-weight: bold; text-transform: uppercase;">{txt['diff_height']}</span><br>
            <span style="color: #ffffff; font-size: 16px; font-weight: bold;">{diff_height_display:.2f} {h_unit}</span>
        </div>
        <div style="text-align: center; border-left: 1px solid #333566; padding-left: 10px; flex: 1;">
            <span style="color: #a0a5c0; font-size: 11px; font-weight: bold; text-transform: uppercase;">{txt['sight_angle']}</span><br>
            <span style="color: #00d2ff; font-size: 16px; font-weight: bold;">{angulo_deg:.4f}°</span>
        </div>
        <div style="text-align: center; border-left: 1px solid #333566; padding-left: 10px; flex: 1.2;">
            <span style="color: #a0a5c0; font-size: 11px; font-weight: bold; text-transform: uppercase;">{txt['angular_adj']}</span><br>
            <span style="color: #33ff77; font-size: 16px; font-weight: bold;">{moa:.2f} MOA | {mrad:.2f} mrad</span>
        </div>
        <div style="text-align: center; border-left: 1px solid #333566; padding-left: 10px; flex: 1.2;">
            <span style="color: #a0a5c0; font-size: 11px; font-weight: bold; text-transform: uppercase;">{txt['spot_size_lbl']}</span><br>
            <span style="color: #FFE600; font-size: 16px; font-weight: bold;">Ø {spot_size_display:.2f} {h_unit}</span>
        </div>
        <div style="text-align: center; border-left: 1px solid #333566; padding-left: 10px; flex: 1;">
            <span style="color: #a0a5c0; font-size: 11px; font-weight: bold; text-transform: uppercase;">{txt['curv_drop_lbl']}</span><br>
            <span style="color: #ff77ff; font-size: 16px; font-weight: bold;">{curv_drop_display:.3f} {h_unit}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- TABLA DE HISTORIAL CON CONFIRMACIÓN VERDE / ROJA ---
st.markdown("---")
col_hist_head, col_hist_btn = st.columns([2.2, 1.8])

with col_hist_head:
    st.subheader(txt["history_title"])

with col_hist_btn:
    if not st.session_state["confirm_clear"]:
        if st.button(txt["clear_history"], use_container_width=True):
            st.session_state["confirm_clear"] = True
            st.rerun()
    else:
        st.write(f"**{txt['confirm_clear_msg']}**")
        col_yes, col_no = st.columns(2)

        with col_yes:
            st.markdown('<div class="btn-confirm-yes">', unsafe_allow_html=True)
            if st.button(txt["confirm_yes"], use_container_width=True):
                st.session_state["history"] = []
                st.session_state["confirm_clear"] = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_no:
            st.markdown('<div class="btn-confirm-cancel">', unsafe_allow_html=True)
            if st.button(txt["confirm_cancel"], use_container_width=True):
                st.session_state["confirm_clear"] = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

if st.session_state["history"]:
    df_history = pd.DataFrame(st.session_state["history"])
    st.dataframe(
        df_history,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Perfil / Carrera": st.column_config.TextColumn("Perfil / Carrera", width="medium"),
            "Dirección": st.column_config.TextColumn("Dirección", width="small"),
            "MOA": st.column_config.NumberColumn("MOA", format="%.2f"),
            "mrad": st.column_config.NumberColumn("mrad", format="%.2f"),
        }
    )
else:
    st.info(txt["empty_history"])
