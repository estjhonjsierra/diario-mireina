python
import streamlit as st
import streamlit.components.v1 as components
import json
import os
from datetime import datetime, timedelta, date
import pytz
import io
import random
from pathlib import Path
import math
import colorsys  # <--- NUEVO: para colores del día

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

# ==============================================================================
# 1B. RUTAS ROBUSTAS PARA GITHUB / STREAMLIT CLOUD
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent

def ruta_asset(nombre: str) -> Path:
    """Devuelve la ruta absoluta de un archivo que vive junto a app.py."""
    return BASE_DIR / nombre

PORTADA_CANDIDATAS = [
    ruta_asset("portada.jpg"),
    ruta_asset("portada.jpeg"),
    ruta_asset("portada.png"),
]
PORTADA_PATH = next((p for p in PORTADA_CANDIDATAS if p.is_file()), None)
PORTADA_RELATIVA = PORTADA_PATH.relative_to(BASE_DIR).as_posix() if PORTADA_PATH is not None else None

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
# FUNCIÓN PARA COLOR DEL DÍA (AUTOMÁTICO Y ÚNICO)
# ==============================================================================
def color_del_dia(fecha):
    """Genera un color pastel único basado en el día del año."""
    dia_ano = fecha.timetuple().tm_yday
    hue = (dia_ano * 137.508) % 360  # ángulo dorado
    r, g, b = colorsys.hls_to_rgb(hue/360, 0.78, 0.72)
    return f"hsl({hue:.0f}, 75%, 82%)"

fondo_del_dia = color_del_dia(fecha_actual_colombia)

# ==============================================================================
# 3. ESTILOS CSS AVANZADOS CON COLOR DINÁMICO
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

/* Fondo dinámico: se combina el tema elegido con el color del día */
.stApp {{
    background: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.4) 0%, {fondo_del_dia} 80%) !important;
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
    transition: transform 0.3s ease, box-shadow 0.3s ease;
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
# Los mensajes de agosto ya están en tu código original. Yo los mantengo.
# Solo amplío las listas de SALUDOS_61, REFLEXIONES_61, BENDICIONES_61 y CIERRES_61
# para que los mensajes sean mucho más largos y profundos.
# ==============================================================================

# ==============================================================================
# 6B. MOTOR DEFINITIVO DE SEPTIEMBRE + OCTUBRE 2026 (61 DÍAS EXACTOS)
# ==============================================================================
CICLO_INICIO_61 = date(2026, 9, 1)
CICLO_FIN_61 = date(2026, 10, 31)
CICLO_TOTAL_61 = (CICLO_FIN_61 - CICLO_INICIO_61).days + 1  # 61

TEMAS_61 = [
    "La mujer que no se rinde", "Pequeñas victorias", "La calma también es progreso", "Orgullo por tu camino",
    "La fuerza de seguir", "Tu sonrisa como refugio", "Sueños que toman forma", "Tu manera de cuidar",
    "Elegancia para afrontar el día", "Lo que haces sí importa", "Un respiro para el alma", "Confianza en tus capacidades",
    "La belleza de tu constancia", "Una pausa merecida", "Coraje para los días difíciles", "Tu luz en medio de la rutina",
    "Celebrar sin culpa", "Una página para agradecer", "La distancia no borra el cariño", "Tu futuro empieza hoy",
    "El valor de ser auténtica", "Una noche para soltar", "Todo lo que ya has logrado", "Tu corazón también necesita descanso",
    "Un abrazo convertido en palabras", "Tu esfuerzo silencioso", "La magia de lo cotidiano", "Fe para continuar",
    "No tienes que poder con todo", "La mujer detrás de los logros", "Una razón para sonreír", "Tu historia merece ternura",
    "Serenidad para tomar decisiones", "Tu próxima victoria", "Cuidarte también es avanzar", "El orgullo de lo construido",
    "Una mirada amable hacia ti", "Lo que hoy parece pequeño", "Tu disciplina tiene frutos", "La esperanza de lo que viene",
    "Tu hogar, tu refugio", "La alegría de compartir", "Una meta a la vez", "La fuerza de volver a empezar",
    "Tu talento merece reconocimiento", "Un día con intención", "La ternura de los detalles", "No olvides celebrar tu proceso",
    "Un futuro que se acerca", "Tu mejor versión no necesita prisa", "Paz para cerrar el día", "Una sonrisa desde la distancia",
    "Tu constancia habla por ti", "Hay belleza en perseverar", "Lo que mereces escuchar", "La tranquilidad de confiar",
    "Un capítulo nuevo", "Tu corazón sabe el camino", "La mujer que admiro", "Un último impulso",
    "Cierre de un ciclo maravilloso"
]

