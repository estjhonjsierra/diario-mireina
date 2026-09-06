import streamlit as st
import streamlit.components.v1 as components
import json
import os
from datetime import datetime, timedelta, date
import pytz
import io
import random
from pathlib import Path

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
MENSAJES_DIARIOS = {
    "2026-07-26": {
        "fecha_str": "Domingo, 26 de Julio",
        "titulo": "Un rincón creado con el corazón 🦋🧸🌸",
        "poema": """Mi reina hermosa,
Hoy empieza un detalle hecho a la medida de tu luz. Quería que tuvieras un espacio que te recuerde lo increíble que eres, en todo momento, de día o de noche, incluso cuando la rutina presione. Gracias por ser mi lugar seguro, por tu dedicación impecable en TQ y por construir con tanta valentía tu futuro profesional en Administración. Hoy domingo te deseo calma, alegría y que recuerdes que mi admiración por ti no tiene límites. Te quiero infinitamente."""
    },
    "2026-07-27": {
        "fecha_str": "Lunes, 27 de Julio",
        "titulo": "Fuerza para iniciar la semana 🌸⭐",
        "poema": """Lunes de nuevos comienzos, mi reina.
Sé la disciplina y el compromiso con el que te levantas a dar lo mejor de ti en TQ. Nunca dudes del talento gigantesco que habita en ti ni de lo lejos que vas a llegar. Cuando sientas que la semana pesa, recuerda que aquí hay alguien a cientos de kilómetros sosteniendo tu mano en el pensamiento. ¡A romperla hoy! Te quiero mucho."""
    },
    "2026-07-28": {
        "fecha_str": "Martes, 28 de Julio",
        "titulo": "La calma en tus ojos ✨🧸",
        "poema": """Hay una serenidad única en tu mirada que me devuelve la paz en cualquier momento. Hoy martes solo quiero recordarte que no tienes que poder con todo al mismo tiempo. Vas paso a paso, construyendo un imperio de sueños para ti y tu hijita. Eres elegancia, tenacidad y ternura en una sola persona. Disfruta tu día mi reina hermosa. Te quiero."""
    },
    "2026-07-29": {
        "fecha_str": "Miércoles, 29 de Julio",
        "titulo": "Distancia que acorta el cariño 🏔️✈️",
        "poema": """De Medellín a Bucaramanga hay montañas, pero no hay distancia capaz de apagar lo mucho que te quiero. Mitad de semana, mi administradora estrella. Cada esfuerzo en tus estudios y en tu trabajo es una semilla de un futuro brillante. Te pienso a cada hora y me llena de orgullo decir que eres mi reina."""
    },
    "2026-07-30": {
        "fecha_str": "Jueves, 30 de Julio",
        "titulo": "Luz en el camino 🌸✨",
        "poema": """Casi viernes, mi vida.
Tu sonrisa tiene la magia de iluminar hasta el día más gris. Gracias por tu ternura, por tu escucha y por tu forma tan linda de ser. Que hoy sea un día fluido en el trabajo, donde las cosas salgan a tu favor y donde sientas que todo tu empeño valdrá la pena. Te quiero con todo mi ser."""
    },
    "2026-07-31": {
        "fecha_str": "Viernes, 31 de Julio",
        "titulo": "Rumbo al descanso y tus momentos alegres 💖✨",
        "poema": """¡Llegó el viernes y se cierra Julio!
Sé lo mucho que anhelas el fin de semana para desconectarte, relajarte en tus momentos libres y disfrutar de esos instantes invaluables de felicidad con tu hijita. Que hoy el tiempo se pase volando en el trabajo para que comiences a disfrutar de tu tiempo de paz. ¡Te mereces todo el descanso del mundo! Te quiero mucho."""
    },
    "2026-08-01": {
        "fecha_str": "Sábado, 01 de Agosto",
        "titulo": "Bienvenido Agosto 🌻🧸",
        "poema": """Iniciamos un nuevo mes, mi reina.
Sábado de tranquilidad, de sonreír sin afanes y de regalarte el tiempo libre que tanto trabajas en la semana. Deseo que tu corazón se llene de risas, de desconexión y de esa paz pura de hogar. Disfruta tu fin de semana mi reina bella, te quiero y te pienso a cada segundo."""
    },
    "2026-08-02": {
        "fecha_str": "Domingo, 02 de Agosto",
        "titulo": "La dulzura de tus pausas y el santuario de tu paz 🌸🧸✨",
        "poema": """Mi reina amada, hoy amanece con la calma dulce que solo el domingo sabe regalarnos.
Quiero que te detengas por un momento y respires profundo, sintiendo cómo el aire puro llena tu pecho.
A veces me pongo a reflexionar en todo el universo de cosas que sostienes con tanta gracia y elegancia:
desde tus responsabilidades impecables en Tecnoquímicas (TQ), donde dejas tu sello de excelencia a diario,
hasta las metas tan ambiciosas que construyes noche tras noche en tu carrera de Administración de Empresas,
pasando por el pilar más hermoso y sagrado de tu vida: el amor infinito con el que guías los pasos de tu hijita.

Eres una mujer sencillamente extraordinaria, un ser lleno de una luz que no se apaga con nada.
Quiero que hoy te regales un instante de desconexión absoluta de las exigencias externas.
Un momento donde el café o el té sepan más rico, donde las risas en tu hogar llenen cada rincón,
y donde sientas que no hay afán, no hay prisa y no hay pendientes urgentes que no puedan esperar.

Recuerda que aunque nos separen las montañas entre Medellín y Bucaramanga,
mis pensamientos viajan constantes como una brisa tibia para abrazarte en la distancia.
Eres mi refugio, mi motivo constante de orgullo y la reina absoluta de mi corazón.
Disfruta de la tranquilidad de tu espacio, ríe con el alma y nunca olvides lo infinitamente que te quiero.
Que tu domingo sea un verdadero bálsamo de amor y paz pura."""
    },
    "2026-08-03": {
        "fecha_str": "Lunes, 03 de Agosto",
        "titulo": "El inicio de una semana brillante para mi reina 👑💼💖",
        "poema": """Comienza una nueva semana, mi vida hermosa, y con ella nacen múltiples oportunidades para que deslumbres.
Sé que los lunes a veces traen consigo el peso de los informes, la rutina agitada en Tecnoquímicas y la exigencia,
pero quiero recordarte la mujer extremadamente capaz, perspicaz e infinitamente talentosa que eres.
No existe reto administrativo que te quede grande ni obstáculo que tu tenacidad no pueda superar.

Camina hoy con la frente en alto, vistiendo esa seguridad deslumbrante que te caracteriza
y esa sonrisa magnética que tiene el poder divino de iluminar cualquier oficina o lugar donde estés.
Cuando sientas que la jornada se torna un poco densa o que el cansancio intenta rozar tus alas,
recuerda que a cientos de kilómetros hay alguien que te admira profundamente desde el alma,
alguien que celebra cada uno de tus logros silenciosos y que cuenta las horas para recordarte cuánto vales.

¡A conquistarlo todo hoy, mi administradora estrella!
Te sostengo en la distancia con un abrazo cálido y apretado.
Estoy contigo en cada paso de tu día."""
    },
    "2026-08-04": {
        "fecha_str": "Martes, 04 de Agosto",
        "titulo": "La gracia de tu perseverancia y la serenidad de tu alma ✨🕊️🌸",
        "poema": """Martes para contemplar la belleza de tu constancia, mi reina bella.
Es cautivador ver cómo encajas con tanta soltura la dulzura de una madre amorosa
con la firmeza y visión de una profesional y futura administradora brillante.
Cada paso firme que das en TQ, cada noche que le dedicas a repasar tus libros y guías universitarias,
no solo es muestra de tu disciplina de hierro, sino el cimiento de un futuro radiante para ti y tu princesa.

Deseo de todo corazón que hoy encuentres momentos de profunda serenidad en medio del movimiento.
Que las tareas fluyan con soltura, que los archivos se gestionen rápido y sin tropiezos,
y que las personas a tu alrededor sepan valorar la enorme luz y el orden impecable que tú aportas.

Al final de la tarde, cuando regreses a tu refugio, quiero que respires y sientas orgullo de ti.
Nunca olvides que en mi corazón ocupas un lugar sagrado e inamovible.
Cuídate mucho hoy, mi mujer maravillosa. Te quiero con una fuerza que trasciende la distancia."""
    },
    "2026-08-05": {
        "fecha_str": "Miércoles, 05 de Agosto",
        "titulo": "Puentes invisibles entre Medellín y Bucaramanga 🏔️✈️💕",
        "poema": """Llegamos a la mitad de la semana, mi vida hermosa.
A veces contemplo el mapa de nuestra patria y me quedo mirando los kilómetros que separan
las verdes montañas antioqueñas de los majestuosos paisajes bumangueses.
Sin embargo, me da una ternura inmensa comprobar que no existe geografía capaz de distanciar
lo que se siente desde lo más profundo del corazón.

Cada pensamiento mío hacia ti viaja a la velocidad de la luz, envolviéndote en un manto cálido
que busca protegerte de las prisas del trabajo y darte un respiro lleno de dulzura.
Eres mi pensamiento preferido en las mañanas y el pensamiento con el que cierro mis ojos de noche.

Espero que hoy tu jornada laboral en TQ sea fluida y tranquila,
que tus ideas brillen en cada conversación y que sientas una chispa de paz constante en tu pecho.
Sigue adelante con esa entereza que te hace única, porque estás haciendo un trabajo magistral.
Te quiero con un cariño profundo, maduro y leal."""
    },
    "2026-08-06": {
        "fecha_str": "Jueves, 06 de Agosto",
        "titulo": "Tu esfuerzo silencioso construye un imperio indestructible 🏰📜🌷",
        "poema": """Casi rozamos el fin de semana, mi administradora soñada.
Hoy jueves quiero rendirle un tributo muy especial a ese esfuerzo silencioso que no todos ven:
a las madrugadas constantes, a los minutos que le robas al descanso para avanzar en tus entregas,
a la paciencia infinita con la que resuelves cada detalle laboral en Tecnoquímicas,
y al amor incondicional con el que atiendes las risas y necesidades de tu hijita.

Quizás a veces sientas cansancio en el cuerpo, y es completamente natural y válido,
pero quiero que por un instante intentes mirarte a través de mis ojos:
verías a una mujer majestuosa, inteligente, capaz de vencer cualquier tempestad y llena de ternura.

No te exijas más de lo debido; lo estás haciendo perfecto, paso a paso.
Cada semilla que siembras hoy florecerá en jardines de éxito y estabilidad para los tuyos.
Te pienso a cada segundo y te mando un beso lleno de devoción."""
    },
    "2026-08-07": {
        "fecha_str": "Viernes, 07 de Agosto",
        "titulo": "Festivo nacional y el merecido santuario de tu descanso 🇨🇴🌸💖",
        "poema": """¡Feliz viernes y feliz festivo de la Batalla de Boyacá, mi reina adorada!
Qué alegría tan gigante siente mi corazón al saber que hoy el calendario nos regala este respiro,
permitiéndote pausar por completo la rutina exigente de Tecnoquímicas y los libros de la universidad.
Hoy es un día sagrado para desconectar la mente, soltar los correos y entregarte a la calma.

Aprovecha este festivo para disfrutar de tu hogar sin mirar el reloj.
Siente la dicha de desayunar despacio, de tomarte tu café o té mientras conversas placenteramente,
de abrazar a tu hijita y regalarse risas llenas de la paz más pura que existe.

Que tu casa se llene de energía renovada y que este día libre sea un abrazo para tu espíritu.
Desde Medellín celebro tu descanso porque sé cuánto has trabajado y cuánto te lo mereces.
Eres la reina de mi universo y hoy deseo que te consientan como la mujer grandiosa que eres.
¡Disfruta enormemente tu viernes de descanso, mi amor!"""
    },
    "2026-08-08": {
        "fecha_str": "Sábado, 08 de Agosto",
        "titulo": "Sábado de magia, libertad y risas inolvidables de hogar 🧸🌈✨",
        "poema": """Sábado con aroma a hogar, a tranquilidad y a momentos memorables, mi reina consentida.
Me llena de una profunda paz imaginarte relajada, vistiendo tus prendas más cómodas,
disfrutando de tu tiempo libre al lado de tu pequeña y dejando que las horas transcurran suavecito,
sin la presión de alarmas, correos corporativos ni llamadas urgentes.

Te mereces cada segundo de esta libertad. Te mereces reír con libertad, disfrutar un antojo delicioso,
mirar una película que te guste o simplemente descansar sintiendo que el deber está cumplido.
Desde la distancia, te envío un abrazo envolvente cargado de ositos, mariposas y bendiciones.

Que la alegría de hoy llene tus tanques de energía y que sientas en todo instante mi presencia afectuosa.
Gracias por existir y por ser ese faro de luz que alegra mi vida de una forma tan bonita.
Te adoro con toda mi alma, mi reina hermosa."""
    },
    "2026-08-09": {
        "fecha_str": "Domingo, 09 de Agosto",
        "titulo": "Un remanso de amor puro para acariciar tu alma ☕🦋🌺",
        "poema": """Llegamos al domingo, mi vida hermosa, ese día sagrado donde el mundo desacelera
para permitirnos reconectar con lo verdaderamente valioso de la existencia.
Hoy quiero pedirte que te mimes de manera especial, que escuches a tu cuerpo y le permitas descansar.
La semana laboral arrancará mañana, pero hoy el tiempo es únicamente para tu bienestar y tu familia.

Gracias por permitirme ser parte de tu historia, por escucharme con esa dulzura que tienes,
por compartir conmigo tus sueños de ser una gran Administradora y por tus risas compartidas.
Construir este lazo contigo, desafiando cualquier distancia, es una de las cosas más bellas de mi vida.

Que este domingo cierre con una tranquilidad inmensa en tu pecho y con la absoluta certeza
de que eres profundamente amada, respetada y valorada por quien te escribe desde Medellín.
Un abrazo inmenso y un beso dulce hasta Bucaramanga."""
    },
    "2026-08-10": {
        "fecha_str": "Lunes, 10 de Agosto",
        "titulo": "Fuerza invencible y la majestuosidad de tu camino 💼👑✨",
        "poema": """Nuevo lunes, mi reina hermosa, y una nueva oportunidad para deslumbrar al mundo
con la firmeza de tu carácter y la elegancia de tu inteligencia.
Sé que retomar el ritmo tras un fin de semana festivo exige una cuota extra de energía,
pero si de algo estoy seguro es de la berraquera gigante que habita en tu corazón.

Enfréntate a esta jornada recordando que eres una mujer empoderada, metódica y brillante.
Que tus gestiones en Tecnoquímicas salgan fluidas, que los problemas encuentren solución rápida
y que sientas la satisfacción de saber que dominas cada proceso con maestría.

Yo estaré aquí, siendo tu admirador número uno a la distancia, enviándote la mejor vibración
y recordándote a cada rato que tu potencial no tiene fronteras.
¡A romperla hoy, mi futura Administradora! Que tengas un lunes de puros éxitos."""
    },
    "2026-08-11": {
        "fecha_str": "Martes, 11 de Agosto",
        "titulo": "Orgullo infinito por tu impecable labor en TQ 📦💖🌷",
        "poema": """Martes de enfoque y realizaciones, mi vida bella.
Cada vez que pienso en la dedicación impecable que le pones a tus actividades en Tecnoquímicas,
en tu cuidado por los detalles para que los registros y procesos funcionen sin errores,
se me hincha el pecho de un orgullo verdadero.
Eres el reflejo de lo que ocurre cuando se combina talento, ética y compromiso.

Deseo que hoy las horas en el trabajo transcurran livianas y agradables,
que las interacciones con tus compañeros sean amables y productivas,
y que sientas el reconocimiento implícito que genera tu excelente labor.

Cuando el sol se ponga y regreses a descansar a tu casa, recuerda que siempre habrá aquí
un espacio cálido para escucharte, leerte y desearte la noche más reparadora.
Te quiero de una forma única y especial, mi reina."""
    },
    "2026-08-12": {
        "fecha_str": "Miércoles, 12 de Agosto",
        "titulo": "Mitad de semana: La luz inagotable que emana de ti 🌟💫🧸",
        "poema": """¡Miércoles, mi reina adorada! Llegamos al corazón de la semana.
Sé que el esfuerzo acumulado entre las jornadas laborales de TQ y las exigencias de la carrera
puede empezar a sentirse en los hombros, pero también conozco la luz inagotable de tu espíritu.
Tienes una fuerza interior que te renueva y te permite salir victoriosa de cada reto.

Tómate pausas breves durante el día, bebe agüita fresca, estira tu espalda y regálate una sonrisa.
Estás construyendo un monumento de estabilidad y superación para ti y para tu hijita.
Ningún trasnocho es en vano, ninguna lectura de universidad cae en saco roto; todo dará sus frutos dorados.

Te envío un abrazo tan profundo y cálido que cruce los valles y llegue directo a tu pecho
para recordarte que nunca estás sola. Te quiero con todo mi corazón."""
    },
    "2026-08-13": {
        "fecha_str": "Jueves, 13 de Agosto",
        "titulo": "La visión de una futura Administradora brillante 🎓📜💖",
        "poema": """Jueves con perspectiva de victoria, mi vida.
Al contemplar el entusiasmo y la seriedad con que asumes tus estudios de Administración de Empresas,
no puedo evitar imaginarte en un futuro muy cercano liderando equipos con sabiduría,
tomando decisiones estratégicas de alto nivel y siendo esa ejecutiva admirable que ya se vislumbra en ti.

Tu mente estructurada, tu capacidad de análisis y tu tenacidad son herramientas indestructibles.
No te abrumes si algún tema universitario parece complejo; tómalo con calma, que tú tienes el intelecto de sobra.
Me siento profundamente honrado de ser testigo de tu crecimiento y de acompañarte en este viaje.

Sigue brillando con esa humildad tan bella que te caracteriza.
El futuro te tiene preparadas cosas gigantescas. Te pienso con amor y profunda admiración."""
    },
    "2026-08-14": {
        "fecha_str": "Viernes, 14 de Agosto",
        "titulo": "El suspiro de alivio al conquistar una nueva semana 🌅🌸✨",
        "poema": """¡Por fin es viernes, mi reina deslumbrante!
Qué alegría se siente en el aire al mirar atrás y comprobar que lograste conquistar otra semana más.
Cumpliste tus metas en Tecnoquímicas, le cumpliste a tus materias de la universidad
y mantuviste el amor encendido en tu hogar como la madre maravillosa que eres.

Que el ritmo de hoy en el trabajo sea amable y apresurado para que la tarde te reciba con los brazos abiertos.
Prepárate para cerrar las carpetas, apagar el computador y sumergirte en ese espacio de descanso
donde solo importan las risas, la buena comida y la paz.

Esta noche es para que te consientas como te mereces.
Yo estaré celebrando tus logros desde Medellín y enviándote todo mi afecto en cada pensamiento.
¡Que tengas un viernes sensacional, mi vida!"""
    },
    "2026-08-15": {
        "fecha_str": "Sábado, 15 de Agosto",
        "titulo": "Sábado para honrar tu amor maternal y tu bella esencia 🧸👑💕",
        "poema": """Sábado radiante, mi reina hermosa.
Una de las facetas que más profundamente me cautivan de ti es el amor desbordante,
paciente y dulce con el que guías y cuidas el universo de tu pequeña hijita.
Ver la complicidad que comparten y la felicidad que construyes en tu hogar
me demuestra la pureza y la grandeza de tu corazón.

Hoy sábado es un día perfecto para nutrir esa complicidad:
para jugar, salir a caminar, compartir un helado o simplemente acurrucarse en casa sin afanes.
Deseo que la alegría inunde cada rincón de tu hogar y que descanses con la conciencia en paz.

Gracias por enseñarme lo que significa el amor abnegado y la fortaleza verdadera.
Disfruta de cada instante de tu sábado, mi reina bella. Te adoro con todo mi ser."""
    },
    "2026-08-16": {
        "fecha_str": "Domingo, 16 de Agosto",
        "titulo": "Domingo de paz plena, café caliente y pensamientos mutuos ☕✨🕊️",
        "poema": """Domingo de calma infinita, mi vida hermosa.
Hoy te propongo un pacto de tranquilidad total: regálate momentos de silencio sanador,
escucha las canciones de Beéle, Melendi o el afrobeat que tanto te gusta y alegran tu alma,
bebe un café o té caliente a sorbos pausados y permite que cualquier vestigio de fatiga desaparezca.

A veces la vida nos exige andar deprisa, pero los domingos existen como un recordatorio dulce
de que lo verdaderamente sagrado son los afectos reales y la paz interior.
Aunque la distancia física nos mantenga en ciudades distintas,
quiero que sepas que en pensamiento estoy a tu lado, sonriéndote y cuidándote.

Que este día termine con una serenidad hermosa en tu pecho.
Te quiero con un cariño limpio, transparente y eterno."""
    },
    "2026-08-17": {
        "fecha_str": "Lunes, 17 de Agosto",
        "titulo": "Lunes festivo de desconexión total y amor familiar 🎈🌸💖",
        "poema": """¡Un nuevo lunes festivo para celebrar la vida, mi reina adorada!
Qué regalo maravilloso del calendario tener este día extra para prolongar la descanso de tu fin de semana.
Hoy el inicio de semana no viene acompañado de despertadores madrugadores ni de compromisos de TQ,
sino de la oportunidad perfecta para consentirte y regalarte bienestar.

Disfruta de este día festivo de la Asunción con una sonrisa amplia.
Comparte momentos bellos con tu hijita, preparen algo sabroso para almorzar,
y permite que tu mente se limpie de cualquier preocupación laboral o académica.

Desde Medellín te mando un abrazo lleno de ternura que te acompañe durante todo el día.
Mi admiración y mi afecto por ti son una constante firme que no depende de fechas.
¡Pásala increíble hoy, mi reina!"""
    },
    "2026-08-18": {
        "fecha_str": "Martes, 18 de Agosto",
        "titulo": "Renovar el espíritu y retomar el rumbo con ilusión 💫💼✨",
        "poema": """Martes con la energía al cien por ciento, mi vida.
Tras un fin de semana prolongado y lleno de descanso, hoy la semana arranca de forma más corta
pero igualmente repleta de metas bonitas por alcanzar.
Llega a Tecnoquímicas con la compostura de quien sabe que tiene las riendas de su trabajo bajo control.

Confío plenamente en tus destrezas, en tu sentido práctico y en tu inteligencia rápida.
Que la jornada sea fluida, que las tareas se completen con agilidad y que el ambiente laboral sea grato.

Recuerda que aquí en Antioquia hay alguien que no deja de pensarte con orgullo,
alguien que valora cada gesto tuyo y que se siente bendecido por tenerte en su día a día.
¡A triunfar hoy, mi reina empoderada!"""
    },
    "2026-08-19": {
        "fecha_str": "Miércoles, 19 de Agosto",
        "titulo": "Latidos sincronizados más allá de las fronteras 🏔️✈️💖",
        "poema": """Miércoles de reflexiones bonitas, mi reina amada.
A veces contemplo el cielo atardecer y me imagino la vista de Bucaramanga a la distancia.
Me reconforta enormemente saber que bajo ese mismo cielo habita una mujer increíble,
llena de virtudes, trabajando duro por sus sueños y cuidando a los suyos con amor.

La distancia entre nuestras ciudades se vuelve diminuta cuando hay una conexión honesta,
basada en el respeto, la complicidad, el apoyo mutuo y un cariño que crece día con día.
Gracias por tu ternura, por tus palabras y por ser esa presencia luminosa que me acompaña.

Que este miércoles te traiga la satisfacción del trabajo bien hecho en TQ y momentos de risas.
Te amo con una fuerza sincera y permanente."""
    },
    "2026-08-20": {
        "fecha_str": "Jueves, 20 de Agosto",
        "titulo": "Sutileza, inteligencia y firmeza en un solo ser 👑🦋🌸",
        "poema": """Jueves de resplandor, mi reina consentida.
Es inspirador observar la combinación tan perfecta que se da en tu personalidad:
posees la dulzura más tierno para tratar a las personas que amas,
la distinción en tu forma de expresarte y comportarte,
y la firmeza indispensable para no rendirte jamás ante los retos de la universidad y el trabajo.

Esa riqueza de virtudes te convierte en un ser humano sencillamente excepcional.
Deseo que el día de hoy responda a toda esa luz que llevas dentro:
que tus gestiones salgan bien al primer intento y que la gente a tu alrededor te facilite las tareas.

Te envío mi cariño envuelto en palabras sinceras para recordarte que vales oro.
Que tengas un jueves maravilloso, mi vida."""
    },
    "2026-08-21": {
        "fecha_str": "Viernes, 21 de Agosto",
        "titulo": "Viernes de victoria para la dueña de mis pensamientos 🏆💖✨",
        "poema": """¡Llegamos al viernes, mi reina victoriosa!
Otra semana laboral cerrada con éxito en Tecnoquímicas, otro escalón superado en la universidad
y otro periodo donde demostraste que tu berraquera no tiene límites.
Te mereces un aplauso de pie por la disciplina impecable que le pones a todo.

Que las horas laborales de hoy pasen rápido y sin complicaciones.
Esta noche arranca el fin de semana y quiero que te prepares para consentirte:
disfruta de una cena sabrosa, ponte cómoda y desconecta el chip de la productividad obligatoria.

Yo estaré desde aquí celebrando tus victorias y enviándote todo mi amor.
¡Feliz viernes, mi mujer soñada!"""
    },
    "2026-08-22": {
        "fecha_str": "Sábado, 22 de Agosto",
        "titulo": "Un fin de semana para tejer recuerdos de oro 🧸🌟🌺",
        "poema": """Sábado de descanso ganado a pulso, mi reina adorada.
El fin de semana es ese espacio donde puedes dedicarte sin apuros a lo que más amas:
a compartir tiempo de calidad con tu hijita, a ver sus sonrisas y a descansar tu cuerpo.

Aprovecha este sábado para vivir el presente sin pensar en los correos del lunes.
Salgan a pasear, disfruten del clima, coman algo que les encante o descansen en casa plácidamente.
La felicidad se construye con estos momentos sencillos pero profundos.

Gracias por ser la mujer bondadosa, auténtica y hermosa que alegra mis días a la distancia.
Disfruta tu sábado al máximo, mi reina bella. Te amo con todo mi corazón."""
    },
    "2026-08-23": {
        "fecha_str": "Domingo, 23 de Agosto",
        "titulo": "La poesía viva que escribes con cada uno de tus actos 📖💖✨",
        "poema": """Domingo de calma y afecto sincero, mi vida hermosa.
Hay personas que buscan la poesía en los libros antiguos, pero yo prefiero verla en tu vida diaria:
en el amor abnegado con el que guías a tu niña, en el empeño con el que estudias Administración,
en la responsabilidad con la que cumples en TQ y en la calidez con la que hablas.

Eres una lección constante de superación, elegancia y ternura.
Hoy domingo solo deseo que te regales paz, que descanses tu mente y renueves tus fuerzas.
Mañana empezará una nueva semana, pero hoy el día es para recargar el alma.

Recuerda que no importa la distancia, mi corazón y mis pensamientos habitan a tu lado.
Un beso inmenso hasta Bucaramanga."""
    },
    "2026-08-24": {
        "fecha_str": "Lunes, 24 de Agosto",
        "titulo": "La entereza de tus convicciones en una nueva recta final 💼👑🌸",
        "poema": """Iniciamos la última semana completa del mes de agosto, mi reina soñada.
Mírate al espejo antes de salir de casa y reconoce a la mujer valiente, sabia y capaz que tienes frente a ti.
Todo lo que has construido hasta hoy es el resultado directo de tu esfuerzo constante y tu fe.

Afronta tus compromisos en Tecnoquímicas con la tranquilidad de quien domina su área.
Que la semana comience con noticias positivas, flujos de trabajo despejados y mucha armonía.

Desde Medellín te mando la mejor energía, respaldando cada una de tus metas y celebrando tu camino.
¡A romperla hoy con toda la actitud, mi reina!"""
    },
    "2026-08-25": {
        "fecha_str": "Martes, 25 de Agosto",
        "titulo": "Admiración que florece y se profundiza cada mañana 🌅🧸💕",
        "poema": """Martes luminoso, mi reina hermosa.
Si me pidieran listar las cosas que admiro de ti, no acabaría nunca:
tu capacidad de análisis para los temas administrativos, tu responsabilidad profesional impecable en TQ,
tu amor de madre entregada y la amabilidad con la que tratas a todos.

Cada día que pasa me convenzo más del ser humano extraordinario que eres.
Espero que en medio del ajetreo del día te regales un instante para respirar y valorar lo lejos que has llegado.

Estoy contigo en el pensamiento, sosteniendo tu mano y apoyándote en todo momento.
Cuídate mucho hoy y ten un martes lleno de cosas bonitas."""
    },
    "2026-08-26": {
        "fecha_str": "Miércoles, 26 de Agosto",
        "titulo": "Un pausa para recordarte lo sublime e increíble que eres 🌟✨🌷",
        "poema": """Mitad de semana, mi vida hermosa.
Hoy no quiero hablarte de pendientes ni de tareas; hoy solo quiero aprovechar este mensaje
para hacer una pausa y recordarte lo inmensamente valiosa que eres para mí y para el mundo.

A veces, por andar corriendo tras las responsabilidades, se nos olvida celebrar nuestras propias virtudes.
Tú eres bella por fuera, pero tu belleza interior, tu nobleza y tu trabajo constante son aún mayores.

No permitas que el estrés opaque la certeza de tus capacidades.
Sigue caminando con la cabeza en alto que el futuro te tiene guardadas grandes recompensas.
Te quiero con una intensidad profunda y sincera."""
    },
    "2026-08-27": {
        "fecha_str": "Jueves, 27 de Agosto",
        "titulo": "Tu valentía no conoce fronteras ni se rinde jamás 🛡️💖✨",
        "poema": """Jueves de fortaleza y avance, mi administradora estrella.
Se aproxima el cierre de mes y sé que los requerimientos laborales en TQ y los trabajos universitarios
pueden acumularse un poco. Sin embargo, también conozco de sobra tu templanza y tu capacidad organizativa.

Toma las tareas una a una, sin abrumarte; realiza lo que esté a tu alcance con la excelencia habitual
y confía en tus conocimientos. Recuerda que no estás sola en este proceso:
mi apoyo, mi escucha activa y mi cariño están disponibles para ti a cualquier hora.

Ya casi llega el fin de semana para que puedas descansar.
¡Mucho ánimo hoy, mi reina bella! Estoy orgulloso de ti."""
    },
    "2026-08-28": {
        "fecha_str": "Viernes, 28 de Agosto",
        "titulo": "Cerramos una semana impecable, mi administradora estrella 🎓💼👑",
        "poema": """¡Llegó el viernes, mi reina adorada!
Cerramos la última semana laboral de agosto con un balance profundamente victorioso.
Te entregaste con responsabilidad a tus labores en TQ, avanzaste en tu carrera de Administración
y brindaste amor y seguridad en tu hogar. ¡Eres un ejemplo brillante de superación!

Que las horas de trabajo de hoy transcurran con agilidad y ligereza.
Prepárate para disfrutar de un fin de semana reparador, libre de tensiones y lleno de amor familiar.

Te envío un abrazo envolvente cargado de mariposas, flores y buena energía.
¡Te mereces el mejor descanso del mundo, mi vida!"""
    },
    "2026-08-29": {
        "fecha_str": "Sábado, 29 de Agosto",
        "titulo": "El privilegio de contemplar tu felicidad en la calma 🎈🧸🌸",
        "poema": """Sábado de pura serenidad y regocijo, mi vida hermosa.
Saber que estás disfrutando de tu tiempo libre, desconectada de los compromisos de la oficina
y dedicada a lo que llena de alegría tu corazón, me produce una paz gigante.
Tu felicidad y tu bienestar son mi mayor tranquilidad a la distancia.

Disfruta de este día sin afanes: consiéntete con una comida rica, ríe con tu pequeña,
pasea o simplemente descansa placenteramente en tu hogar.

Gracias por brindarme tu cariño honesto y por ser esa presencia tan especial en mi vida.
Disfruta tu sábado al máximo, mi reina hermosa. Te amo con toda mi alma."""
    },
    "2026-08-30": {
        "fecha_str": "Domingo, 30 de Agosto",
        "titulo": "Agradecimiento desbordado al contemplar este mes juntos 🙏💖✨",
        "poema": """Domingo de reflexión y agradecimiento profundo, mi reina adorada.
Al mirar atrás y contemplar cómo ha transcurrido este mes de agosto,
me llena de alegría ver cada logro que alcanzaste, cada conversación compartida y cada sonrisa.

Gracias por permitirme acompañarte a la distancia a través de este diario y de nuestros mensajes,
por tu dulzura constante y por la confianza bonita que hemos construido.
Hoy domingo regálate un descanso completo, recarga tus energías y prepara tu corazón para septiembre.

Siempre estaré aquí para ti, apoyándote, celebrándote y admirándote.
Que tengas un domingo repleto de paz, mi reina bella."""
    },
    "2026-08-31": {
        "fecha_str": "Lunes, 31 de Agosto",
        "titulo": "El broche de oro para un mes inolvidable y el abrazo eterno 👑🏆💖",
        "poema": """Hoy despedimos el mes de agosto, mi reina hermosa, y el sentimiento que prevalece es el orgullo.
Orgullo de ver cómo enfrentaste cada día con valentía en Tecnoquímicas,
cómo avanzaste en tus estudios de Administración de Empresas y cómo cuidaste con amor de tu princesa.

Cerramos este mes comprobando que la distancia entre Medellín y Bucaramanga es diminuta
frente a la fuerza de nuestro afecto, nuestro respeto y nuestro apoyo incondicional.
Gracias por ser esa mujer transparente, trabajadora y maravillosa que ilumina mi vida.

Recibe este último día de agosto con la alegría del deber cumplido y con la certeza de que lo que viene será aún más brillante.
Gracias por ser mi reina y mi inspiración. Te amo con todo mi ser y te abrazo apretado a la distancia."""
    }
}

