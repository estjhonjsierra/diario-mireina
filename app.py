import streamlit as st
import streamlit.components.v1 as components
import json
import os
from datetime import datetime, timedelta, date
import pytz
import io
import random
import math

# Este archivo está pensado para ejecutarse como app.py en Streamlit Cloud.

# Librerías para generar el PDF elegante con ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTADO INICIAL COMPLETO
# ==============================================================================
st.set_page_config(
    page_title="El Diario de Mi Reina 👑 | Edición Mágica Deluxe 2026",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Control de primera visita y bienvenida
if "bienvenida" not in st.session_state:
    st.balloons()
    st.session_state["bienvenida"] = True

if "efecto_fiesta_actual" not in st.session_state:
    st.session_state["efecto_fiesta_actual"] = None

# Reproductor de música (Estado de reproducción)
if "reproduciendo_musica" not in st.session_state:
    st.session_state["reproduciendo_musica"] = False

# Contadores de estadísticas bonitas
if "sonrisas_count" not in st.session_state:
    st.session_state["sonrisas_count"] = 24

if "metas_cumplidas_count" not in st.session_state:
    st.session_state["metas_cumplidas_count"] = 12

if "cartas_creadas_count" not in st.session_state:
    st.session_state["cartas_creadas_count"] = 48

# Personalizaciones por defecto (Preferencia de Ella)
if "user_font" not in st.session_state:
    st.session_state["user_font"] = "Segoe UI"

if "user_theme" not in st.session_state:
    st.session_state["user_theme"] = "Rosa Algodón"

if "user_particles" not in st.session_state:
    st.session_state["user_particles"] = "🦋 Mariposas & 🌸 Flores"

# ==============================================================================
# 2. SISTEMA DE PALETAS Y PERSONALIZACIÓN DE ESTILOS
# ==============================================================================
tz_colombia = pytz.timezone("America/Bogota")
fecha_actual_colombia = datetime.now(tz_colombia)
dia_semana_num = fecha_actual_colombia.weekday()  # 0: Lunes, 6: Domingo

THEME_PRESETS = {
    "Rosa Algodón": {
        "gradient": "linear-gradient(135deg, #fff0f5 0%, #ffe3ec 40%, #f7d6e0 70%, #fff5f8 100%)",
        "border": "#ff85a1",
        "accent": "#d63384",
        "card_bg": "rgba(255, 255, 255, 0.96)",
        "glow": "rgba(255, 133, 161, 0.35)"
    },
    "Lavanda Imperial": {
        "gradient": "linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 40%, #f5f3ff 70%, #faf5ff 100%)",
        "border": "#c084fc",
        "accent": "#7e22ce",
        "card_bg": "rgba(255, 255, 255, 0.96)",
        "glow": "rgba(192, 132, 252, 0.35)"
    },
    "Melocotón Cálido": {
        "gradient": "linear-gradient(135deg, #fff7ed 0%, #ffedd5 40%, #fff1f2 70%, #fffaf0 100%)",
        "border": "#fb923c",
        "accent": "#c2410c",
        "card_bg": "rgba(255, 255, 255, 0.96)",
        "glow": "rgba(251, 146, 60, 0.35)"
    },
    "Menta Fresca": {
        "gradient": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 40%, #fdf2f8 70%, #f7fee7 100%)",
        "border": "#4ade80",
        "accent": "#15803d",
        "card_bg": "rgba(255, 255, 255, 0.96)",
        "glow": "rgba(74, 222, 128, 0.35)"
    },
    "Atardecer Pastel": {
        "gradient": "linear-gradient(135deg, #fff1f2 0%, #ffe4e6 40%, #fecdd3 70%, #fff5f5 100%)",
        "border": "#fb7185",
        "accent": "#be123c",
        "card_bg": "rgba(255, 255, 255, 0.96)",
        "glow": "rgba(251, 113, 133, 0.35)"
    }
}

FONTS_PRESETS = {
    "Segoe UI": "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "Dancing Script (Cursiva Romántica)": "'Dancing Script', cursive, 'Segoe UI', sans-serif",
    "Poppins (Moderna Elegante)": "'Poppins', sans-serif",
    "Cinzel (Imperial 👑)": "'Cinzel', serif"
}

PARTICLE_SETS = {
    "🦋 Mariposas & 🌸 Flores": ["🦋", "🌸", "🌷", "🌺", "✨", "🦋", "🌸", "🌷", "🌺", "✨", "🦋", "🌸"],
    "⭐ Estrellas & 💖 Corazones": ["⭐", "💖", "✨", "🌟", "💕", "⭐", "💖", "✨", "🌟", "💕", "⭐", "💖"],
    "🧸 Ositos & 👑 Coronas": ["🧸", "👑", "🎀", "🧸", "✨", "👑", "🧸", "👑", "🎀", "🧸", "✨", "👑"],
    "🌈 Mezcla Mágica Completa": ["🧸", "🦋", "⭐", "💖", "🌸", "👑", "🌷", "✨", "💕", "🌺", "🌟", "🎀"]
}

theme_cfg = THEME_PRESETS.get(st.session_state["user_theme"], THEME_PRESETS["Rosa Algodón"])
font_family_css = FONTS_PRESETS.get(st.session_state["user_font"], FONTS_PRESETS["Segoe UI"])
particles_list = PARTICLE_SETS.get(st.session_state["user_particles"], PARTICLE_SETS["🦋 Mariposas & 🌸 Flores"])

# ==============================================================================
# 2B. ESCENOGRAFÍA DINÁMICA DEL CICLO SEPTIEMBRE-OCTUBRE 2026
# ==============================================================================
# El ciclo tiene EXACTAMENTE 61 días: septiembre (30) + octubre (31).
# La página del día se determina automáticamente con la fecha de Colombia.
CICLO_INICIO = date(2026, 9, 1)
CICLO_FIN = date(2026, 10, 31)
CICLO_TOTAL = (CICLO_FIN - CICLO_INICIO).days + 1  # 61

ESCENAS_DIARIAS = [
    {"nombre": "Amanecer Rosa", "emoji": "🌅", "gradiente": "linear-gradient(135deg,#fff7fb 0%,#ffdce8 45%,#f9c5d6 100%)", "acento": "#d63384"},
    {"nombre": "Cielo Lavanda", "emoji": "🌌", "gradiente": "linear-gradient(135deg,#f8f2ff 0%,#e8ddff 48%,#d8c5ff 100%)", "acento": "#7e22ce"},
    {"nombre": "Atardecer Dorado", "emoji": "🌇", "gradiente": "linear-gradient(135deg,#fff9ed 0%,#ffe0b2 48%,#ffc6a8 100%)", "acento": "#b45309"},
    {"nombre": "Noche de Estrellas", "emoji": "✨", "gradiente": "linear-gradient(135deg,#f2f5ff 0%,#dce7ff 45%,#c9d4ff 100%)", "acento": "#3949ab"},
    {"nombre": "Jardín de Primavera", "emoji": "🌸", "gradiente": "linear-gradient(135deg,#f3fff9 0%,#ddf7eb 45%,#ffdced 100%)", "acento": "#16825d"},
    {"nombre": "Café y Calma", "emoji": "☕", "gradiente": "linear-gradient(135deg,#fffaf5 0%,#f5e7da 45%,#efd3c4 100%)", "acento": "#8b5e3c"},
    {"nombre": "Cielo Azul Suave", "emoji": "🦋", "gradiente": "linear-gradient(135deg,#f4fbff 0%,#dff2ff 45%,#c9e7ff 100%)", "acento": "#1261a0"},
]

def escena_del_dia(fecha_obj):
    if CICLO_INICIO <= fecha_obj <= CICLO_FIN:
        posicion = (fecha_obj - CICLO_INICIO).days
    else:
        posicion = abs((fecha_obj - CICLO_INICIO).days)
    return ESCENAS_DIARIAS[posicion % len(ESCENAS_DIARIAS)]

fecha_escena_hoy = datetime.now(tz_colombia).date()

# Resolver SIEMPRE la escena antes de construir cualquier bloque HTML/CSS.
# Se usan variables simples para evitar NameError si este archivo se ejecuta
# en una recarga temprana de Streamlit Cloud.
escena_hoy = escena_del_dia(fecha_escena_hoy)
ESCENA_GRADIENTE_CSS = escena_hoy.get("gradiente", theme_cfg.get("gradient", "linear-gradient(135deg,#fff0f5,#fff5f8)"))
ESCENA_ACENTO_CSS = escena_hoy.get("acento", theme_cfg.get("accent", "#d63384"))
ESCENA_EMOJI = escena_hoy.get("emoji", "✨")
ESCENA_NOMBRE = escena_hoy.get("nombre", "Escena especial")

# ==============================================================================
# 3. ESTILOS CSS AVANZADOS, GOOGLE FONTS & 12 PARTICULAS DINÁMICAS
# ==============================================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Dancing+Script:wght@600;700&family=Poppins:wght@300;400;600;700&display=swap');

/* Tipografía global y lectura ejecutiva */
html, body, [class*="css"], .stMarkdown, p, div, label, span {{
    font-size: 20px !important;
    font-family: {font_family_css} !important;
    line-height: 1.68 !important;
}}

.stTextInput input, .stTextArea textarea, .stSelectbox div, .stMultiSelect, .stRadio label {{
    font-size: 1.05em !important;
    font-family: {font_family_css} !important;
}}

/* Fondo dinámico por tema seleccionado */
.stApp {{
    background: {theme_cfg['gradient']} !important;
    background-attachment: fixed !important;
}}

/* PARTICULAS FLOTANTES CONTINUAS EN EL FONDO (12 PARTICULAS) */
.floating-particle {{
    position: fixed;
    z-index: 0;
    pointer-events: none;
    user-select: none;
    animation: floatParticle 12s infinite ease-in-out;
    opacity: 0.88;
    font-size: 2.5rem;
}}

@keyframes floatParticle {{
    0% {{ transform: translateY(105vh) translateX(0px) rotate(0deg) scale(0.8); opacity: 0; }}
    20% {{ opacity: 0.95; }}
    80% {{ opacity: 0.95; }}
    100% {{ transform: translateY(-15vh) translateX(85px) rotate(360deg) scale(1.4); opacity: 0; }}
}}

.p1  {{ left: 2%;  animation-duration: 11s;   animation-delay: 0s; }}
.p2  {{ left: 10%; animation-duration: 13.5s; animation-delay: 2s; }}
.p3  {{ left: 19%; animation-duration: 9.8s;  animation-delay: 4s; }}
.p4  {{ left: 28%; animation-duration: 12.2s; animation-delay: 1s; }}
.p5  {{ left: 37%; animation-duration: 14s;    animation-delay: 5s; }}
.p6  {{ left: 46%; animation-duration: 8.9s;   animation-delay: 3s; }}
.p7  {{ left: 55%; animation-duration: 12.8s; animation-delay: 6s; }}
.p8  {{ left: 64%; animation-duration: 10.2s; animation-delay: 1.5s; }}
.p9  {{ left: 73%; animation-duration: 13.1s; animation-delay: 3.5s; }}
.p10 {{ left: 82%; animation-duration: 11.4s; animation-delay: 0.8s; }}
.p11 {{ left: 90%; animation-duration: 14.5s; animation-delay: 4.2s; }}
.p12 {{ left: 96%; animation-duration: 9.5s;  animation-delay: 2.2s; }}

/* Keyframes de animación */
@keyframes floatHeader {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-9px) rotate(0.8deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
}}

@keyframes pulseBorder {{
    0% {{ box-shadow: 0 0 15px {theme_cfg['glow']}; }}
    50% {{ box-shadow: 0 0 30px {theme_cfg['border']}; }}
    100% {{ box-shadow: 0 0 15px {theme_cfg['glow']}; }}
}}

@keyframes photoMovement {{
    0% {{ transform: translateY(0px) rotate(0deg) scale(1); box-shadow: 0px 10px 25px rgba(255, 77, 109, 0.3); }}
    50% {{ transform: translateY(-14px) rotate(1.5deg) scale(1.02); box-shadow: 0px 22px 40px rgba(255, 77, 109, 0.45); }}
    100% {{ transform: translateY(0px) rotate(0deg) scale(1); box-shadow: 0px 10px 25px rgba(255, 77, 109, 0.3); }}
}}

/* Encabezados y Tarjetas */
.main-header {{
    text-align: center;
    color: {theme_cfg['accent']};
    font-size: 3.5em !important;
    font-weight: 900;
    margin-bottom: 4px;
    animation: floatHeader 4.5s ease-in-out infinite;
    text-shadow: 3px 3px 16px rgba(214, 51, 132, 0.25);
}}