# ==============================================================================
# LISTAS AMPLIADAS PARA MENSAJES MÁS LARGOS Y PROFUNDOS (8 frases cada una)
# ==============================================================================
SALUDOS_61 = [
    "Mi reina hermosa, hoy quiero recordarte algo sencillo pero inmenso: no tienes que demostrar tu valor cada minuto; ya eres valiosa.",
    "Mi vida, abre esta página despacio. Hoy no viene a exigirte nada, viene a acompañarte.",
    "Reina, hay días para conquistar el mundo y otros para respirar. Ambos días cuentan.",
    "Hoy pensé en ti y en todo lo que haces sin hacer ruido. Por eso esta página lleva tu nombre.",
    "Mi reina, cuando la rutina corra demasiado, vuelve aquí un momento y recuerda quién eres.",
    "Hoy quiero celebrar a la mujer que sigue adelante incluso cuando nadie ve todo el esfuerzo que hay detrás.",
    "Esta página es un abrazo convertido en palabras, escrito para acompañarte en el momento exacto en que la abras.",
    "Reina hermosa, tu historia no se mide solo por resultados; también por la valentía con la que atraviesas cada día.",
    # NUEVAS FRASES (más profundas)
    "Mi amor, hoy el universo conspira para recordarte lo extraordinaria que eres en cada detalle de tu vida. Cada amanecer es un recordatorio de que tienes el poder de crear un día hermoso.",
    "Querida reina, cuando el cansancio intente robarte la sonrisa, recuerda que hay alguien que te admira no solo por lo que haces, sino por quien eres en esencia.",
    "Eres como la luna en la noche: iluminas incluso en los momentos más oscuros. Nunca lo olvides. Tu luz es única y necesaria en este mundo.",
    "Hoy no necesitas ser perfecta, solo necesitas ser tú. Y eso ya es más que suficiente. Tu autenticidad es tu mayor fortaleza.",
]

REFLEXIONES_61 = [
    "Tu vida está hecha de decisiones pequeñas que, juntas, están construyendo algo grande. Sigue a tu ritmo.",
    "No minimices el cansancio ni los logros. Ambos cuentan una parte real de tu historia y ambos merecen respeto.",
    "Hay una versión de ti en el futuro que un día agradecerá muchísimo que hoy hayas decidido no rendirte.",
    "La verdadera fortaleza no siempre se ve como correr. A veces se parece más a detenerse, respirar y volver a empezar.",
    "Todo lo que estás aprendiendo, trabajando y cuidando está formando una vida que merece ser celebrada.",
    "No necesitas tener todo resuelto para estar avanzando. Basta con seguir dando un paso honesto cada día.",
    "Cuando dudes de ti, recuerda cuántas veces ya has superado jornadas que alguna vez parecieron demasiado grandes.",
    "Tu ternura no contradice tu fuerza. Precisamente esa mezcla tan tuya es una de las cosas más bonitas que admiro.",
    # NUEVAS FRASES (más profundas)
    "Cada obstáculo que has superado te ha hecho más fuerte, más sabia y más hermosa por dentro. No hay tropiezo que no te haya enseñado algo valioso.",
    "La vida no se trata de esperar a que pase la tormenta, sino de aprender a bailar bajo la lluvia. Y tú bailas increíble, con una gracia que inspira.",
    "Tu capacidad para amar y cuidar a los demás es un reflejo de la luz inmensa que llevas dentro. Eso te convierte en una persona excepcional.",
    "A veces el silencio es la mejor respuesta, y en él se esconden las reflexiones más profundas. Permítete escuchar lo que tu corazón necesita decirte.",
]

BENDICIONES_61 = [
    "Que Dios bendiga tus decisiones, proteja tu hogar y multiplique las oportunidades bonitas que lleguen a tu vida.",
    "Que hoy encuentres serenidad en medio de la rutina, personas que sumen y motivos sinceros para sonreír.",
    "Que tu camino tenga luz cuando necesites escoger una dirección, y paciencia cuando las cosas tarden un poco más.",
    "Que la paz llegue primero a tu corazón y después a todo aquello que tengas que resolver.",
    "Que nunca te falte una razón para volver a creer en tus sueños, incluso cuando el día se sienta pesado.",
    "Que esta noche puedas cerrar los ojos con la tranquilidad de saber que hiciste lo mejor que pudiste.",
    "Que tu hogar siga siendo un lugar de amor, risas, descanso y recuerdos bonitos.",
    "Que el futuro te sorprenda con oportunidades que hoy todavía no imaginas.",
    # NUEVAS FRASES (más profundas)
    "Que cada paso que des te acerque más a la mujer que sueñas ser, con la certeza de que ya estás en el camino correcto.",
    "Que el universo te devuelva en abundancia toda la bondad que siembras en cada persona que toca tu vida.",
    "Que encuentres motivos para sonreír incluso en los días grises, porque tu luz es más fuerte que cualquier nube.",
    "Que la vida te regale momentos de pura felicidad que se conviertan en los recuerdos más hermosos de tu historia.",
]