RETOS_DIARIOS = {
    "2026-08-01": "🌸 Reto de Hoy: Tómate una taza de tu bebida favorita despacio y regálate 10 minutos de lectura o música en paz.",
    "2026-08-02": "☕ Reto de Hoy: Respira profundo 3 veces, suelta los pendientes de la semana y disfruta un abrazo apretado con tu hijita.",
    "2026-08-03": "💼 Reto de Hoy: Inicia el trabajo en TQ sonriéndote al espejo y recordando que eres una profesional brillante e invencible.",
    "2026-08-04": "🌿 Reto de Hoy: Haz una pausa activa a mitad de mañana, estira tus brazos y bebe un vaso entero de agua fresca.",
    "2026-08-05": "✈️ Reto de Hoy: Escucha una canción que te alegre el alma y recuerda que desde Medellín hay alguien pensándote mucho.",
    "2026-08-06": "🌷 Reto de Hoy: Escribe en una nota un logro reciente tuyo en la universidad y celébralo internamente.",
    "2026-08-07": "🇨🇴 Reto de Hoy: ¡Día festivo! Prohibido pensar en correos o informes. Dedícate 100% a descansar y consentirte.",
    "2026-08-08": "🧸 Reto de Hoy: Prepara o pide tu comida antojo preferida y disfrútala sin ningún tipo de culpa.",
    "2026-08-09": "🕊️ Reto de Hoy: Cierra los ojos 5 minutos antes de dormir y agradece por la paz y el amor que habitan en tu hogar.",
    "2026-08-10": "✨ Reto de Hoy: Camina con postura de reina ejecutiva durante toda tu jornada. ¡El mundo es tuyo!",
    "2026-08-11": "📦 Reto de Hoy: Organiza tu espacio de trabajo de forma armoniosa para que todo fluya con elegancia y sin estrés.",
    "2026-08-12": "🌟 Reto de Hoy: Regálate una mascarilla o un baño relajante al llegar a casa para soltar la tensión del ombligo de semana.",
    "2026-08-13": "🎓 Reto de Hoy: Repasa tus apuntes de Administración sintiendo orgullo por cada concepto que dominas.",
    "2026-08-14": "🌅 Reto de Hoy: Desconéctate del trabajo exactamente a tu hora de salida y celebra el inicio del fin de semana.",
    "2026-08-15": "🌺 Reto de Hoy: Tómate una foto bonita sonriendo junto a tu niña y guárdala como un tesoro de felicidad.",
    "2026-08-16": "☕ Reto de Hoy: Escucha el ritmo suave del afrobeat o de Beéle mientras te preparas un almuerzo delicioso.",
    "2026-08-17": "🎈 Reto de Hoy: ¡Lunes festivo! Regálate una siesta reparadora en la tarde sin mirar la hora.",
    "2026-08-18": "💫 Reto de Hoy: Afronta los pendientes de TQ uno a uno con la calma y la seguridad que te caracterizan.",
    "2026-08-19": "🏔️ Reto de Hoy: Tómate 2 minutos para enviarme un emoji o un saludito que alegre mi día desde Bucaramanga.",
    "2026-08-20": "👑 Reto de Hoy: Mírate al espejo y repite en voz alta: 'Soy una mujer capaz, inteligente, hermosa y amada'.",
    "2026-08-21": "🏆 Reto de Hoy: Planea una noche de películas o descanso cómodo para celebrar el fin de la semana laboral.",
    "2026-08-22": "🌟 Reto de Hoy: Sal a dar una caminata suave, siente la brisa en tu rostro y desconecta por completo tu mente.",
    "2026-08-23": "📖 Reto de Hoy: Lee una frase que te inspire y guárdala en la sección de notas de tu diario interactivo.",
    "2026-08-24": "💼 Reto de Hoy: Mantén una actitud serena ante cualquier imprevisto en la oficina; nada apaga tu luz.",
    "2026-08-25": "🌅 Reto de Hoy: Desayuna despacio disfrutando cada bocado antes de iniciar tus actividades diarias.",
    "2026-08-26": "✨ Reto de Hoy: Haz un cumplido sincero a ti misma sobre lo bien que gestionas tu tiempo y tu vida.",
    "2026-08-27": "🛡️ Reto de Hoy: Si sientes cansancio, delega o posterga lo que no sea urgente. Tu bienestar es lo primero.",
    "2026-08-28": "🎓 Reto de Hoy: Cierra tu semana laboral con un aplauso mental para ti misma por todo lo logrado en agosto.",
    "2026-08-29": "🎈 Reto de Hoy: Ríe a carcajadas con tu hijita y disfruten de un momento de juego o diversión juntas.",
    "2026-08-30": "🙏 Reto de Hoy: Haz una lista mental de 3 cosas hermosas que viviste durante este mes que termina.",
    "2026-08-31": "💖 Reto de Hoy: Recibe este nuevo mes con el corazón lleno de fe, sabiendo que vienen bendiciones aún más grandes."
}

