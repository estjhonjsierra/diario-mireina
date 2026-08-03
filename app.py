import streamlit as st
import streamlit.components.v1 as components
import json
import os
from datetime import datetime, timedelta, date
import pytz
import io
import random

# Librerías para generar el PDF elegante con ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTADO INICIAL COMPLETO
# ==============================================================================
st.set_page_config(
    page_title="El Diario de Mi Reina 👑 | Edición Mágica Deluxe",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Control de primera visita
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
    st.session_state["sonrisas_count"] = 17

if "metas_cumplidas_count" not in st.session_state:
    st.session_state["metas_cumplidas_count"] = 9

if "cartas_creadas_count" not in st.session_state:
    st.session_state["cartas_creadas_count"] = 41

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
dia_semana_num = datetime.now(tz_colombia).weekday()  # 0: Lunes, 6: Domingo

THEME_PRESETS = {
    "Rosa Algodón": {
        "gradient": "linear-gradient(135deg, #fff0f5 0%, #ffe3ec 40%, #f7d6e0 70%, #fff5f8 100%)",
        "border": "#ff85a1",
        "accent": "#d63384",
        "card_bg": "rgba(255, 255, 255, 0.96)"
    },
    "Lavanda Imperial": {
        "gradient": "linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 40%, #f5f3ff 70%, #faf5ff 100%)",
        "border": "#c084fc",
        "accent": "#7e22ce",
        "card_bg": "rgba(255, 255, 255, 0.96)"
    },
    "Melocotón Cálido": {
        "gradient": "linear-gradient(135deg, #fff7ed 0%, #ffedd5 40%, #fff1f2 70%, #fffaf0 100%)",
        "border": "#fb923c",
        "accent": "#c2410c",
        "card_bg": "rgba(255, 255, 255, 0.96)"
    },
    "Menta Fresca": {
        "gradient": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 40%, #fdf2f8 70%, #f7fee7 100%)",
        "border": "#4ade80",
        "accent": "#15803d",
        "card_bg": "rgba(255, 255, 255, 0.96)"
    },
    "Atardecer Pastel": {
        "gradient": "linear-gradient(135deg, #fff1f2 0%, #ffe4e6 40%, #fecdd3 70%, #fff5f5 100%)",
        "border": "#fb7185",
        "accent": "#be123c",
        "card_bg": "rgba(255, 255, 255, 0.96)"
    }
}

FONTS_PRESETS = {
    "Segoe UI": "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "Dancing Script (Cursiva Romántica)": "'Dancing Script', cursive, 'Segoe UI', sans-serif",
    "Poppins (Moderna Elegante)": "'Poppins', sans-serif",
    "Cinzel (Imperial 👑)": "'Cinzel', serif"
}

PARTICLE_SETS = {
    "🦋 Mariposas & 🌸 Flores": ["🦋", "🌸", "🌷", "🌺", "✨", "🦋"],
    "⭐ Estrellas & 💖 Corazones": ["⭐", "💖", "✨", "🌟", "💕", "⭐"],
    "🧸 Ositos & 👑 Coronas": ["🧸", "👑", "🎀", "🧸", "✨", "👑"],
    "🌈 Mezcla Mágica Completa": ["🧸", "🦋", "⭐", "💖", "🌸", "👑", "🌷", "✨"]
}

theme_cfg = THEME_PRESETS.get(st.session_state["user_theme"], THEME_PRESETS["Rosa Algodón"])
font_family_css = FONTS_PRESETS.get(st.session_state["user_font"], FONTS_PRESETS["Segoe UI"])
particles_list = PARTICLE_SETS.get(st.session_state["user_particles"], PARTICLE_SETS["🦋 Mariposas & 🌸 Flores"])

# ==============================================================================
# 3. ESTILOS CSS AVANZADOS, GOOGLE FONTS & PARTICULAS DINÁMICAS
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

/* PARTICULAS FLOTANTES CONTINUAS EN EL FONDO */
.floating-particle {{
    position: fixed;
    z-index: 0;
    pointer-events: none;
    user-select: none;
    animation: floatParticle 11s infinite ease-in-out;
    opacity: 0.88;
    font-size: 2.4rem;
}}

@keyframes floatParticle {{
    0% {{ transform: translateY(105vh) translateX(0px) rotate(0deg) scale(0.8); opacity: 0; }}
    20% {{ opacity: 0.95; }}
    80% {{ opacity: 0.95; }}
    100% {{ transform: translateY(-15vh) translateX(75px) rotate(360deg) scale(1.35); opacity: 0; }}
}}

.p1 {{ left: 3%; animation-duration: 11s; animation-delay: 0s; }}
.p2 {{ left: 15%; animation-duration: 13.5s; animation-delay: 2s; }}
.p3 {{ left: 28%; animation-duration: 9.8s; animation-delay: 4s; }}
.p4 {{ left: 42%; animation-duration: 12.2s; animation-delay: 1s; }}
.p5 {{ left: 56%; animation-duration: 14s; animation-delay: 5s; }}
.p6 {{ left: 70%; animation-duration: 8.9s; animation-delay: 3s; }}
.p7 {{ left: 83%; animation-duration: 12.8s; animation-delay: 6s; }}
.p8 {{ left: 94%; animation-duration: 10.2s; animation-delay: 1.5s; }}

/* Keyframes de animación */
@keyframes floatHeader {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-9px) rotate(0.8deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
}}

