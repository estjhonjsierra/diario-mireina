import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pytz
import io
import random

# Librerías para generar el PDF elegante
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Diario Especial | Laura Sofía 💖🦋",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Efecto de bienvenida inicial
if "bienvenida" not in st.session_state:
    st.balloons()
    st.session_state["bienvenida"] = True

# ==========================================
# 2. ESTILOS CSS AVANZADOS, TIPOGRAFÍA GRANDE & ANIMACIONES FLOTANTES
# ==========================================
st.markdown("""
    <style>
    /* ----------------------------------------------------
       CONFIGURACIÓN GLOBAL DE TIPOGRAFÍA GRANDE (MAYOR TAMAÑO)
       ---------------------------------------------------- */
    html, body, [class*="css"], .stMarkdown, p, div, label, span {
        font-size: 21px !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6 !important;
    }

    /* Entradas de texto, selectores y botones con letra grande */
    .stTextInput input, .stTextArea textarea, .stSelectbox div, .stMultiSelect, .stRadio label {
        font-size: 1.1em !important;
    }

    /* Fondo Degradado Suave con Destellos Pastel */
    .stApp {
        background: linear-gradient(135deg, #fff0f3 0%, #ffe3ec 40%, #f7d6e0 70%, #fff5f7 100%);
        background-attachment: fixed;
    }

    /* ----------------------------------------------------
       MARIPOSAS Y CORAZONES FLOTANTES EN EL FONDO (ANIMADOS)
       ---------------------------------------------------- */
    .floating-particle {
        position: fixed;
        z-index: 0;
        pointer-events: none;
        user-select: none;
        animation: floatParticle 9s infinite ease-in-out;
        opacity: 0.75;
        font-size: 1.8rem;
    }

    @keyframes floatParticle {
        0% {
            transform: translateY(105vh) translateX(0px) rotate(0deg) scale(0.8);
            opacity: 0;
        }
        20% { opacity: 0.85; }
        80% { opacity: 0.85; }
        100% {
            transform: translateY(-15vh) translateX(50px) rotate(360deg) scale(1.25);
            opacity: 0;
        }
    }

    /* Posiciones y ritmos variados para partículas */
    .p1 { left: 5%; animation-duration: 10s; animation-delay: 0s; }
    .p2 { left: 18%; animation-duration: 12s; animation-delay: 2s; }
    .p3 { left: 32%; animation-duration: 9s;  animation-delay: 4s; }
    .p4 { left: 48%; animation-duration: 11s; animation-delay: 1s; }
    .p5 { left: 63%; animation-duration: 13s; animation-delay: 5s; }
    .p6 { left: 78%; animation-duration: 8s;  animation-delay: 3s; }
    .p7 { left: 90%; animation-duration: 12s; animation-delay: 6s; }

    /* ----------------------------------------------------
       KEYFRAMES Y ANIMACIONES DE ELEMENTOS
       ---------------------------------------------------- */
    @keyframes floatHeader {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(1deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    @keyframes flutter {
        0%, 100% { transform: translateY(0px) scale(1) rotate(0deg); }
        25% { transform: translateY(-6px) scale(1.08) rotate(-4deg); }
        50% { transform: translateY(-2px) scale(0.96) rotate(3deg); }
        75% { transform: translateY(-8px) scale(1.05) rotate(-2deg); }
    }

    /* ANIMACIÓN EN VIVO DE LA FOTO (MOVIMIENTO Y BRILLO CONTINUO) */
    @keyframes photoMovement {
        0% {
            transform: translateY(0px) rotate(0deg) scale(1);
            box-shadow: 0px 10px 25px rgba(255, 77, 109, 0.3);
        }
        50% {
            transform: translateY(-14px) rotate(1.5deg) scale(1.02);
            box-shadow: 0px 20px 38px rgba(255, 77, 109, 0.5);
        }
        100% {
            transform: translateY(0px) rotate(0deg) scale(1);
            box-shadow: 0px 10px 25px rgba(255, 77, 109, 0.3);
        }
    }

    /* ----------------------------------------------------
       ESTILOS DE ENCABEZADO Y TARJETAS
       ---------------------------------------------------- */
    .main-header {
        text-align: center;
        color: #c2185b;
        font-size: 3.2em !important;
        font-weight: 900;
        margin-bottom: 5px;
        animation: floatHeader 4s ease-in-out infinite;
        text-shadow: 3px 3px 10px rgba(214, 51, 132, 0.2);
    }

    .sub-header {
        text-align: center;
        color: #4a4a4a;
        font-size: 1.35em !important;
        font-weight: 600;
        margin-bottom: 28px;
    }

    /* Tarjetas Interactivas con Elevación */
    .card {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 24px;
        padding: 28px;
        border-left: 10px solid #ff4d6d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.07);
        margin-bottom: 24px;
        font-size: 1.1em;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 14px 35px rgba(255, 77, 109, 0.2);
    }

    .daily-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
        border: 2px solid #ffb6c1;
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 12px 32px rgba(214, 51, 132, 0.18);
        margin-top: 15px;
        animation: floatHeader 6s ease-in-out infinite;
    }

    /* FOTO ANIMADA EN VIVO CON MOVIMIENTO FLOTANTE Y MARIPOSA */
    .photo-card-moving {
        border: 4px solid #ff85a1;
        border-radius: 26px;
        padding: 16px;
        background: #ffffff;
        text-align: center;
        font-size: 1.25em;
        font-weight: bold;
        color: #d63384;
        animation: photoMovement 5s ease-in-out infinite;
        transition: all 0.4s ease;
    }

    .photo-card-moving:hover {
        transform: scale(1.04) rotate(1deg) !important;
        border-color: #ff4d6d;
    }

    .mood-response-box {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f3 100%);
        border-radius: 20px;
        padding: 25px;
        border: 2px solid #ff85a1;
        margin-top: 20px;
        box-shadow: 0 8px 22px rgba(255, 133, 161, 0.25);
        font-size: 1.15em;
        line-height: 1.7;
    }

    .surprise-box {
        background: #ffffff;
        border-radius: 20px;
        padding: 22px;
        border: 2px dashed #ff4d6d;
        margin-top: 18px;
        text-align: center;
        font-size: 1.2em;
        animation: flutter 4s infinite ease-in-out;
    }

    /* Botones Grandes y Llamativos */
    .stButton>button {
        font-size: 1.2em !important;
        border-radius: 18px !important;
        padding: 14px 28px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ff4d6d 0%, #ff758f 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(255, 77, 109, 0.35) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: scale(1.04) !important;
        box-shadow: 0 10px 25px rgba(255, 77, 109, 0.5) !important;
    }

    /* Badge Flotante Decorativo */
    .floating-badge {
        display: inline-block;
        animation: flutter 3s ease-in-out infinite;
        font-size: 1.5em;
    }

    .counter-box {
        background: linear-gradient(135deg, #ff758f 0%, #ff4d6d 100%);
        color: white;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(255, 77, 109, 0.3);
        margin-bottom: 15px;
    }
    .counter-box h2 {
        color: white !important;
        margin: 0;
        font-size: 2.2em !important;
    }
    </style>

    <!-- INYECCIÓN DE CORAZONES Y MARIPOSAS FLOTANTES EN PANTALLA -->
    <div class="floating-particle p1">🦋</div>
    <div class="floating-particle p2">💖</div>
    <div class="floating-particle p3">🦋</div>
    <div class="floating-particle p4">💕</div>
    <div class="floating-particle p5">🌸</div>
    <div class="floating-particle p6">🦋</div>
    <div class="floating-particle p7">✨</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. BASE DE DATOS EXTENDIDA DE MENSAJES DIARIOS
# ==========================================
MENSAJES_DIARIOS = {
    "2026-07-26": {
        "fecha_str": "Domingo, 26 de Julio",
        "titulo": "✨ Un rincón creado con el corazón 🦋💖",
        "poema": """Mi reina hermosa,
Hoy empieza un detalle hecho a la medida de tu luz. Quería que tuvieras un espacio que te recuerde lo increíble que eres, incluso cuando la rutina presione. Gracias por ser mi lugar seguro, por tu dedicación en TQ y por construir con tanta valentía tu futuro profesional en Administración. Hoy domingo te deseo calma y que recuerdes que mi admiración por ti no tiene límites. Te amo infinitamente."""
    },
    "2026-07-27": {
        "fecha_str": "Lunes, 27 de Julio",
        "titulo": "💪 Fuerza para iniciar la semana 🦋🌸",
        "poema": """Lunes de nuevos comienzos, mi reina.
Sé la disciplina y el compromiso con el que te levantas a dar lo mejor de ti en TQ. Nunca dudes del talento gigantesco que habita en ti ni de lo lejos que vas a llegar. Cuando sientas que la semana pesa, recuerda que aquí hay alguien a cientos de kilómetros sosteniendo tu mano en el pensamiento. ¡A romperla hoy!"""
    },
    "2026-07-28": {
        "fecha_str": "Martes, 28 de Julio",
        "titulo": "🌹 La calma en tus ojos ✨💖",
        "poema": """Hay una serenidad única en tu mirada que me devuelve la paz en cualquier momento. Hoy martes solo quiero recordarte que no tienes que poder con todo al mismo tiempo. Vas paso a paso, construyendo un imperio de sueños para ti y tu hijita. Eres elegancia, tenacidad y ternura en una sola persona. Disfruta tu día mi niña hermosa."""
    },
    "2026-07-29": {
        "fecha_str": "Miércoles, 29 de Julio",
        "titulo": "🏔️ Distancia que acorta el amor 🦋✈️",
        "poema": """De Medellín a Bucaramanga hay montañas, pero no hay distancia capaz de apagar lo que siento por ti. Mitad de semana, mi administradora estrella. Cada esfuerzo en tus estudios y en tu trabajo es una semilla de un futuro brillante. Te pienso a cada hora y me llena de orgullo decir que eres mi reina."""
    },
    "2026-07-30": {
        "fecha_str": "Jueves, 30 de Julio",
        "titulo": "✨ Luz en el camino 🌸💖",
        "poema": """Casi viernes, mi vida.
Tu sonrisa tiene la magia de iluminar hasta el día más gris. Gracias por tu ternura, por tu escucha y por tu forma tan linda de amar. Que hoy sea un día fluido en el trabajo, donde las cosas salgan a tu favor y donde sientas que todo tu empeño valdrá la pena. Te amo con todo mi ser."""
    },
    "2026-07-31": {
        "fecha_str": "Viernes, 31 de Julio",
        "titulo": "🏡 Rumbo al descanso y la finca 🦋🌱",
        "poema": """¡Llegó el viernes y se cierra Julio!
Sé lo mucho que anhelas el fin de semana para desconectarte, respirar aire puro en la finca y disfrutar de esos momentos invaluables con tu hijita. Que hoy el tiempo se pase volando en el trabajo para que comiences a disfrutar de tu espacio de paz. ¡Te mereces todo el descanso del mundo!"""
    },
    "2026-08-01": {
        "fecha_str": "Sábado, 01 de Agosto",
        "titulo": "🌸 Bienvenido Agosto 💖✨",
        "poema": """Iniciamos un nuevo mes, mi reina.
Sábado de tranquilidad, de aire fresco en la finca y de regalarte el tiempo que tanto trabajas en la semana. Deseo que tu corazón se llene de risas, de desconexión y de ese amor puro de hogar. Disfruta tu fin de semana mi reina bella, te pienso donde estés."""
    },
    "2026-08-02": {
        "fecha_str": "Domingo, 02 de Agosto",
        "titulo": "☕ Paz para el alma 🦋❤️",
        "poema": """Un café por la mañana, tranquilidad en la naturaleza y el calor de quienes amas. Los domingos son para recargar el alma y tú mereces llenarte de toda la energía bonita posible. Gracias por existir, por ser tan auténtica y por darle un sentido tan lindo a mis días."""
    },
    "2026-08-03": {
        "fecha_str": "Lunes, 03 de Agosto",
        "titulo": "🚀 Con la mente en alto 💼✨",
        "poema": """Iniciamos semana de trabajo y metas.
Recuerda que cada reto laboral en TQ demuestra la mujer capaz, inteligente y estructurada que eres. No te achiquopales ante ningún obstáculo; tienes la capacidad y la berraquera para resolver lo que sea. ¡Estoy muy orgulloso de ti!"""
    },
    "2026-08-04": {
        "fecha_str": "Martes, 04 de Agosto",
        "titulo": "🎓 Tu futuro como Administradora 💖📚",
        "poema": """Ver tu entrega con los estudios de Administración me inspira a diario. Sé las noches de cansancio y el sacrificio de equilibrar todo: trabajo, estudio y hogar. Pero créeme, reina, cada trasnocho se convertirá en los triunfos más grandes de tu vida. Sigue firme, vas increíble."""
    },
    "2026-08-05": {
        "fecha_str": "Miércoles, 05 de Agosto",
        "titulo": "💖 Mi refugio preferido 🦋✨",
        "poema": """Si me preguntaran dónde quiero estar, siempre diría que a tu lado o en tu pensamiento. Eres esa persona con la que hablar de todo y de nada se siente perfecto. Mitad de semana mi reina, que hoy las tareas salgan rápido y sin contratiempos."""
    },
    "2026-08-06": {
        "fecha_str": "Jueves, 06 de Agosto",
        "titulo": "🌟 Orgullo y admiración 🌸👑",
        "poema": """No hay un solo día en que no me sienta afortunado de tenerte en mi vida. Admirar tu belleza es fácil, pero admirar tu temple, tu rol como madre y tu ética impecable es lo que realmente me tiene cautivado. Un abrazo apretado desde aquí."""
    },
    "2026-08-07": {
        "fecha_str": "Viernes, 07 de Agosto",
        "titulo": "🍕 Noche de antojitos y relax 🍿❤️",
        "poema": """¡Viernes! Hoy es día de soltar las cargas de la oficina, quizás pedir esa lasaña o pasta deliciosa que tanto te gusta y relajarse. Mañana nos espera un fin de semana hermoso. Que tengas una tarde tranquila y feliz mi reina."""
    },
    "2026-08-08": {
        "fecha_str": "Sábado, 08 de Agosto",
        "titulo": "🍃 Respirar y disfrutar 🦋🏡",
        "poema": """Que la brisa de la finca te despeje cualquier estrés y que el sonido de la naturaleza te llene de calma. Pasa un sábado espectacular rodeada de amor, risas con tu niña y esos pequeños momentos que hacen la vida bella."""
    },
    "2026-08-09": {
        "fecha_str": "Domingo, 09 de Agosto",
        "titulo": "🍿 Pelis de terror y descanso 👻💖",
        "poema": """Domingo ideal para acurrucarse a ver películas (o una buena de terror de las tuyas 👻), comer algo rico y recargar baterías sin afanes. Que descanses profundamente para que inicies la semana renovada."""
    },
    "2026-08-10": {
        "fecha_str": "Lunes, 10 de Agosto",
        "titulo": "💎 Eres invencible 🦋🔥",
        "poema": """Empieza otra semana para brillar. A veces se nos olvida lo fuertes que somos hasta que nos toca demostrarlo, y tú, mi reina, has demostrado una y otra vez que no hay meta que te quede grande. ¡Con toda hoy en TQ!"""
    },
    "2026-08-15": {
        "fecha_str": "Sábado, 15 de Agosto",
        "titulo": "🏡 El lugar donde eres feliz 🌸💖",
        "poema": """Nada se compara a ver la paz que sientes cuando estás en la finca. Que este sábado sea para disfrutar de los tuyos, tomar el sol y olvidar cualquier pendiente de trabajo. Disfrútalo al máximo mi cielo."""
    },
    "2026-08-20": {
        "fecha_str": "Jueves, 20 de Agosto",
        "titulo": "💖 Siempre en mi corazón 🦋✈️",
        "poema": """No importa cuántos correos o tareas tengas hoy en TQ, tómate un minuto para respirar y sentir que desde Medellín te estoy enviando todo mi amor y la mejor energía. Eres maravillosa."""
    },
    "2026-08-26": {
        "fecha_str": "Miércoles, 26 de Agosto",
        "titulo": "💖 Un mes en este diario y siempre 🦋👑",
        "poema": """Mi reina hermosa, hoy cumplimos un mes en este rinconcito especial. Gracias por permitirme estar a tu lado en la distancia, apoyarte y recordarte a diario lo infinitamente especial que eres para mí. ¡Te amo con el alma!"""
    }
}

# ==========================================
# 4. FUNCIONES DE PERSISTENCIA Y PDF
# ==========================================
DB_FILE = "diario_laura.json"

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
        fontSize=14,
        textColor=colors.HexColor("#222222"),
        leading=24,
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

    story.append(Paragraph("💖 CARTA DE PENSAMIENTOS 🦋", title_style))
    story.append(Paragraph("🌸 ✨ 🦋 ✨ 💖 ✨ 🌸", title_style))
    story.append(Paragraph(f"<b>Fecha y Hora:</b> {fecha_hora_str} (Hora Colombia)", meta_style))
    story.append(Paragraph(f"<b>Asunto:</b> {titulo}", ParagraphStyle('Sub', parent=title_style, fontSize=18, textColor=colors.HexColor("#ff85a1"))))
    story.append(Spacer(1, 14))
    
    contenido_formateado = contenido.replace('
', '<br/>')
    story.append(Paragraph(contenido_formateado, body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Con todo mi amor y admiración,<br/><b>{remitente}</b> ✨🦋", footer_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("🌸 ✨ 🦋 ✨ 💖 ✨ 🌸", title_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ==========================================
# 5. ENCABEZADO Y MARCA PRINCIPAL
# ==========================================
st.markdown("<h1 class='main-header'>✨ El Diario de Laura Sofía 💖🦋</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>De Medellín a Bucaramanga 🏔️✈️🌳 | Un rincón lleno de magia, mariposas y amor</p>", unsafe_allow_html=True)

# ==========================================
# 6. MENÚ PRINCIPAL DE 5 PESTAÑAS
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👑 Bienvenida & Portada", 
    "✍️ Mi Diario Interactivo", 
    "🍕 Nuestros Detalles & Gustos", 
    "📜 Generador de Cartas PDF ✨",
    "🌟 Frasco de Recuerdos & Extra 💕"
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
                ¡Bienvenida a tu lugar seguro, mi Reina! <span class='floating-badge'>👑🦋</span>
            </h3>
            <p style='color: #222; font-size: 1.15em; line-height: 1.8;'>
                Este diario fue creado exclusivamente para ti, para acompañarte durante tus metas en <b>TQ</b>, 
                tus trasnochos estudiando <b>Administración de Empresas</b> y tus momentos de descanso.
                ¡Llena tus días de mariposas, corazones y sonrisas! 🌸✨
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Fecha actual en Colombia
        tz_colombia = pytz.timezone("America/Bogota")
        fecha_colombia = datetime.now(tz_colombia)
        fecha_hoy_key = fecha_colombia.strftime("%Y-%m-%d")
        
        mensaje_hoy = MENSAJES_DIARIOS.get(fecha_hoy_key, {
            "fecha_str": fecha_colombia.strftime("%A, %d de %B"),
            "titulo": "✨ Un mensaje especial para ti 🦋💖",
            "poema": "Mi reina hermosa, recuerda siempre lo increíble, inteligente y hermosa que eres. Cada día es una nueva oportunidad para acercarte a tus sueños. ¡Te amo con todo mi corazón!"
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
        
        # SECCIÓN DE SORPRESAS Y ÁNIMO INTEGRADA AQUÍ
        st.markdown("<h3 style='color: #d63384; font-size: 1.5em;'>🌟 Rinconcito de Sorpresas & Ánimo 🦋</h3>", unsafe_allow_html=True)
        st.write("¿Quieres una chispa de alegría extra hoy?")
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🎉 Celebración 💖"):
                st.balloons()
                st.snow()
                
        with col_btn2:
            if st.button("🎲 Mensaje Sorpresa 🦋"):
                st.balloons()
                frases = [
                    "Recordatorio: Tienes una sonrisa preciosa que devuelve la paz a cualquiera. 😊✨",
                    "Vas a ser una Administradora de Empresas brillante. ¡Orgullo total de tu disciplina! 🎓💪",
                    "Disfruta cada segundo del fin de semana en la finca con tu hijita. 🏡💖",
                    "¡Muchos éxitos hoy en TQ! Que tengas una jornada fluida e impecable. 💼🌟",
                    "Desde Medellín te mando toda la buena energía, mariposas y un abrazo apretado. 🏔️✈️",
                    "No olvides regalarte una pausa activa, tomar agüita y respirar profundo. ☕🌸",
                    "Eres la reina de tu propio destino y nada te queda grande. 👑🔥"
                ]
                st.session_state["mensaje_sorpresa_actual"] = random.choice(frases)

        with col_btn3:
            if st.button("🌸 Afirmación 🦋"):
                afirmaciones = [
                    "✨ 'Soy capaz, inteligente y estoy construyendo un futuro hermoso paso a paso.'",
                    "✨ 'Mi trabajo en TQ y mis estudios están rindiendo frutos admirables.'",
                    "✨ 'Merezco momentos de paz, descanso y desconexión total.'",
                    "✨ 'Tengo la fuerza para superar cualquier imprevisto con elegancia y serenidad.'"
                ]
                st.session_state["mensaje_sorpresa_actual"] = random.choice(afirmaciones)

        if "mensaje_sorpresa_actual" in st.session_state:
            st.markdown(f"""
            <div class='surprise-box'>
                <p style='color: #d63384; font-weight: bold; margin-bottom: 6px; font-size: 1.1em;'>💖 Nota especial para ti 🦋:</p>
                <b>{st.session_state['mensaje_sorpresa_actual']}</b>
            </div>
            """, unsafe_allow_html=True)

    with col_foto:
        # FOTO CON ANIMACIÓN Y MOVIMIENTO CONTINUO
        st.markdown("""
        <div class='photo-card-moving'>
            <b>📸 Nuestro Rincón Especial 💖🦋</b>
            <p style='font-size: 0.85em; font-weight: normal; margin-top: 4px; color: #666;'>
                (¡Mira cómo flota nuestra foto!)
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        # Carga dinámica de foto de portada
        if os.path.exists("portada.jpg"):
            st.image("portada.jpg", caption="¡Siempre juntos y flotando de amor, mi reina hermosa! ✨💖🦋", use_container_width=True)
        elif os.path.exists("portada.jpeg"):
            st.image("portada.jpeg", caption="¡Siempre juntos y flotando de amor, mi reina hermosa! ✨💖🦋", use_container_width=True)
        elif os.path.exists("portada.png"):
            st.image("portada.png", caption="¡Siempre juntos y flotando de amor, mi reina hermosa! ✨💖🦋", use_container_width=True)
        else:
            st.image(
                "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
                caption="¡Brillando con tu luz propia donde vayas! ✨🦋",
                use_container_width=True
            )
            
        st.markdown("""
        <div style='background: white; border-radius: 20px; padding: 20px; margin-top: 18px; border: 2px solid #ffb6c1; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.05);'>
            <p style='margin:0; color:#333; font-size: 1.1em;'>
                <b>Ruta del Amor:</b> Medellín ↔ Bucaramanga 🏔️✈️<br>
                <b>Estado Actual:</b> Pensándote 24/7 con mariposas 💭❤️🦋
            </p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: MI DIARIO INTERACTIVO
# ------------------------------------------
with tab2:
    st.markdown("<h3 style='color: #d63384;'>✍️ Mi Diario Personal e Interactivo 🦋</h3>", unsafe_allow_html=True)
    st.write("Escribe lo que viviste hoy, desahógate o guarda un lindo recuerdo.")
    
    tz_colombia = pytz.timezone("America/Bogota")
    fecha_hoy = datetime.now(tz_colombia).strftime("%d/%m/%Y %I:%M %p")
    
    st.write("---")
    st.markdown("#### **¿Cómo te sientes en este momento, mi reina?** 🌸")
    st.caption("*(Selecciona tu estado de ánimo y mira la respuesta automática)*")
    
    # Selector Dinámico y Visual
    estado_animo = st.radio(
        "Selecciona tu estado de ánimo:",
        options=[
            "😴 Cansada", 
            "🙂 Tranquila", 
            "😊 Motivada", 
            "⭐ Excelente", 
            "💖 Imparable", 
            "🤯 Abrumada / Estresada"
        ],
        horizontal=True,
        index=1,
        label_visibility="collapsed"
    )
    
    # DICCIONARIO DE RESPUESTAS AUTOMÁTICAS E INSTANTÁNEAS
    respuestas_animo = {
        "😴 Cansada": """💆‍♀️ **Mi vida hermosa:** Sé que has tenido un día largo entre la oficina de TQ, tareas o la rutina. Te has esforzado un montón.
        Por favor regálate una ducha tibia, ponte ropa cómoda y permite que tu mente descanse. ¡Hiciste un trabajo fabuloso hoy y estoy muy orgulloso de ti! 🦋""",
        
        "🙂 Tranquila": """☕ **Paz para tu corazón:** Qué dicha saber que estás disfrutando de un momento de calma. 
        Tómate un café o té, escucha una bonita canción y disfruta esta serenidad. Te mereces cada segundo de tranquilidad. 🌸""",
        
        "😊 Motivada": """🚀 **¡Esa es la actitud, mi reina!**: Tu energía positiva contagia y mueve montañas. 
        Aprovecha este impulso para avanzar en tus metas de Administración o proyectos personales. ¡Vas con toda! ✨""",
        
        "⭐ Excelente": """🌟 **¡Qué felicidad verte así!**: Tu alegría ilumina todo a tu alrededor y llena el aire de mariposas. 
        Guarda este momento de satisfacción en tu diario y celebra cada logro, por pequeño o grande que sea. 💖""",
        
        "💖 Imparable": """👑 **¡Eres una mujer poderosa e invencible!**: No hay reto laboral ni examen de universidad que pueda contigo. 
        Tienes la berraquera y la inteligencia para devorarte el mundo. ¡A brillar! 🦋🔥""",
        
        "🤯 Abrumada / Estresada": """🤗 **Respira profundo, mi cielo:** Cierra los ojos 5 segundos. No tienes que resolver todo en un solo día.
        Ve paso a paso. Recuerda que aquí estoy siempre para escucharte, apoyarte y sostenerte cuando sientas que la carga pesa. ❤️"""
    }
    
    # Tarjeta de Respuesta Dinámica
    st.markdown(f"""
    <div class='mood-response-box'>
        {respuestas_animo[estado_animo]}
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    col_input1, col_input2 = st.columns([1.2, 0.8])
    with col_input1:
        titulo_entrada = st.text_input("Título para tu nota de hoy:", placeholder="Ej: Avances en TQ / Tarde bonita en la finca...")
    with col_input2:
        etiqueta_entrada = st.selectbox("Categoría:", ["💼 Trabajo TQ", "🎓 Universidad / Administración", "🏡 Finca / Familia", "💖 Pensamientos", "🍿 Descanso"])

    contenido_entrada = st.text_area(
        "Escribe aquí tus pensamientos del día:", 
        height=190, 
        placeholder="Hoy me sentí... logré terminar mis pendientes y compartí tiempo con..."
    )
    
    if st.button("💾 Guardar Entrada en mi Diario 💖"):
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
            st.success("¡Entrada guardada con éxito en tu diario personal! 📖✨🦋")
            st.balloons()
        else:
            st.warning("Por favor escribe un título y el contenido antes de guardar.")

    st.write("---")
    st.markdown("### 📚 Tus Memorias y Notas Guardadas 🦋")
    
    entradas_guardadas = cargar_entradas()
    if entradas_guardadas:
        busqueda = st.text_input("🔍 Buscar en mis notas pasadas:", placeholder="Escribe palabras clave...")
        
        for item in entradas_guardadas:
            if busqueda.lower() in item['titulo'].lower() or busqueda.lower() in item['contenido'].lower():
                cat = item.get('categoria', '💖 Pensamientos')
                with st.expander(f"📅 {item['fecha']} — {item['titulo']} ({item['animo']}) [{cat}]"):
                    st.markdown(f"**Categoría:** {cat}")
                    st.markdown(f"**Estado de ánimo:** {item['animo']}")
                    st.write(item['contenido'])
    else:
        st.info("Aún no tienes entradas guardadas. ¡Inaugura tu diario escribiendo la primera arriba! ✨🦋")

# ------------------------------------------
# TAB 3: NUESTROS DETALLES & GUSTOS
# ------------------------------------------
with tab3:
    st.markdown("<h3 style='color: #d63384;'>🍕 Nuestros Detalles, Gustos & Momentos 🦋</h3>", unsafe_allow_html=True)
    st.write("Un rinconcito que reúne las cosas que nos encantan y nuestras dinámicas favoritas.")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #d63384;'>🍕 Antojitos & Comidas Favoritas</h3>
            <ul>
                <li><b>Plato estrella:</b> Lasaña caliente y pastas 🍝</li>
                <li><b>El infaltable nocturno:</b> Perro caliente de medianoche 🌭</li>
                <li><b>Noche de pelis:</b> Crispeticas y chocolates 🍿🍫</li>
                <li><b>Bebida de paz:</b> Un buen café por la mañana ☕</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card'>
            <h3 style='color: #d63384;'>⚽ La Famosa Apuesta</h3>
            <ul>
                <li><b>Tu equipo de corazón:</b> ¡Noruega! 🇳🇴</li>
                <li><b>Mi equipo:</b> Francia / Argentina 🇫🇷🇦🇷</li>
                <li><b>Premio acordado:</b> Una cena deliciosa pagada por el perdedor 😉🥂</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #d63384;'>🍿 Lista de Películas de Terror (Por Ver)</h3>
            <p>Checklist para nuestras maratones:</p>
        </div>
        """, unsafe_allow_html=True)
        
        peli1 = st.checkbox("👻 Evil Dead Rise (La favorita para asustarse)", value=True)
        peli2 = st.checkbox("🕯️ El Conjuro 3", value=False)
        peli3 = st.checkbox("🎈 It (Eso)", value=False)
        peli4 = st.checkbox("🚪 Un Lugar en Silencio", value=True)
        
        if peli1 and peli2 and peli3 and peli4:
            st.success("¡Listos para una maratón completa con luces apagadas! 🍿🎃")

        st.markdown("""
        <div class='card' style='margin-top: 15px;'>
            <h3 style='color: #d63384;'>🏡 El Lugar Sagrado</h3>
            <p><b>La Finca los fines de semana:</b> El espacio perfecto para desconectar del trabajo de TQ, respirar aire puro, recargar energías y compartir risas con tu hijita. ✨🌳🦋</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 4: GENERADOR DE CARTAS EN PDF
# ------------------------------------------
with tab4:
    st.markdown("<h3 style='color: #d63384;'>📜 Redactar y Generar Carta Elegante en PDF 🦋</h3>", unsafe_allow_html=True)
    st.write("Escribe una reflexión, carta o nota importante para descargarla en formato PDF profesional con sellos de fecha y hora.")
    
    col_pdf1, col_pdf2 = st.columns(2)
    with col_pdf1:
        titulo_carta = st.text_input("Título o Asunto de la carta:", "Mis reflexiones y metas ✨")
        remitente_carta = st.text_input("Firma / Remitente:", "Laura Sofía 💖")
    
    contenido_carta = st.text_area(
        "Escribe aquí el cuerpo de tu carta:", 
        height=250, 
        placeholder="Hoy quiero dejar por escrito lo agradecida que me siento por los avances en mi vida profesional y personal..."
    )
    
    tz_colombia = pytz.timezone("America/Bogota")
    fecha_hora_actual = datetime.now(tz_colombia).strftime("%d/%m/%Y a las %I:%M %p")
    
    st.caption(f"🕒 **Sello de fecha y hora automática:** {fecha_hora_actual} (Hora oficial de Colombia)")
    
    if st.button("🎨 Generar y Preparar Archivo PDF 📄"):
        if contenido_carta.strip():
            pdf_bytes = generar_pdf_carta(titulo_carta, remitente_carta, contenido_carta, fecha_hora_actual)
            st.success("¡Tu carta PDF se ha generado correctamente con un diseño elegante! 💖🦋")
            
            st.download_button(
                label="📥 Descargar Carta en Formato PDF",
                data=pdf_bytes,
                file_name=f"Carta_LauraSofia_{datetime.now().strftime('%d_%m_%Y')}.pdf",
                mime="application/pdf"
            )
            st.balloons()
        else:
            st.warning("Escribe algo en el campo de texto antes de generar el documento PDF.")

# ------------------------------------------
# TAB 5: FRASCO DE RECUERDOS & FUNCIONES ADICIONALES (CORTESÍA ESPECIAL)
# ------------------------------------------
with tab5:
    st.markdown("<h3 style='color: #d63384;'>🌟 El Frasco de los Recuerdos & Deseos 🏺✨</h3>", unsafe_allow_html=True)
    st.write("¡Un extra especial interactivo creado para regalarte momentos de amor y alegría!")
    
    col_extra1, col_extra2 = st.columns([1.1, 0.9], gap="large")
    
    with col_extra1:
        st.markdown("""
        <div class='card'>
            <h4 style='color: #d63384;'>🏺 Sacar una nota del Frasco Mágico</h4>
            <p>Haz clic abajo para sacar una notita aleatoria con recuerdos, razones por las que eres increíble o planes a futuro:</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔮 Sacar una Notita del Frasco 🌸"):
            notas_frasco = [
                "🦋 **Razón #1:** La forma en que te entregas con tanto amor a tu hijita.",
                "💖 **Razón #2:** Tu determinación imperturbable para culminar tus estudios de Administración.",
                "🌸 **Razón #3:** Tu risa y cómo ilumina cualquier conversación a la distancia.",
                "🍝 **Plan Futuro:** Una cena romántica para celebrar tus triunfos en TQ.",
                "🏡 **Momento Paz:** Un fin de semana soleado en la finca sin revisar correos.",
                "👑 **Razón #4:** Tu elegancia, tu inteligencia y tu corazón noble.",
                "🍿 **Noche Especial:** Maratón de películas de terror con crispeticas y tu cobijita favorita."
            ]
            nota_sacada = random.choice(notas_frasco)
            st.balloons()
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fff0f5 0%, #ffe3ec 100%); padding: 22px; border-radius: 20px; border: 2px solid #ff4d6d; text-align: center; font-size: 1.25em;'>
                {nota_sacada}
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        st.write("---")
        st.markdown("#### 🎵 Música & Ambiente para Leer tu Diario")
        st.write("Te sugiero poner tu playlist favorita en Spotify mientras navegas por tus notas:")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        st.caption("*(Puedes pausar o reproducir esta melodía suave de fondo)*")

    with col_extra2:
        st.markdown("""
        <div class='counter-box'>
            <p style='margin: 0; font-weight: bold;'>✨ RECORDATORIO DIARIO ✨</p>
            <h2>¡Eres Incansable!</h2>
            <p style='margin: 0; font-size: 1.1em;'>Medellín & Bucaramanga unidos siempre 🏔️✈️💖</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📊 Resumen de tu Diario")
        total_notas = len(cargar_entradas())
        st.metric(label="Total de memorias guardadas:", value=f"{total_notas} entradas 📖")
        
        if total_notas > 0:
            entries = cargar_entradas()
            # Descarga de respaldo de entradas
            json_bytes = json.dumps(entries, ensure_ascii=False, indent=4).encode('utf-8')
            st.download_button(
                label="📥 Descargar Copia de Seguridad de mi Diario (.json)",
                data=json_bytes,
                file_name="Copia_Seguridad_Diario_LauraSofia.json",
                mime="application/json"
            )