CANCIONES_DIARIAS = {
    "2026-08-01": {"titulo": "Inolvidable - Beéle 🎶", "desc": "Una melodía fresca para arrancar Agosto con la mejor vibra y alegría en el corazón."},
    "2026-08-02": {"titulo": "Caminando por la Vida - Melendi 🎸", "desc": "Un recordatorio de avanzar paso a paso, sonriendo y disfrutando el viaje."},
    "2026-08-03": {"titulo": "Vivir Mi Vida - Marc Anthony 💃", "desc": "Energía pura de Lunes para conquistar cada meta laboral en TQ con entusiasmo."},
    "2026-08-04": {"titulo": "Afrobeat Essentials 🥁", "desc": "Ritmos envolventes y cálidos para acompañar tu tarde de trabajo con fluidez."},
    "2026-08-05": {"titulo": "Hasta Ese Día - Lasso 🎵", "desc": "Una letra romántica que acorta los kilómetros entre Medellín y Bucaramanga."},
    "2026-08-06": {"titulo": "Color Esperanza - Diego Torres 🌈", "desc": "Fuerza y motivación pura para tu carrera de Administración de Empresas."},
    "2026-08-07": {"titulo": "Paz y Calma Acoustic 🍃", "desc": "Acordes suaves para saborear este festivo patrio en la serenidad de tu hogar."},
    "2026-08-08": {"titulo": "Mi Persona Favorita - Alejandro Sanz 💖", "desc": "Una dedicatoria dulce para celebrar tu amor con tu linda hijita."},
    "2026-08-09": {"titulo": "Un Beso en Madrid - TINI & Alejandro Sanz ☕", "desc": "Música suave para acompañar tu café del domingo con nostalgia bonita."},
    "2026-08-10": {"titulo": "La Gozadera - Gente de Zona 🎉", "desc": "Chispa y dinamismo para iniciar una semana de éxitos y buena actitud."},
    "2026-08-11": {"titulo": "Destino o Casualidad - Melendi ✨", "desc": "Una canción especial para pensar en cómo la vida nos conecta de formas bellas."},
    "2026-08-12": {"titulo": "Loco - Beéle 🌴", "desc": "Sabor caribeño y alegría contagiosa para superar el ombligo de semana."},
    "2026-08-13": {"titulo": "La Promesa - Melendi 📜", "desc": "Palabras sinceras de admiración y respeto para la reina de mi corazón."},
    "2026-08-14": {"titulo": "Viernes de Fiesta & Sol ☀️", "desc": "Ritmo alegre para cerrar las carpetas del trabajo y dar la bienvenida al fin de semana."},
    "2026-08-15": {"titulo": "Bonito - Jarabe de Palo 🌸", "desc": "Porque todo en ti es bonito: tu forma de ser, tu sonrisa y tu dedicación."},
    "2026-08-16": {"titulo": "Si Tú La Ves - Nicky Jam & Wisin 🎶", "desc": "Un tema con ritmo alegre para llenar de dinamismo tu tarde libre."},
    "2026-08-17": {"titulo": "Risa - Babylon Summer 🎈", "desc": "Música relajante para sacarle el máximo provecho a este lunes festivo."},
    "2026-08-18": {"titulo": "Aprender a Volar - Patricia Sosa 🦅", "desc": "Inspiración pura para retomar la jornada con la seguridad de una mujer invencible."},
    "2026-08-19": {"titulo": "Más Allá de la Distancia 🏔️", "desc": "Melodía instrumental para acompañar tus pensamientos de media tarde."},
    "2026-08-20": {"titulo": "Tuyo - Rodrigo Amarante 🌹", "desc": "Un toque elegante y envolvente para celebrar el jueves con sofisticación."},
    "2026-08-21": {"titulo": "Celebra la Vida - Axel 🏆", "desc": "Himno de alegría para celebrar que lograste superar otra semana más."},
    "2026-08-22": {"titulo": "Amanecer - Bomba Estéreo 🌅", "desc": "Buena vibra, luz y energía colorida para disfrutar de tu sábado en familia."},
    "2026-08-23": {"titulo": "Qué Bonito - Rosario 🌺", "desc": "Una de las letras más bellas para homenajear la pureza de tus sentimientos."},
    "2026-08-24": {"titulo": "Un Stoppeable - Sia 🚀", "desc": "Fuerza mental pura para comerte el mundo en la recta final de agosto."},
    "2026-08-25": {"titulo": "Barranquilla - Beéle 🌊", "desc": "Ritmos frescos que alegran la mente y refrescan tus momentos libres."},
    "2026-08-26": {"titulo": "La Mujer Perfecta - Kurt 👑", "desc": "Dedicatoria directa a ti: inteligente, trabajadora, madre amorosa y bella."},
    "2026-08-27": {"titulo": "Casi Un Hogar - Melendi 🏡", "desc": "Melodía acogedora para recargar energías al llegar a tu casa en la noche."},
    "2026-08-28": {"titulo": "Cierre de Mes Triunfal 🎓", "desc": "Música de celebración por haber demostrado tu excelencia en TQ y la U."},
    "2026-08-29": {"titulo": "Volví a Nacer - Carlos Vives 🌻", "desc": "Alegría vallenata contagiosa para disfrutar de un fin de semana pleno."},
    "2026-08-30": {"titulo": "Gracias a la Vida - Mercedes Sosa 🙏", "desc": "Reflexión y paz en el corazón para despedir el mes con gratitud."},
    "2026-08-31": {"titulo": "Un Viaje Inolvidable - Éxitos Beéle 👑", "desc": "El cierre perfecto para un mes donde demostraste que eres la reina de mi mundo."}
}

