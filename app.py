import streamlit as st
import json
import os
from datetime import datetime, timedelta, date
import pytz
import io
import random

# Librerías para generar el PDF elegante con ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y BIENVENIDA
# ==========================================
st.set_page_config(
    page_title="El Diario de Mi Reina 👑",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Efecto de bienvenida inicial
if "bienvenida" not in st.session_state:
    st.balloons()
    st.session_state["bienvenida"] = True

# ==========================================
# 2. SISTEMA DE COLORES PASTEL DINÁMICOS POR DÍA
# ==========================================
tz_colombia = pytz.timezone("America/Bogota")
dia_semana_num = datetime.now(tz_colombia).weekday()  # 0: Lunes, 6: Domingo

PALETAS_PASTEL = {
    0: {"nombre": "Rosa Algodón de Azúcar (Lunes)", "gradient": "linear-gradient(135deg, #fff0f5 0%, #ffe3ec 40%, #f7d6e0 70%, #fff5f8 100%)"},
    1: {"nombre": "Lavanda Suave (Martes)", "gradient": "linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 40%, #f5f3ff 70%, #faf5ff 100%)"},
    2: {"nombre": "Melocotón Dulce (Miércoles)", "gradient": "linear-gradient(135deg, #fff7ed 0%, #ffedd5 40%, #fff1f2 70%, #fffaf0 100%)"},
    3: {"nombre": "Menta & Rosas (Jueves)", "gradient": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 40%, #fdf2f8 70%, #f7fee7 100%)"},
    4: {"nombre": "Seda Rosa Pastel (Viernes)", "gradient": "linear-gradient(135deg, #fdf2f8 0%, #fce7f3 40%, #fbcfe8 70%, #fff0f5 100%)"},
    5: {"nombre": "Lila Perlado (Sábado)", "gradient": "linear-gradient(135deg, #faf5ff 0%, #f3e8ff 40%, #ffe4e6 70%, #fcf5ff 100%)"},
    6: {"nombre": "Cuarzo Rosa Cálido (Domingo)", "gradient": "linear-gradient(135deg, #fff1f2 0%, #ffe4e6 40%, #fecdd3 70%, #fff5f5 100%)"}
}

fondo_hoy = PALETAS_PASTEL[dia_semana_num]["gradient"]
nombre_paleta = PALETAS_PASTEL[dia_semana_num]["nombre"]

# ==========================================
# 3. ESTILOS CSS AVANZADOS & ANIMACIONES
# ==========================================
st.markdown(f"""
<style>
/* Tipografía global */
html, body, [class*="css"], .stMarkdown, p, div, label, span {{
    font-size: 20px !important;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6 !important;
}}

.stTextInput input, .stTextArea textarea, .stSelectbox div, .stMultiSelect, .stRadio label {{
    font-size: 1.05em !important;
}}

/* Fondo dinámico por día de la semana */
.stApp {{
    background: {fondo_hoy} !important;
    background-attachment: fixed !important;
}}

/* PARTÍCULAS FLOTANTES */
.floating-particle {{
    position: fixed;
    z-index: 0;
    pointer-events: none;
    user-select: none;
    animation: floatParticle 9s infinite ease-in-out;
    opacity: 0.85;
    font-size: 2.2rem;
}}

@keyframes floatParticle {{
    0% {{ transform: translateY(105vh) translateX(0px) rotate(0deg) scale(0.8); opacity: 0; }}
    20% {{ opacity: 0.95; }}
    80% {{ opacity: 0.95; }}
    100% {{ transform: translateY(-15vh) translateX(65px) rotate(360deg) scale(1.35); opacity: 0; }}
}}

.p1 {{ left: 3%; animation-duration: 10s; animation-delay: 0s; }}
.p2 {{ left: 14%; animation-duration: 12s; animation-delay: 2s; }}
.p3 {{ left: 26%; animation-duration: 9s; animation-delay: 4s; }}
.p4 {{ left: 38%; animation-duration: 11s; animation-delay: 1s; }}
.p5 {{ left: 52%; animation-duration: 13s; animation-delay: 5s; }}
.p6 {{ left: 66%; animation-duration: 8s; animation-delay: 3s; }}
.p7 {{ left: 80%; animation-duration: 12s; animation-delay: 6s; }}
.p8 {{ left: 92%; animation-duration: 10s; animation-delay: 1.5s; }}

/* Animaciones */
@keyframes floatHeader {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-8px) rotate(1deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
}}

@keyframes flutter {{
    0%, 100% {{ transform: translateY(0px) scale(1) rotate(0deg); }}
    25% {{ transform: translateY(-6px) scale(1.08) rotate(-4deg); }}
    50% {{ transform: translateY(-2px) scale(0.96) rotate(3deg); }}
    75% {{ transform: translateY(-8px) scale(1.05) rotate(-2deg); }}
}}

@keyframes photoMovement {{
    0% {{ transform: translateY(0px) rotate(0deg) scale(1); box-shadow: 0px 10px 25px rgba(255, 77, 109, 0.3); }}
    50% {{ transform: translateY(-14px) rotate(1.5deg) scale(1.02); box-shadow: 0px 20px 38px rgba(255, 77, 109, 0.5); }}
    100% {{ transform: translateY(0px) rotate(0deg) scale(1); box-shadow: 0px 10px 25px rgba(255, 77, 109, 0.3); }}
}}

/* Encabezados y Tarjetas */
.main-header {{
    text-align: center;
    color: #c2185b;
    font-size: 3.2em !important;
    font-weight: 900;
    margin-bottom: 5px;
    animation: floatHeader 4s ease-in-out infinite;
    text-shadow: 3px 3px 10px rgba(214, 51, 132, 0.2);
}}

.sub-header {{
    text-align: center;
    color: #4a4a4a;
    font-size: 1.3em !important;
    font-weight: 600;
    margin-bottom: 20px;
}}

.theme-badge {{
    text-align: center;
    background: rgba(255, 255, 255, 0.88);
    border: 2px solid #ff85a1;
    border-radius: 20px;
    padding: 6px 18px;
    width: fit-content;
    margin: 0 auto 20px auto;
    font-size: 0.95em;
    font-weight: bold;
    color: #d63384;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}}

.card {{
    background: rgba(255, 255, 255, 0.96);
    border-radius: 24px;
    padding: 26px;
    border-left: 10px solid #ff4d6d;
    box-shadow: 0 10px 30px rgba(0,0,0,0.07);
    margin-bottom: 24px;
    font-size: 1.05em;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 14px 35px rgba(255, 77, 109, 0.2);
}}

.daily-card {{
    background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
    border: 2px solid #ffb6c1;
    border-radius: 24px;
    padding: 26px;
    box-shadow: 0 12px 32px rgba(214, 51, 132, 0.18);
    margin-top: 15px;
    animation: floatHeader 6s ease-in-out infinite;
}}

.photo-card-moving {{
    border: 4px solid #ff85a1;
    border-radius: 26px;
    padding: 16px;
    background: #ffffff;
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    color: #d63384;
    animation: photoMovement 5s ease-in-out infinite;
    transition: all 0.4s ease;
}}

.photo-card-moving:hover {{
    transform: scale(1.04) rotate(1deg) !important;
    border-color: #ff4d6d;
}}

.mood-response-box {{
    background: linear-gradient(135deg, #ffffff 0%, #fff0f3 100%);
    border-radius: 20px;
    padding: 22px;
    border: 2px solid #ff85a1;
    margin-top: 18px;
    box-shadow: 0 8px 22px rgba(255, 133, 161, 0.25);
    font-size: 1.1em;
    line-height: 1.7;
}}

.surprise-box {{
    background: #ffffff;
    border-radius: 22px;
    padding: 22px;
    border: 2px dashed #ff4d6d;
    margin-top: 18px;
    text-align: center;
    font-size: 1.15em;
    animation: flutter 4s infinite ease-in-out;
    box-shadow: 0 10px 25px rgba(255, 77, 109, 0.15);
}}

.coupon-card {{
    background: #ffffff;
    border: 3px dashed #ff85a1;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    margin-bottom: 15px;
    transition: all 0.3s ease;
}}

.coupon-card:hover {{
    transform: scale(1.03);
    border-color: #ff4d6d;
}}

.stButton>button {{
    font-size: 1.1em !important;
    border-radius: 18px !important;
    padding: 10px 22px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #ff4d6d 0%, #ff758f 100%) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 8px 20px rgba(255, 77, 109, 0.35) !important;
    transition: all 0.3s ease !important;
}}

.stButton>button:hover {{
    transform: scale(1.04) !important;
    box-shadow: 0 10px 25px rgba(255, 77, 109, 0.5) !important;
}}
</style>

<!-- Partículas flotantes -->
<div class="floating-particle p1">🧸</div>
<div class="floating-particle p2">🦋</div>
<div class="floating-particle p3">⭐</div>
<div class="floating-particle p4">💖</div>
<div class="floating-particle p5">🧸</div>
<div class="floating-particle p6">🦋</div>
<div class="floating-particle p7">✨</div>
<div class="floating-particle p8">🌸</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. BASE DE DATOS DE MENSAJES DIARIOS
# ==========================================
MENSAJES_DIARIOS = {
    "2026-07-26": {
        "fecha_str": "Domingo, 26 de Julio",
        "titulo": " Un rincón creado con el corazón 🦋🧸🌸",
        "poema": """Mi reina hermosa,
Hoy empieza un detalle hecho a la medida de tu luz. Quería que tuvieras un espacio que te recuerde lo increíble que eres, incluso cuando la rutina presione. Gracias por ser mi lugar seguro, por tu dedicación en TQ y por construir con tanta valentía tu futuro profesional en Administración. Hoy domingo te deseo calma y que recuerdes que mi admiración por ti no tiene límites. Te quiero infinitamente."""
    },
    "2026-07-27": {
        "fecha_str": "Lunes, 27 de Julio",
        "titulo": " Fuerza para iniciar la semana 🌸⭐",
        "poema": """Lunes de nuevos comienzos, mi reina.
Sé la disciplina y el compromiso con el que te levantas a dar lo mejor de ti en TQ. Nunca dudes del talento gigantesco que habita en ti ni de lo lejos que vas a llegar. Cuando sientas que la semana pesa, recuerda que aquí hay alguien a cientos de kilómetros sosteniendo tu mano en el pensamiento. ¡A romperla hoy! Te quiero mucho."""
    },
    "2026-07-28": {
        "fecha_str": "Martes, 28 de Julio",
        "titulo": " La calma en tus ojos ✨🧸",
        "poema": """Hay una serenidad única en tu mirada que me devuelve la paz en cualquier momento. Hoy martes solo quiero recordarte que no tienes que poder con todo al mismo tiempo. Vas paso a paso, construyendo un imperio de sueños para ti y tu hijita. Eres elegancia, tenacidad y ternura en una sola persona. Disfruta tu día mi reina hermosa. Te quiero."""
    },
    "2026-07-29": {
        "fecha_str": "Miércoles, 29 de Julio",
        "titulo": " Distancia que acorta el cariño 🏔️✈️",
        "poema": """De Medellín a Bucaramanga hay montañas, pero no hay distancia capaz de apagar lo mucho que te quiero. Mitad de semana, mi administradora estrella. Cada esfuerzo en tus estudios y en tu trabajo es una semilla de un futuro brillante. Te pienso a cada hora y me llena de orgullo decir que eres mi reina."""
    },
    "2026-07-30": {
        "fecha_str": "Jueves, 30 de Julio",
        "titulo": " Luz en el camino 🌸✨",
        "poema": """Casi viernes, mi vida.
Tu sonrisa tiene la magia de iluminar hasta el día más gris. Gracias por tu ternura, por tu escucha y por tu forma tan linda de ser. Que hoy sea un día fluido en el trabajo, donde las cosas salgan a tu favor y donde sientas que todo tu empeño valdrá la pena. Te quiero con todo mi ser."""
    },
    "2026-07-31": {
        "fecha_str": "Viernes, 31 de Julio",
        "titulo": " Rumbo al descanso y la finca 🏡🌳",
        "poema": """¡Llegó el viernes y se cierra Julio!
Sé lo mucho que anhelas el fin de semana para desconectarte, respirar aire puro en la finca y disfrutar de esos momentos invaluables con tu hijita. Que hoy el tiempo se pase volando en el trabajo para que comiences a disfrutar de tu espacio de paz. ¡Te mereces todo el descanso del mundo! Te quiero mucho."""
    },
    "2026-08-01": {
        "fecha_str": "Sábado, 01 de Agosto",
        "titulo": " Bienvenido Agosto 🌻🧸",
        "poema": """Iniciamos un nuevo mes, mi reina.
Sábado de tranquilidad, de aire fresco en la finca y de regalarte el tiempo que tanto trabajas en la semana. Deseo que tu corazón se llene de risas, de desconexión y de esa paz pura de hogar. Disfruta tu fin de semana mi reina bella, te quiero y te pienso donde estés."""
    },
    "2026-08-02": {
        "fecha_str": "Domingo, 02 de Agosto",
        "titulo": " Paz para el alma ☕🌸",
        "poema": """Un café por la mañana, tranquilidad en la naturaleza y el calor de quienes amas. Los domingos son para recargar el alma y tú mereces llenarte de toda la energía bonita posible. Gracias por existir, por ser tan auténtica y por darle un sentido tan lindo a mis días. Te quiero muchísimo."""
    }
}

COMBOS_ICONOS = ["🧸🦋💖", "⭐🌸✨", "☕🏡🌳", "👑🎉💖", "🎀🧸✨", "🕊️🌷🌸"]

# ==========================================
# 5. FUNCIONES DE PERSISTENCIA
# ==========================================
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

# Funciones de Cápsula del Tiempo
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

# ==========================================
# 6. GENERADOR DE PDF ELEGANTE (REPORTLAB)
# ==========================================
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
    story.append(Paragraph(f"<b>Asunto:</b> {titulo}", ParagraphStyle('Sub', parent=title_style, fontSize=16, textColor=colors.HexColor("#ff85a1"))))
    story.append(Spacer(1, 14))
    
    contenido_formateado = contenido.replace('\n', '<br/>')
    story.append(Paragraph(contenido_formateado, body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Con todo mi cariño y admiración,<br/><b>{remitente}</b> 💖", footer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ==========================================
# 7. ENCABEZADO Y MARCA PRINCIPAL
# ==========================================
st.markdown("<h1 class='main-header'>👑 El Diario de Mi Reina 💖🧸🦋</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>De Medellín a Bucaramanga 🏔️✈️🌳 | Un rincón lleno de magia, ositos, mariposas y mucho cariño</p>", unsafe_allow_html=True)
st.markdown(f"<div class='theme-badge'>🎨 Tono Pastel de Hoy: {nombre_paleta}</div>", unsafe_allow_html=True)

# ==========================================
# 8. MENÚ PRINCIPAL DE 8 PESTAÑAS
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏠 Bienvenida & Portada",
    "📝 Mi Diario Interactivo",
    "📚 Histórico de Memorias",
    "🎯 Planificador & Hábitos",
    "🎟️ Antojitos & Cupones",
    "📄 Generador PDF",
    "🏺 Frasco de Recuerdos",
    "⏳ Cápsula Secreta & Sorpresa"
])

# ------------------------------------------
# TAB 1: BIENVENIDA & PORTADA
# ------------------------------------------
with tab1:
    col_texto, col_foto = st.columns([1.15, 0.85], gap="large")
    with col_texto:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #d63384; margin-bottom: 10px; font-size: 1.55em;'>
                ¡Bienvenida a tu lugar seguro, Mi Reina! <span class='floating-badge'>👑🧸🦋</span>
            </h3>
            <p style='color: #222; font-size: 1.1em; line-height: 1.8;'>
                Este diario fue creado exclusivamente para ti, para acompañarte durante tus metas en 
                <b>TQ</b>, tus trasnochos estudiando <b>Administración de Empresas</b> y tus momentos de 
                descanso. ¡Llena tus días de ositos, mariposas, estrellas y sonrisas! 🌸✨⭐
            </p>
        </div>
        """, unsafe_allow_html=True)

        fecha_colombia = datetime.now(tz_colombia)
        fecha_hoy_key = fecha_colombia.strftime("%Y-%m-%d")
        
        mensaje_hoy = MENSAJES_DIARIOS.get(fecha_hoy_key, {
            "fecha_str": fecha_colombia.strftime("%A, %d de %B"),
            "titulo": "✨ Un mensaje especial para ti",
            "poema": "Mi reina hermosa, recuerda siempre lo increíble, inteligente y hermosa que eres. Cada día es una nueva oportunidad para acercarte a tus sueños. ¡Te quiero con todo mi corazón!"
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
        st.markdown("<h3 style='color: #d63384; font-size: 1.4em;'>🌸 Rinconcito de Sorpresas & Notas Especiales ✨</h3>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🎉 Fiesta Mágica"):
                st.balloons()
                st.snow()
        with col_btn2:
            if st.button("🦋 Mensaje Sorpresa"):
                st.balloons()
                frases = [
                    "Recordatorio: Tienes una sonrisa preciosa que devuelve la paz a cualquiera. 💖",
                    "Vas a ser una Administradora de Empresas brillante. ¡Orgullo total de tu disciplina! 🎓",
                    "Disfruta cada segundo del fin de semana en la finca con tu hijita. 🏡🌳",
                    "¡Muchos éxitos hoy en TQ! Que tengas una jornada fluida e impecable. ⭐",
                    "Desde Medellín te mando toda la buena energía, ositos, mariposas y un abrazo apretado. 🧸✈️"
                ]
                st.session_state["mensaje_sorpresa_actual"] = random.choice(frases)
                st.session_state["iconos_combo_actual"] = random.choice(COMBOS_ICONOS)
        with col_btn3:
            if st.button("⭐ Afirmación ✨"):
                afirmaciones = [
                    "\"Soy capaz, inteligente y estoy construyendo un futuro hermoso paso a paso.\"",
                    "\"Mi trabajo en TQ y mis estudios están rindiendo frutos admirables.\"",
                    "\"Merezco momentos de paz, descanso y desconexión total.\"",
                    "\"Tengo la fuerza para superar cualquier imprevisto con elegancia y serenidad.\""
                ]
                st.session_state["mensaje_sorpresa_actual"] = random.choice(afirmaciones)
                st.session_state["iconos_combo_actual"] = random.choice(COMBOS_ICONOS)

        if "mensaje_sorpresa_actual" in st.session_state:
            combo_icons = st.session_state.get("iconos_combo_actual", "🧸🦋✨")
            st.markdown(f"""
            <div class='surprise-box'>
                <div style='font-size: 1.6em; margin-bottom: 8px;'>{combo_icons}</div>
                <p style='color: #d63384; font-weight: bold; margin-bottom: 6px;'>Nota especial para ti, Mi Reina:</p>
                <b>{st.session_state['mensaje_sorpresa_actual']}</b>
            </div>
            """, unsafe_allow_html=True)

    with col_foto:
        st.markdown("""
        <div class='photo-card-moving'>
            📸 Nuestro Rincón Especial ❤️🦋🧸
            <p style='font-size: 0.85em; font-weight: normal; margin-top: 4px; color: #666;'>
                (¡Mira cómo flota nuestra foto!)
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        # Carga de la foto sin mover la maquetación
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

# ------------------------------------------
# TAB 2: MI DIARIO INTERACTIVO
# ------------------------------------------
with tab2:
    st.markdown("<h3 style='color: #d63384;'>📝 Mi Diario Personal e Interactivo</h3>", unsafe_allow_html=True)
    st.write("Escribe lo que viviste hoy, desahógate o guarda un lindo recuerdo.")
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
        "😴 Cansada": "😴 **Mi vida hermosa:** Sé que has tenido un día largo entre la oficina de TQ, tareas o la rutina. Te has esforzado un montón. Por favor regálate una ducha tibia, ponte ropa cómoda y permite que tu mente descanse. ¡Hiciste un trabajo fabuloso hoy y estoy muy orgulloso de ti! Te quiero mucho.",
        "🌿 Tranquila": "🌿 **Paz para tu corazón:** Qué dicha saber que estás disfrutando de un momento de calma. Tómate un café o té, escucha una bonita canción y disfruta esta serenidad. Te mereces cada segundo de tranquilidad, mi reina.",
        "🔥 Motivada": "🔥 **¡Esa es la actitud, mi reina!**: Tu energía positiva contagia y mueve montañas. Aprovecha este impulso para avanzar en tus metas de Administración o proyectos personales. ¡Vas con toda! Te quiero.",
        "✨ Excelente": "✨ **¡Qué felicidad verte así!**: Tu alegría ilumina todo a tu alrededor y llena el aire de mariposas y estrellas. Guarda este momento de satisfacción en tu diario y celebra cada logro, por pequeño o grande que sea.",
        "🚀 Imparable": "🚀 **¡Eres una mujer poderosa e invencible!**: No hay reto laboral ni examen de universidad que pueda contigo. Tienes la berraquera y la inteligencia para devorarte el mundo. ¡A brillar, mi reina!",
        "🤯 Abrumada / Estresada": "🤯 **Respira profundo, mi cielo:** Cierra los ojos 5 segundos. No tienes que resolver todo en un solo día. Ve paso a paso. Recuerda que aquí estoy siempre para escucharte, apoyarte y acompañarte. Te quiero mucho."
    }

    st.markdown(f"""
    <div class='mood-response-box'>
        {respuestas_animo[estado_animo]}
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col_input1, col_input2 = st.columns([1.2, 0.8])
    with col_input1:
        titulo_entrada = st.text_input("Título para tu nota de hoy:", placeholder="Ej: Avances en TQ / Tarde bonita en la finca...")
    with col_input2:
        etiqueta_entrada = st.selectbox("Categoría:", ["💼 Trabajo TQ", "🎓 Universidad / Administración", "🏡 Finca / Familia", "💭 Pensamientos", "☕ Descanso"])

    contenido_entrada = st.text_area("Escribe aquí tus pensamientos del día:", height=180, placeholder="Hoy me sentí... logré terminar mis pendientes y compartí tiempo con...")

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
        else:
            st.warning("Por favor escribe un título y el contenido antes de guardar.")

# ------------------------------------------
# TAB 3: HISTÓRICO DE MEMORIAS & GESTIÓN
# ------------------------------------------
with tab3:
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
        st.info("Aún no tienes entradas guardadas en tu histórico. ¡Escribe la primera en la pestaña 'Mi Diario Interactivo'!")

# ------------------------------------------
# TAB 4: PLANIFICADOR & HÁBITOS
# ------------------------------------------
with tab4:
    st.markdown("<h3 style='color: #d63384;'>🎯 Planificador & Hábitos Diarios de Mi Reina</h3>", unsafe_allow_html=True)
    st.write("Un organizador sencillo para cuidar tu salud, tus estudios en Administración y tus metas en TQ.")
    st.write("---")
    
    col_hab1, col_hab2 = st.columns(2, gap="large")
    
    with col_hab1:
        st.markdown("<h4 style='color: #c2185b;'>🌸 Bienestar & Autocuidado</h4>", unsafe_allow_html=True)
        h1 = st.checkbox("Tomar al menos 2 litros de agua 💧")
        h2 = st.checkbox("Hacer una pausa activa y estirar la espalda 🧘‍♀️")
        h3 = st.checkbox("Disfrutar un café/té con tranquilidad ☕")
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
        st.success("¡Eres sencillamente increíble, mi reina! Cumpliste todos tus hábitos de hoy. 🎉")
    elif porcentaje >= 50:
        st.info("¡Vas super bien! Recuerda no presionarte y disfrutar el proceso paso a paso. ✨")

# ------------------------------------------
# TAB 5: ANTOJITOS & CUPONES
# ------------------------------------------
with tab5:
    st.markdown("<h3 style='color: #d63384;'>🎟️ Antojitos, Gustos & Cupones Especiales</h3>", unsafe_allow_html=True)
    st.write("¡Canjea tus cupones simbólicos cuando quieras consentirte!")
    
    col_c1, col_c2 = st.columns(2, gap="large")
    
    with col_c1:
        st.markdown("""
        <div class='coupon-card'>
            <h4 style='color: #c2185b; margin-bottom: 5px;'>🍝 Cupón: Noche de Lasaña / Pastas</h4>
            <p style='color: #555; font-size: 0.95em;'>Válido para disfrutar tu comida preferida sin preocupaciones.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🍕 Canjear Cupón Pasta/Lasaña"):
            st.balloons()
            st.success("¡Cupón Canjeado! Que disfrutes un banquete delicioso mi reina. 😋")

        st.markdown("""
        <div class='coupon-card'>
            <h4 style='color: #c2185b; margin-bottom: 5px;'>🎬 Cupón: Peli de Terror & Popcorn</h4>
            <p style='color: #555; font-size: 0.95em;'>Válido para una maratón espeluznante y llena de descanso.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🍿 Canjear Cupón Película"):
            st.balloons()
            st.success("¡Cupón Canjeado! Prepara las cotufas para la peli. 🍿🎃")

    with col_c2:
        st.markdown("""
        <div class='coupon-card'>
            <h4 style='color: #c2185b; margin-bottom: 5px;'>🏡 Cupón: Fin de Semana en la Finca</h4>
            <p style='color: #555; font-size: 0.95em;'>Válido para desconectarte del trabajo de TQ y respirar aire puro.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌿 Canjear Cupón Finca"):
            st.balloons()
            st.success("¡Cupón Canjeado! Modo paz y naturaleza activado. 🌳✨")

        st.markdown("""
        <div class='coupon-card'>
            <h4 style='color: #c2185b; margin-bottom: 5px;'>🛋️ Cupón: Tarde de Cero Estrés</h4>
            <p style='color: #555; font-size: 0.95em;'>Válido para soltar los pendientes y descansar profundamente.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💖 Canjear Cupón Cero Estrés"):
            st.balloons()
            st.success("¡Cupón Canjeado! Inhala paz, exhala tensión. 🧘‍♀️")

# ------------------------------------------
# TAB 6: GENERADOR DE CARTAS PDF
# ------------------------------------------
with tab6:
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
        st.success("¡Tu carta PDF ha sido creada exitosamente! 🎉")
        st.download_button(
            label="📥 Descargar Carta en PDF",
            data=pdf_bytes,
            file_name=f"Carta_Mi_Reina_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

# ------------------------------------------
# TAB 7: FRASCO DE RECUERDOS & RULETA MÁGICA
# ------------------------------------------
with tab7:
    st.markdown("<h3 style='color: #d63384;'>🏺 Frasco de Recuerdos & Ruleta Mágica</h3>", unsafe_allow_html=True)
    st.write("Saca una notita del frasco virtual cada vez que quieras sonreír.")

    razones = [
        "Por tu sonrisa que ilumina mis días a la distancia.",
        "Por la admiración gigante que siento al verte estudiar Administración.",
        "Por tu profesionalismo y entrega impecable en TQ.",
        "Por el cariño tan hermoso con el que cuidas a tu hijita y a tu hogar.",
        "Por tu dulzura, tus chistes y cada conversación compartida.",
        "Por la magia que le transmites a todo lo que haces.",
        "Por ser mi lugar seguro y mi reina consentida.",
        "Por lo lindo que es tenerte en mi vida y compartir estos detalles."
    ]

    if st.button("🏺 Sacar una nota del Frasco"):
        nota = random.choice(razones)
        combo = random.choice(COMBOS_ICONOS)
        st.balloons()
        st.markdown(f"""
        <div class='surprise-box' style='background: #fff0f5; border: 3px solid #ff4d6d;'>
            <div style='font-size: 1.8em; margin-bottom: 6px;'>{combo}</div>
            <h3 style='color: #c2185b; margin: 0;'>Notita del Frasco para Mi Reina:</h3>
            <p style='font-size: 1.25em; margin-top: 10px; color: #333;'><b>{nota}</b></p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 8: CÁPSULA DEL TIEMPO & SORPRESA DEFINITIVA
# ------------------------------------------
with tab8:
    st.markdown("<h3 style='color: #d63384;'>⏳ Cápsula del Tiempo & Sorpresas Secretas</h3>", unsafe_allow_html=True)
    st.write("¡Este es un lugar mágico! Aquí puedes encontrar o crear mensajes que solo pueden ser desbloqueados en el futuro.")

    st.write("---")
    st.markdown("<h4 style='color: #c2185b;'>🔒 Dejar un Mensaje Candado (Cápsula)</h4>", unsafe_allow_html=True)
    
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
    st.markdown("<h4 style='color: #c2185b;'>🔑 Abrir Cápsulas del Tiempo Guardadas</h4>", unsafe_allow_html=True)
    
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

    st.write("---")
    st.markdown("<h4 style='color: #c2185b;'>🎲 Ruleta de Ideas para Citas & Planes Sorpresa</h4>", unsafe_allow_html=True)
    
    planes_citas = [
        "🍕 **Noche de Pizza a la Distancia:** Pedir cada uno su pizza favorita y hacer videollamada para comer juntos.",
        "🎬 **Cine Virtual:** Ver la misma peli de terror al tiempo compartiendo reacciones por chat.",
        "☕ **Tarde de Café & Charla:** Tomar un café virtual sin afanes para hablar de la semana.",
        "🏡 **Plan Finca:** Picnic improvisado con música suave en el jardín de la finca.",
        "🍦 **Noche de Helado:** Ir a por un heladito o postre rico para celebrar que culminaste la semana."
    ]

    if st.button("🎲 Girar Ruleta de Citas"):
        plan_elegido = random.choice(planes_citas)
        st.balloons()
        st.markdown(f"""
        <div style='background: #fff0f3; border: 2px dashed #ff4d6d; padding: 18px; border-radius: 20px; text-align: center;'>
            <h3 style='color: #d63384; margin: 0;'>✨ Plan Sorpresa Generado:</h3>
            <p style='font-size: 1.15em; color: #222; margin-top: 8px;'>{plan_elegido}</p>
        </div>
        """, unsafe_allow_html=True)