.sub-header {{
    text-align: center;
    color: #4a4a4a;
    font-size: 1.38em !important;
    font-weight: 600;
    margin-bottom: 20px;
}}

.theme-badge {{
    text-align: center;
    background: rgba(255, 255, 255, 0.94);
    border: 2px solid {theme_cfg['border']};
    border-radius: 22px;
    padding: 8px 24px;
    width: fit-content;
    margin: 0 auto 22px auto;
    font-size: 1em;
    font-weight: bold;
    color: {theme_cfg['accent']};
    box-shadow: 0 5px 15px rgba(0,0,0,0.06);
    animation: pulseBorder 3s infinite ease-in-out;
}}

.card {{
    background: {theme_cfg['card_bg']};
    border-radius: 26px;
    padding: 28px;
    border-left: 10px solid {theme_cfg['border']};
    box-shadow: 0 12px 32px rgba(0,0,0,0.07);
    margin-bottom: 25px;
    font-size: 1.05em;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

.card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 16px 38px rgba(255, 77, 109, 0.22);
}}

.daily-card {{
    background: linear-gradient(135deg, #ffffff 0%, #fff0f3 100%);
    border: 2.5px solid {theme_cfg['border']};
    border-radius: 26px;
    padding: 28px;
    box-shadow: 0 14px 35px rgba(214, 51, 132, 0.18);
    margin-top: 16px;
    animation: floatHeader 6.5s ease-in-out infinite;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}
.daily-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 20px 50px rgba(214, 51, 132, 0.3);
}}

.photo-card-moving {{
    border: 4px solid {theme_cfg['border']};
    border-radius: 28px;
    padding: 18px;
    background: #ffffff;
    text-align: center;
    font-size: 1.25em;
    font-weight: bold;
    color: {theme_cfg['accent']};
    animation: photoMovement 5s ease-in-out infinite;
    transition: all 0.4s ease;
}}

/* Timeline Custom Styles */
.timeline-container {{
    position: relative;
    padding: 20px 0;
    margin: 20px 0;
}}

.timeline-item {{
    position: relative;
    padding-left: 45px;
    margin-bottom: 30px;
    border-left: 4px solid {theme_cfg['border']};
}}

.timeline-icon {{
    position: absolute;
    left: -22px;
    top: 0;
    background: #ffffff;
    border: 3px solid {theme_cfg['border']};
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2em;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}}

.timeline-content {{
    background: #ffffff;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.05);
}}

/* Stat Box Styles */
.stat-box {{
    background: #ffffff;
    border-radius: 22px;
    padding: 22px;
    text-align: center;
    border: 2px solid {theme_cfg['border']};
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    transition: transform 0.3s ease;
}}

.stat-box:hover {{
    transform: scale(1.04);
}}

.stat-number {{
    font-size: 2.2em !important;
    font-weight: 900;
    color: {theme_cfg['accent']};
    margin: 5px 0;
}}

/* Botones con estilo elegante */
.stButton>button {{
    font-size: 1.05em !important;
    border-radius: 20px !important;
    padding: 12px 26px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, {theme_cfg['border']} 0%, {theme_cfg['accent']} 100%) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 8px 22px rgba(255, 77, 109, 0.35) !important;
    transition: all 0.3s ease !important;
}}

.stButton>button:hover {{
    transform: scale(1.05) !important;
    box-shadow: 0 12px 28px rgba(255, 77, 109, 0.52) !important;
}}

/* ==========================================================================
   EDICIÓN DELUXE 2.0 — CAPA VISUAL EXTRA
   ========================================================================== */
:root {{
    --rose-50: #fff7fa;
    --rose-100: #ffe8ef;
    --rose-200: #ffd1df;
    --rose-300: #ffabc3;
    --rose-400: #ff7da0;
    --rose-500: #ed4d83;
    --rose-600: #cc2f69;
    --rose-700: #a61d52;
    --ink: #342332;
    --muted: #6f6170;
    --glass: rgba(255,255,255,0.78);
    --glass-strong: rgba(255,255,255,0.93);
}}

.deluxe-shell {{
    position: relative;
    overflow: hidden;
    border-radius: 34px;
    padding: 30px;
    margin: 8px 0 28px 0;
    background:
        radial-gradient(circle at 15% 15%, rgba(255,255,255,.95), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(255,182,210,.38), transparent 26%),
        radial-gradient(circle at 70% 85%, rgba(214,179,255,.28), transparent 30%),
        linear-gradient(135deg, rgba(255,247,250,.96), rgba(255,232,239,.93));
    border: 1px solid rgba(255,125,160,.45);
    box-shadow:
        0 28px 70px rgba(112,48,77,.13),
        inset 0 1px 0 rgba(255,255,255,.96);
}}

.deluxe-shell::before {{
    content: "";
    position: absolute;
    width: 420px;
    height: 420px;
    right: -180px;
    top: -210px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,.86), rgba(255,255,255,0));
    pointer-events: none;
}}

.deluxe-shell::after {{
    content: "";
    position: absolute;
    width: 300px;
    height: 300px;
    left: -150px;
    bottom: -180px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,174,201,.32), rgba(255,174,201,0));
    pointer-events: none;
}}

.deluxe-kicker {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 14px;
    border-radius: 999px;
    color: #a61d52;
    background: rgba(255,255,255,.74);
    border: 1px solid rgba(237,77,131,.25);
    font-size: 0.84rem;
    font-weight: 800;
    letter-spacing: .04em;
    text-transform: uppercase;
}}

.deluxe-title {{
    font-size: clamp(2rem, 4vw, 3.7rem);
    font-weight: 900;
    color: #9b1d4f;
    margin: 12px 0 4px 0;
    line-height: 1.06;
    letter-spacing: -0.03em;
}}

.deluxe-subtitle {{
    color: #604e5e;
    max-width: 820px;
    margin: 0;
    font-size: 1.05rem;
}}

.daily-orbit {{
    margin-top: 22px;
    display: grid;
    grid-template-columns: 1.25fr .9fr .9fr;
    gap: 14px;
}}

.orbit-card {{
    position: relative;
    min-height: 140px;
    padding: 20px;
    border-radius: 24px;
    background: rgba(255,255,255,.74);
    border: 1px solid rgba(237,77,131,.17);
    box-shadow: 0 12px 30px rgba(80,35,62,.08);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}
.orbit-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 18px 38px rgba(80,35,62,.13);
}}

.orbit-card strong {{
    color: #9b1d4f;
}}

.orbit-date {{
    font-size: 1.8rem;
    font-weight: 900;
    color: #b02059;
    line-height: 1.1;
}}

.orbit-label {{
    font-size: .78rem;
    color: #876f7e;
    font-weight: 800;
    letter-spacing: .08em;
    text-transform: uppercase;
}}

.progress-track {{
    width: 100%;
    height: 10px;
    background: rgba(255,255,255,.74);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 12px;
    border: 1px solid rgba(237,77,131,.14);
}}

.progress-fill {{
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #ff8fb0, #d83f78, #a61d52);
    box-shadow: 0 0 18px rgba(216,63,120,.25);
}}

.quote-card {{
    margin-top: 16px;
    padding: 20px 22px;
    border-radius: 24px;
    border: 1px dashed rgba(166,29,82,.42);
    background: rgba(255,255,255,.67);
    color: #4d3a48;
    box-shadow: 0 12px 26px rgba(80,35,62,.07);
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}
.quote-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 18px 38px rgba(80,35,62,.13);
}}

.quote-card .quote-mark {{
    font-size: 3rem;
    line-height: .7;
    color: #e64c82;
    vertical-align: middle;
    margin-right: 8px;
}}

.mini-pill-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
}}

.mini-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 11px;
    border-radius: 999px;
    background: rgba(255,255,255,.72);
    border: 1px solid rgba(237,77,131,.18);
    color: #755f6d;
    font-size: .86rem;
    font-weight: 700;
}}

.letter-card {{
    position: relative;
    padding: 34px;
    border-radius: 30px;
    background:
        linear-gradient(180deg, rgba(255,255,255,.98), rgba(255,247,250,.98)),
        repeating-linear-gradient(
            to bottom,
            transparent 0,
            transparent 30px,
            rgba(218,177,195,.12) 31px,
            transparent 32px
        );
    border: 1px solid rgba(166,29,82,.22);
    box-shadow: 0 24px 50px rgba(80,35,62,.11);
    overflow: hidden;
}}

.letter-card::before {{
    content: "♥";
    position: absolute;
    right: 24px;
    top: 13px;
    font-size: 4.5rem;
    color: rgba(237,77,131,.10);
    transform: rotate(12deg);
}}

.letter-heading {{
    color: #9b1d4f;
    font-size: 1.85rem;
    font-weight: 900;
    margin-bottom: 6px;
}}

.letter-body {{
    color: #413440;
    font-size: 1.05rem;
    line-height: 1.95;
    white-space: pre-line;
}}

.signature {{
    margin-top: 26px;
    color: #a61d52;
    font-family: "Dancing Script", cursive;
    font-size: 1.9rem;
    font-weight: 700;
}}

.ritual-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    margin-top: 16px;
}}

.ritual-card {{
    padding: 22px;
    border-radius: 24px;
    background: rgba(255,255,255,.84);
    border: 1px solid rgba(237,77,131,.18);
    box-shadow: 0 12px 28px rgba(80,35,62,.07);
    min-height: 160px;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}
.ritual-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 18px 38px rgba(80,35,62,.13);
}}

.ritual-number {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #ffadc7, #d83f78);
    color: white;
    font-weight: 900;
    box-shadow: 0 8px 16px rgba(216,63,120,.22);
}}

.ritual-card h4 {{
    color: #9b1d4f;
    margin: 14px 0 8px 0;
}}

.ritual-card p {{
    color: #655262;
    margin: 0;
    line-height: 1.65;
}}

.secret-stage {{
    position: relative;
    min-height: 330px;
    display: grid;
    place-items: center;
    padding: 24px;
    border-radius: 32px;
    background:
        radial-gradient(circle at 50% 35%, rgba(255,255,255,.95), transparent 23%),
        radial-gradient(circle at 25% 50%, rgba(248,152,190,.23), transparent 25%),
        radial-gradient(circle at 80% 65%, rgba(157,131,255,.18), transparent 30%),
        linear-gradient(145deg, #2f1931, #5e2849 52%, #22142d);
    color: white;
    box-shadow: 0 28px 60px rgba(38,18,39,.24);
    overflow: hidden;
}}

.secret-stage::before,
.secret-stage::after {{
    content: "✦";
    position: absolute;
    color: rgba(255,255,255,.52);
    animation: twinkle 3.4s ease-in-out infinite;
}}

.secret-stage::before {{
    left: 8%;
    top: 15%;
    font-size: 2rem;
}}

.secret-stage::after {{
    right: 10%;
    bottom: 13%;
    font-size: 2.4rem;
    animation-delay: 1.2s;
}}

@keyframes twinkle {{
    0%, 100% {{ opacity: .28; transform: scale(.82) rotate(0deg); }}
    50% {{ opacity: 1; transform: scale(1.22) rotate(16deg); }}
}}

.secret-lock {{
    width: 118px;
    height: 118px;
    border-radius: 34px;
    display: grid;
    place-items: center;
    font-size: 4rem;
    background: linear-gradient(145deg, rgba(255,255,255,.14), rgba(255,255,255,.04));
    border: 1px solid rgba(255,255,255,.18);
    box-shadow: 0 20px 45px rgba(0,0,0,.22);
    backdrop-filter: blur(8px);
    animation: lockFloat 5s ease-in-out infinite;
}}

@keyframes lockFloat {{
    0%,100% {{ transform: translateY(0) rotate(-2deg); }}
    50% {{ transform: translateY(-12px) rotate(2deg); }}
}}

.secret-title {{
    text-align: center;
    font-size: 1.7rem;
    font-weight: 900;
    margin-top: 16px;
}}

.secret-text {{
    text-align: center;
    max-width: 760px;
    color: rgba(255,255,255,.86);
    line-height: 1.8;
}}

.countdown-card {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-top: 18px;
}}

.countdown-item {{
    text-align: center;
    padding: 18px 10px;
    border-radius: 20px;
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.12);
}}

.countdown-number {{
    display: block;
    font-size: 2.3rem;
    font-weight: 900;
    color: #ffd6e4;
    line-height: 1;
}}

.countdown-label {{
    font-size: .75rem;
    margin-top: 8px;
    color: rgba(255,255,255,.72);
    text-transform: uppercase;
    letter-spacing: .08em;
}}