LINEA_DEL_TIEMPO_RECUERDOS = [
    {
        "fecha": "25/03/2026",
        "titulo": "❤️ Primer saludo",
        "desc": "Quedó registrada la primera conversación del chat con un saludo sencillo, y desde ahí empezó a sentirse la confianza.",
        "icono": "❤️"
    },
    {
        "fecha": "10/04/2026",
        "titulo": "📝 Checklist resuelto",
        "desc": "Se ayudó a diligenciar el checklist desde la tablet y SharePoint hasta lograr que la opción apareciera correctamente.",
        "icono": "📝"
    },
    {
        "fecha": "14/04/2026",
        "titulo": "📦 Causal de descontinuación",
        "desc": "Se aclaró la causal del producto descontinuado y quedó la referencia como 824 baja rotación.",
        "icono": "📦"
    },
    {
        "fecha": "17/04/2026",
        "titulo": "🔗 Envío de enlaces",
        "desc": "Se compartieron enlaces de SharePoint y soportes para carpeta y checklist, mostrando apoyo constante.",
        "icono": "🔗"
    },
    {
        "fecha": "02/06/2026",
        "titulo": "♻️ Devolución en CEDI",
        "desc": "Se revisó un formato de devolución en el CEDI del Éxito y se aclaró el número correcto para el registro.",
        "icono": "♻️"
    },
    {
        "fecha": "06/07/2026",
        "titulo": "🌷 Conversación más cercana",
        "desc": "La charla empezó a fluir con más cariño y admiración; ambos dijeron que podían hablar más seguido.",
        "icono": "🌷"
    },
    {
        "fecha": "07/07/2026",
        "titulo": "💬 Más sobre ustedes",
        "desc": "Hablaron de estudio, ciudad, comida favorita, redes y el deseo de conocerse en persona con respeto.",
        "icono": "💬"
    },
    {
        "fecha": "12/07/2026",
        "titulo": "🎂 Cumpleaños y familia",
        "desc": "Compartieron edades, fechas de cumpleaños y detalles de familia, dejando ver una confianza más profunda.",
        "icono": "🎂"
    },
    {
        "fecha": "13/07/2026",
        "titulo": "🎵 Música compartida",
        "desc": "Descubrieron gustos musicales en común y hablaron de afrobeat, Beéle y Melendi con mucho entusiasmo.",
        "icono": "🎵"
    },
    {
        "fecha": "18/07/2026",
        "titulo": "🚗 Apoyo en carretera",
        "desc": "Hubo mensajes de cuidado cuando el regreso se complicó por un accidente y el trayecto se hizo más largo.",
        "icono": "🚗"
    },
    {
        "fecha": "19/07/2026",
        "titulo": "💪 Ánimo y sueños",
        "desc": "Se dieron palabras de apoyo para seguir adelante con los sueños, el estudio y las responsabilidades.",
        "icono": "💪"
    },
    {
        "fecha": "22/07/2026",
        "titulo": "📆 Calendario para verse",
        "desc": "Empezaron a mirar agendas para encontrar un momento y verse pronto, con muchas ganas de acercarse.",
        "icono": "📆"
    },
    {
        "fecha": "23/07/2026",
        "titulo": "💖 Te quiero mucho",
        "desc": "La conversación subió de tono emocional y ella le dijo que lo quería mucho, con ternura y confianza.",
        "icono": "💖"
    },
    {
        "fecha": "25/07/2026",
        "titulo": "📍 Ubicación compartida",
        "desc": "Compartieron ubicación en tiempo real, coordinaron la llegada y se acompañaron durante el trayecto.",
        "icono": "📍"
    },
    {
        "fecha": "26/07/2026",
        "titulo": "🌙 Cierre con cariño",
        "desc": "El chat cerró con confirmaciones de afecto, cuidado y la sensación de estar siempre pendientes el uno del otro.",
        "icono": "🌙"
    }
]

