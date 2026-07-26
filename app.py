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

# =========================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTADO INICIAL COMPLETO
# =========================================================
st.set_page_config(
    page_title="El Diario de Mi Reina | Edición Mágica Deluxe",
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

# Contadores de estadísticas
if "sonrisas_count" not in st.session_state:
    st.session_state["sonrisas_count"] = 17

if "metas_cumplidas_count" not in st.session_state:
    st.session_state["metas_cumplidas_count"] = 9

if "cartas_creadas_count" not in st.session_state:
    st.session_state["cartas_creadas_count"] = 41

# Personalizaciones por defecto
if "user_font" not in st.session_state:
    st.session_state["user_font"] = "Segoe UI"

if "user_theme" not in st.session_state:
    st.session_state["user_theme"] = "Rosa Algodón"

if "user_particles" not in st.session_state:
    st.session_state["user_particles"] = "🦋 Mariposas & Flores"

# =========================================================
# 2. SISTEMA DE PALETAS Y PERSONALIZACIÓN DE ESTILOS
# =========================================================
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
    "Cinzel (Imperial)": "'Cinzel', serif"
}

PARTICLE_SETS = {
    "🦋 Mariposas & Flores": ["🦋", "🌸", "🌺", "🌷", "✨", "💫"],
    "❤️ Corazones": ["❤️", "💖", "💕", "💗", "💘", "✨"],
    "⭐ Estrellas & Destellos": ["⭐", "🌟", "✨", "💫", "⚡", "🌙"],
    "🧸 Ositos & Coronas": ["🧸", "👑", "💖", "🌸", "✨", "💫"],
    "✨ Mezcla Mágica Completa": ["🦋", "🌸", "🧸", "👑", "💖", "⭐", "🌷", "✨"]
}

theme_cfg = THEME_PRESETS.get(st.session_state["user_theme"], THEME_PRESETS["Rosa Algodón"])
font_family_css = FONTS_PRESETS.get(st.session_state["user_font"], FONTS_PRESETS["Segoe UI"])
particles_list = PARTICLE_SETS.get(st.session_state["user_particles"], PARTICLE_SETS["🦋 Mariposas & Flores"])

# =========================================================
# 3. ESTILOS CSS AVANZADOS & PARTICULAS DINÁMICAS
# =========================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Dancing+Script:wght@600;700&family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"], .stMarkdown, p, div, label, span {{
    font-size: 20px !important;
    font-family: {font_family_css} !important;
    line-height: 1.68 !important;
}}

.stApp {{
    background: {theme_cfg['gradient']} !important;
    background-attachment: fixed !important;
}}

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

.main-header {{
    text-align: center;
    color: {theme_cfg['accent']};
    font-size: 3.4em !important;
    font-weight: 900;
    margin-bottom: 4px;
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
}}