.stars-canvas-wrap {{
    position: relative;
    border-radius: 28px;
    overflow: hidden;
    min-height: 380px;
    background: linear-gradient(180deg, #111027 0%, #281838 48%, #5b2d50 100%);
    box-shadow: 0 24px 54px rgba(30,18,43,.25);
    border: 1px solid rgba(255,255,255,.08);
}}

.star-label {{
    position: absolute;
    left: 24px;
    top: 20px;
    z-index: 2;
    color: rgba(255,255,255,.84);
    font-weight: 800;
    letter-spacing: .04em;
}}

.glow-dot {{
    position: absolute;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #fff;
    box-shadow:
        0 0 7px #fff,
        0 0 14px rgba(255,189,218,.9),
        0 0 24px rgba(255,111,168,.55);
    animation: dotPulse 2.8s infinite ease-in-out;
}}

@keyframes dotPulse {{
    0%,100% {{ transform: scale(.65); opacity: .44; }}
    50% {{ transform: scale(1.25); opacity: 1; }}
}}

.constellation-line {{
    position: absolute;
    height: 1px;
    background: linear-gradient(90deg, rgba(255,255,255,.06), rgba(255,196,223,.55), rgba(255,255,255,.06));
    transform-origin: left center;
}}

.moment-card {{
    padding: 22px;
    border-radius: 26px;
    background: linear-gradient(135deg, rgba(255,255,255,.94), rgba(255,243,248,.94));
    border: 1px solid rgba(166,29,82,.18);
    box-shadow: 0 14px 32px rgba(80,35,62,.08);
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}
.moment-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 18px 38px rgba(80,35,62,.13);
}}

.moment-card h4 {{
    color: #9b1d4f;
    margin: 0 0 8px 0;
}}

.moment-card p {{
    color: #5d4d59;
    margin: 0;
}}

.day-marker {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 14px;
    background: linear-gradient(135deg, #ff91b4, #d83f78);
    color: white;
    font-weight: 900;
    box-shadow: 0 8px 18px rgba(216,63,120,.2);
}}

.retro-badge {{
    display: inline-block;
    padding: 5px 10px;
    margin-left: 7px;
    border-radius: 999px;
    background: #fff0f4;
    color: #a61d52;
    border: 1px solid #ffd0df;
    font-size: .76rem;
    font-weight: 800;
}}

.fade-in {{
    animation: deluxeFade .75s ease both;
}}