FRASES_ESCRITAS_POR_TI = [
    "\"Hoy solo quería recordarte que estoy profundamente orgulloso de ti.\"",
    "\"Eres una mujer extraordinaria, madre amorosa y profesional impecable.\"",
    "\"Nunca olvides que tu inteligencia y tenacidad no tienen techo.\"",
    "\"Si el día se pone pesado, respira profundo: aquí estoy pensándote día y noche.\"",
    "\"Tu sonrisa tiene el poder exacto de arreglarme cualquier mal día.\"",
    "\"De Medellín a Bucaramanga hay muchos kilómetros, pero estás aquí en mi pecho.\"",
    "\"Vas a ser una Administradora de Empresas fabulosa. ¡Confío en ti!\""
]

COMBOS_ICONOS = ["🧸🦋💖", "⭐🌸✨", "☕✨🌷", "👑🎉💖", "🎀🧸✨", "🕊️🌷🌸", "🌈✨🎈", "🎆👑💖"]

PREGUNTAS_TRIVIA = [
    {
        "pregunta": "¿En qué empresa trabaja nuestra reina demostrando su talento día a día?",
        "opciones": ["TQ (Tecnoquímicas)", "Bancolombia", "Ecopetrol", "Nutresa"],
        "correcta": "TQ (Tecnoquímicas)",
        "explicacion": "¡Exacto! En TQ eres la más profesional y dedicada. 💼✨"
    },
    {
        "pregunta": "¿Qué carrera profesional está estudiando con tanta tenacidad?",
        "opciones": ["Administración de Empresas", "Ingeniería Industrial", "Derecho", "Medicina"],
        "correcta": "Administración de Empresas",
        "explicacion": "¡Sí! Futura Administradora de Empresas brillante. 🎓👑"
    },
    {
        "pregunta": "¿Cuál es su plan favorito en sus momentos libres para relajarse?",
        "opciones": ["Compartir en familia y descansar", "Trabajar horas extra", "Hacer fila en el banco", "Estar en tráfico"],
        "correcta": "Compartir en familia y descansar",
        "explicacion": "¡Amo ver lo feliz, libre y en paz que te pones disfrutando con tu hijita! 💖✨"
    },
    {
        "pregunta": "¿Qué dos ciudades conectan este lazo y cariño gigante?",
        "opciones": ["Medellín y Bucaramanga", "Bogotá y Cali", "Cartagena y Pereira", "Manizales y Armenia"],
        "correcta": "Medellín y Bucaramanga",
        "explicacion": "¡Así es! De Medellín a Bucaramanga no hay distancia que apague este sentimiento. 🏔️✈️"
    }
]