.daily-card {{
    background: linear-gradient(135deg, #ffffff 0%, #fff0f3 100%);
    border: 2.5px solid {theme_cfg['border']};
    border-radius: 26px;
    padding: 28px;
    box-shadow: 0 14px 35px rgba(214, 51, 132, 0.18);
    margin-top: 16px;
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
}}

.stat-box {{
    background: #ffffff;
    border-radius: 22px;
    padding: 22px;
    text-align: center;
    border: 2px solid {theme_cfg['border']};
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
}}

.stat-number {{
    font-size: 2.2em !important;
    font-weight: 900;
    color: {theme_cfg['accent']};
}}
</style>

<div class="floating-particle p1">{particles_list[0]}</div>
<div class="floating-particle p2">{particles_list[1]}</div>
<div class="floating-particle p3">{particles_list[2]}</div>
<div class="floating-particle p4">{particles_list[3]}</div>
<div class="floating-particle p5">{particles_list[4]}</div>
<div class="floating-particle p6">{particles_list[5]}</div>
<div class="floating-particle p7">{particles_list[0]}</div>
<div class="floating-particle p8">{particles_list[1]}</div>
""", unsafe_allow_html=True)

# =========================================================
# 4. MOTOR JS MULTI-EFECTO FIESTA MÁGICA
# =========================================================
def lanzar_efecto_fiesta_js(tipo_efecto):
    if tipo_efecto == "confetti_boom":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
        confetti({ particleCount: 180, spread: 100, origin: { y: 0.6 } });
        </script>
        """
        components.html(js_code, height=0)
    elif tipo_efecto == "fuegos_artificiales":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
        confetti({ particleCount: 200, startVelocity: 45, spread: 360, origin: { y: 0.4 } });
        </script>
        """
        components.html(js_code, height=0)
    elif tipo_efecto == "estrellas_doradas":
        js_code = """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
        confetti({ particleCount: 120, spread: 110, origin: { y: 0.6 }, colors: ['#ffd700', '#ffa500'] });
        </script>
        """
        components.html(js_code, height=0)

# =========================================================
# 5. BASE DE DATOS Y PERSISTENCIA DE DATOS
# =========================================================
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

# =========================================================
# 6. BASE DE DATOS DE MENSAJES, RECUERDOS & FRASES
# =========================================================
MENSAJES_DIARIOS = {
    "2026-07-26": {
        "fecha_str": "Domingo, 26 de Julio",
        "titulo": "🌸 Un rincón creado con el corazón 👑",
        "poema": """Mi reina hermosa,
Hoy empieza un detalle hecho a la medida de tu luz. Quería que tuvieras un espacio que te recuerde lo increíble que eres en todo momento. Gracias por ser mi lugar seguro, por tu dedicación impecable en TQ y por construir con tanta valentía tu futuro profesional en Administración. Te quiero infinitamente."""
    },
    "2026-07-27": {
        "fecha_str": "Lunes, 27 de Julio",
        "titulo": "✨ Fuerza para iniciar la semana 🚀",
        "poema": """Lunes de nuevos comienzos, mi reina.
Sé la disciplina y el compromiso con el que te levantas a dar lo mejor de ti en TQ. Nunca dudes del talento gigantesco que habita en ti. ¡A romperla hoy! Te quiero mucho."""
    }
}

LINEA_DEL_TIEMPO_RECUERDOS = [
    {
        "fecha": "Mayo 2025 - Junio 2026",
        "titulo": "🤝 Soporte Técnico & Conexión Profesional",
        "desc": "Consultas operativas sobre SharePoint, formatos PEC y checklists de droguerías TQ recomendada por Juliana.",
        "icono": "💻"
    },
    {
        "fecha": "06 de Julio de 2026",
        "titulo": "✨ El Inicio de Nuestra Cercanía Personal",
        "desc": "El primer saludo no laboral ('Pasaba no más para saludarte'). Laura resalta sus estados y surge el coqueteo.",
        "icono": "📲"
    },
    {
        "fecha": "07-08 de Julio de 2026",
        "titulo": "🎶 Charla sobre Gustos Musicales & Fútbol",
        "desc": "Coincidencias sobre la Selección, la apuesta del Mundial y la revelación de Jhon sobre su gusto por el merengue.",
        "icono": "🎵"
    }
]

FRASES_ESCRITAS_POR_TI = [
    "\"Hoy solo quería recordarte que estoy profundamente orgulloso de ti.\"",
    "\"Eres una mujer extraordinaria, madre amorosa y profesional impecable.\"",
    "\"Nunca olvides que tu inteligencia y tenacidad no tienen techo.\"",
    "\"De Medellín a Bucaramanga hay muchos kilómetros, pero estás aquí en mi pecho.\""
]

COMBOS_ICONOS = ["🌸🧸✨", "👑💖🌟", "🦋🌷💫", "❤️🎈🧸"]

PREGUNTAS_TRIVIA = [
    {
        "pregunta": "¿En qué empresa trabaja nuestra reina demostrando su talento día a día?",
        "opciones": ["TQ (Tecnoquímicas)", "Bancolombia", "Ecopetrol", "Nutresa"],
        "correcta": "TQ (Tecnoquímicas)",
        "explicacion": "¡Exacto! En TQ eres la más profesional y dedicada."
    }
]

FORTUNAS = [
    "Fortuna de Hoy: 'El esfuerzo de hoy en tus estudios de Administración se convertirá en el éxito gigante de mañana.'",
    "Fortuna de Hoy: 'Alguien a la distancia te está pensando en este preciso instante con una sonrisa enorme.'"
]

# =========================================================
# 7. GENERADOR DE PDF ELEGANTE CON REPORTLAB
# =========================================================
def generar_pdf_carta(titulo, remitente, contenido, fecha_hora_str):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, textColor=colors.HexColor("#d63384"), alignment=1, spaceAfter=15)
    meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=12, textColor=colors.HexColor("#666666"), alignment=1, spaceAfter=20)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=13, textColor=colors.HexColor("#222222"), leading=22, spaceAfter=18)
    footer_style = ParagraphStyle('FooterStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor("#ff4d6d"), alignment=2, spaceBefore=25)

    story.append(Paragraph("💌 CARTA DE PENSAMIENTOS", title_style))
    story.append(Paragraph(f"<b>Fecha y Hora:</b> {fecha_hora_str} (Hora Colombia)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#ff85a1"), spaceAfter=18))
    story.append(Paragraph(f"<b>Asunto:</b> {titulo}", ParagraphStyle('Sub', parent=title_style, fontSize=16, textColor=colors.HexColor("#ff85a1"))))
    story.append(Spacer(1, 14))
    
    contenido_formateado = contenido.replace('\n', '<br/>')
    story.append(Paragraph(contenido_formateado, body_style))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#ffc6ff"), spaceAfter=15))
    story.append(Paragraph(f"Con todo mi cariño y admiración,<br/><b>{remitente}</b>", footer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# =========================================================
# 8. ENCABEZADO PRINCIPAL Y REPRODUCTOR
# =========================================================
st.markdown("<h1 class='main-header'>👑 El Diario de Mi Reina 👑</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>De Medellín a Bucaramanga | Un espacio lleno de magia, recuerdos y momentos especiales</p>", unsafe_allow_html=True)
st.markdown(f"<div class='theme-badge'>🎨 Tema Activo: {st.session_state['user_theme']} | Tipografía: {st.session_state['user_font']}</div>", unsafe_allow_html=True)

if st.session_state["efecto_fiesta_actual"]:
    lanzar_efecto_fiesta_js(st.session_state["efecto_fiesta_actual"])
    st.session_state["efecto_fiesta_actual"] = None

col_mus1, col_mus2 = st.columns([1.2, 0.8])
with col_mus1:
    if st.button("🎵 Reproducir / Pausar nuestra canción especial"):
        st.session_state["reproduciendo_musica"] = not st.session_state["reproduciendo_musica"]

with col_mus2:
    if st.session_state["reproduciendo_musica"]:
        st.markdown("""
        <div style='background: white; border-radius: 18px; padding: 10px 18px; border: 2px solid #ff85a1;'>
            <span style='color: #d63384; font-weight: bold;'>🎶 Reproduciendo nuestra melodía...</span>
        </div>
        """, unsafe_allow_html=True)

st.write("---")

# =========================================================
# 9. PESTAÑAS INTERACTIVAS (PARTE 1: PESTAÑAS 1 A 5)
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏡 Portada", "📜 Línea del Tiempo", "📅 Calendario", "📊 Estadísticas", "🎨 Personalización"
])

# --- TAB 1: PORTADA ---
with tab1:
    col_texto, col_foto = st.columns([1.15, 0.85], gap="large")
    with col_texto:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #d63384;'>¡Bienvenida a tu espacio consentido, Mi Reina! 👑</h3>
            <p>Este diario interactivo fue diseñado con todo el amor del mundo para acompañarte en tus metas en <b>TQ</b>, tus jornadas de estudio en <b>Administración de Empresas</b> y tus momentos libres.</p>
        </div>
        """, unsafe_allow_html=True)

        fecha_colombia = datetime.now(tz_colombia)
        fecha_hoy_key = fecha_colombia.strftime("%Y-%m-%d")
        mensaje_hoy = MENSAJES_DIARIOS.get(fecha_hoy_key, {
            "fecha_str": fecha_colombia.strftime("%A, %d de %B"),
            "titulo": "✨ Un mensaje especial para ti",
            "poema": "Mi reina hermosa, recuerda siempre lo increíble, inteligente y hermosa que eres."
        })

        st.markdown(f"""
        <div class='daily-card'>
            <span style='background-color: #ff85a1; color: white; padding: 6px 14px; border-radius: 12px;'>{mensaje_hoy['fecha_str']}</span>
            <h3 style='color: #c2185b; margin-top: 14px;'>{mensaje_hoy['titulo']}</h3>
            <p style='white-space: pre-line;'>{mensaje_hoy['poema']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_foto:
        st.markdown("<div class='stat-box'><b>📍 Ruta Medellín ➔ Bucaramanga</b><br>Pensándote 24/7 con mariposas y sonrisas 🦋</div>", unsafe_allow_html=True)

# --- TAB 2: LÍNEA DEL TIEMPO ---
with tab2:
    st.markdown("<h3 style='color: #d63384;'>📜 Línea del Tiempo de Nuestra Relación</h3>", unsafe_allow_html=True)
    for hito in LINEA_DEL_TIEMPO_RECUERDOS:
        st.markdown(f"""
        <div class='timeline-item'>
            <div class='timeline-icon'>{hito['icono']}</div>
            <div>
                <b>{hito['fecha']}</b>
                <h4 style='color: #c2185b; margin: 2px 0;'>{hito['titulo']}</h4>
                <p style='color: #444;'>{hito['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: CALENDARIO ---
with tab3:
    st.markdown("<h3 style='color: #d63384;'>📅 Calendario Interactivo</h3>", unsafe_allow_html=True)
    fecha_sel = st.date_input("Elige una fecha:", value=date.today())
    st.info(f"Mostrando actividades y recuerdos registrados para el: {fecha_sel.strftime('%d/%m/%Y')}")

# --- TAB 4: ESTADÍSTICAS ---
with tab4:
    st.markdown("<h3 style='color: #d63384;'>📊 Estadísticas Bonitas & Logros</h3>", unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Sonrisas Registradas", st.session_state["sonrisas_count"])
    col_s2.metric("Metas Cumplidas", st.session_state["metas_cumplidas_count"])
    col_s3.metric("Cartas Creadas", st.session_state["cartas_creadas_count"])

# --- TAB 5: PERSONALIZACIÓN ---
with tab5:
    st.markdown("<h3 style='color: #d63384;'>🎨 Centro de Personalización Mágica</h3>", unsafe_allow_html=True)
    nuevo_tema = st.selectbox("Tema:", list(THEME_PRESETS.keys()))
    nueva_fuente = st.selectbox("Tipografía:", list(FONTS_PRESETS.keys()))
    if st.button("Aplicar Cambios"):
        st.session_state["user_theme"] = nuevo_tema
        st.session_state["user_font"] = nueva_fuente
        st.success("¡Personalización guardada!")
        st.rerun()