@keyframes deluxeFade {{
    0% {{ opacity: 0; transform: translateY(12px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}

.lift {{
    transition: transform .25s ease, box-shadow .25s ease;
}}

.lift:hover {{
    transform: translateY(-5px);
    box-shadow: 0 18px 38px rgba(80,35,62,.13);
}}

/* Escena diaria: el fondo cambia suavemente sin perder la identidad del diario */
.stApp {{
    background: {ESCENA_GRADIENTE_CSS} !important;
    background-attachment: fixed !important;
}}
.daily-scene-badge {{
    display:inline-flex; align-items:center; gap:8px;
    padding:8px 16px; border-radius:999px;
    background:rgba(255,255,255,.82);
    border:1px solid rgba(255,255,255,.95);
    box-shadow:0 8px 24px rgba(0,0,0,.08);
    font-weight:800; color:{ESCENA_ACENTO_CSS};
    backdrop-filter: blur(10px);
}}

/* Mejoras visuales adicionales */
.card, .orbit-card, .daily-card, .moment-card, .quote-card {{
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}
.card:hover, .orbit-card:hover, .daily-card:hover, .moment-card:hover, .quote-card:hover {{
    transform: translateY(-8px) scale(1.01);
    box-shadow: 0 20px 50px rgba(214, 51, 132, 0.3) !important;
}}

.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}}

.stApp > div {{
    position: relative;
    z-index: 1;
}}

@media (max-width: 900px) {{
    .daily-orbit {{
        grid-template-columns: 1fr;
    }}
    .ritual-grid {{
        grid-template-columns: 1fr;
    }}
    .countdown-card {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
    .deluxe-shell {{
        padding: 20px;
        border-radius: 26px;
    }}
}}

@media (prefers-reduced-motion: reduce) {{
    *,
    *::before,
    *::after {{
        animation-duration: .001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .001ms !important;
        scroll-behavior: auto !important;
    }}
}}
</style>

<!-- 12 Partículas flotantes decorativas configurables -->
<div class="floating-particle p1">{particles_list[0]}</div>
<div class="floating-particle p2">{particles_list[1]}</div>
<div class="floating-particle p3">{particles_list[2]}</div>
<div class="floating-particle p4">{particles_list[3]}</div>
<div class="floating-particle p5">{particles_list[4]}</div>
<div class="floating-particle p6">{particles_list[5]}</div>
<div class="floating-particle p7">{particles_list[6]}</div>
<div class="floating-particle p8">{particles_list[7]}</div>
<div class="floating-particle p9">{particles_list[8]}</div>
<div class="floating-particle p10">{particles_list[9]}</div>
<div class="floating-particle p11">{particles_list[10]}</div>
<div class="floating-particle p12">{particles_list[11]}</div>
""", unsafe_allow_html=True)
# ==============================================================================
# 4. MOTOR JS MULTI-EFECTO FIESTA MÁGICA (8 EFECTOS DIFERENTES)
# ==============================================================================
def lanzar_efecto_fiesta_js(tipo_efecto):
    """Genera componentes JavaScript interactivos para efectos visuales sorprendentes."""
    if tipo_efecto == "confetti_boom":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            var count = 250;
            var defaults = { origin: { y: 0.7 } };
            function fire(particleRatio, opts) {
                confetti(Object.assign({}, defaults, opts, {
                    particleCount: Math.floor(count * particleRatio)
                }));
            }
            fire(0.25, { spread: 26, startVelocity: 55, colors: ['#ff4d6d', '#ff85a1', '#ffffff'] });
            fire(0.2, { spread: 60, colors: ['#ffd166', '#06d6a0', '#118ab2'] });
            fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
            fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2, colors: ['#ffc6ff', '#bdb2ff'] });
            fire(0.1, { spread: 120, startVelocity: 45 });
        </script>
        """
        components.html(js_code, height=0)

    elif tipo_efecto == "lluvia_emojis":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            var scalar = 2.5;
            var teddy = confetti.shapeFromText({ text: '🧸', scalar });
            var butterfly = confetti.shapeFromText({ text: '🦋', scalar });
            var heart = confetti.shapeFromText({ text: '💖', scalar });
            var crown = confetti.shapeFromText({ text: '👑', scalar });
            var star = confetti.shapeFromText({ text: '⭐', scalar });
            var flower = confetti.shapeFromText({ text: '🌸', scalar });

            confetti({
                shapes: [teddy, butterfly, heart, crown, star, flower],
                scalar: 3,
                particleCount: 70,
                spread: 160,
                origin: { y: 0.4 },
                startVelocity: 35
            });
        </script>
        """
        components.html(js_code, height=0)

    elif tipo_efecto == "fuegos_artificiales":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            var duration = 3.8 * 1000;
            var animationEnd = Date.now() + duration;
            var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

            function randomInRange(min, max) {
                return Math.random() * (max - min) + min;
            }

            var interval = setInterval(function() {
                var timeLeft = animationEnd - Date.now();
                if (timeLeft <= 0) {
                    return clearInterval(interval);
                }
                var particleCount = 55 * (timeLeft / duration);
                confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
                confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
            }, 250);
        </script>
        """
        components.html(js_code, height=0)

    elif tipo_efecto == "estrellas_doradas":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 140,
                spread: 110,
                origin: { y: 0.6 },
                colors: ['#ffd700', '#ffa500', '#fff8dc', '#ffdf00']
            });
        </script>
        """
        components.html(js_code, height=0)

    elif tipo_efecto == "lluvia_corazones_3d":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            var scalar = 2.8;
            var h1 = confetti.shapeFromText({ text: '💕', scalar });
            var h2 = confetti.shapeFromText({ text: '💖', scalar });
            var h3 = confetti.shapeFromText({ text: '💗', scalar });
            var h4 = confetti.shapeFromText({ text: '❤️', scalar });

            confetti({
                shapes: [h1, h2, h3, h4],
                scalar: 3.2,
                particleCount: 80,
                spread: 140,
                origin: { y: 0.5 },
                startVelocity: 40
            });
        </script>
        """
        components.html(js_code, height=0)

    elif tipo_efecto == "burbujas_magicas":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            var scalar = 2.2;
            var b1 = confetti.shapeFromText({ text: '🫧', scalar });
            var b2 = confetti.shapeFromText({ text: '✨', scalar });

            confetti({
                shapes: [b1, b2],
                scalar: 2.5,
                particleCount: 65,
                spread: 180,
                origin: { y: 0.3 },
                startVelocity: 20
            });
        </script>
        """
        components.html(js_code, height=0)

# ==============================================================================
# 5. BASE DE DATOS Y PERSISTENCIA DE DATOS
# ==============================================================================
DB_FILE = "diario_laura.json"
CAPSULAS_FILE = "capsulas_laura.json"

def cargar_entradas():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_entradas(entradas):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(entradas, f, ensure_ascii=False, indent=4)

def eliminar_entrada_por_indice(index):
    entradas = cargar_entradas()
    if 0 <= index < len(entradas):
        entradas.pop(index)
        guardar_entradas(entradas)
        return True
    return False

def borrar_todo_el_historial():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

def cargar_capsulas():
    if os.path.exists(CAPSULAS_FILE):
        try:
            with open(CAPSULAS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_capsula(nueva_capsula):
    capsulas = cargar_capsulas()
    capsulas.append(nueva_capsula)
    with open(CAPSULAS_FILE, "w", encoding="utf-8") as f:
        json.dump(capsulas, f, ensure_ascii=False, indent=4)

# ==============================================================================
# 6. BASE DE DATOS EXTENDIDA DE MENSAJES DIARIOS, RETOS Y CANCIONES
# ==============================================================================
MENSAJES_DIARIOS = {
    # ... (aquí van todos los mensajes que tenías, desde el 26/07 hasta el 31/08)
    # Para no repetir el contenido, mantén el tuyo. Yo pondré un ejemplo mínimo.
}

RETOS_DIARIOS = {
    # ... (tus retos)
}

CANCIONES_DIARIAS = {
    # ... (tus canciones)
}

LINEA_DEL_TIEMPO_RECUERDOS = [
    # ... (tu línea de tiempo)
]

FRASES_ESCRITAS_POR_TI = [
    # ... (tus frases)
]

COMBOS_ICONOS = ["🧸🦋💖", "⭐🌸✨", "☕✨🌷", "👑🎉💖", "🎀🧸✨", "🕊️🌷🌸", "🌈✨🎈", "🎆👑💖"]

PREGUNTAS_TRIVIA = [
    # ... (tus preguntas)
]

FORTUNAS = [
    # ... (tus fortunas)
]

# ==============================================================================
# 7. GENERADOR DE PDF ELEGANTE CON REPORTLAB
# ==============================================================================
def generar_pdf_carta(titulo, remitente, contenido, fecha_hora_str):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor("#d63384"),
        alignment=1,
        spaceAfter=15
    )
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        textColor=colors.HexColor("#666666"),
        alignment=1,
        spaceAfter=20
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        textColor=colors.HexColor("#222222"),
        leading=22,
        spaceAfter=18
    )
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor("#ff4d6d"),
        alignment=2,
        spaceBefore=25
    )

    story.append(Paragraph("👑 CARTA DE PENSAMIENTOS 👑", title_style))
    story.append(Paragraph(f"<b>Fecha y Hora:</b> {fecha_hora_str} (Hora Colombia)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#ff85a1"), spaceAfter=18))
    story.append(Paragraph(f"<b>Asunto:</b> {titulo}", ParagraphStyle('Sub', parent=title_style, fontSize=16, textColor=colors.HexColor("#ff85a1"))))
    story.append(Spacer(1, 14))
    
    contenido_formateado = contenido.replace('\n', '<br/>')
    story.append(Paragraph(contenido_formateado, body_style))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#ffc6ff"), spaceAfter=15))
    story.append(Paragraph(f"Con todo mi cariño y admiración,<br/><b>{remitente}</b> 💖", footer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ==============================================================================
# 8A. MOTOR DE MENSAJES PROFUNDOS — 2 MESES AUTOMÁTICOS
# ==============================================================================
DOS_MESES_INICIO = date(2026, 9, 1)
DOS_MESES_FIN = date(2026, 10, 31)

DIAS_ES = [
    "lunes", "martes", "miércoles", "jueves",
    "viernes", "sábado", "domingo"
]

MESES_ES = [
    "", "enero", "febrero", "marzo", "abril", "mayo",
    "junio", "julio", "agosto", "septiembre", "octubre",
    "noviembre", "diciembre"
]

SALUDOS_PROFUNDOS = [
    "Mi reina hermosa, hoy quiero que hagas una pausa y recuerdes algo que a veces la vida intenta hacernos olvidar: eres mucho más que todo lo que tienes pendiente.",
    # ... (todos los saludos que tenías)
]

REFLEXIONES_PROFUNDAS = [
    # ... (todas las reflexiones)
]

BENDICIONES_PROFUNDAS = [
    # ... (todas las bendiciones)
]

CIERRES_AMOROSOS = [
    # ... (todos los cierres)
]

TITULOS_PROFUNDOS = [
    # ... (todos los títulos)
]

RETOS_NUEVOS = [
    # ... (todos los retos nuevos)
]

CANCIONES_NUEVAS = [
    # ... (todas las canciones nuevas)
]

def fecha_es(fecha_obj):
    """Devuelve la fecha en español sin depender del locale del servidor."""
    return f"{DIAS_ES[fecha_obj.weekday()].capitalize()}, {fecha_obj.day:02d} de {MESES_ES[fecha_obj.month]} de {fecha_obj.year}"

def indice_ciclico(lista, numero):
    return lista[numero % len(lista)]

def dia_editorial(fecha_obj):
    return (fecha_obj - DOS_MESES_INICIO).days

def contenido_automatico_dos_meses(fecha_obj):
    """
    Construye una entrada completa para cualquier fecha.
    Durante la ventana septiembre-octubre se utiliza el ciclo de dos meses.
    Fuera de la ventana se mantiene el motor, evitando que el diario quede sin contenido.
    """
    n = dia_editorial(fecha_obj)
    if n < 0:
        n = n % 61

    saludo = indice_ciclico(SALUDOS_PROFUNDOS, n)
    reflexion = indice_ciclico(REFLEXIONES_PROFUNDAS, n * 3 + 1)
    bendicion = indice_ciclico(BENDICIONES_PROFUNDAS, n * 5 + 2)
    cierre = indice_ciclico(CIERRES_AMOROSOS, n * 7 + 3)
    titulo = indice_ciclico(TITULOS_PROFUNDOS, n * 11 + 4)
    reto = indice_ciclico(RETOS_NUEVOS, n * 13 + 5)
    cancion_titulo, cancion_desc = indice_ciclico(CANCIONES_NUEVAS, n * 17 + 6)

    if fecha_obj.weekday() == 0:
        enfoque = "💼 Lunes de nuevo comienzo"
    elif fecha_obj.weekday() == 1:
        enfoque = "🌸 Martes para avanzar"
    elif fecha_obj.weekday() == 2:
        enfoque = "✨ Miércoles para respirar"
    elif fecha_obj.weekday() == 3:
        enfoque = "🌷 Jueves para confiar"
    elif fecha_obj.weekday() == 4:
        enfoque = "🎉 Viernes para celebrar"
    elif fecha_obj.weekday() == 5:
        enfoque = "🧸 Sábado para disfrutar"
    else:
        enfoque = "🕊️ Domingo para agradecer"

    poema = (
        f"{saludo}\n\n"
        f"{reflexion}\n\n"
        f"{bendicion}\n\n"
        f"{cierre}"
    )

    return {
        "fecha_str": fecha_es(fecha_obj),
        "titulo": f"{enfoque} · {titulo}",
        "poema": poema,
        "reto": f"🌸 Reto especial: {reto}",
        "cancion": {
            "titulo": f"{cancion_titulo} 🎶",
            "desc": cancion_desc
        },
        "dia_n": n + 1 if 0 <= n < 61 else None,
        "periodo": "Septiembre — Octubre 2026",
        "sello": f"Página {n + 1:02d} de 61"
    }

# Construimos las 61 fechas
MENSAJES_2_MESES = {}
RETOS_2_MESES = {}
CANCIONES_2_MESES = {}

cursor_fecha = DOS_MESES_INICIO
while cursor_fecha <= DOS_MESES_FIN:
    contenido = contenido_automatico_dos_meses(cursor_fecha)
    clave_cursor = cursor_fecha.strftime("%Y-%m-%d")
    MENSAJES_2_MESES[clave_cursor] = contenido
    RETOS_2_MESES[clave_cursor] = contenido["reto"]
    CANCIONES_2_MESES[clave_cursor] = contenido["cancion"]
    cursor_fecha += timedelta(days=1)

# Actualizar los diccionarios globales
MENSAJES_DIARIOS.update(MENSAJES_2_MESES)
RETOS_DIARIOS.update(RETOS_2_MESES)
CANCIONES_DIARIAS.update(CANCIONES_2_MESES)

def contenido_hoy():
    """Contenido sincronizado con la fecha real de Colombia."""
    hoy = datetime.now(tz_colombia).date()
    clave = hoy.strftime("%Y-%m-%d")
    if clave in MENSAJES_2_MESES:
        return MENSAJES_2_MESES[clave]
    base = MENSAJES_DIARIOS.get(clave)
    if base:
        return {
            "fecha_str": base.get("fecha_str", fecha_es(hoy)),
            "titulo": base.get("titulo", "✨ Una página especial para ti"),
            "poema": base.get("poema", ""),
            "reto": RETOS_DIARIOS.get(clave, "🌸 Regálate diez minutos de calma."),
            "cancion": CANCIONES_DIARIAS.get(
                clave,
                {"titulo": "Inolvidable - Beéle 🎶", "desc": "Una melodía bonita para acompañarte."}
            ),
            "dia_n": None,
            "periodo": "Diario del corazón",
            "sello": "Página especial"
        }
    return contenido_automatico_dos_meses(hoy)

def porcentaje_dos_meses(fecha_obj):
    total = (DOS_MESES_FIN - DOS_MESES_INICIO).days + 1
    pos = (fecha_obj - DOS_MESES_INICIO).days + 1
    pos = max(1, min(total, pos))
    return int(round((pos / total) * 100))

def dias_restantes_dos_meses(fecha_obj):
    if fecha_obj < DOS_MESES_INICIO:
        return (DOS_MESES_FIN - DOS_MESES_INICIO).days + 1
    if fecha_obj > DOS_MESES_FIN:
        return 0
    return (DOS_MESES_FIN - fecha_obj).days

def mensaje_corto_de_hora(fecha_hora_obj):
    hora = fecha_hora_obj.hour
    if 5 <= hora < 12:
        return "☀️ Buenos días, mi reina. Que el comienzo de esta página sea suave y luminoso."
    if 12 <= hora < 18:
        return "🌤️ Buenas tardes, mi reina. Haz una pausa y recuerda que no todo tiene que resolverse de una vez."
    if 18 <= hora < 23:
        return "🌙 Buenas noches, mi reina. El día ya hizo su parte; ahora también mereces descansar."
    return "✨ En esta hora tranquila, recuerda que tu corazón también necesita descanso."

def html_escape_simple(texto):
    return (
        str(texto)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )

def calcular_contador_relacion():
    inicio = date(2026, 7, 26)
    hoy = datetime.now(tz_colombia).date()
    return max(0, (hoy - inicio).days)

def etiqueta_momento():
    hora = datetime.now(tz_colombia).hour
    if 5 <= hora < 12:
        return "Mañana ☀️"
    if 12 <= hora < 18:
        return "Tarde 🌤️"
    if 18 <= hora < 23:
        return "Noche 🌙"
    return "Madrugada ✨"
    # ==============================================================================
# 8. ENCABEZADO PRINCIPAL, BARRA DE MÚSICA & BANNER SORPRESA
# ==============================================================================
st.markdown("<h1 class='main-header'>👑 El Diario de Mi Reina 💖🧸🦋</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>De Medellín a Bucaramanga 🏔️✈️✨ | Un espacio lleno de magia, recuerdos y momentos especiales</p>", unsafe_allow_html=True)
st.markdown(f"<div class='theme-badge'>🎨 Tema Activo: {st.session_state['user_theme']} | Tipografía: {st.session_state['user_font']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; margin:-8px 0 18px 0;'><span class='daily-scene-badge'>{ESCENA_EMOJI} Escena de hoy: {ESCENA_NOMBRE} · {fecha_escena_hoy.strftime('%d/%m/%Y')}</span></div>", unsafe_allow_html=True)

# ==============================================================================
# 8B. PORTADA DELUXE — "HOY ES UNA PÁGINA NUEVA" (CON RELOJ EN VIVO)
# ==============================================================================
contenido_hoy_actual = contenido_hoy()
fecha_hora_actual = datetime.now(tz_colombia)
hoy_real = fecha_hora_actual.date()
progreso_60 = porcentaje_dos_meses(hoy_real)
restantes_60 = dias_restantes_dos_meses(hoy_real)
paginas_relacion = calcular_contador_relacion()
momento_actual = etiqueta_momento()

st.markdown(f"""
<div class="deluxe-shell fade-in">
    <div class="deluxe-kicker">✨ EDICIÓN DELUXE · {contenido_hoy_actual['sello']}</div>
    <div class="deluxe-title">Hoy también escribí algo para ti, mi reina. 👑</div>
    <p class="deluxe-subtitle">
        Una página que cambia sola cada día, reconoce la fecha de Colombia y guarda una nueva reflexión
        para acompañarte durante septiembre y octubre.
    </p>

    <div class="daily-orbit">
        <div class="orbit-card lift">
            <div class="orbit-label">Fecha de hoy</div>
            <div class="orbit-date">{fecha_es(hoy_real)}</div>
            <div class="mini-pill-row">
                <span class="mini-pill">🕰️ {momento_actual}</span>
                <span class="mini-pill">🇨🇴 Hora Colombia</span>
            </div>
        </div>

        <div class="orbit-card lift">
            <div class="orbit-label">Maratón de 2 meses</div>
            <strong style="font-size:1.6rem;">{progreso_60}%</strong>
            <div class="progress-track">
                <div class="progress-fill" style="width:{progreso_60}%;"></div>
            </div>
            <div style="margin-top:10px;color:#6f6170;">
                Quedan <b>{restantes_60}</b> días dentro de este ciclo.
            </div>
        </div>

        <div class="orbit-card lift">
            <div class="orbit-label">Nuestro contador</div>
            <strong style="font-size:1.6rem;">{paginas_relacion} días</strong>
            <div style="margin-top:8px;color:#6f6170;">
                de páginas, conversaciones, risas y recuerdos.
            </div>
        </div>

        <!-- NUEVO: RELOJ EN VIVO -->
        <div class="orbit-card lift">
            <div class="orbit-label">Hora en Colombia 🇨🇴</div>
            <div id="reloj" style="font-size: 2rem; font-weight: 900; color: #b02059; font-family: monospace;">Cargando...</div>
        </div>
    </div>

    <div class="quote-card">
        <span class="quote-mark">“</span>
        <strong>{mensaje_corto_de_hora(fecha_hora_actual)}</strong>
        <div style="margin-top:8px;color:#5d4d59;">
            El diario no espera a que alguien lo actualice: cambia con la fecha automáticamente.
        </div>
    </div>
</div>

<script>
    function actualizarReloj() {
        const ahora = new Date();
        const opciones = {{ timeZone: 'America/Bogota', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }};
        const horaCol = ahora.toLocaleTimeString('es-CO', opciones);
        const relojElem = document.getElementById('reloj');
        if (relojElem) relojElem.textContent = horaCol;
    }
    actualizarReloj();
    setInterval(actualizarReloj, 1000);
</script>
""", unsafe_allow_html=True)

# Ejecución de efectos si se solicitaron
if st.session_state["efecto_fiesta_actual"]:
    lanzar_efecto_fiesta_js(st.session_state["efecto_fiesta_actual"])
    st.session_state["efecto_fiesta_actual"] = None

# 🎵 REPRODUCTOR DE MÚSICA OPCIONAL (NO AUTOMÁTICO)
st.write("")
col_mus1, col_mus2 = st.columns([1.2, 0.8])
with col_mus1:
    if st.button("🎵 Reproducir / Pausar nuestra canción especial"):
        st.session_state["reproduciendo_musica"] = not st.session_state["reproduciendo_musica"]

with col_mus2:
    if st.session_state["reproduciendo_musica"]:
        st.markdown("""
        <div style='background: rgba(255,255,255,.92); border-radius: 20px; padding: 14px 18px; border: 2px solid #ff85a1; box-shadow: 0 10px 28px rgba(214,51,132,.12); text-align: center;'>
            <div style='color: #d63384; font-weight: 900; font-size: 0.95em;'>🎶 Música especial de mi reina</div>
            <div style='color:#6b5360; font-size:.82em; margin:4px 0 8px;'>
                Coloca tus archivos <b>sin_miedo.mp3</b> y <b>besame.mp3</b> junto al archivo .py para reproducirlos dentro del diario.
            </div>
            <div style='display:flex; justify-content:center; gap:8px; flex-wrap:wrap; margin-bottom:10px;'>
                <span style='background:#fff0f5; padding:5px 10px; border-radius:999px;'>❤️ Sin Miedo</span>
                <span style='background:#f7f0ff; padding:5px 10px; border-radius:999px;'>💋 Bésame</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Reproductores reales para archivos propios.
col_song1, col_song2 = st.columns(2, gap="medium")
with col_song1:
    if os.path.exists("sin_miedo.mp3"):
        st.audio("sin_miedo.mp3", format="audio/mp3", start_time=0)
        st.caption("❤️ Sin Miedo · archivo local")
    else:
        st.markdown("<div class='card' style='text-align:center;'>❤️ <b>Sin Miedo</b><br><small>Agrega <code>sin_miedo.mp3</code> para habilitar el reproductor.</small></div>", unsafe_allow_html=True)
with col_song2:
    if os.path.exists("besame.mp3"):
        st.audio("besame.mp3", format="audio/mp3", start_time=0)
        st.caption("💋 Bésame · archivo local")
    else:
        st.markdown("<div class='card' style='text-align:center;'>💋 <b>Bésame</b><br><small>Agrega <code>besame.mp3</code> para habilitar el reproductor.</small></div>", unsafe_allow_html=True)

st.write("---")

# ==============================================================================
# 9. MENÚ PRINCIPAL DE 19 PESTAÑAS (INCLUYE LA NUEVA 💝 SORPRESA)
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18, tab19 = st.tabs([
    "🏠 Portada",
    "⏳ Línea del Tiempo",
    "📅 Calendario",
    "📊 Estadísticas",
    "🎨 Personalización",
    "📝 Diario",
    "📚 Memorias",
    "🎯 Planificador",
    "🎟️ Cupones",
    "📄 PDF Cartas",
    "🏺 Frasco Fortuna",
    "🔒 Cápsula Tiempo",
    "🧠 Trivia",
    "✈️ Contador",
    "💌 Carta de Hoy",
    "🌙 Ritual Diario",
    "🎁 Caja Secreta",
    "🌌 Cielo de Hoy",
    "💝 Sorpresa"   # <--- NUEVA PESTAÑA
])

# ------------------------------------------------------------------------------
# TAB 1: PORTADA (ya se mostró arriba, pero aquí podrías poner contenido extra)
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <p style='font-size: 1.2rem; color: #4a4a4a;'>
            Esta es tu portada mágica. Cada día se renueva con un mensaje especial para ti. 💖
        </p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: LÍNEA DEL TIEMPO
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("<h3 style='color: #d63384;'>⏳ Línea del Tiempo de Nuestros Recuerdos Inolvidables</h3>", unsafe_allow_html=True)
    st.write("Un recorrido cronológico por los hitos más bonitos que hemos construido juntos.")
    st.write("---")

    st.markdown("<div class='timeline-container'>", unsafe_allow_html=True)
    for hito in LINEA_DEL_TIEMPO_RECUERDOS:
        st.markdown(f"""
        <div class='timeline-item'>
            <div class='timeline-icon'>{hito['icono']}</div>
            <div class='timeline-content'>
                <span style='background: #ff85a1; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; font-weight: bold;'>{hito['fecha']}</span>
                <h4 style='color: #c2185b; margin-top: 8px; margin-bottom: 6px;'>{hito['titulo']}</h4>
                <p style='color: #444; font-size: 1.02em; margin: 0;'>{hito['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 3: CALENDARIO
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("<h3 style='color: #d63384;'>📅 Calendario Interactivo de Recuerdos & Vivencias</h3>", unsafe_allow_html=True)
    st.write("Selecciona cualquier fecha para consultar lo que se escribió o los mensajes asignados a ese día.")
    st.write("---")

    col_cal1, col_cal2 = st.columns([1, 1.2], gap="large")

    with col_cal1:
        fecha_seleccionada = st.date_input(
            "📆 Elige una fecha en el calendario:",
            value=fecha_actual_colombia.date(),
            min_value=date(2026, 1, 1),
            max_value=date(2026, 12, 31)
        )
        st.info("💡 Cada día en la lista tiene un mensaje, reto y canción asociados.")

    with col_cal2:
        fecha_str_key = fecha_seleccionada.strftime("%Y-%m-%d")
        entradas_totales = cargar_entradas()
        
        entradas_dia = [e for e in entradas_totales if e['fecha'].startswith(fecha_seleccionada.strftime("%d/%m/%Y"))]
        mensaje_sistema = MENSAJES_DIARIOS.get(fecha_str_key, None)
        reto_sistema = RETOS_DIARIOS.get(fecha_str_key, None)
        cancion_sistema = CANCIONES_DIARIAS.get(fecha_str_key, None)

        st.markdown(f"#### 📖 Memorias del {fecha_seleccionada.strftime('%d de %B de %Y')}")
        
        if mensaje_sistema:
            st.markdown(f"""
            <div style='background: #ffffff; border-radius: 18px; padding: 18px; border-left: 6px solid #ff4d6d; box-shadow: 0 6px 18px rgba(0,0,0,0.05); margin-bottom: 15px;'>
                <span style='color: #d63384; font-weight: bold;'>💌 Mensaje Especial del Día:</span>
                <h4 style='margin-top: 5px; color: #c2185b;'>{mensaje_sistema['titulo']}</h4>
                <p style='color: #333; font-size: 0.98em;'>{mensaje_sistema['poema']}</p>
            </div>
            """, unsafe_allow_html=True)

        if reto_sistema:
            st.info(f"✨ **Reto asignado:** {reto_sistema}")

        if cancion_sistema:
            st.success(f"🎵 **Música sugerida:** {cancion_sistema['titulo']} - *{cancion_sistema['desc']}*")

        if entradas_dia:
            st.markdown("<b>📝 Entradas escritas por ti este día:</b>", unsafe_allow_html=True)
            for item in entradas_dia:
                st.markdown(f"""
                <div style='background: #fff0f3; border-radius: 16px; padding: 14px; margin-top: 10px; border: 1.5px solid #ff85a1;'>
                    <b>{item['titulo']}</b> ({item['animo']})<br/>
                    <small style='color: #666;'>Categoría: {item.get('categoria', 'General')}</small>
                    <p style='margin-top: 8px; color: #222;'>{item['contenido']}</p>
                </div>
                """, unsafe_allow_html=True)
        elif not mensaje_sistema:
            st.warning("No hay notas escritas ni mensajes especiales registrados para este día específico.")

# ------------------------------------------------------------------------------
# TAB 4: ESTADÍSTICAS
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("<h3 style='color: #d63384;'>📊 Estadísticas Bonitas & Logros de Nuestra Reina</h3>", unsafe_allow_html=True)
    st.write("Un resumen interactivo y en tiempo real de todo lo que has construido en tu diario.")
    st.write("---")

    entradas_historial = cargar_entradas()
    dias_escritos = len(set(e['fecha'].split()[0] for e in entradas_historial)) if entradas_historial else 0
    palabras_totales = sum(len(e['contenido'].split()) for e in entradas_historial) if entradas_historial else 0

    col_st1, col_st2, col_st3 = st.columns(3)
    col_st4, col_st5 = st.columns(2)

    with col_st1:
        st.markdown(f"""
        <div class='stat-box'>
            <div style='font-size: 1.8em;'>📖</div>
            <div class='stat-number'>{dias_escritos}</div>
            <div style='color: #555; font-weight: bold;'>Días Escritos</div>
        </div>
        """, unsafe_allow_html=True)

    with col_st2:
        st.markdown(f"""
        <div class='stat-box'>
            <div style='font-size: 1.8em;'>📝</div>
            <div class='stat-number'>{palabras_totales:,}</div>
            <div style='color: #555; font-weight: bold;'>Palabras Redactadas</div>
        </div>
        """, unsafe_allow_html=True)

    with col_st3:
        st.markdown(f"""
        <div class='stat-box'>
            <div style='font-size: 1.8em;'>❤️</div>
            <div class='stat-number'>{st.session_state['cartas_creadas_count']}</div>
            <div style='color: #555; font-weight: bold;'>Cartas Especiales</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    with col_st4:
        st.markdown(f"""
        <div class='stat-box'>
            <div style='font-size: 1.8em;'>😊</div>
            <div class='stat-number'>{st.session_state['sonrisas_count']}</div>
            <div style='color: #555; font-weight: bold;'>Sonrisas Registradas</div>
        </div>
        """, unsafe_allow_html=True)

    with col_st5:
        st.markdown(f"""
        <div class='stat-box'>
            <div style='font-size: 1.8em;'>🌸</div>
            <div class='stat-number'>{st.session_state['metas_cumplidas_count']}</div>
            <div style='color: #555; font-weight: bold;'>Metas Cumplidas</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h4 style='color: #c2185b;'>🎯 Acciones de Progreso</h4>", unsafe_allow_html=True)
    if st.button("🌸 Celebrar Cumplimiento de una Nueva Meta"):
        st.session_state["metas_cumplidas_count"] += 1
        st.balloons()
        lanzar_efecto_fiesta_js("fuegos_artificiales")
        st.success("¡Felicidades por avanzar hacia tus metas, mi reina! 🎉")

# ------------------------------------------------------------------------------
# TAB 5: PERSONALIZACIÓN
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("<h3 style='color: #d63384;'>🎨 Centro de Personalización Mágica</h3>", unsafe_allow_html=True)
    st.write("Cambia los colores, las tipografías y las partículas flotantes del diario en tiempo real.")
    st.write("---")

    col_cfg1, col_cfg2, col_cfg3 = st.columns(3)

    with col_cfg1:
        st.markdown("#### **🎨 Paleta de Colores**")
        nuevo_tema = st.selectbox(
            "Selecciona tu combinación favorita:",
            options=list(THEME_PRESETS.keys()),
            index=list(THEME_PRESETS.keys()).index(st.session_state["user_theme"])
        )

    with col_cfg2:
        st.markdown("#### **🔤 Tipografía Elegante**")
        nueva_fuente = st.selectbox(
            "Selecciona la letra del diario:",
            options=list(FONTS_PRESETS.keys()),
            index=list(FONTS_PRESETS.keys()).index(st.session_state["user_font"])
        )

    with col_cfg3:
        st.markdown("#### **✨ Partículas Flotantes**")
        nuevas_particulas = st.selectbox(
            "Selecciona los elementos que vuelan:",
            options=list(PARTICLE_SETS.keys()),
            index=list(PARTICLE_SETS.keys()).index(st.session_state["user_particles"])
        )

    st.write("---")
    if st.button("✨ Aplicar Cambios de Personalización"):
        st.session_state["user_theme"] = nuevo_tema
        st.session_state["user_font"] = nueva_fuente
        st.session_state["user_particles"] = nuevas_particulas
        st.success("¡Personalización guardada con éxito! Reaplicando magia...")
        st.balloons()
        st.rerun()

# ------------------------------------------------------------------------------
# TAB 6: DIARIO
# ------------------------------------------------------------------------------
with tab6:
    st.markdown("<h3 style='color: #d63384;'>📝 Mi Diario Personal e Interactivo</h3>", unsafe_allow_html=True)
    st.write("Escribe lo que viviste hoy, desahógate o guarda un lindo recuerdo de tu día o de tu noche.")
    fecha_hoy = datetime.now(tz_colombia).strftime("%d/%m/%Y %I:%M%p")
    
    st.write("---")
    st.markdown("#### **¿Cómo te sientes en este momento, mi reina?** 💭")
    st.caption("*(Selecciona tu estado de ánimo y mira la respuesta automática)*")
    
    estado_animo = st.radio(
        "Selecciona tu estado de ánimo:",
        options=["😴 Cansada", "🌿 Tranquila", "🔥 Motivada", "✨ Excelente", "🚀 Imparable", "🤯 Abrumada / Estresada"],
        horizontal=True,
        index=1,
        label_visibility="collapsed"
    )

    respuestas_animo = {
        "😴 Cansada": "😴 **Mi vida hermosa:** Sé que has tenido una jornada larga entre la oficina de TQ, tareas o tus pendientes. Te has esforzado un montón. Por favor regálate un baño tibio, ponte ropa cómoda y permite que tu mente descanse. ¡Hiciste un trabajo fabuloso hoy!",
        "🌿 Tranquila": "🌿 **Paz para tu corazón:** Qué dicha saber que estás disfrutando de tus momentos libres y de calma. Tómate un café o té, escucha una bonita canción y disfruta esta serenidad. Te mereces cada segundo de tranquilidad, mi reina.",
        "🔥 Motivada": "🔥 **¡Esa es la actitud, mi reina!**: Tu energía positiva contagia y mueve montañas. Aprovecha este impulso para avanzar en tus metas de Administración o proyectos personales. ¡Vas con toda!",
        "✨ Excelente": "✨ **¡Qué felicidad verte así!**: Tu alegría ilumina todo a tu alrededor y llena el aire de mariposas y estrellas. Guarda este momento de satisfacción en tu diario y celebra cada logro.",
        "🚀 Imparable": "🚀 **¡Eres una mujer poderosa e invencible!**: No hay reto laboral ni examen de universidad que pueda contigo. Tienes la berraquera e inteligencia para devorarte el mundo.",
        "🤯 Abrumada / Estresada": "🤯 **Respira profundo, mi cielo:** Cierra los ojos 5 segundos. No tienes que resolver todo en un solo día. Ve paso a paso. Recuerda que aquí estoy siempre para escucharte y apoyarte, de día y de noche."
    }

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #fff0f3 100%); border-radius: 22px; padding: 22px; border: 2px solid #ff85a1; margin-top: 15px; box-shadow: 0 8px 22px rgba(255, 133, 161, 0.2);'>
        {respuestas_animo[estado_animo]}
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col_input1, col_input2 = st.columns([1.2, 0.8])
    with col_input1:
        titulo_entrada = st.text_input("Título para tu nota de hoy:", placeholder="Ej: Avances en TQ / Una noche tranquila / Tiempo libre en familia...")
    with col_input2:
        etiqueta_entrada = st.selectbox("Categoría:", ["💼 Trabajo TQ", "🎓 Universidad / Administración", "🏡 Hogar / Familia", "💭 Pensamientos", "☕ Tiempo Libre / Descanso"])

    contenido_entrada = st.text_area("Escribe aquí tus pensamientos del día:", height=180, placeholder="Hoy me sentí... logré terminar mis pendientes y compartí un tiempo muy especial con...")

    if st.button("💾 Guardar Entrada en mi Diario"):
        if titulo_entrada.strip() and contenido_entrada.strip():
            entradas = cargar_entradas()
            nueva = {
                "fecha": fecha_hoy,
                "animo": estado_animo,
                "categoria": etiqueta_entrada,
                "titulo": titulo_entrada,
                "contenido": contenido_entrada
            }
            entradas.insert(0, nueva)
            guardar_entradas(entradas)
            st.success("¡Entrada guardada con éxito en tu diario personal! ✨")
            st.balloons()
            lanzar_efecto_fiesta_js("confetti_boom")
        else:
            st.warning("Por favor escribe un título y el contenido antes de guardar.")

# ------------------------------------------------------------------------------
# TAB 7: MEMORIAS
# ------------------------------------------------------------------------------
with tab7:
    st.markdown("<h3 style='color: #d63384;'>📚 Histórico de Memorias & Gestión de Notas</h3>", unsafe_allow_html=True)
    st.write("Aquí se guardan todas tus entradas pasadas. Puedes buscarlas, leerlas o eliminar las que no desees guardar.")
    
    entradas_guardadas = cargar_entradas()

    if entradas_guardadas:
        st.write("---")
        col_search, col_clean = st.columns([1.2, 0.8])
        with col_search:
            busqueda = st.text_input("🔍 Buscar en tu historial:", placeholder="Escribe palabras clave...")
        with col_clean:
            st.markdown("<p style='font-size:0.85em; color:#666; margin-bottom:5px;'>Zona de Gestión Global:</p>", unsafe_allow_html=True)
            confirmar_borrado = st.checkbox("⚠️ Confirmo que deseo borrar TODO el historial")
            if st.button("🗑️ Limpiar Todo el Historial"):
                if confirmar_borrado:
                    borrar_todo_el_historial()
                    st.success("¡El historial de notas ha sido limpiado por completo!")
                    st.rerun()
                else:
                    st.warning("Por favor marca la casilla de confirmación primero.")

        st.write("---")
        for idx, item in enumerate(entradas_guardadas):
            if busqueda.lower() in item['titulo'].lower() or busqueda.lower() in item['contenido'].lower():
                cat = item.get('categoria', '💭 Pensamientos')
                with st.expander(f"📅 {item['fecha']} - {item['titulo']} ({item['animo']}) [{cat}]"):
                    st.markdown(f"**Categoría:** `{cat}`")
                    st.markdown(f"**Estado de ánimo:** {item['animo']}")
                    st.write(item['contenido'])
                    st.write("")
                    if st.button(f"🗑️ Eliminar esta nota", key=f"del_{idx}"):
                        eliminar_entrada_por_indice(idx)
                        st.success("Nota eliminada correctamente.")
                        st.rerun()

        st.write("---")
        json_data = json.dumps(entradas_guardadas, ensure_ascii=False, indent=4)
        st.download_button(
            label="📥 Descargar Copia de Respaldo de mi Historial (.JSON)",
            data=json_data,
            file_name=f"Historial_Diario_Mi_Reina_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    else:
        st.info("Aún no tienes entradas guardadas en tu histórico. ¡Escribe la primera en la pestaña 'Diario'!")

# ------------------------------------------------------------------------------
# TAB 8: PLANIFICADOR
# ------------------------------------------------------------------------------
with tab8:
    st.markdown("<h3 style='color: #d63384;'>🎯 Planificador & Hábitos Diarios de Mi Reina</h3>", unsafe_allow_html=True)
    st.write("Un organizador sencillo para cuidar tu salud, tus estudios en Administración y tus metas en TQ.")
    st.write("---")
    
    col_hab1, col_hab2 = st.columns(2, gap="large")
    
    with col_hab1:
        st.markdown("<h4 style='color: #c2185b;'>🌸 Bienestar & Autocuidado</h4>", unsafe_allow_html=True)
        h1 = st.checkbox("Tomar al menos 2 litros de agua 💧")
        h2 = st.checkbox("Hacer una pausa activa y estirar la espalda 🧘‍♀️")
        h3 = st.checkbox("Disfrutar un café/té con tranquilidad en tu tiempo libre ☕")
        h4 = st.checkbox("Dormir al menos 7 horas hoy 😴")

    with col_hab2:
        st.markdown("<h4 style='color: #c2185b;'>💼 Éxito Laboral & Universitario</h4>", unsafe_allow_html=True)
        h5 = st.checkbox("Completar tareas prioritarias en TQ 📊")
        h6 = st.checkbox("Avanzar en lecturas/trabajos de Administración 📚")
        h7 = st.checkbox("Organizar el correo/agenda del día ✉️")
        h8 = st.checkbox("Regalarme 15 minutos de desconexión total 🌿")

    puntos = sum([h1, h2, h3, h4, h5, h6, h7, h8])
    porcentaje = int((puntos / 8) * 100)

    st.write("---")
    st.markdown(f"#### **Tu Progreso de Hoy:** {porcentaje}%")
    st.progress(porcentaje / 100)

    if porcentaje == 100:
        st.balloons()
        lanzar_efecto_fiesta_js("estrellas_doradas")
        st.success("¡Eres sencillamente increíble, mi reina! Cumpliste todos tus hábitos de hoy. 🎉")
    elif porcentaje >= 50:
        st.info("¡Vas super bien! Recuerda no presionarte y disfrutar el proceso paso a paso. ✨")

# ------------------------------------------------------------------------------
# TAB 9: CUPONES
# ------------------------------------------------------------------------------
with tab9:
    st.markdown("<h3 style='color: #d63384;'>🎟️ Antojitos, Gustos & Cupones Especiales</h3>", unsafe_allow_html=True)
    st.write("¡Canjea tus cupones simbólicos cuando quieras consentirte en tus momentos libres!")
    
    col_c1, col_c2 = st.columns(2, gap="large")
    
    with col_c1:
        st.markdown("""
        <div style='background: #ffffff; border: 3px dashed #ff85a1; border-radius: 22px; padding: 22px; text-align: center; margin-bottom: 18px;'>
            <h4 style='color: #c2185b; margin-bottom: 5px;'>🍝 Cupón: Noche de Lasaña / Pastas</h4>
            <p style='color: #555; font-size: 0.95em;'>Válido para disfrutar tu comida preferida sin preocupaciones.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🍕 Canjear Cupón Pasta/Lasaña"):
            st.balloons()
            lanzar_efecto_fiesta_js("confetti_boom")
            st.success("¡Cupón Canjeado! Que disfrutes un banquete delicioso mi reina. 😋")

        st.markdown("""
        <div style='background: #ffffff; border: 3px dashed #ff85a1; border-radius: 22px; padding: 22px; text-align: center; margin-bottom: 18px;'>
            <h4 style='color: #c2185b; margin-bottom: 5px;'>🎬 Cupón: Peli de Terror & Popcorn</h4>
            <p style='color: #555; font-size: 0.95em;'>Válido para una maratón espeluznante y llena de descanso en tu noche libre.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🍿 Canjear Cupón Película"):
            st.balloons()
            st.success("¡Cupón Canjeado! Prepara las cotufas para la peli. 🍿🎃")

    with col_c2:
        st.markdown("""
        <div style='background: #ffffff; border: 3px dashed #ff85a1; border-radius: 22px; padding: 22px; text-align: center; margin-bottom: 18px;'>
            <h4 style='color: #c2185b; margin-bottom: 5px;'>✨ Cupón: Tarde Alegre de Desconexión</h4>
            <p style='color: #555; font-size: 0.95em;'>Válido para soltar la rutina de TQ, reírte mucho y respirar aire puro.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌿 Canjear Tarde Alegre"):
            st.balloons()
            lanzar_efecto_fiesta_js("lluvia_emojis")
            st.success("¡Cupón Canjeado! Modo paz y felicidad activado. ✨🌷")

        st.markdown("""
        <div style='background: #ffffff; border: 3px dashed #ff85a1; border-radius: 22px; padding: 22px; text-align: center; margin-bottom: 18px;'>
            <h4 style='color: #c2185b; margin-bottom: 5px;'>🛋️ Cupón: Momento de Cero Estrés</h4>
            <p style='color: #555; font-size: 0.95em;'>Válido para soltar los pendientes a cualquier hora y descansar profundamente.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💖 Canjear Cupón Cero Estrés"):
            st.balloons()
            st.success("¡Cupón Canjeado! Inhala paz, exhala tensión. 🧘‍♀️")

# ------------------------------------------------------------------------------
# TAB 10: PDF CARTAS
# ------------------------------------------------------------------------------
with tab10:
    st.markdown("<h3 style='color: #d63384;'>📄 Generador de Cartas en PDF</h3>", unsafe_allow_html=True)
    st.write("Crea y descarga cartas elegantes en formato PDF para guardar tus momentos o imprimirlos.")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        titulo_carta = st.text_input("Asunto o Título de la Carta:", value="Un mensaje especial para mi reina 👑")
    with col_p2:
        remitente_carta = st.text_input("Remitente:", value="Tu admirador desde Medellín ✈️")

    contenido_carta = st.text_area(
        "Escribe el mensaje de la carta:",
        height=200,
        value="Mi reina hermosa, te escribo este mensaje para recordarte lo mucho que te quiero y lo orgulloso que me siento de ver todo tu esfuerzo en TQ y en la Universidad. Eres una mujer simplemente extraordinaria..."
    )

    if st.button("📄 Generar PDF Elegante"):
        fecha_hora_actual = datetime.now(tz_colombia).strftime("%d/%m/%Y %I:%M%p")
        pdf_bytes = generar_pdf_carta(titulo_carta, remitente_carta, contenido_carta, fecha_hora_actual)
        st.session_state["cartas_creadas_count"] += 1
        st.success("¡Tu carta PDF ha sido creada exitosamente! 🎉")
        st.download_button(
            label="📥 Descargar Carta en PDF",
            data=pdf_bytes,
            file_name=f"Carta_Mi_Reina_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

# ------------------------------------------------------------------------------
# TAB 11: FRASCO DE LA FORTUNA
# ------------------------------------------------------------------------------
with tab11:
    st.markdown("<h3 style='color: #d63384;'>🏺 Frasco de Recuerdos & Galleta de la Fortuna</h3>", unsafe_allow_html=True)
    st.write("Saca una notita del frasco virtual o abre una galleta de la fortuna para recargar tu día o noche.")

    col_f1, col_f2 = st.columns(2, gap="large")

    with col_f1:
        st.markdown("<h4 style='color: #c2185b;'>🏺 Notita del Frasco</h4>", unsafe_allow_html=True)
        razones = [
            "Por tu sonrisa que ilumina mis días y mis noches a la distancia.",
            "Por la admiración gigante que siento al verte estudiar Administración.",
            "Por tu profesionalismo y entrega impecable en TQ.",
            "Por el cariño tan hermoso con el que cuidas a tu hijita y a tu hogar.",
            "Por tu dulzura, tus chistes y cada conversación compartida en tus momentos libres.",
            "Por la magia que le transmites a todo lo que haces.",
            "Por ser mi lugar seguro y mi reina consentida.",
            "Por lo lindo que es tenerte en mi vida y compartir estos detalles."
        ]

        if st.button("🏺 Sacar Notita"):
            nota = random.choice(razones)
            combo = random.choice(COMBOS_ICONOS)
            st.balloons()
            st.markdown(f"""
            <div style='background: #fff0f5; border-radius: 22px; padding: 22px; border: 3px solid #ff4d6d; text-align: center;'>
                <div style='font-size: 1.8em; margin-bottom: 6px;'>{combo}</div>
                <h3 style='color: #c2185b; margin: 0;'>Notita del Frasco:</h3>
                <p style='font-size: 1.2em; margin-top: 10px; color: #333;'><b>{nota}</b></p>
            </div>
            """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("<h4 style='color: #c2185b;'>🥠 Galleta de la Fortuna</h4>", unsafe_allow_html=True)
        if st.button("🥠 Abrir Galleta"):
            fortuna_hoy = random.choice(FORTUNAS)
            st.balloons()
            lanzar_efecto_fiesta_js("estrellas_doradas")
            st.markdown(f"""
            <div style='background: #fff7ed; border-radius: 22px; padding: 22px; border: 3px dashed #fb923c; text-align: center;'>
                <div style='font-size: 2em; margin-bottom: 6px;'>🥠✨</div>
                <p style='font-size: 1.2em; color: #d97706;'><b>{fortuna_hoy}</b></p>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 12: CÁPSULA DEL TIEMPO
# ------------------------------------------------------------------------------
with tab12:
    st.markdown("<h3 style='color: #d63384;'>⏳ Cápsula del Tiempo & Mensajes Candado</h3>", unsafe_allow_html=True)
    st.write("¡Guarda o descubre mensajes con candado que solo se pueden abrir en fechas futuras específicas!")

    st.write("---")
    st.markdown("<h4 style='color: #c2185b;'>🔒 Dejar un Mensaje Candado</h4>", unsafe_allow_html=True)
    
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        titulo_capsula = st.text_input("Título de la cápsula:", placeholder="Ej: Abrir cuando tengas un examen difícil...")
        fecha_desbloqueo = st.date_input("Fecha en que se podrá desbloquear:", min_value=date.today())
    with col_cap2:
        mensaje_capsula = st.text_area("Mensaje Secreto:", placeholder="Escribe el mensaje que estará guardado bajo llave...")

    if st.button("🔒 Cerrar y Guardar Cápsula"):
        if titulo_capsula and mensaje_capsula:
            nueva_c = {
                "titulo": titulo_capsula,
                "fecha_desbloqueo": fecha_desbloqueo.strftime("%Y-%m-%d"),
                "mensaje": mensaje_capsula,
                "creado": datetime.now(tz_colombia).strftime("%d/%m/%Y")
            }
            guardar_capsula(nueva_c)
            st.success(f"¡Cápsula guardada con éxito! Permanecerá bajo candado hasta el {fecha_desbloqueo.strftime('%d/%m/%Y')}.")
            st.balloons()
        else:
            st.warning("Completa el título y el mensaje antes de guardar.")

    st.write("---")
    st.markdown("<h4 style='color: #c2185b;'>🔑 Abrir Cápsulas Guardadas</h4>", unsafe_allow_html=True)
    
    capsulas_existentes = cargar_capsulas()
    fecha_hoy_str = datetime.now(tz_colombia).strftime("%Y-%m-%d")

    if capsulas_existentes:
        for idx, cap in enumerate(capsulas_existentes):
            es_alcanzada = fecha_hoy_str >= cap['fecha_desbloqueo']
            
            if es_alcanzada:
                with st.expander(f"🔓 DESBLOQUEADA: {cap['titulo']} (Guardada el {cap['creado']})"):
                    st.success("¡Esta cápsula ya se puede abrir!")
                    st.markdown(f"**Mensaje Secreto:**\n\n*{cap['mensaje']}*")
            else:
                with st.expander(f"🔒 BLOQUEADA: {cap['titulo']} (Se abre el: {cap['fecha_desbloqueo']})"):
                    st.warning(f"⏰ Esta cápsula está bajo candado. Regresa el {cap['fecha_desbloqueo']} para leer su contenido.")
    else:
        st.info("Aún no hay cápsulas creadas. ¡Crea la primera para guardar una sorpresa hacia el futuro!")

# ------------------------------------------------------------------------------
# TAB 13: TRIVIA
# ------------------------------------------------------------------------------
with tab13:
    st.markdown("<h3 style='color: #d63384;'>🧠 Minijuego: Trivia Especial de Nuestra Reina</h3>", unsafe_allow_html=True)
    st.write("Responde estas preguntas interactivas para poner a prueba tus logros y detalles favoritos.")

    score = 0
    st.write("---")

    for i, q in enumerate(PREGUNTAS_TRIVIA):
        st.markdown(f"**Pregunta {i+1}: {q['pregunta']}**")
        resp = st.radio(f"Selecciona tu respuesta para la pregunta {i+1}:", options=q['opciones'], key=f"triv_{i}")
        
        if resp == q['correcta']:
            st.markdown(f"<span style='color: #2e7d32; font-weight: bold;'>✅ {q['explicacion']}</span>", unsafe_allow_html=True)
            score += 1
        else:
            st.caption("💡 Intenta otra respuesta o confirma tu favorita.")
        st.write("")

    st.write("---")
    if st.button("🏆 Validar Puntaje de Trivia"):
        st.balloons()
        if score == len(PREGUNTAS_TRIVIA):
            lanzar_efecto_fiesta_js("fuegos_artificiales")
            st.success(f"¡PUNTAJE PERFECTO! {score}/{len(PREGUNTAS_TRIVIA)} 👑 Eres la reina indiscutible de este lugar.")
        else:
            st.info(f"Obtuviste {score}/{len(PREGUNTAS_TRIVIA)} correctas. ¡Eres increíble de todas formas!")

# ------------------------------------------------------------------------------
# TAB 14: CONTADOR
# ------------------------------------------------------------------------------
with tab14:
    st.markdown("<h3 style='color: #d63384;'>✈️ Medellín - Bucaramanga: Contador & Calculadora</h3>", unsafe_allow_html=True)
    st.write("Estadísticas divertidas de la ruta espacial que une nuestros pensamientos.")

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <h2 style='color: #c2185b; margin: 0;'>📍 390 KM</h2>
            <p style='margin-top: 5px; color: #555;'>Distancia aproximada entre Medellín y Bucaramanga</p>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <h2 style='color: #c2185b; margin: 0;'>✈️ 55 MIN</h2>
            <p style='margin-top: 5px; color: #555;'>Tiempo de vuelo que nos conecta en un abrir y cerrar de ojos</p>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <h2 style='color: #c2185b; margin: 0;'>💯 1000%</h2>
            <p style='margin-top: 5px; color: #555;'>Nivel de admiración y cariño diario hacia mi reina</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h4 style='color: #c2185b;'>💖 Calculadora Mágica de Compatibilidad</h4>", unsafe_allow_html=True)
    nombre1 = st.text_input("Tu Nombre:", value="Laura (Mi Reina)")
    nombre2 = st.text_input("El Nombre de quien te piensa:", value="Tu admirador de Medellín")

    if st.button("🔮 Calcular Compatibilidad Mágica"):
        st.balloons()
        lanzar_efecto_fiesta_js("confetti_boom")
        st.markdown("""
        <div style='background: #fdf2f8; border-radius: 24px; padding: 22px; border: 3px solid #f472b6; text-align: center;'>
            <h2 style='color: #d63384; margin: 0;'>✨ Resultado: 100% COMPATIBILIDAD PERFECTION ✨</h2>
            <p style='color: #333; margin-top: 10px; font-size: 1.15em;'>
                Los astros, las montañas y los corazones confirman que no hay combinación más bonita. 🧸🦋
            </p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 15: CARTA DE HOY
# ------------------------------------------------------------------------------
with tab15:
    carta = contenido_hoy()
    st.markdown("<h3 style='color: #d63384;'>💌 Carta de Hoy — escrita por la fecha</h3>", unsafe_allow_html=True)
    st.write("Esta sección toma el día real de Colombia y transforma el mensaje automático en una carta más íntima.")
    st.write("---")

    st.markdown(f"""
    <div class="letter-card fade-in">
        <div class="day-marker">📅 {carta['fecha_str']}</div>
        <span class="retro-badge">{carta['sello']}</span>
        <div class="letter-heading">{carta['titulo']}</div>
        <div class="letter-body">{html_escape_simple(carta['poema'])}</div>
        <div class="signature">Con amor, desde Medellín. 💖</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col_carta1, col_carta2 = st.columns(2, gap="large")

    with col_carta1:
        st.markdown("#### ✨ La intención de hoy")
        st.info(
            "No tienes que resolver tu vida hoy. Esta carta existe para acompañar un día concreto, "
            "reconocer el esfuerzo que ya hiciste y regalarte una razón para respirar."
        )

    with col_carta2:
        st.markdown("#### 🎵 Banda sonora")
        st.success(
            f"**{carta['cancion']['titulo']}**\n\n{carta['cancion']['desc']}"
        )

    if st.button("💖 Volver a leer la carta con otra energía", key="releer_carta_hoy"):
        st.balloons()
        st.toast("Guarda esta página en el corazón. 🌷")

# ------------------------------------------------------------------------------
# TAB 16: RITUAL DIARIO
# ------------------------------------------------------------------------------
with tab16:
    st.markdown("<h3 style='color: #d63384;'>🌙 Ritual Diario de Mi Reina</h3>", unsafe_allow_html=True)
    st.write("Una rutina emocional de tres momentos para que el diario se sienta distinto durante todo el día.")
    st.write("---")

    ahora_ritual = datetime.now(tz_colombia)
    hora_ritual = ahora_ritual.hour

    if 5 <= hora_ritual < 12:
        momento_destacado = "☀️ Mañana"
        mensaje_momento = "Comienza sin cargar todo el día en la cabeza. Hoy solo necesitas dar el siguiente paso."
    elif 12 <= hora_ritual < 18:
        momento_destacado = "🌤️ Tarde"
        mensaje_momento = "Haz una pausa. No eres una máquina y tampoco tienes que vivir corriendo para demostrar nada."
    elif 18 <= hora_ritual < 23:
        momento_destacado = "🌙 Noche"
        mensaje_momento = "Baja el ritmo. Lo pendiente puede esperar; tu descanso también forma parte de tus metas."
    else:
        momento_destacado = "✨ Madrugada"
        mensaje_momento = "Esta página encontró una hora silenciosa. Que la calma te acompañe y mañana sea más amable."

    st.markdown(f"""
    <div class="moment-card fade-in">
        <h4>{momento_destacado} · Tu mensaje especial ahora</h4>
        <p>{mensaje_momento}</p>
    </div>
    """, unsafe_allow_html=True)

    rituales = [
        ("☀️", "Inicio", "Respira profundo y elige una prioridad real. No diez."),
        ("🌤️", "Pausa", "Mira lejos de la pantalla, estira el cuerpo y toma agua."),
        ("🌙", "Cierre", "Reconoce una cosa que hiciste bien y deja el resto para mañana.")
    ]

    ritual_html = '<div class="ritual-grid">'
    for num, (icono, titulo, texto) in enumerate(rituales, start=1):
        ritual_html += f"""
        <div class="ritual-card lift">
            <div class="ritual-number">{num}</div>
            <h4>{icono} {titulo}</h4>
            <p>{texto}</p>
        </div>
        """
    ritual_html += "</div>"
    st.markdown(ritual_html, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 💭 Pregunta del día")
    preguntas_ritual = [
        "¿Qué parte de mí necesita hoy un poco más de paciencia?",
        "¿Qué pequeño logro estoy olvidando celebrar?",
        "¿Qué puedo soltar esta noche para descansar mejor?",
        "¿Qué quiero que mi yo del futuro agradezca de este día?",
        "¿Cuál fue mi momento más bonito de hoy?"
    ]
    q_actual = preguntas_ritual[(ahora_ritual.timetuple().tm_yday + ahora_ritual.year) % len(preguntas_ritual)]
    st.markdown(f"""
    <div class="quote-card">
        <span class="quote-mark">?</span>
        <strong>{q_actual}</strong>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 17: CAJA SECRETA
# ------------------------------------------------------------------------------
with tab17:
    st.markdown("<h3 style='color: #d63384;'>🎁 Caja Secreta de Mi Reina</h3>", unsafe_allow_html=True)
    st.write("Una pequeña experiencia sorpresa. El contenido cambia según el número del día.")
    st.write("---")

    numero_dia_sorpresa = (datetime.now(tz_colombia).date() - date(2026, 1, 1)).days
    sorpresas = [
        "Hoy eres oficialmente la protagonista de esta página. 👑",
        "Hay personas que inspiran sin proponérselo. Tú eres una de ellas. 🌷",
        "La sorpresa de hoy es un recordatorio: también mereces que te cuiden. 💖",
        "No todo regalo viene en una caja. Algunos llegan escritos. ✉️",
        "Hoy el diario te manda una misión: sonreír antes de terminar de leer. 😊",
        "Hay un abrazo escondido en estas palabras. Imagina que acaba de llegar. 🫂",
        "Tu contraseña secreta de hoy: 'voy a confiar en mi proceso'. ✨",
        "Premio simbólico del día: cinco minutos de paz sin sentir culpa. 🕊️",
        "Sorpresa: alguien está muy orgulloso de ti. Sí, otra vez. 😌",
        "Hoy la caja trae una promesa: no minimizar tus propios logros. 🏆",
        "Tu misión secreta: hacer algo pequeño que te haga feliz.",
        "La caja de hoy contiene una dosis de fe y otra de paciencia.",
        "Hoy está permitido no tener todas las respuestas.",
        "Tu regalo escondido es una frase: 'vas mejor de lo que crees'.",
        "No abras la caja con prisa. Léela despacio. 🌙"
    ]
    sorpresa = sorpresas[numero_dia_sorpresa % len(sorpresas)]

    st.markdown(f"""
    <div class="secret-stage fade-in">
        <div>
            <div style="display:grid;place-items:center;">
                <div class="secret-lock">🎁</div>
                <div class="secret-title">Caja secreta · {fecha_es(datetime.now(tz_colombia).date())}</div>
                <div class="secret-text">{sorpresa}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("🎉 Abrir la caja con efectos", key="abrir_caja_deluxe"):
        st.balloons()
        lanzar_efecto_fiesta_js("lluvia_corazones_3d")
        st.success("¡Sorpresa desbloqueada! Hoy también hay motivos para sonreír. 💖")

# ------------------------------------------------------------------------------
# TAB 18: CIELO DE HOY
# ------------------------------------------------------------------------------
with tab18:
    st.markdown("<h3 style='color: #d63384;'>🌌 Cielo de Hoy — Tu Constelación</h3>", unsafe_allow_html=True)
    st.write("Una escena visual que convierte la fecha en una pequeña constelación simbólica.")
    st.write("---")

    hoy_cielo = datetime.now(tz_colombia).date()
    contenido_cielo = contenido_hoy()

    semillas = [
        (12, 18), (24, 35), (36, 14), (47, 42), (58, 24),
        (70, 12), (82, 32), (18, 64), (34, 80), (52, 70),
        (67, 58), (84, 72), (9, 82), (44, 56), (76, 86)
    ]

    semilla_fecha = hoy_cielo.toordinal()
    rng_cielo = random.Random(semilla_fecha)
    estrellas = []

    for i, (base_x, base_y) in enumerate(semillas):
        jitter_x = rng_cielo.uniform(-1.7, 1.7)
        jitter_y = rng_cielo.uniform(-1.7, 1.7)
        x = max(4, min(95, base_x + jitter_x))
        y = max(7, min(92, base_y + jitter_y))
        size = rng_cielo.randint(5, 10)
        delay = rng_cielo.uniform(0.0, 2.8)
        estrellas.append((x, y, size, delay))

    star_parts = [
        "<!DOCTYPE html>",
        "<html lang='es'>",
        "<head>",
        "<meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<style>",
        "*{box-sizing:border-box}",
        "html,body{margin:0;padding:0;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif}",
        ".sky{position:relative;width:100%;height:430px;overflow:hidden;border-radius:30px;",
        "background:",
        "radial-gradient(circle at 20% 18%,rgba(255,214,232,.18),transparent 18%),",
        "radial-gradient(circle at 75% 30%,rgba(169,151,255,.20),transparent 23%),",
        "radial-gradient(circle at 50% 80%,rgba(255,137,193,.12),transparent 28%),",
        "linear-gradient(180deg,#090d24 0%,#171334 42%,#382044 74%,#57294d 100%);",
        "border:1px solid rgba(255,255,255,.10);",
        "box-shadow:0 24px 58px rgba(18,10,34,.30)","}",
        ".sky:before{content:'';position:absolute;inset:0;background-image:radial-gradient(circle at 10% 30%,rgba(255,255,255,.55) 0 1px,transparent 1.5px),radial-gradient(circle at 34% 62%,rgba(255,255,255,.38) 0 1px,transparent 1.5px),radial-gradient(circle at 81% 20%,rgba(255,255,255,.42) 0 1px,transparent 1.5px);background-size:130px 130px,170px 170px,210px 210px;opacity:.55}",
        ".topline{position:absolute;left:24px;top:18px;z-index:20;color:rgba(255,255,255,.88);font-weight:800;font-size:.95rem;letter-spacing:.03em}",
        ".subline{position:absolute;right:24px;top:18px;z-index:20;color:rgba(255,255,255,.68);font-size:.82rem}",
        ".star{position:absolute;border-radius:50%;background:#fff;box-shadow:0 0 8px #fff,0 0 16px rgba(255,195,224,.9),0 0 28px rgba(255,117,175,.52);animation:twinkle 2.7s ease-in-out infinite;}",
        "@keyframes twinkle{0%,100%{opacity:.42;transform:scale(.64)}50%{opacity:1;transform:scale(1.28)}}",
        ".line{position:absolute;height:1px;transform-origin:left center;background:linear-gradient(90deg,rgba(255,255,255,.02),rgba(255,213,232,.52),rgba(255,255,255,.02));opacity:.72}",
        ".planet{position:absolute;right:11%;bottom:9%;width:82px;height:82px;border-radius:50%;background:radial-gradient(circle at 33% 29%,#fff6fb 0 8%,#ffd2e4 21%,#e77ba9 45%,#742d5a 77%,#32142f 100%);box-shadow:0 0 30px rgba(255,136,189,.20),inset -12px -12px 25px rgba(0,0,0,.25)}",
        ".planet:after{content:'';position:absolute;left:-18px;top:30px;width:118px;height:20px;border:2px solid rgba(255,224,239,.54);border-radius:50%;transform:rotate(-16deg)}",
        ".love{position:absolute;left:10%;bottom:10%;z-index:20;color:rgba(255,255,255,.88);max-width:58%;font-size:.95rem;line-height:1.55}",
        ".footer{position:absolute;left:50%;bottom:15px;transform:translateX(-50%);z-index:20;color:rgba(255,255,255,.42);font-size:.72rem;white-space:nowrap}",
        "</style>",
        "</head>",
        "<body>",
        f"<div class='sky'><div class='topline'>✨ Constelación del día · {fecha_es(hoy_cielo)}</div>",
        f"<div class='subline'>Página {contenido_cielo.get('dia_n','—')} · {ESCENA_EMOJI} {ESCENA_NOMBRE}</div>",
    ]

    for x, y, size, delay in estrellas:
        star_parts.append(
            f"<span class='star' style='left:{x:.2f}%;top:{y:.2f}%;width:{size}px;height:{size}px;animation-delay:{delay:.2f}s'></span>"
        )

    for i in range(len(estrellas) - 1):
        x1, y1 = estrellas[i][0], estrellas[i][1]
        x2, y2 = estrellas[i + 1][0], estrellas[i + 1][1]
        dx = x2 - x1
        dy = y2 - y1
        distance = (dx * dx + dy * dy) ** 0.5
        angle = math.degrees(math.atan2(dy, dx))
        star_parts.append(
            f"<span class='line' style='left:{x1:.2f}%;top:{y1:.2f}%;width:{distance:.2f}%;transform:rotate({angle:.2f}deg)'></span>"
        )

    star_parts.extend([
        "<div class='planet'></div>",
        f"<div class='love'>💖 {html_escape_simple(contenido_cielo.get('titulo','Hoy también hay una estrella para ti.'))}</div>",
        "<div class='footer'>Hecha con cariño · cambia automáticamente con la fecha de Colombia 🇨🇴</div>",
        "</div>",
        "</body>",
        "</html>"
    ])

    components.html("".join(star_parts), height=445, scrolling=False)

    st.write("")
    st.markdown(f"""
    <div class="quote-card">
        <span class="quote-mark">✦</span>
        Hoy la constelación lleva tu nombre simbólicamente. No importa que el día cambie;
        la intención detrás de esta página permanece: recordarte cuánto vales.
        <br><br>
        <b>{html_escape_simple(contenido_cielo['titulo'])}</b>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 19: SORPRESA DEL DÍA (NUEVA)
# ==============================================================================
with tab19:
    st.markdown("<h3 style='color: #d63384;'>💝 Sorpresa del Día para Mi Reina</h3>", unsafe_allow_html=True)
    st.write("Cada día guarda un mensaje especial, como una carta que se abre con el corazón. 💌")
    
    mensajes_sorpresa = [
        "Hoy la luna brilla más porque tú estás en mi vida. 🌙",
        "Tu sonrisa es mi combustible para seguir soñando. ☀️",
        "Eres la protagonista de mi historia favorita. 📖",
        "No importa la distancia, mi corazón late al ritmo del tuyo. 💓",
        "Cada página de este diario es un verso dedicado a ti. 🖋️",
        "Si pudiera darte algo, te daría la certeza de que eres increíble. 🌟",
        "Hoy solo quiero que sepas que eres mi mayor orgullo. 👑",
        "Tu esfuerzo en TQ y en la U me inspira cada día. 💼🎓",
        "Eres la razón por la que este diario existe. 💌",
        "Que tu día esté lleno de paz y pequeñas alegrías. 🕊️",
        "Eres más fuerte de lo que crees, y más amada de lo que imaginas. 💖",
        "Cada amanecer es una oportunidad para recordarte lo valiosa que eres. 🌅",
        "Tu constancia es admirable, tu corazón es gigante. 🧸",
        "Hoy, mañana y siempre, estoy orgulloso de ti. ✨",
        "Nada ni nadie puede opacar tu luz. 🌟",
        "Eres la mujer más hermosa, por dentro y por fuera. 🌷",
        "Gracias por ser tú, simplemente tú. 🦋",
        "Tus sueños son importantes, y yo creo en ellos. 🚀",
        "La distancia es solo un número, el cariño es infinito. 🏔️",
        "Hoy es un buen día para sonreír, porque existes. 😊"
    ]
    
    dia_actual = datetime.now(tz_colombia).timetuple().tm_yday
    mensaje_hoy = mensajes_sorpresa[dia_actual % len(mensajes_sorpresa)]
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #fff0f5, #ffe3ec); 
                border-radius: 30px; padding: 40px 30px; 
                border: 3px dashed #ff85a1; 
                box-shadow: 0 15px 35px rgba(255,77,109,0.2);
                text-align: center;'>
        <div style='font-size: 3rem;'>💌</div>
        <p style='font-size: 1.6rem; font-weight: bold; color: #c2185b; margin: 15px 0;'>
            {mensaje_hoy}
        </p>
        <p style='color: #6f6170; font-size: 1.1rem;'>
            — Un pensamiento que nace hoy, justo para ti —
        </p>
        <div style='margin-top: 20px; font-size: 2.5rem;'>
            🧸🦋✨
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("🎁 Abrir la sorpresa extra", key="sorpresa_extra"):
        st.balloons()
        st.snow()
        st.success("¡Sorpresa! Este es un abrazo virtual desde Medellín. 🧸🦋")
        lanzar_efecto_fiesta_js("lluvia_corazones_3d")

# ==============================================================================
# FIN DEL CÓDIGO
# ==============================================================================