FORTUNAS = [
    "🥠 Fortuna de Hoy: 'El esfuerzo de hoy en tus estudios de Administración se convertirá en el éxito gigante de mañana.'",
    "🥠 Fortuna de Hoy: 'Alguien a la distancia te está pensando en este preciso instante, de día y de noche, con una sonrisa enorme.'",
    "🥠 Fortuna de Hoy: 'Un momento libre lleno de paz, risas y abrazos reconfortantes te espera muy pronto.'",
    "🥠 Fortuna de Hoy: 'Tu ternura y elegancia abrirán las puertas a todas las metas que te propongas.'",
    "🥠 Fortuna de Hoy: 'Hoy es un día perfecto para regalarte un antojo y tomarte un delicioso café caliente en tu tiempo libre.'",
    "🥠 Fortuna de Hoy: 'La vida te devolverá duplicada toda la luz y amor que le entregas a tu hijita.'"
]

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

SALUDOS_61 = [
    "Mi reina hermosa, hoy quiero recordarte algo sencillo pero inmenso: no tienes que demostrar tu valor cada minuto; ya eres valiosa.",
    "Mi vida, abre esta página despacio. Hoy no viene a exigirte nada, viene a acompañarte.",
    "Reina, hay días para conquistar el mundo y otros para respirar. Ambos días cuentan.",
    "Hoy pensé en ti y en todo lo que haces sin hacer ruido. Por eso esta página lleva tu nombre.",
    "Mi reina, cuando la rutina corra demasiado, vuelve aquí un momento y recuerda quién eres.",
    "Hoy quiero celebrar a la mujer que sigue adelante incluso cuando nadie ve todo el esfuerzo que hay detrás.",
    "Esta página es un abrazo convertido en palabras, escrito para acompañarte en el momento exacto en que la abras.",
    "Reina hermosa, tu historia no se mide solo por resultados; también por la valentía con la que atraviesas cada día.",
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

# El motor de septiembre-octubre tiene prioridad.
MENSAJES_DIARIOS.update(MENSAJES_61)
RETOS_DIARIOS.update(RETOS_61_MAP)
CANCIONES_DIARIAS.update(CANCIONES_61_MAP)

# ==============================================================================
# 6C. VARIABLES DEL DÍA PARA TODA LA APLICACIÓN
# ==============================================================================
FECHA_HOY_CO = datetime.now(tz_colombia)
HOY_CO = FECHA_HOY_CO.date()
CLAVE_HOY = HOY_CO.strftime("%Y-%m-%d")
CONTENIDO_HOY_61 = MENSAJES_61.get(CLAVE_HOY, contenido_61_dias(HOY_CO))
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
# 6E. AUDIO OPCIONAL SIN ROMPER LA APP
# ==============================================================================
AUDIO_CANDIDATAS = {
    "Sin Miedo": [ruta_asset("sin_miedo.mp3"), ruta_asset("sin_miedo.wav"), ruta_asset("sin_miedo.ogg")],
    "Bésame": [ruta_asset("besame.mp3"), ruta_asset("besame.wav"), ruta_asset("besame.ogg")],
}

def encontrar_audio(nombre):
    for candidato in AUDIO_CANDIDATAS[nombre]:
        if candidato.is_file():
            return candidato
    return None

AUDIO_SIN_MIEDO = encontrar_audio("Sin Miedo")
AUDIO_BESAME = encontrar_audio("Bésame")


# Helper seguro para insertar texto del usuario/mensajes en HTML sin romper el marcado.
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
# ESTILOS DELUXE ADICIONALES — BLOQUE SEPARADO, SIN F-STRING
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
# 8B. BANNER DELUXE SEGURO — SIN JAVASCRIPT EMBEBIDO EN F-STRINGS
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
        <strong>{mensaje_corto_de_hora(FECHA_HOY_CO)}</strong>
        <div style="margin-top:8px;color:#5d4d59;">{CONTENIDO_HOY_61['titulo']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("---")

# ==============================================================================
# 9. MENÚ PRINCIPAL DE 19 PESTAÑAS — LISTA INDEXABLE, SIN UNPACKING
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

# ------------------------------------------------------------------------------
# TAB 1: PORTADA & BIENVENIDA CON FOTOS FLOTANTES Y FRASES SORPRESA
# ------------------------------------------------------------------------------
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

        # Frase escrita por ti que aparece aleatoriamente
        frase_sorpresa_hoy = random.choice(FRASES_ESCRITAS_POR_TI)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ffffff 0%, #fff0f3 100%); border-radius: 22px; padding: 22px; border-left: 8px solid #ff4d6d; box-shadow: 0 8px 25px rgba(255, 77, 109, 0.15); margin-bottom: 22px;'>
            <p style='color: #ff4d6d; font-weight: bold; font-size: 0.95em; margin-bottom: 4px;'>💬 Un pensamiento tuyo para ella:</p>
            <p style='color: #333; font-size: 1.15em; font-style: italic; margin: 0;'>{frase_sorpresa_hoy}</p>
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

        # TARJETA DEL MENSAJE DIARIO CAMBIANTE AUTOMÁTICO
        st.markdown(f"""
        <div class='daily-card'>
            <span style='background-color: #ff85a1; color: white; padding: 8px 18px; border-radius: 16px; font-weight: bold; font-size: 1.05em;'>
                📅 {mensaje_hoy['fecha_str']} (Actualización Automática 🇨🇴)
            </span>
            <h3 style='color: #c2185b; margin-top: 18px; margin-bottom: 14px; font-size: 1.5em;'>{mensaje_hoy['titulo']}</h3>
            <p style='color: #222; font-size: 1.15em; line-height: 1.85; white-space: pre-line;'>
            {mensaje_hoy['poema']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        # BLOQUE CAMBIANTE DE CANCIÓN Y RETO DIARIO
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

        st.write("")
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

# ------------------------------------------------------------------------------
# TAB 2: LÍNEA DEL TIEMPO DE NUESTROS RECUERDOS
# ------------------------------------------------------------------------------
with tabs[1]:
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
# TAB 3: CALENDARIO INTERACTIVO CON COLORES
# ------------------------------------------------------------------------------
with tabs[2]:
    st.markdown("<h3 style='color: #d63384;'>📅 Calendario Interactivo de Recuerdos & Vivencias</h3>", unsafe_allow_html=True)
    st.write("Selecciona cualquier fecha para consultar lo que se escribió o los mensajes asignados a ese día.")
    st.write("---")

    col_cal1, col_cal2 = st.columns([1, 1.2], gap="large")

    with col_cal1:
        fecha_seleccionada = st.date_input(
            "📆 Elige una fecha en el calendario:",
            value=date.today(),
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
# TAB 4: ESTADÍSTICAS BONITAS
# ------------------------------------------------------------------------------
with tabs[3]:
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
# TAB 5: CENTRO DE PERSONALIZACIÓN COMPLETO
# ------------------------------------------------------------------------------
with tabs[4]:
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
# TAB 6: MI DIARIO INTERACTIVO
# ------------------------------------------------------------------------------
with tabs[5]:
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
# TAB 7: HISTÓRICO DE MEMORIAS
# ------------------------------------------------------------------------------
with tabs[6]:
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
# TAB 8: PLANIFICADOR & HÁBITOS
# ------------------------------------------------------------------------------
with tabs[7]:
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
# TAB 9: ANTOJITOS & CUPONES
# ------------------------------------------------------------------------------
with tabs[8]:
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
# TAB 10: GENERADOR DE CARTAS PDF
# ------------------------------------------------------------------------------
with tabs[9]:
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
# TAB 11: FRASCO DE RECUERDOS & FORTUNA
# ------------------------------------------------------------------------------
with tabs[10]:
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
# TAB 12: CÁPSULA DEL TIEMPO SECRETA
# ------------------------------------------------------------------------------
with tabs[11]:
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
# TAB 13: TRIVIA DE NUESTRO AMOR & TEST
# ------------------------------------------------------------------------------
with tabs[12]:
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
# TAB 14: CONTADOR DE DISTANCIA & CALCULADORA
# ------------------------------------------------------------------------------
with tabs[13]:
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

# ============================================================================== 
# TAB 15: CARTA DE HOY
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
# TAB 16: RITUAL DIARIO
# ============================================================================== 
with tabs[15]:
    st.markdown("<h3 style='color:#d63384;'>🌙 Ritual Diario</h3>", unsafe_allow_html=True)
    st.write("Tres pequeños momentos para que el diario acompañe tu mañana, tu tarde y tu noche.")
    st.write("---")
    rituales = [
        ("☀️", "Mañana", "Elige una prioridad. No diez. Una sola que haga que hoy valga la pena."),
        ("🌤️", "Tarde", "Mira lejos de la pantalla, estira los hombros y regálate unos minutos de calma."),
        ("🌙", "Noche", "Nombra una cosa que hiciste bien y deja el resto para mañana."),
    ]
    cols = st.columns(3)
    for i, (icono, titulo, texto_ritual) in enumerate(rituales):
        with cols[i]:
            st.markdown(f"""
            <div class='card' style='text-align:center;min-height:180px;'>
                <div style='font-size:2.3rem;'>{icono}</div>
                <h4 style='color:#9b1d4f;'>{titulo}</h4>
                <p style='color:#5d4d59;'>{texto_ritual}</p>
            </div>
            """, unsafe_allow_html=True)
    preguntas = [
        "¿Qué pequeño logro estoy olvidando celebrar?",
        "¿Qué puedo soltar esta noche para descansar mejor?",
        "¿Qué quiero agradecer de hoy?",
        "¿Qué parte de mí necesita más paciencia?",
        "¿Cuál fue mi momento más bonito del día?",
    ]
    q = preguntas[HOY_CO.toordinal() % len(preguntas)]
    st.markdown(f"<div class='quote-card'><span class='quote-mark'>?</span><strong>{q}</strong></div>", unsafe_allow_html=True)

# ============================================================================== 
# TAB 17: CAJA SECRETA
# ============================================================================== 
with tabs[16]:
    st.markdown("<h3 style='color:#d63384;'>🎁 Caja Secreta</h3>", unsafe_allow_html=True)
    st.write("La sorpresa cambia con la fecha para que cada entrada se sienta diferente.")
    st.write("---")
    cajas = [
        "Hoy eres oficialmente la protagonista de esta página. 👑",
        "Tu regalo de hoy es una certeza: vas mejor de lo que crees.",
        "Hay un abrazo escondido en estas palabras. Imagina que acaba de llegar. 🫂",
        "Hoy está permitido no tener todas las respuestas.",
        "Tu misión secreta: hacer algo pequeño que te haga feliz.",
        "No minimices un logro solo porque ya te acostumbraste a ser excelente.",
        "Esta caja contiene cinco minutos de paz sin culpa. 🕊️",
        "Sorpresa: alguien está profundamente orgulloso de ti. 💖",
    ]
    sorpresa = cajas[HOY_CO.toordinal() % len(cajas)]
    st.markdown(f"""
    <div style='padding:42px 26px;border-radius:30px;background:linear-gradient(145deg,#2e1730,#5e294b 55%,#22142d);color:#fff;text-align:center;box-shadow:0 24px 55px rgba(38,18,39,.23);'>
        <div style='font-size:4rem;'>🎁</div>
        <div style='font-size:1.6rem;font-weight:900;'>Caja del día · {CONTENIDO_HOY_61['sello']}</div>
        <p style='font-size:1.1rem;max-width:760px;margin:16px auto;line-height:1.8;color:rgba(255,255,255,.88);'>{sorpresa}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🎉 Abrir con magia", key="caja_secreta_final"):
        st.balloons()
        lanzar_efecto_fiesta_js("lluvia_corazones_3d")
        st.success("¡Sorpresa abierta! Guarda este momento en el corazón. 💖")

# ============================================================================== 
# TAB 18: CIELO DE HOY
# ============================================================================== 
with tabs[17]:
    st.markdown("<h3 style='color:#d63384;'>🌌 Cielo de Hoy</h3>", unsafe_allow_html=True)
    st.write("Una constelación simbólica distinta según la fecha. Este bloque se renderiza con components.html separado del Python.")
    st.write("---")
    seed = HOY_CO.toordinal()
    rng = random.Random(seed)
    puntos = []
    for _ in range(18):
        puntos.append((rng.randint(5,95), rng.randint(10,90), rng.randint(4,9), round(rng.uniform(0,2.6),2)))
    html_parts = [
        "<html><head><style>",
        "html,body{margin:0;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif}",
        ".sky{position:relative;height:440px;width:100%;overflow:hidden;border-radius:30px;background:radial-gradient(circle at 22% 20%,rgba(255,255,255,.18),transparent 18%),radial-gradient(circle at 75% 28%,rgba(177,159,255,.2),transparent 24%),linear-gradient(180deg,#090c22 0%,#17122f 46%,#42204a 100%);box-shadow:0 24px 56px rgba(25,12,40,.3)}",
        ".sky:after{content:'';position:absolute;inset:0;background-image:radial-gradient(circle,rgba(255,255,255,.72) 0 1px,transparent 1.5px);background-size:120px 120px;opacity:.42}",
        ".star{position:absolute;border-radius:50%;background:#fff;box-shadow:0 0 8px #fff,0 0 16px rgba(255,197,224,.85),0 0 26px rgba(255,112,173,.42);animation:pulse 2.8s ease-in-out infinite}",
        ".line{position:absolute;height:1px;transform-origin:left center;background:linear-gradient(90deg,rgba(255,255,255,.03),rgba(255,207,229,.5),rgba(255,255,255,.03));opacity:.68}",
        ".caption{position:absolute;z-index:5;left:22px;top:18px;color:rgba(255,255,255,.9);font-weight:800}.footer{position:absolute;z-index:5;left:22px;bottom:18px;color:rgba(255,255,255,.66);font-size:.82rem}.moon{position:absolute;right:9%;bottom:9%;width:78px;height:78px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff9fc 0 10%,#ffd9ea 25%,#e77eaa 55%,#6d2856 100%);box-shadow:0 0 34px rgba(255,142,195,.24)}",
        "@keyframes pulse{0%,100%{opacity:.4;transform:scale(.65)}50%{opacity:1;transform:scale(1.25)}}",
        "</style></head><body><div class='sky'>",
        f"<div class='caption'>✨ {CONTENIDO_HOY_61['fecha_str']} · {CONTENIDO_HOY_61['sello']}</div>",
        f"<div class='footer'>{ESCENA_HOY_61[0]} {ESCENA_HOY_61[1]} · una constelación que cambia con cada día.</div>",
        "<div class='moon'></div>",
    ]
    for x,y,size,delay in puntos:
        html_parts.append(f"<span class='star' style='left:{x}%;top:{y}%;width:{size}px;height:{size}px;animation-delay:{delay}s'></span>")
    for i in range(len(puntos)-1):
        x1,y1=puntos[i][0],puntos[i][1]; x2,y2=puntos[i+1][0],puntos[i+1][1]
        dx=x2-x1; dy=y2-y1
        dist=(dx*dx+dy*dy)**0.5
        angle=math.degrees(math.atan2(dy,dx))
        html_parts.append(f"<span class='line' style='left:{x1}%;top:{y1}%;width:{dist:.2f}%;transform:rotate({angle:.2f}deg)'></span>")
    html_parts += ["</div></body></html>"]
    components.html("".join(html_parts), height=455, scrolling=False)
    st.markdown(f"<div class='quote-card'><span class='quote-mark'>✦</span><strong>{html_escape_61(CONTENIDO_HOY_61['titulo'])}</strong><div style='margin-top:8px;'>Hoy el cielo también tiene una página escrita para ti.</div></div>", unsafe_allow_html=True)

# ============================================================================== 
# TAB 19: SORPRESA DEL DÍA + AUDIO OPCIONAL
# ============================================================================== 
with tabs[18]:
    st.markdown("<h3 style='color:#d63384;'>💝 Sorpresa del Día</h3>", unsafe_allow_html=True)
    st.write("Nada de archivos obligatorios. La música solo aparece como reproductor si algún día subes tus propios archivos al repositorio.")
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
    st.write("Las canciones **no son necesarias para que la app funcione**. Cuando quieras agregarlas, solo sube tus propios archivos a GitHub.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='card'><b>❤️ Sin Miedo</b><br><small>Reproductor disponible cuando exista sin_miedo.mp3 / wav / ogg.</small></div>", unsafe_allow_html=True)
        if AUDIO_SIN_MIEDO:
            st.audio(str(AUDIO_SIN_MIEDO))
    with c2:
        st.markdown("<div class='card'><b>💋 Bésame</b><br><small>Reproductor disponible cuando exista besame.mp3 / wav / ogg.</small></div>", unsafe_allow_html=True)
        if AUDIO_BESAME:
            st.audio(str(AUDIO_BESAME))