CIERRES_61 = [
    "Y desde Medellín te mando un abrazo enorme hasta Bucaramanga. ❤️",
    "No importa cuántos kilómetros marque el mapa: hoy también estoy cerquita de ti en pensamiento. ✈️💖",
    "Descansa, sonríe y sigue siendo esa mujer increíble que admiro tanto. 👑",
    "Te quiero, te respeto y me encanta poder acompañarte aunque sea a través de estas páginas. 🌷",
    "Qué bonito sería poder decirte esto frente a frente; mientras llega ese momento, aquí queda escrito. 💌",
    "Cierra esta página sabiendo que alguien está profundamente orgulloso de ti. ✨",
    "Mañana habrá una nueva página. Por hoy, quédate con esta: eres muchísimo más capaz de lo que a veces crees. 🌙",
    "Con todo mi cariño, admiración y un pedacito de mi corazón en cada palabra. 💖",
    # NUEVAS FRASES (más profundas)
    "Hasta que la distancia se convierta en un abrazo, estas palabras serán el puente que nos une. Te llevo en mi corazón como el pensamiento más hermoso.",
    "Cada noche que cae es un recordatorio de que un nuevo día traerá nuevas razones para sonreír. Descansa con la paz de saber que eres profundamente amada.",
    "Te llevo en mi corazón como el pensamiento más hermoso, incluso cuando la rutina intenta robarme el tiempo para pensar en ti.",
    "Eres mi razón para creer que el amor trasciende cualquier frontera. Te quiero hoy, mañana y siempre. Que sueñes con los ángeles, mi reina.",
]

RETOS_61 = [
    "Regálate diez minutos sin celular y toma tu bebida favorita con calma.",
    "Anota mentalmente tres cosas que hiciste bien hoy.",
    "Haz una pausa, estira los hombros y respira profundamente tres veces.",
    "Escucha una canción que te haga sonreír y deja que el día baje de velocidad.",
    "Antes de dormir, di en voz alta una meta que te emocione.",
    "Haz algo pequeño por ti sin sentir que tienes que merecerlo primero.",
    "Mira una foto que te haga feliz y agradece ese recuerdo.",
    "Cierra el día perdonándote cualquier pendiente que no haya podido salir perfecto.",
]

CANCIONES_61 = [
    ("Sin Miedo 🎶", "Canción especial para recordarte que tus sueños merecen valentía."),
    ("Bésame 💋", "Una dedicatoria romántica para una tarde o noche tranquila."),
    ("Inolvidable - Beéle 🌴", "Una vibra cálida para acompañar una sonrisa."),
    ("Destino o Casualidad - Melendi ✨", "Porque algunas historias llegan cuando uno menos lo espera."),
    ("Bonito - Jarabe de Palo 🌸", "Para recordarte que lo bonito también vive en los días sencillos."),
    ("Color Esperanza - Diego Torres 🌈", "Un empujoncito de optimismo para seguir adelante."),
    ("Vivir Mi Vida - Marc Anthony 💃", "Para celebrar que cada día trae una oportunidad nueva."),
]

ESCENAS_61 = [
    ("🌅", "Amanecer de Rosas", "linear-gradient(135deg,#fff8fb 0%,#ffd7e6 45%,#f5afc8 100%)", "#c2185b"),
    ("🌌", "Noche Lavanda", "linear-gradient(135deg,#f6f0ff 0%,#e4d7ff 45%,#cdb9ff 100%)", "#6d28d9"),
    ("🌇", "Atardecer Dorado", "linear-gradient(135deg,#fffaf0 0%,#ffe2b8 45%,#ffc5a3 100%)", "#a9550a"),
    ("🌸", "Jardín Suave", "linear-gradient(135deg,#f5fff9 0%,#ddf7ea 48%,#ffdcea 100%)", "#167a56"),
    ("☕", "Café y Calma", "linear-gradient(135deg,#fffaf6 0%,#f3e3d5 48%,#e9cbbb 100%)", "#7b5135"),
    ("🦋", "Cielo Azul", "linear-gradient(135deg,#f5fcff 0%,#ddf2ff 48%,#c7e4fb 100%)", "#145c97"),
    ("✨", "Cielo de Estrellas", "linear-gradient(135deg,#f2f4ff 0%,#dce6ff 48%,#c6d1ff 100%)", "#3046a0"),
]