@keyframes flutter {{
    0%, 100% {{ transform: translateY(0px) scale(1) rotate(0deg); }}
    25% {{ transform: translateY(-6px) scale(1.05) rotate(-3deg); }}
    50% {{ transform: translateY(-2px) scale(0.98) rotate(2deg); }}
    75% {{ transform: translateY(-7px) scale(1.03) rotate(-2deg); }}
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
    font-size: 3.4em !important;
    font-weight: 900;
    margin-bottom: 4px;
    animation: floatHeader 4.5s ease-in-out infinite;
    text-shadow: 3px 3px 14px rgba(214, 51, 132, 0.22);
}}

.sub-header {{
    text-align: center;
    color: #4a4a4a;
    font-size: 1.35em !important;
    font-weight: 600;
    margin-bottom: 20px;
}}

.theme-badge {{
    text-align: center;
    background: rgba(255, 255, 255, 0.92);
    border: 2px solid {theme_cfg['border']};
    border-radius: 22px;
    padding: 8px 24px;
    width: fit-content;
    margin: 0 auto 22px auto;
    font-size: 0.98em;
    font-weight: bold;
    color: {theme_cfg['accent']};
    box-shadow: 0 5px 15px rgba(0,0,0,0.06);
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

<!-- Partículas flotantes decorativas configurables -->
<div class="floating-particle p1">{particles_list[0]}</div>
<div class="floating-particle p2">{particles_list[1]}</div>
<div class="floating-particle p3">{particles_list[2]}</div>
<div class="floating-particle p4">{particles_list[3]}</div>
<div class="floating-particle p5">{particles_list[4]}</div>
<div class="floating-particle p6">{particles_list[5]}</div>
<div class="floating-particle p7">{particles_list[0]}</div>
<div class="floating-particle p8">{particles_list[1]}</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. MOTOR JS MULTI-EFECTO FIESTA MÁGICA
# ==============================================================================
def lanzar_efecto_fiesta_js(tipo_efecto):
    """Genera componentes JavaScript interactivos para efectos visuales sorprendentes."""
    if tipo_efecto == "confetti_boom":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            var count = 220;
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
                particleCount: 60,
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
            var duration = 3.5 * 1000;
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
                var particleCount = 50 * (timeLeft / duration);
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
                particleCount: 120,
                spread: 110,
                origin: { y: 0.6 },
                colors: ['#ffd700', '#ffa500', '#fff8dc', '#ffdf00']
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
# 6. BASE DE DATOS EXTENDIDA DE MENSAJES DIARIOS, LÍNEA DEL TIEMPO & FRASES
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
        "titulo": "La dulzura de tus pausas y la grandeza de tus sueños 🌸🧸✨",
        "poema": """Mi reina amada, hoy domingo amanece con la calma perfecta para que tu alma respire profundo y se llene de luz. A veces me detengo a pensar en todo lo que cargas sobre tus hombros con tanta elegancia y fortaleza: tus responsabilidades impecables en TQ, las metas gigantescas que construyes día a día en tu carrera de Administración de Empresas, y sobre todo, ese amor incondicional, puro y hermoso con el que guías y cuidas el camino de tu hijita. Eres un ser sencillamente extraordinario.

Quiero que hoy te regales un instante de desconexión absoluta, de esos donde el tiempo se detiene, donde el café sabe más rico y donde la mente se libera de cualquier pendiente. Recuerda que no importa cuántos kilómetros separen a Medellín de Bucaramanga; mis pensamientos, mi admiración y mi corazón completo están contigo en cada segundo. Eres mi refugio, mi motivo de orgullo y la mujer más bella de mi universo. Disfruta de la calidez de tu hogar, ríe con el alma y recuerda siempre lo infinitamente que te quiero."""
    },
    "2026-08-03": {
        "fecha_str": "Lunes, 03 de Agosto",
        "titulo": "El inicio de una semana brillante para mi reina 👑💼💖",
        "poema": """Comienza una nueva semana, mi vida hermosa, y con ella nacen múltiples oportunidades para que vuelvas a demostrar de qué estás hecha. Sé que los lunes a veces traen consigo el peso de los informes, la rutina en Tecnoquímicas y la exigencia constante, pero quiero recordarte la mujer capaz, perspicaz e infinitamente talentosa que eres. No hay reto administrativo que te quede grande ni obstáculo que tu tenacidad no pueda derribar.

Camina hoy con la frente en alto, vistiendo esa seguridad que te caracteriza y esa sonrisa que tiene el poder de iluminar cualquier espacio. Cuando sientas que la jornada se torna intensa o que el cansancio intenta rozar tus alas, recuerda que a la distancia hay alguien que te admira profundamente, que celebra cada uno de tus logros silenciosos y que cuenta las horas para recordarte lo mucho que vales. ¡A conquistarlo todo hoy, mi administradora estrella! Te amo y te sostengo en la distancia."""
    },
    "2026-08-04": {
        "fecha_str": "Martes, 04 de Agosto",
        "titulo": "La gracia de tu perseverancia y la paz de tu mirada ✨🕊️",
        "poema": """Martes para contemplar la belleza de tu constancia, mi reina bella. Es cautivador ver cómo encajas con tanta gracia la dulzura de una madre entregada con la firmeza de una profesional brillante. Cada paso que das en TQ, cada noche que le dedicas a repasar tus apuntes de la universidad, no solo es muestra de tu disciplina, sino también el cimiento del futuro radiante que mereces tú y tu pequeña.

Deseo de corazón que hoy encuentres momentos de serenidad en medio de la agitación. Que las tareas fluyan con soltura, que las personas a tu alrededor valoren la luz y el orden que aportas, y que al final de la tarde puedas suspirar sabiendo que lo hiciste excelente. Nunca olvides que en mi corazón ocupas el lugar más sagrado y que no hay día en que no agradezca por haberte atravesado en mi vida. Cuídate mucho, mi reina hermosa."""
    },
    "2026-08-05": {
        "fecha_str": "Miércoles, 05 de Agosto",
        "titulo": "Puentes invisibles entre Medellín y Bucaramanga 🏔️✈️💕",
        "poema": """Llegamos a la mitad de la semana, mi vida. A veces observo el mapa y contemplo los cientos de kilómetros que separan las montañas antioqueñas de los hermosos valles bumangueses; sin embargo, me da risa y ternura comprobar que no existe geografía capaz de distanciar lo que se siente desde el alma. Cada pensamiento mío viaja velozmente hacia ti, envolviéndote en un abrazo cálido que busca protegerte del estrés.

Eres mi pensamiento favorito en las mañanas y el suspiro con el que cierro mis noches. Espero que hoy tu jornada laboral sea ligera, que tus ideas brillen en cada reunión y que sientas una chispa de felicidad constante en tu pecho. Sigue adelante con esa valentía que te caracteriza, mi reina, porque estás haciendo un trabajo formidable en todos los ámbitos de tu vida. Te quiero con una profundidad que las palabras apenas logran esbozar."""
    },
    "2026-08-06": {
        "fecha_str": "Jueves, 06 de Agosto",
        "titulo": "Tu esfuerzo silencioso construye un imperio 🏰📜🌷",
        "poema": """Casi rozamos el fin de semana, mi administradora soñada. Hoy jueves quiero rendirle un homenaje a ese esfuerzo silencioso que nadie más ve: a las madrugadas, a los minutos robados al descanso para cumplir con tus entregas de la universidad, a la paciencia infinita con la que gestionas cada detalle en TQ y al amor inconmensurable que le dedicas a tu princesa en casa.

Quizás a veces sientas cansancio, y es completamente válido, pero quiero que te mires a través de mis ojos por un instante: verías a una mujer majestuosa, inteligente, invencible y llena de una ternura que conmueve. No te rindas jamás, pero tampoco te exijas más de la cuenta. Vas por el camino correcto y cada semilla sembrada florecerá en abundancia. Te amo con todo mi ser y te pienso a cada instante de mi día."""
    },
    "2026-08-07": {
        "fecha_str": "Viernes, 07 de Agosto",
        "titulo": "Fiesta patria y el refugio de tus abrazos 🇨🇴🌸💖",
        "poema": """¡Feliz viernes y festivo, mi reina adorada! Qué alegría tan inmensa siento al saber que el calendario nos regala este respiro para que puedas pausar el ajetreo del trabajo y regalarte el descanso que tanto te mereces. Hoy es un día para bajar las revoluciones, para dejar los correos y las hojas de cálculo a un lado, y entregarte de lleno al calor de tu hogar, a las risas con tu hijita y a esos placeres sencillos que llenan el alma.

Que este día de fiesta patria sea el pretexto perfecto para consentirte, tomarte ese café o té sin prisa, disfrutar de una rica comida y recargar tus energías en paz. Mi corazón celebra contigo este descanso porque sé cuánto has trabajado durante la semana. Gracias por existir, por brindarme tu afecto sincero y por ser esa reina maravillosa que alegra mis días. Disfruta enormemente tu viernes, vida mía."""
    },
    "2026-08-08": {
        "fecha_str": "Sábado, 08 de Agosto",
        "titulo": "Sábado de magia, libertad y sonrisas de hogar 🧸🌈✨",
        "poema": """Sábado con aroma a hogar, a tranquilidad y a momentos inolvidables, mi reina consentida. Me llena el corazón de una profunda alegría imaginarte relajada, vistiendo tu ropa más cómoda, disfrutando del tiempo libre al lado de tu hijita y dejando que las horas transcurran suavemente, sin la presión de las alarmas ni las agendas apretadas.

Te mereces cada segundo de esta libertad. Te mereces reír hasta que te duela la panza, ver tu película o serie favorita, comer algo delicioso y sentir cómo la paz abraza tu casa. Desde la distancia, te envío un abrazo gigante cargado de ositos, mariposas y todo el cariño del universo. Que la felicidad de hoy sea el combustible para tu espíritu. Te adoro con toda mi alma, mi reina hermosa."""
    },
    "2026-08-09": {
        "fecha_str": "Domingo, 09 de Agosto",
        "titulo": "Un remanso de amor para recargar el alma ☕🦋🌺",
        "poema": """Llegamos al domingo, mi vida hermosa, ese día sagrado donde el mundo parece bajar la velocidad para permitirnos reconectar con lo que verdaderamente importa. Hoy quiero pedirte que te mimes de forma especial, que escuches a tu cuerpo y le permitas descansar profundamente. La semana laboral arrancará mañana, pero hoy el tiempo le pertenece única y exclusivamente a tu bienestar y al amor de tu familia.

Gracias por permitirme ser parte de tu universo, por escucharme, por compartir conmigo tus metas, tus chistes y tu día a día. Construir este vínculo contigo, a pesar de la distancia, es uno de los regalos más lindos de mi vida. Que este domingo termine con una tranquilidad inmensa en tu pecho y con la certeza absoluta de que eres profundamente amada y valorada. Un beso gigante hasta la hermosa Bucaramanga."""
    },
    "2026-08-10": {
        "fecha_str": "Lunes, 10 de Agosto",
        "titulo": "Fuerza imparable y la elegancia de tus pasos 💼👑✨",
        "poema": """Nuevo lunes, mi reina hermosa, y una nueva oportunidad para deslumbrar al mundo con tu profesionalismo y tu carácter brillante. Sé que volver a la rutina de TQ tras un fin de semana reconfortante requiere un impulso extra, pero si de algo estoy completamente seguro, es de la berraquera y el compromiso inquebrantable que laten en tu corazón.

Enfréntate a este inicio de semana recordando que eres la futura Administradora de Empresas más capaz, metódica y talentosa. Deja que tu inteligencia abra caminos y que tu serenidad resuelva cualquier eventualidad. Yo estaré aquí, como tu admirador número uno, enviándote la mejor energía en cada hora del día y recordándote que en Medellín hay un corazón que late al ritmo del tuyo. ¡Muchos éxitos en tu jornada hoy!"""
    },
    "2026-08-11": {
        "fecha_str": "Martes, 11 de Agosto",
        "titulo": "Orgullo absoluto por tu entrega en TQ 📦💖🌷",
        "poema": """Martes de trabajo duro, mi vida bella. Cada vez que pienso en la dedicación que le pones a tus labores en Tecnoquímicas, en tu minuciosidad para que todo salga perfecto y en la ética con la que asumes cada tarea, se me hincha el pecho de un orgullo indescriptible. Eres el claro ejemplo de que cuando una mujer combina inteligencia, valores y determinación, no existen límites para su éxito.

Deseo que hoy las cosas fluyan con una armonía increíble, que los pendientes se resuelvan con rapidez y que tus compañeros y superiores reconozcan el inmenso valor que representas. Y al final de la tarde, cuando regreses a tu refugio, recuerda que siempre habrá un espacio para ti en mis palabras para desahogarte, hacerte reír o simplemente acompañar tu descanso. Te quiero de una forma muy especial, mi reina."""
    },
    "2026-08-12": {
        "fecha_str": "Miércoles, 12 de Agosto",
        "titulo": "Mitad de semana: Tu luz que nunca se apaga 🌟💫🧸",
        "poema": """¡Miércoles, mi reina adorada! Hemos alcanzado la cúspide de la semana. Sé que el cansancio acumulado de la rutina puede empezar a sentirse un poco en el cuerpo, pero también sé que tu espíritu posee una luz inextinguible que te impulsa a dar lo mejor de ti en todo instante.

Tómate breves pausas durante el día, respira el aire fresco, hidrátate bien y regálate una sonrisa en el espejo. Estás construyendo un camino maravilloso para ti y para tu hijita, paso a paso, con esfuerzo y amor verdadero. Nada de lo que haces cae en saco roto; todo dará sus frutos dorados muy pronto. Te envío un abrazo tan fuerte y apretado que logre cruzar la Cordillera Oriental para llegar directito a tu corazón. Te amo profundamente."""
    },
    "2026-08-13": {
        "fecha_str": "Jueves, 13 de Agosto",
        "titulo": "La sabiduría de una futura Administradora brillante 🎓📜💖",
        "poema": """Jueves con sabor a victoria cercana, mi vida. Al contemplar tus esfuerzos en los estudios de Administración de Empresas, no puedo evitar visualizarte en un futuro no muy lejano liderando grandes proyectos, tomando decisiones estratégicas y siendo esa ejecutiva admirable que desde ya se está perfilando en ti. Tu mente aguda y tu visión estructurada son tus mayores herramientas.

Nunca te sientas abrumada por la cantidad de lecturas o exámenes; recuerda que cada concepto que dominas hoy es un peldaño más en la escalera de tu triunfo personal. Me siento profundamente afortunado de poder presenciar tu crecimiento, apoyarte moralmente y celebrar cada nota y cada logro académico a tu lado. Sigue brillando, mi reina, que el mundo entero es tuyo. Te quiero con todas las fuerzas de mi alma."""
    },
    "2026-08-14": {
        "fecha_str": "Viernes, 14 de Agosto",
        "titulo": "El suspiro de alivio al ver llegar el descanso 🌅🌸✨",
        "poema": """¡Por fin es viernes, mi reina deslumbrante! Qué satisfacción tan grande se siente al mirar hacia atrás y ver todo lo que lograste conquistar durante esta semana de trabajo en TQ y estudios universitarios. Te entregaste al máximo, demostraste una vez más tu valía y ahora la puerta del fin de semana se abre de par en par para recibirte como la verdadera reina que eres.

Que las horas laborales de hoy se deslicen de manera rápida y placentera. Prepárate para soltar los informes, cerrar las carpetas y sumergirte en ese ambiente cálido de descanso, risas en familia y desconexión total. Recuerda que esta noche es tuya para relajarte, consentirte y disfrutar de una buena comida. Te pienso a cada instante y te envío miles de besos y abrazos virtuales."""
    },
    "2026-08-15": {
        "fecha_str": "Sábado, 15 de Agosto",
        "titulo": "Sábado para celebrar tu amor maternal y tu belleza 🧸👑💕",
        "poema": """Sábado radiante, mi reina hermosa. Una de las virtudes que más me enamoran y me conmueven de ti es el amor desbordante, paciente y dulce con el que educas y cuidas a tu hijita. Ver la complicidad, el cariño y el hogar tan lindo que has construido para ambas demuestra la pureza y la nobleza gigantesca que habitan en tu corazón.

Hoy sábado es un día perfecto para disfrutar de ese vínculo sagrado, para jugar, compartir, pasear o simplemente acurrucarse a ver películas juntas. Deseo que la felicidad inunde cada rincón de tu casa y que la paz permanezca en tu alma durante todo el fin de semana. Gracias por mostrarme lo que significa el amor real y la dedicación sin límites. Te adoro con todo mi ser, mi reina bella."""
    },
    "2026-08-16": {
        "fecha_str": "Domingo, 16 de Agosto",
        "titulo": "Domingo de paz profunda y latidos compartidos ☕✨🕊️",
        "poema": """Domingo de serenidad absoluta, mi vida hermosa. Hoy te propongo un pacto con la tranquilidad: regálate momentos de introspección bonita, escucha la música que alegra tu espíritu, tómate un café bien caliente a sorbos lentos y permite que el cansancio se evapore por completo.

A veces la vida nos lleva a mil por hora, pero días como hoy existen para recordarnos que lo más valioso es el presente y los afectos verdaderos. Aunque no pueda estar físicamente sentado a tu lado compartiendo ese café, quiero que sepas que en pensamiento estoy ahí, contemplando tu sonrisa y agradeciendo a la vida por haber cruzado nuestros caminos. Disfruta enormemente este domingo mi reina. Te quiero más de lo que las palabras pueden expresar."""
    },
    "2026-08-17": {
        "fecha_str": "Lunes, 17 de Agosto",
        "titulo": "Lunes festivo de desconexión y tiempo en familia 🎈🌸💖",
        "poema": """¡Un lunes festivo que sabe a gloria, mi reina adorada! Qué bendición tan grande tener este día adicional de descanso para romper la rutina y recargar la mente. Hoy el lunes no viene cargado de afanes ni de metas laborales, sino de la oportunidad maravillosa de prolongar la paz de tu fin de semana.

Aprovecha cada minuto de este día festivo para recargar tus baterías emocionales. Sal a respirar aire puro, comparte momentos alegres con tu hijita, coman algo que les encante y descansa profundamente. Mi corazón celebra saberte tranquila y feliz en tu hogar. Recuerda que no importa el día ni la hora, mi admiración y mi cariño por ti permanecen firmes e inalterables. ¡Pásala de maravilla hoy, mi reina!"""
    },
    "2026-08-18": {
        "fecha_str": "Martes, 18 de Agosto",
        "titulo": "Renovar la energía con el corazón lleno de ilusión 💫💼✨",
        "poema": """Martes con la energía totalmente renovada, mi vida. Después de un fin de semana largo y reconfortante, hoy la semana laboral arranca de una forma más corta pero igualmente llena de propósitos. Llega a Tecnoquímicas con la serenidad de quien sabe que tiene todo bajo control y con la frescura que te regaló el descanso.

Confío plenamente en tus destrezas, en tu criterio acertado y en tu capacidad para resolver cualquier imprevisto con la mayor de las elegancias. Que tu día esté lleno de interacciones positivas, avances significativos en tus metas y sorpresas agradables. Recuerda que aquí en Medellín hay alguien que no deja de pensarte ni un solo minuto y que se siente inmensamente afortunado de tenerte en su vida. ¡A triunfar hoy!"""
    },
    "2026-08-19": {
        "fecha_str": "Miércoles, 19 de Agosto",
        "titulo": "Latidos constantes más allá de los kilómetros 🏔️✈️💖",
        "poema": """Miércoles de reflexiones profundas, mi reina amada. A veces contemplo el mapa nocturno de Colombia y me imagino las luces de Bucaramanga desde la distancia. Me gusta pensar que entre la maraña de calles y luces, hay un lugarcito iluminado por la calidez de tu presencia, donde habitas con tu gracia, tus sueños y tu ternura.

La distancia física es apenas un detalle cuando dos almas logran conectar de la forma sincera y bonita en que lo hemos hecho. Gracias por tu escucha atenta, por cada mensaje que alegra mis jornadas y por ser esa presencia constante que le da color a mis días. Que este miércoles te traiga la satisfacción del deber cumplido y momentos de mucha paz. Te amo con un cariño infinito y eterno."""
    },
    "2026-08-20": {
        "fecha_str": "Jueves, 20 de Agosto",
        "titulo": "Elegancia, ternura y determinación en un solo ser 👑🦋🌸",
        "poema": """Jueves de resplandor, mi reina consentida. Es fascinante contemplar la combinación tan perfecta que habita en ti: tienes la dulzura más tierna para tratar a quienes amas, la elegancia impecable en tu comportamiento diario y la determinación de hierro para no rendirte jamás ante tus metas profesionales y universitarias.

Esa mezcla de virtudes te convierte en una mujer única, de esas que dejan una huella imborrable en el corazón de quien tiene el privilegio de conocerlas. Deseo que el día de hoy responda a toda esa belleza que llevas dentro: que las cosas te salgan bien al primer intento, que el clima sea agradable y que sientas en todo momento la calidez de mi cariño rodeándote. Te quiero con toda la fuerza de mi ser."""
    },
    "2026-08-21": {
        "fecha_str": "Viernes, 21 de Agosto",
        "titulo": "Viernes victorioso para la mujer de mi vida 🏆💖✨",
        "poema": """¡Llegamos al viernes, mi reina victoriada! Otra semana superada con honores, otra muestra más de tu capacidad organizativa en TQ y de tu entrega absoluta a tu carrera de Administración. Te mereces una aplauso de pie por la constancia que le imprimes a cada uno de tus días.

Que el cierre de la jornada de hoy sea suave y ágil, dejándote libre para comenzar a disfrutar de tu tiempo libre. Esta noche regálate un momento consentido: prepara o pide tu cena favorita, ponte cómoda y desconéctate por completo del estrés. Yo estaré desde aquí enviándote todo mi amor y recordando lo orgulloso que me siento de ti. ¡Feliz viernes, mi vida hermosa!"""
    },
    "2026-08-22": {
        "fecha_str": "Sábado, 22 de Agosto",
        "titulo": "Un fin de semana para crear recuerdos dorados 🧸🌟🌺",
        "poema": """Sábado de descanso merecido, mi reina adorada. El fin de semana es el lienzo en blanco donde escribes tus momentos más felices junto a tu hijita, libre de los correos de TQ y de la carga académica de la universidad. Deseo de corazón que hoy llenes ese lienzo de colores vivos, de risas contagiosas y de abrazos apretados.

Permítete disfrutar de los pequeños detalles: el sol de la mañana, un helado delicioso, un juego divertido o una siesta reparadora. La vida está hecha de estos instantes de felicidad sencilla y pura. Gracias por ser esa mujer transparente, bondadosa y maravillosa que alegra mi existencia. Disfruta tu sábado al máximo, mi reina bella. Te amo profundamente."""
    },
    "2026-08-23": {
        "fecha_str": "Domingo, 23 de Agosto",
        "titulo": "La poesía que escribes con cada uno de tus actos 📖💖✨",
        "poema": """Domingo de calma y afecto, mi vida hermosa. Hay personas que leen poesía en los libros, pero yo prefiero leerla en la forma en que vives tu vida: en la devoción con la que crías a tu pequeña, en la pasión con la que estudias para ser una gran administradora, en la responsabilidad con la que cumples en TQ y en la calidez con la que tratas a quienes te rodean.

Eres un poema viviente de superación, elegancia y amor. Hoy domingo solo deseo que descanses, que recargues la mente y que sientas una paz profunda en tu alma. Mañana vendrán nuevos retos, pero hoy el universo entero se detiene para consentirte. Recuerda que no importa la distancia, mi corazón está siempre contigo. Un beso gigante hasta Bucaramanga."""
    },
    "2026-08-24": {
        "fecha_str": "Lunes, 24 de Agosto",
        "titulo": "La firmeza de tus convicciones en una nueva semana 💼👑🌸",
        "poema": """Iniciamos la última semana completa de agosto, mi reina soñada. Mírate al espejo antes de salir de casa y reconoce a la mujer empoderada, sabia y fuerte que tienes en frente. Nada de lo que has logrado hasta hoy ha sido casualidad; ha sido el fruto directo de tu trabajo duro, tu inteligencia y tu fe inquebrantable.

Afronta las tareas de Tecnoquímicas hoy con la seguridad de que eres una pieza clave e insustituible por tu talento. Que la semana empiece con pie derecho, con buenas noticias, flujos de trabajo despejados y el corazón lleno de optimismo. Desde Medellín te mando la mejor energía y mi admiración perpetua. ¡A romperla toda hoy, mi reina!"""
    },
    "2026-08-25": {
        "fecha_str": "Martes, 25 de Agosto",
        "titulo": "Admiración que crece con cada amanecer 🌅🧸💕",
        "poema": """Martes radiante, mi reina hermosa. Si me preguntaran qué es lo que más admiro de ti, no sabría por dónde empezar: si por la agudeza con la que entiendes los procesos administrativos, por la solidez de tu ética laboral en TQ, por la dulzura maternal que desbordas o por la sencillez y carisma con el que iluminas cualquier conversación.

Cada día que pasa me convenzo más de lo increíble y valiosa que eres. Espero que en medio de las correderas del día te regales un momento para respirar y recordar que vas por el camino correcto hacia todas tus metas. Estoy contigo en pensamiento, sosteniendo tu mano y apoyando cada uno de tus pasos. Cuídate mucho y ten un martes fabuloso."""
    },
    "2026-08-26": {
        "fecha_str": "Miércoles, 26 de Agosto",
        "titulo": "Un recordatorio de lo extraordinaria que eres 🌟✨🌷",
        "poema": """Mitad de semana, mi vida. Hoy no quiero hablarte de tareas ni de pendientes; hoy solo quiero usar este espacio para hacer un pausa y recordarte lo extraordinaria que eres. A veces, en medio del ajetreo diario, se nos olvida celebrar nuestras propias virtudes, y por eso estoy yo aquí: para recordártelas todos los días de la vida.

Eres bella por fuera con una gracia deslumbrante, pero eres aún más hermosa por dentro, con un corazón generoso, trabajador y noble. No dejes que ningún momento de estrés opaque la certeza de lo lejos que vas a llegar. Sigue adelante con paso firme, mi reina, que tu futuro está repleto de bendiciones gigantescas. Te amo de aquí al infinito."""
    },
    "2026-08-27": {
        "fecha_str": "Jueves, 27 de Agosto",
        "titulo": "Tu valentía no conoce fronteras ni cansancio 🛡️💖✨",
        "poema": """Jueves de fortaleza, mi administradora estrella. Se acerca el final del mes y sé que los cierres en el trabajo y los compromisos de la universidad pueden intensificarse. Sin embargo, también conozco la madera de la que estás hecha: eres una mujer valiente, metódica y resiliente que sabe sobreponerse a cualquier cansancio con una sonrisa digna.

No te presiones más de la cuenta; haz lo que esté en tus manos con la excelencia de siempre y confía en el proceso. Recuerda que no estás sola; aunque la geografía nos ponga en ciudades distintas, mi apoyo incondicional y mi cariño están a tu lado 24/7 para levantarte el ánimo cuando lo necesites. Falta muy poco para el fin de semana. ¡Ánimo, mi reina bella!"""
    },
    "2026-08-28": {
        "fecha_str": "Viernes, 28 de Agosto",
        "titulo": "Cerramos una semana impecable, mi administradora estrella 🎓💼👑",
        "poema": """¡Llegó el viernes, mi reina adorada! Cerramos la última semana laboral de agosto y el balance no podría ser más positivo. Te entregaste con el alma a tus responsabilidades en TQ, avanzaste en tus materias de Administración de Empresas y mantuviste encendida la chispa de amor en tu hogar. ¡Eres un ejemplo viviente de triunfo y dedicación!

Que las horas de hoy fluyan de manera impecable y sin contratiempos. Prepara el espíritu para disfrutar de un fin de semana reparador, libre de compromisos pesados y lleno de tiempo de calidad con tu hijita y tus seres queridos. Te envío un abrazo gigante lleno de ternura, estrellas y mariposas. ¡Te mereces el mejor fin de semana del mundo!"""
    },
    "2026-08-29": {
        "fecha_str": "Sábado, 29 de Agosto",
        "titulo": "El regalo de verte sonreír en tus momentos libres 🎈🧸🌸",
        "poema": """Sábado de pura alegría y relajación, mi vida hermosa. Nada me genera más paz interna que saber que estás disfrutando de tu tiempo libre, desconectada de las obligaciones y dedicada por completo a lo que hace feliz a tu corazón. Tu sonrisa tiene el poder mágico de arreglarme cualquier día a la distancia.

Disfruta de este sábado sin prisas. Regálate un gusto gastronómico, ríe con tu pequeña, pasea o descansa profundamente en tu cama. Te mereces todas las cosas lindas que la vida tiene para ofrecer. Desde Medellín te mando todo mi amor, mis pensamientos más dulces y un abrazo rompe costillas. Te adoro con todo mi corazón, mi reina consen."""
    },
    "2026-08-30": {
        "fecha_str": "Domingo, 30 de Agosto",
        "titulo": "Casi cerramos Agosto rodeados de puro agradecimiento 🙏💖✨",
        "poema": """Domingo de calma y agradecimiento profundo, mi reina adorada. Miramos hacia atrás y vemos cómo el mes de agosto se nos escapa entre las manos, dejando tras de sí un rastro hermoso de esfuerzos coronados, conversaciones compartidas, risas a la distancia y momentos inolvidables.

Gracias por permitirme ser parte de tus días durante todo este mes, por leer mis mensajitos, por compartir conmigo tus vivencias y por brindarme la ternura de tu afecto. Hoy domingo te pido que te consientas al máximo, recargues tus energías con amor de hogar y te prepares espiritualmente para recibir septiembre con la mejor actitud. Siempre estaré aquí para ti, mi reina. Te amo infinitamente."""
    },
    "2026-08-31": {
        "fecha_str": "Lunes, 31 de Agosto",
        "titulo": "Cierre de un mes mágico y el abrazo eterno a la distancia 👑🏆💖",
        "poema": """Hoy se cierra el mes de agosto, mi reina hermosa, y no puedo sentirme más orgulloso de todo lo que conquistaste en estos 31 días. Te vi luchar con firmeza en Tecnoquímicas, avanzar a pasos agigantados en tu carrera de Administración de Empresas, entregar el corazón como madre amorosa y brillar con una luz propia que no deja de maravillarme.

Cerramos este mes con la certeza de que nuestro lazo, construido con respeto, admiración y cariño sincero desde Medellín a Bucaramanga, es cada día más fuerte y bonito. Recibe este último día de agosto con la frente en alto, con la alegría de la meta cumplida y con la convicción absoluta de que lo mejor está por venir. Gracias por ser mi reina, mi inspiración y mi lugar seguro. Te amo con toda mi alma y te sostengo siempre en mi corazón."""
    }
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

# 🎵 REPRODUCTOR DE MÚSICA OPCIONAL (NO AUTOMÁTICO)
st.write("")
col_mus1, col_mus2 = st.columns([1.2, 0.8])
with col_mus1:
    if st.button("🎵 Reproducir / Pausar nuestra canción especial"):
        st.session_state["reproduciendo_musica"] = not st.session_state["reproduciendo_musica"]

with col_mus2:
    if st.session_state["reproduciendo_musica"]:
        st.markdown("""
        <div style='background: white; border-radius: 18px; padding: 10px 18px; border: 2px solid #ff85a1; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center;'>
            <span style='color: #d63384; font-weight: bold; font-size: 0.9em;'>🎶 Reproduciendo nuestra melodía de paz...</span>
            <audio autoplay loop controls style='width: 100%; height: 32px; margin-top: 5px;'>
                <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3" type="audio/mpeg">
                Tu navegador no soporta el reproductor de audio.
            </audio>
        </div>
        """, unsafe_allow_html=True)

st.write("---")

# ==============================================================================
# 9. MENÚ PRINCIPAL DE 14 PESTAÑAS INTERACTIVAS
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14 = st.tabs([
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
    "✈️ Contador"
])

# ------------------------------------------------------------------------------
# TAB 1: PORTADA & BIENVENIDA CON FOTOS FLOTANTES Y FRASES SORPRESA
# ------------------------------------------------------------------------------
with tab1:
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

        fecha_colombia = datetime.now(tz_colombia)
        fecha_hoy_key = fecha_colombia.strftime("%Y-%m-%d")
        
        mensaje_hoy = MENSAJES_DIARIOS.get(fecha_hoy_key, {
            "fecha_str": fecha_colombia.strftime("%A, %d de %B"),
            "titulo": "✨ Un mensaje especial para ti",
            "poema": "Mi reina hermosa, recuerda siempre lo increíble, inteligente y hermosa que eres. Cada día y cada noche es una nueva oportunidad para acercarte a tus sueños. ¡Te quiero con todo mi corazón!"
        })

        st.markdown(f"""
        <div class='daily-card'>
            <span style='background-color: #ff85a1; color: white; padding: 8px 18px; border-radius: 16px; font-weight: bold; font-size: 1.05em;'>
                📅 {mensaje_hoy['fecha_str']}
            </span>
            <h3 style='color: #c2185b; margin-top: 18px; margin-bottom: 14px; font-size: 1.5em;'>{mensaje_hoy['titulo']}</h3>
            <p style='color: #222; font-size: 1.15em; line-height: 1.85; white-space: pre-line;'>
            {mensaje_hoy['poema']}
            </p>
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
                efectos = ["confetti_boom", "lluvia_emojis", "fuegos_artificiales", "estrellas_doradas"]
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
        
        if os.path.exists("portada.jpg"):
            st.image("portada.jpg", caption="¡Siempre juntos, mi reina hermosa! ❤️", use_container_width=True)
        elif os.path.exists("portada.jpeg"):
            st.image("portada.jpeg", caption="¡Siempre juntos, mi reina hermosa! ❤️", use_container_width=True)
        elif os.path.exists("portada.png"):
            st.image("portada.png", caption="¡Siempre juntos, mi reina hermosa! ❤️", use_container_width=True)
        else:
            st.image(
                "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
                caption="¡Brillando con tu luz propia donde vayas! ✨",
                use_container_width=True
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
# TAB 3: CALENDARIO INTERACTIVO CON COLORES
# ------------------------------------------------------------------------------
with tab3:
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
        st.info("💡 Cada día en la lista tiene un color asociado para reflejar tu estado de ánimo o las entradas registradas.")

    with col_cal2:
        fecha_str_key = fecha_seleccionada.strftime("%Y-%m-%d")
        entradas_totales = cargar_entradas()
        
        # Filtrar entradas del diario para esa fecha
        entradas_dia = [e for e in entradas_totales if e['fecha'].startswith(fecha_seleccionada.strftime("%d/%m/%Y"))]
        mensaje_sistema = MENSAJES_DIARIOS.get(fecha_str_key, None)

        st.markdown(f"#### 📖 Memorias del {fecha_seleccionada.strftime('%d de %B de %Y')}")
        
        if mensaje_sistema:
            st.markdown(f"""
            <div style='background: #ffffff; border-radius: 18px; padding: 18px; border-left: 6px solid #ff4d6d; box-shadow: 0 6px 18px rgba(0,0,0,0.05); margin-bottom: 15px;'>
                <span style='color: #d63384; font-weight: bold;'>💌 Mensaje Especial del Día:</span>
                <h4 style='margin-top: 5px; color: #c2185b;'>{mensaje_sistema['titulo']}</h4>
                <p style='color: #333; font-size: 0.98em;'>{mensaje_sistema['poema']}</p>
            </div>
            """, unsafe_allow_html=True)

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
# TAB 5: CENTRO DE PERSONALIZACIÓN COMPLETO
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
# TAB 6: MI DIARIO INTERACTIVO
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
# TAB 7: HISTÓRICO DE MEMORIAS
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
# TAB 8: PLANIFICADOR & HÁBITOS
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
# TAB 9: ANTOJITOS & CUPONES
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
# TAB 10: GENERADOR DE CARTAS PDF
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
# TAB 11: FRASCO DE RECUERDOS & FORTUNA
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
# TAB 12: CÁPSULA DEL TIEMPO SECRETA
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
# TAB 13: TRIVIA DE NUESTRO AMOR & TEST
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
# TAB 14: CONTADOR DE DISTANCIA & CALCULADORA
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