def contenido_61_dias(fecha_obj):
    if CICLO_INICIO_61 <= fecha_obj <= CICLO_FIN_61:
        idx = (fecha_obj - CICLO_INICIO_61).days
    else:
        idx = (fecha_obj - CICLO_INICIO_61).days % CICLO_TOTAL_61
    weekday = fecha_obj.weekday()
    enfoques = [
        "💼 Lunes de nuevo comienzo", "🌸 Martes para avanzar", "✨ Miércoles para respirar",
        "🌷 Jueves para confiar", "🎉 Viernes para celebrar", "🧸 Sábado para disfrutar", "🕊️ Domingo para agradecer"
    ]
    escena = ESCENAS_61[idx % len(ESCENAS_61)]
    cancion = CANCIONES_61[idx % len(CANCIONES_61)]
    texto = "\n\n".join([
        SALUDOS_61[idx % len(SALUDOS_61)],
        REFLEXIONES_61[(idx * 3 + 1) % len(REFLEXIONES_61)],
        BENDICIONES_61[(idx * 5 + 2) % len(BENDICIONES_61)],
        CIERRES_61[(idx * 7 + 3) % len(CIERRES_61)],
    ])
    reto = RETOS_61[(idx * 11 + 1) % len(RETOS_61)]
    return {
        "fecha_str": fecha_es_61(fecha_obj),
        "titulo": f"{enfoques[weekday]} · {TEMAS_61[idx % len(TEMAS_61)]}",
        "poema": texto,
        "reto": f"🌸 {reto}",
        "cancion": {"titulo": cancion[0], "desc": cancion[1]},
        "dia_n": idx + 1,
        "porcentaje": int(round(((idx + 1) / CICLO_TOTAL_61) * 100)),
        "escena": escena,
        "sello": f"Página {idx + 1:02d} de 61",
    }

def fecha_es_61(fecha_obj):
    dias = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
    meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    return f"{dias[fecha_obj.weekday()].capitalize()}, {fecha_obj.day:02d} de {meses[fecha_obj.month - 1]} de {fecha_obj.year}"

MENSAJES_61 = {}
RETOS_61_MAP = {}
CANCIONES_61_MAP = {}
FECHA_CURSOR_61 = CICLO_INICIO_61
while FECHA_CURSOR_61 <= CICLO_FIN_61:
    c = contenido_61_dias(FECHA_CURSOR_61)
    k = FECHA_CURSOR_61.strftime("%Y-%m-%d")
    MENSAJES_61[k] = c
    RETOS_61_MAP[k] = c["reto"]
    CANCIONES_61_MAP[k] = c["cancion"]
    FECHA_CURSOR_61 += timedelta(days=1)

# Actualizar los diccionarios principales con los mensajes de 61 días
MENSAJES_DIARIOS.update(MENSAJES_61)
RETOS_DIARIOS.update(RETOS_61_MAP)
CANCIONES_DIARIAS.update(CANCIONES_61_MAP)

# ==============================================================================
# 6C. VARIABLES DEL DÍA PARA TODA LA APLICACIÓN
# ==============================================================================
FECHA_HOY_CO = datetime.now(tz_colombia)
HOY_CO = FECHA_HOY_CO.date()
CLAVE_HOY = HOY_CO.strftime("%Y-%m-%d")
CONTENIDO_HOY_61 = MENSAJES_61.get(CLAVE_HOY)
if CONTENIDO_HOY_61 is None:
    CONTENIDO_HOY_61 = contenido_61_dias(HOY_CO)
ESCENA_HOY_61 = CONTENIDO_HOY_61["escena"]
DIAS_CICLO_TRANSCURRIDOS = CONTENIDO_HOY_61["dia_n"]
DIAS_RESTANTES_61 = max(CICLO_TOTAL_61 - DIAS_CICLO_TRANSCURRIDOS, 0)
PAGINA_PORCENTAJE_61 = CONTENIDO_HOY_61["porcentaje"]

# ==============================================================================
# 6D. HORA / MOMENTO DEL DÍA
# ==============================================================================
def momento_del_dia_61(hora):
    if 5 <= hora < 12:
        return "☀️ Buenos días"
    if 12 <= hora < 18:
        return "🌤️ Buenas tardes"
    if 18 <= hora < 23:
        return "🌙 Buenas noches"
    return "✨ Madrugada"

MOMENTO_HOY_61 = momento_del_dia_61(FECHA_HOY_CO.hour)

# ==============================================================================
# 6E. AUDIO OPCIONAL PARA REPRODUCIR MÚSICA
# ==============================================================================
AUDIO_CANDIDATAS = {
    "Sin Miedo": [ruta_asset("sin_miedo.mp3"), ruta_asset("sin_miedo.wav"), ruta_asset("sin_miedo.ogg")],
    "Bésame": [ruta_asset("besame.mp3"), ruta_asset("besame.wav"), ruta_asset("besame.ogg")],
    "Diaria": [ruta_asset("cancion_diaria.mp3"), ruta_asset("cancion_diaria.wav"), ruta_asset("cancion_diaria.ogg")],
}

def encontrar_audio(nombre):
    for candidato in AUDIO_CANDIDATAS.get(nombre, []):
        if candidato.is_file():
            return candidato
    return None

AUDIO_DIARIA = encontrar_audio("Diaria")
AUDIO_SIN_MIEDO = encontrar_audio("Sin Miedo")
AUDIO_BESAME = encontrar_audio("Bésame")

# Helper seguro para insertar texto en HTML
def html_escape_61(texto):
    return (str(texto).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;"))

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
# 8. ENCABEZADO PRINCIPAL, BARRA DE MÚSICA & BANNER SORPRESA
# ==============================================================================
st.markdown("<h1 class='main-header'>👑 El Diario de Mi Reina 💖🧸🦋</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>De Medellín a Bucaramanga 🏔️✈️✨ | Un espacio lleno de magia, recuerdos y momentos especiales</p>", unsafe_allow_html=True)
st.markdown(f"<div class='theme-badge'>🎨 Tema Activo: {st.session_state['user_theme']} | Tipografía: {st.session_state['user_font']}</div>", unsafe_allow_html=True)

# Ejecución de efectos si se solicitaron
if st.session_state["efecto_fiesta_actual"]:
    lanzar_efecto_fiesta_js(st.session_state["efecto_fiesta_actual"])
    st.session_state["efecto_fiesta_actual"] = None

st.write("---")

# ==============================================================================
# ESTILOS DELUXE ADICIONALES
# ==============================================================================
st.markdown("""
<style>
.deluxe-shell { position:relative; overflow:hidden; border-radius:32px; padding:30px; margin:10px 0 24px 0; background:linear-gradient(135deg,rgba(255,255,255,.96),rgba(255,232,240,.92)); border:1px solid rgba(216,63,120,.22); box-shadow:0 24px 60px rgba(80,35,62,.12); }
.deluxe-kicker { display:inline-flex; padding:7px 13px; border-radius:999px; background:#fff4f8; color:#a61d52; font-size:.82rem; font-weight:800; }
.deluxe-title { color:#9b1d4f; font-size:clamp(2rem,4vw,3.5rem); font-weight:900; line-height:1.08; margin:14px 0 6px; }
.deluxe-subtitle { color:#604e5e; font-size:1.02rem; max-width:860px; }
.daily-orbit { display:grid; grid-template-columns:1.35fr .9fr .85fr; gap:14px; margin-top:20px; }
.orbit-card { min-height:145px; padding:20px; border-radius:24px; background:rgba(255,255,255,.78); border:1px solid rgba(216,63,120,.16); box-shadow:0 12px 28px rgba(80,35,62,.08); transition:transform .25s ease,box-shadow .25s ease; }
.orbit-card:hover { transform:translateY(-4px); box-shadow:0 18px 36px rgba(80,35,62,.13); }
.orbit-label { color:#876f7e; font-size:.74rem; font-weight:800; text-transform:uppercase; letter-spacing:.08em; }
.orbit-date { color:#b02059; font-size:1.55rem; font-weight:900; margin-top:7px; line-height:1.2; }
.orbit-card strong { color:#9b1d4f; }
.mini-pill-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
.mini-pill { padding:6px 10px; border-radius:999px; background:#fff7fa; border:1px solid #f4d2df; color:#765f6d; font-size:.82rem; font-weight:700; }
.progress-track { width:100%; height:10px; background:#fff; border-radius:999px; overflow:hidden; margin-top:11px; border:1px solid #f0d5df; }
.progress-fill { height:100%; border-radius:999px; background:linear-gradient(90deg,#ff96b6,#d83f78,#a61d52); }
.quote-card { margin-top:16px; padding:20px 22px; border-radius:24px; border:1px dashed rgba(166,29,82,.38); background:rgba(255,255,255,.7); color:#4d3a48; }
.quote-mark { font-size:3rem; line-height:.6; color:#e64c82; vertical-align:middle; margin-right:7px; }
@media(max-width:900px) { .daily-orbit { grid-template-columns:1fr; } }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 8B. BANNER DELUXE CON MENSAJE PROFUNDO
# ==============================================================================
st.markdown(f"""
<div class="deluxe-shell">
    <div class="deluxe-kicker">{ESCENA_HOY_61[0]} EDICIÓN ESPECIAL · {CONTENIDO_HOY_61['sello']}</div>
    <div class="deluxe-title">Hoy también escribí algo para ti, mi reina. 👑</div>
    <p class="deluxe-subtitle">Una página nueva cada día durante septiembre y octubre. El contenido se actualiza solo con la fecha de Colombia.</p>
    <div class="daily-orbit">
        <div class="orbit-card lift">
            <div class="orbit-label">Fecha de hoy</div>
            <div class="orbit-date">{CONTENIDO_HOY_61['fecha_str']}</div>
            <div class="mini-pill-row">
                <span class="mini-pill">{MOMENTO_HOY_61}</span>
                <span class="mini-pill">🇨🇴 Colombia · {FECHA_HOY_CO.strftime('%H:%M:%S')}</span>
            </div>
        </div>
        <div class="orbit-card lift">
            <div class="orbit-label">Maratón septiembre + octubre</div>
            <strong style="font-size:1.6rem;">{PAGINA_PORCENTAJE_61}%</strong>
            <div class="progress-track"><div class="progress-fill" style="width:{PAGINA_PORCENTAJE_61}%;"></div></div>
            <div style="margin-top:10px;color:#6f6170;">Quedan <b>{DIAS_RESTANTES_61}</b> días dentro del ciclo.</div>
        </div>
        <div class="orbit-card lift">
            <div class="orbit-label">Página de hoy</div>
            <strong style="font-size:1.6rem;">{DIAS_CICLO_TRANSCURRIDOS} / 61</strong>
            <div style="margin-top:8px;color:#6f6170;">Una página diferente, una razón más para sonreír.</div>
        </div>
    </div>
    <div class="quote-card">
        <span class="quote-mark">“</span>
        <strong>"{CONTENIDO_HOY_61['titulo']}"</strong>
        <div style="margin-top:8px;color:#5d4d59;">{CONTENIDO_HOY_61['fecha_str']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("---")

# ==============================================================================
# 9. MENÚ PRINCIPAL DE 19 PESTAÑAS
# ==============================================================================
tabs = st.tabs([
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
    "💝 Sorpresa"
])

# ==============================================================================
# TAB 1: PORTADA (con mensaje largo y profundo)
# ==============================================================================
with tabs[0]:
    col_texto, col_foto = st.columns([1.15, 0.85], gap="large")
    
    with col_texto:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #d63384; margin-bottom: 10px; font-size: 1.55em;'>
                ¡Bienvenida a tu espacio consentido, Mi Reina! <span class='floating-badge'>👑🧸🦋</span>
            </h3>
            <p style='color: #222; font-size: 1.1em; line-height: 1.8;'>
                Este diario interactivo fue diseñado con todo el amor del mundo para acompañarte en tus metas en 
                <b>TQ</b>, tus jornadas de estudio en <b>Administración de Empresas</b> y en cada uno de tus momentos libres, 
                alegres y especiales. ¡Un rincón mágico para recordarte lo mucho que vales, en todo momento, de día y de noche! ✨💖
            </p>
        </div>
        """, unsafe_allow_html=True)

        # CÁLCULO DINÁMICO DE HOY EN HORA COLOMBIA
        fecha_colombia = datetime.now(tz_colombia)
        fecha_hoy_key = fecha_colombia.strftime("%Y-%m-%d")
        
        mensaje_hoy = MENSAJES_DIARIOS.get(fecha_hoy_key, {
            "fecha_str": fecha_colombia.strftime("%A, %d de %B"),
            "titulo": "✨ Un mensaje especial para ti",
            "poema": "Mi reina hermosa, recuerda siempre lo increíble, inteligente y hermosa que eres. Cada día y cada noche es una nueva oportunidad para acercarte a tus sueños. ¡Te quiero con todo mi corazón!"
        })

        reto_hoy = RETOS_DIARIOS.get(fecha_hoy_key, "🌸 Reto de Hoy: Tómate 10 minutos para consentirte y tomar tu bebida favorita en calma.")
        cancion_hoy = CANCIONES_DIARIAS.get(fecha_hoy_key, {"titulo": "Inolvidable - Beéle 🎶", "desc": "Una melodía llena de sol y buena vibra para ti."})

        # TARJETA DEL MENSAJE DIARIO (sin "Actualización Automática")
        st.markdown(f"""
        <div class='daily-card'>
            <span style='background-color: #ff85a1; color: white; padding: 8px 18px; border-radius: 16px; font-weight: bold; font-size: 1.05em;'>
                📅 {mensaje_hoy['fecha_str']} · Un día especial para ti, mi reina 💖
            </span>
            <h3 style='color: #c2185b; margin-top: 18px; margin-bottom: 14px; font-size: 1.5em;'>{mensaje_hoy['titulo']}</h3>
            <p style='color: #222; font-size: 1.15em; line-height: 1.85; white-space: pre-line;'>
            {mensaje_hoy['poema']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col_m_extra1, col_m_extra2 = st.columns(2)
        with col_m_extra1:
            st.markdown(f"""
            <div style='background: white; border-radius: 20px; padding: 18px; border: 2px solid #ff85a1; box-shadow: 0 6px 20px rgba(0,0,0,0.05);'>
                <h4 style='color: #d63384; margin-top: 0;'>🎵 Canción del Día:</h4>
                <b>{cancion_hoy['titulo']}</b>
                <p style='font-size: 0.9em; color: #555; margin-top: 4px;'>{cancion_hoy['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_m_extra2:
            st.markdown(f"""
            <div style='background: white; border-radius: 20px; padding: 18px; border: 2px solid #fb923c; box-shadow: 0 6px 20px rgba(0,0,0,0.05);'>
                <h4 style='color: #c2410c; margin-top: 0;'>✨ Desafío Bonito de Hoy:</h4>
                <p style='font-size: 0.92em; color: #333; margin: 0;'>{reto_hoy}</p>
            </div>
            """, unsafe_allow_html=True)

        # ==================================================
        # REPRODUCTOR DE MÚSICA CON AUTOPLAY (en la Portada)
        # ==================================================
        st.write("---")
        st.markdown("<h4 style='color: #d63384;'>🎵 Canción Especial para Hoy</h4>", unsafe_allow_html=True)
        
        if AUDIO_DIARIA:
            # Convertir Path a string para la URL
            audio_url = str(AUDIO_DIARIA)
            
            # Determinar el tipo MIME según la extensión
            if audio_url.endswith('.mp3'):
                mime_type = 'audio/mpeg'
            elif audio_url.endswith('.wav'):
                mime_type = 'audio/wav'
            elif audio_url.endswith('.ogg'):
                mime_type = 'audio/ogg'
            else:
                mime_type = 'audio/mpeg'
            
            # Crear reproductor con autoplay y controles visibles
            audio_html = f"""
            <audio controls autoplay style="width:100%; margin-top:10px; border-radius: 12px;">
                <source src="{audio_url}" type="{mime_type}">
                Tu navegador no soporta audio HTML5.
            </audio>
            <p style='font-size:0.9rem; color:#888; margin-top:6px;'>
                💖 Si no se reproduce automáticamente, haz clic en el botón de play.
            </p>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
            st.caption("🎶 Canción dedicada con todo el cariño desde Medellín.")
        else:
            st.info("🎧 No encontré un archivo de música. Sube una canción con el nombre `cancion_diaria.mp3` (o .wav, .ogg) a la raíz del repositorio.")
            st.markdown("**Instrucciones:**")
            st.markdown("1. Elige tu canción favorita y renómbrala como `cancion_diaria.mp3`.")
            st.markdown("2. Súbela a la carpeta raíz de tu repositorio de GitHub (junto a `app.py`).")
            st.markdown("3. Después de subirla, recarga esta página y aparecerá el reproductor.")

        # Botones mágicos (los mismos que ya tenías)
        st.write("---")
        st.markdown("<h3 style='color: #d63384; font-size: 1.4em;'>🌸 Botones Mágicos & Variedad de Celebración ✨</h3>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🎉 Fiesta Mágica Multi-Efecto"):
                st.balloons()
                st.snow()
                efectos = ["confetti_boom", "lluvia_emojis", "fuegos_artificiales", "estrellas_doradas", "lluvia_corazones_3d", "burbujas_magicas"]
                st.session_state["efecto_fiesta_actual"] = random.choice(efectos)
                st.rerun()

        with col_btn2:
            if st.button("🦋 Mensaje Sorpresa"):
                st.balloons()
                st.session_state["mensaje_sorpresa_actual"] = random.choice(FRASES_ESCRITAS_POR_TI)
                st.session_state["iconos_combo_actual"] = random.choice(COMBOS_ICONOS)

        with col_btn3:
            if st.button("⭐ Registrar Sonrisa 😊"):
                st.session_state["sonrisas_count"] += 1
                st.toast("¡Sonrisa registrada! Gracias por alegrar el mundo. 😊✨")
                st.balloons()

        if "mensaje_sorpresa_actual" in st.session_state:
            combo_icons = st.session_state.get("iconos_combo_actual", "🧸🦋✨")
            st.markdown(f"""
            <div style='background: #ffffff; border-radius: 24px; padding: 22px; border: 2.5px dashed #ff4d6d; margin-top: 20px; text-align: center; box-shadow: 0 12px 28px rgba(255, 77, 109, 0.18);'>
                <div style='font-size: 1.6em; margin-bottom: 8px;'>{combo_icons}</div>
                <p style='color: #d63384; font-weight: bold; margin-bottom: 6px;'>Nota especial escrita para ti:</p>
                <b>{st.session_state['mensaje_sorpresa_actual']}</b>
            </div>
            """, unsafe_allow_html=True)

    with col_foto:
        st.markdown("""
        <div class='photo-card-moving'>
            📸 Fotos Flotantes & Momentos Inolvidables ❤️
            <p style='font-size: 0.85em; font-weight: normal; margin-top: 4px; color: #666;'>
                (Levitando con tus recuerdos más especiales)
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        if PORTADA_PATH is not None:
            st.image(
                str(PORTADA_PATH),
                caption="¡Siempre juntos, mi reina hermosa! ❤️",
                use_container_width=True,
            )
        else:
            st.warning(
                "No encontré portada.jpg, portada.jpeg ni portada.png junto a app.py. "
                "Sube la foto al mismo nivel que app.py en GitHub."
            )

        st.markdown("""
        <div style='background: white; border-radius: 20px; padding: 18px; margin-top: 18px; border: 2px solid #ffb6c1; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.05);'>
            <p style='margin:0; color:#333; font-size: 1.05em;'>
                📍 <b>Ruta Especial:</b> Medellín ✈️ Bucaramanga<br>
                🧸 <b>Estado Actual:</b> Pensándote 24/7 con ositos y mariposas
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 15: CARTA DE HOY (con mensaje largo)
# ==============================================================================
with tabs[14]:
    st.markdown("<h3 style='color:#d63384;'>💌 Carta de Hoy</h3>", unsafe_allow_html=True)
    st.write("Una carta que cambia automáticamente cada día del ciclo de 61 días.")
    st.write("---")
    st.markdown(f"""
    <div class='card'>
        <div style='font-weight:900;color:#a61d52;font-size:1.2rem;'>{CONTENIDO_HOY_61['titulo']}</div>
        <div style='margin-top:14px;white-space:pre-line;color:#3f3440;line-height:1.95;'>{html_escape_61(CONTENIDO_HOY_61['poema'])}</div>
        <div style='margin-top:22px;color:#a61d52;font-family:cursive;font-size:1.5rem;'>Con cariño, desde Medellín. 💖</div>
    </div>
    """, unsafe_allow_html=True)
    st.info(f"🎯 Reto de hoy: {CONTENIDO_HOY_61['reto']}")
    st.success(f"🎵 Banda sonora: {CONTENIDO_HOY_61['cancion']['titulo']} — {CONTENIDO_HOY_61['cancion']['desc']}")

# ==============================================================================
# TAB 19: SORPRESA DEL DÍA (con reproductor de música adicional)
# ==============================================================================
with tabs[18]:
    st.markdown("<h3 style='color:#d63384;'>💝 Sorpresa del Día</h3>", unsafe_allow_html=True)
    st.write("Un mensaje especial y la canción que te dedico hoy.")
    st.write("---")
    mensajes_sorpresa_2 = [
        "La distancia no impide que una palabra llegue exactamente donde debe. 💌",
        "Hoy el diario te recuerda que descansar también es una forma de avanzar.",
        "Tu sonrisa sigue siendo una de mis imágenes favoritas del día. 😊",
        "Hay cosas que no necesitan explicación; solo necesitan tiempo, respeto y cariño.",
        "Esta página existe porque tú mereces detalles que duren más que un instante. 👑",
        "Hoy la sorpresa es simple: alguien cree muchísimo en ti. ✨",
    ]
    msg = mensajes_sorpresa_2[HOY_CO.toordinal() % len(mensajes_sorpresa_2)]
    st.markdown(f"""
    <div class='card' style='text-align:center;padding:38px;'>
        <div style='font-size:3rem;'>💌</div>
        <div style='font-size:1.45rem;color:#c2185b;font-weight:900;'>{msg}</div>
        <div style='margin-top:14px;color:#6f6170;'>{CONTENIDO_HOY_61['fecha_str']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🎵 Canciones especiales")
    st.write("La música está disponible si subes los archivos a GitHub.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='card'><b>❤️ Sin Miedo</b><br><small>Reproductor disponible cuando exista sin_miedo.mp3 / wav / ogg.</small></div>", unsafe_allow_html=True)
        if AUDIO_SIN_MIEDO:
            st.audio(str(AUDIO_SIN_MIEDO))
    with c2:
        st.markdown("<div class='card'><b>💋 Bésame</b><br><small>Reproductor disponible cuando exista besame.mp3 / wav / ogg.</small></div>", unsafe_allow_html=True)
        if AUDIO_BESAME:
            st.audio(str(AUDIO_BESAME))

# ==============================================================================
# EL RESTO DE LAS PESTAÑAS (las que ya tienes) se mantienen igual.
# No las repito para ahorrar espacio, pero en tu archivo original están completas.
# ==============================================================================

# ... (Tus otras pestañas: Línea del Tiempo, Calendario, Estadísticas, etc.)
