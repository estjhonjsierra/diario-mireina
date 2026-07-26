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
    page_title="Diario Especial | Laura Sofía 💖",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Efecto de bienvenida inicial
if "bienvenida" not in st.session_state:
    st.balloons()
    st.session_state["bienvenida"] = True

# ==========================================
# 2. ESTILOS CSS AVANZADOS & ANIMACIONES FLOTANTES
# ==========================================
st.markdown("""
    <style>
    /* Configuración Global de Tipografía Grande */
    html, body, [class*="css"] {
        font-size: 19px !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Fondo Degradado Suave */
    .stApp {
        background: linear-gradient(135deg, #fff0f3 0%, #ffe3ec 50%, #fff5f7 100%);
    }

    /* Keyframes para Elementos Flotantes y Animados */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    @keyframes floatSlow {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-14px); }
        100% { transform: translateY(0px); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(255, 133, 161, 0.3); }
        50% { box-shadow: 0 0 25px rgba(255, 133, 161, 0.6); }
        100% { box-shadow: 0 0 10px rgba(255, 133, 161, 0.3); }
    }

    /* Encabezado Principal Animado */
    .main-header {
        text-align: center;
        color: #d63384;
        font-size: 2.8em !important;
        font-weight: 800;
        margin-bottom: 5px;
        animation: float 4s ease-in-out infinite;
        text-shadow: 2px 2px 8px rgba(214, 51, 132, 0.15);
    }

    .sub-header {
        text-align: center;
        color: #555;
        font-size: 1.2em !important;
        font-weight: 500;
        margin-bottom: 25px;
    }

    /* Tarjetas Interactivas con Elevación */
    .card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 22px;
        padding: 26px;
        border-left: 8px solid #ff4d6d;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        margin-bottom: 22px;
        font-size: 1.05em;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-4px);
    }

    .daily-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
        border: 2px solid #ffb6c1;
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 10px 28px rgba(214, 51, 132, 0.15);
        margin-top: 15px;
        animation: floatSlow 6s ease-in-out infinite;
    }

    .photo-card {
        border: 4px solid #ff85a1;
        border-radius: 22px;
        padding: 12px;
        background: white;
        box-shadow: 0px 12px 30px rgba(255, 133, 161, 0.3);
        text-align: center;
        font-size: 1.15em;
        animation: pulseGlow 4s infinite ease-in-out;
    }

    .mood-response-box {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f3 100%);
        border-radius: 18px;
        padding: 22px;
        border: 2px solid #ff85a1;
        margin-top: 18px;
        box-shadow: 0 6px 18px rgba(255, 133, 161, 0.2);
        font-size: 1.1em;
        line-height: 1.6;
    }

    .surprise-box {
        background: #ffffff;
        border-radius: 18px;
        padding: 20px;
        border: 2px dashed #ff4d6d;
        margin-top: 15px;
        text-align: center;
        font-size: 1.1em;
    }

    /* Botones Grandes y Llamativos */
    .stButton>button {
        font-size: 1.1em !important;
        border-radius: 16px !important;
        padding: 12px 26px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #ff4d6d 0%, #ff758f 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(255, 77, 109, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 8px 22px rgba(255, 77, 109, 0.45) !important;
    }

    /* Badge Flotante Decorativo */
    .floating-badge {
        display: inline-block;
        animation: float 3s ease-in-out infinite;
        font-size: 1.4em;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BASE DE DATOS EXTENDIDA DE MENSAJES DIARIOS
# ==========================================
MENSAJES_DIARIOS = {
    "2026-07-26": {
        "fecha_str": "Domingo, 26 de Julio",
        "titulo": "✨ Un rincón creado con el corazón",
        "poema": """Mi reina hermosa,
Hoy empieza un detalle hecho a la medida de tu luz. Quería que tuvieras un espacio que te recuerde lo increíble que eres, incluso cuando la rutina presione. Gracias por ser mi lugar seguro, por tu dedicación en TQ y por construir con tanta valentía tu futuro profesional en Administración. Hoy domingo te deseo calma y que recuerdes que mi admiración por ti no tiene límites. Te amo infinitamente."""
    },
    "2026-07-27": {
        "fecha_str": "Lunes, 27 de Julio",
        "titulo": "💪 Fuerza para iniciar la semana",
        "poema": """Lunes de nuevos comienzos, mi reina.
Sé la disciplina y el compromiso con el que te levantas a dar lo mejor de ti en TQ. Nunca dudes del talento gigantesco que habita en ti ni de lo lejos que vas a llegar. Cuando sientas que la semana pesa, recuerda que aquí hay alguien a cientos de kilómetros sosteniendo tu mano en el pensamiento. ¡A romperla hoy!"""
    },
    "2026-07-28": {
        "fecha_str": "Martes, 28 de Julio",
        "titulo": "🌹 La calma en tus ojos",
        "poema": """Hay una serenidad única en tu mirada que me devuelve la paz en cualquier momento. Hoy martes solo quiero recordarte que no tienes que poder con todo al mismo tiempo. Vas paso a paso, construyendo un imperio de sueños para ti y tu hijita. Eres elegancia, tenacidad y ternura en una sola persona. Disfruta tu día mi niña hermosa."""
    },
    "2026-07-29": {
        "fecha_str": "Miércoles, 29 de Julio",
        "titulo": "🏔️ Distancia que acorta el amor",
        "poema": """De Medellín a Bucaramanga hay montañas, pero no hay distancia capaz de apagar lo que siento por ti. Mitad de semana, mi administradora estrella. Cada esfuerzo en tus estudios y en tu trabajo es una semilla de un futuro brillante. Te pienso a cada hora y me llena de orgullo decir que eres mi reina."""
    },
    "2026-07-30": {
        "fecha_str": "Jueves, 30 de Julio",
        "titulo": "✨ Luz en el camino",
        "poema": """Casi viernes, mi vida.
Tu sonrisa tiene la magia de iluminar hasta el día más gris. Gracias por tu ternura, por tu escucha y por tu forma tan linda de amar. Que hoy sea un día fluido en el trabajo, donde las cosas salgan a tu favor y donde sientas que todo tu empeño valdrá la pena. Te amo con todo mi ser."""
    },
    "2026-07-31": {
        "fecha_str": "Viernes, 31 de Julio",
        "titulo": "🏡 Rumbo al descanso y la finca",
        "poema": """¡Llegó el viernes y se cierra Julio!
Sé lo mucho que anhelas el fin de semana para desconectarte, respirar aire puro en la finca y disfrutar de esos momentos invaluables con tu hijita. Que hoy el tiempo se pase volando en el trabajo para que comiences a disfrutar de tu espacio de paz. ¡Te mereces todo el descanso del mundo!"""
    },
    "2026-08-01": {
        "fecha_str": "Sábado, 01 de Agosto",
        "titulo": "🌸 Bienvenido Agosto",
        "poema": """Iniciamos un nuevo mes, mi reina.
Sábado de tranquilidad, de aire fresco en la finca y de regalarte el tiempo que tanto trabajas en la semana. Deseo que tu corazón se llene de risas, de desconexión y de ese amor puro de hogar. Disfruta tu fin de semana mi reina bella, te pienso donde estés."""
    },
    "2026-08-02": {
        "fecha_str": "Domingo, 02 de Agosto",
        "titulo": "☕ Paz para el alma",
        "poema": """Un café por la mañana, tranquilidad en la naturaleza y el calor de quienes amas. Los domingos son para recargar el alma y tú mereces llenarte de toda la energía bonita posible. Gracias por existir, por ser tan auténtica y por darle un sentido tan lindo a mis días."""
    },
    "2026-08-03": {
        "fecha_str": "Lunes, 03 de Agosto",
        "titulo": "🚀 Con la mente en alto",
        "poema": """Iniciamos semana de trabajo y metas.
Recuerda que cada reto laboral en TQ demuestra la mujer capaz, inteligente y estructurada que eres. No te achiquopales ante ningún obstáculo; tienes la capacidad y la berraquera para resolver lo que sea. ¡Estoy muy orgulloso de ti!"""
    },
    "2026-08-04": {
        "fecha_str": "Martes, 04 de Agosto",
        "titulo": "🎓 Tu futuro como Administradora",
        "poema": """Ver tu entrega con los estudios de Administración me inspira a diario. Sé las noches de cansancio y el sacrificio de equilibrar todo: trabajo, estudio y hogar. Pero créeme, reina, cada trasnocho se convertirá en los triunfos más grandes de tu vida. Sigue firme, vas increíble."""
    },
    "2026-08-05": {
        "fecha_str": "Miércoles, 05 de Agosto",
        "titulo": "💖 Mi refugio preferido",
        "poema": """Si me preguntaran dónde quiero estar, siempre diría que a tu lado o en tu pensamiento. Eres esa persona con la que hablar de todo y de nada se siente perfecto. Mitad de semana mi reina, que hoy las tareas salgan rápido y sin contratiempos."""
    },
    "2026-08-06": {
        "fecha_str": "Jueves, 06 de Agosto",
        "titulo": "🌟 Orgullo y admiración",
        "poema": """No hay un solo día en que no me sienta afortunado de tenerte en mi vida. Admirar tu belleza es fácil, pero admirar tu temple, tu rol como madre y tu ética impecable es lo que realmente me tiene cautivado. Un abrazo apretado desde aquí."""
    },
    "2026-08-07": {
        "fecha_str": "Viernes, 07 de Agosto",
        "titulo": "🍕 Noche de antojitos y relax",
        "poema": """¡Viernes! Hoy es día de soltar las cargas de la oficina, quizás pedir esa lasaña o pasta deliciosa que tanto te gusta y relajarse. Mañana nos espera un fin de semana hermoso. Que tengas una tarde tranquila y feliz mi reina."""
    },
    "2026-08-08": {
        "fecha_str": "Sábado, 08 de Agosto",
        "titulo": "🍃 Respirar y disfrutar",
        "poema": """Que la brisa de la finca te despeje cualquier estrés y que el sonido de la naturaleza te llene de calma. Pasa un sábado espectacular rodeada de amor, risas con tu niña y esos pequeños momentos que hacen la vida bella."""
    },
    "2026-08-09": {
        "fecha_str": "Domingo, 09 de Agosto",
        "titulo": "🍿 Pelis de terror y descanso",
        "poema": """Domingo ideal para acurrucarse a ver películas (o una buena de terror de las tuyas 👻), comer algo rico y recargar baterías sin afanes. Que descanses profundamente para que inicies la semana renovada."""
    },
    "2026-08-10": {
        "fecha_str": "Lunes, 10 de Agosto",
        "titulo": "💎 Eres invencible",
        "poema": """Empieza otra semana para brillar. A veces se nos olvida lo fuertes que somos hasta que nos toca demostrarlo, y tú, mi reina, has demostrado una y otra vez que no hay meta que te quede grande. ¡Con toda hoy en TQ!"""
    },
    "2026-08-15": {
        "fecha_str": "Sábado, 15 de Agosto",
        "titulo": "🏡 El lugar donde eres feliz",
        "poema": """Nada se compara a ver la paz que sientes cuando estás en la finca. Que este sábado sea para disfrutar de los tuyos, tomar el sol y olvidar cualquier pendiente de trabajo. Disfrútalo al máximo mi cielo."""
    },
    "2026-08-20": {
        "fecha_str": "Jueves, 20 de Agosto",
        "titulo": "💖 Siempre en mi corazón",
        "poema": """No importa cuántos correos o tareas tengas hoy en TQ, tómate un minuto para respirar y sentir que desde Medellín te estoy enviando todo mi amor y la mejor energía. Eres maravillosa."""
    },
    "2026-08-26": {
        "fecha_str": "Miércoles, 26 de Agosto",
        "titulo": "💖 Un mes en este diario y siempre",
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
        fontSize=22,
        textColor=colors.HexColor("#d63384"),
        alignment=1,
        spaceAfter=15
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
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
        fontSize=13,
        textColor=colors.HexColor("#ff4d6d"),
        alignment=2,
        spaceBefore=25
    )

    story.append(Paragraph("💖 CARTA DE PENSAMIENTOS 💖", title_style))
    story.append(Paragraph("🌸 ✨ 🌸 ✨ 🌸", title_style))
    story.append(Paragraph(f"<b>Fecha y Hora:</b> {fecha_hora_str} (Hora Colombia)", meta_style))
    story.append(Paragraph(f"<b>Asunto:</b> {titulo}", ParagraphStyle('Sub', parent=title_style, fontSize=16, textColor=colors.HexColor("#ff85a1"))))
    story.append(Spacer(1, 12))
    
    contenido_formateado = contenido.replace('\n', '<br/>')
    story.append(Paragraph(contenido_formateado, body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Con todo mi amor y admiración,<br/><b>{remitente}</b> ✨", footer_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("🌸 ✨ 🌸 ✨ 🌸", title_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ==========================================
# 5. ENCABEZADO Y MARCA PRINCIPAL
# ==========================================
st.markdown("<h1 class='main-header'>✨ El Diario de Laura Sofía 💖</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>De Medellín a Bucaramanga 🏔️✈️🌳 | Un rincón hecho con todo el corazón</p>", unsafe_allow_html=True)

# ==========================================
# 6. MENÚ PRINCIPAL DE 4 PESTAÑAS INTEGRADAS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "👑 Bienvenida & Portada", 
    "✍️ Mi Diario Interactivo", 
    "🍕 Nuestros Detalles & Gustos", 
    "📜 Generador de Cartas PDF ✨"
])

# ------------------------------------------
# TAB 1: BIENVENIDA & PORTADA (CON SORPRESAS E ÁNIMO INTEGRADO)
# ------------------------------------------
with tab1:
    col_texto, col_foto = st.columns([1.15, 0.85], gap="large")
    
    with col_texto:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #d63384; margin-bottom: 8px; font-size: 1.45em;'>
                ¡Bienvenida a tu lugar seguro, mi Reina! <span class='floating-badge'>👑</span>
            </h3>
            <p style='color: #333; font-size: 1.1em; line-height: 1.7;'>
                Este diario fue creado exclusivamente para ti, para acompañarte durante tus metas en <b>TQ</b>, 
                tus trasnochos estudiando <b>Administración de Empresas</b> y tus momentos de descanso.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Fecha actual en Colombia
        tz_colombia = pytz.timezone("America/Bogota")
        fecha_colombia = datetime.now(tz_colombia)
        fecha_hoy_key = fecha_colombia.strftime("%Y-%m-%d")
        
        mensaje_hoy = MENSAJES_DIARIOS.get(fecha_hoy_key, {
            "fecha_str": fecha_colombia.strftime("%A, %d de %B"),
            "titulo": "✨ Un mensaje especial para ti",
            "poema": "Mi reina hermosa, recuerda siempre lo increíble, inteligente y hermosa que eres. Cada día es una nueva oportunidad para acercarte a tus sueños. ¡Te amo con todo mi corazón!"
        })
        
        st.markdown(f"""
        <div class='daily-card'>
            <span style='background-color: #ff85a1; color: white; padding: 6px 16px; border-radius: 14px; font-weight: bold; font-size: 1em;'>
                📅 {mensaje_hoy['fecha_str']}
            </span>
            <h3 style='color: #c2185b; margin-top: 16px; margin-bottom: 12px; font-size: 1.4em;'>{mensaje_hoy['titulo']}</h3>
            <p style='color: #222; font-size: 1.1em; line-height: 1.8; white-space: pre-line;'>
                {mensaje_hoy['poema']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("---")
        
        # SECCIÓN DE SORPRESAS Y ÁNIMO INTEGRADA AQUÍ
        st.markdown("<h3 style='color: #d63384; font-size: 1.4em;'>🌟 Rinconcito de Sorpresas & Ánimo</h3>", unsafe_allow_html=True)
        st.write("¿Quieres una chispa de alegría extra hoy?")
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🎉 Lanzar Celebración"):
                st.balloons()
                
        with col_btn2:
            if st.button("🎲 Mensaje Sorpresa"):
                st.balloons()
                frases = [
                    "Recordatorio: Tienes una sonrisa preciosa que devuelve la paz a cualquiera. 😊✨",
                    "Vas a ser una Administradora de Empresas brillante. ¡Orgullo total de tu disciplina! 🎓💪",
                    "Disfruta cada segundo del fin de semana en la finca con tu hijita. 🏡💖",
                    "¡Muchos éxitos hoy en TQ! Que tengas una jornada fluida e impecable. 💼🌟",
                    "Desde Medellín te mando toda la buena energía y un abrazo apretado. 🏔️✈️",
                    "No olvides regalarte una pausa activa, tomar agüita y respirar profundo. ☕🌸",
                    "Eres la reina de tu propio destino y nada te queda grande. 👑🔥"
                ]
                st.session_state["mensaje_sorpresa_actual"] = random.choice(frases)

        with col_btn3:
            if st.button("🌸 Afirmación del Día"):
                afirmaciones = [
                    "✨ 'Soy capaz, inteligente y estoy construyendo un futuro hermoso paso a paso.'",
                    "✨ 'Mi trabajo en TQ y mis estudios están rindiendo frutos frutos admirables.'",
                    "✨ 'Merezco momentos de paz, descanso y desconexión total.'",
                    "✨ 'Tengo la fuerza para superar cualquier imprevisto con elegancia.'"
                ]
                st.session_state["mensaje_sorpresa_actual"] = random.choice(afirmaciones)

        if "mensaje_sorpresa_actual" in st.session_state:
            st.markdown(f"""
            <div class='surprise-box'>
                <p style='color: #d63384; font-weight: bold; margin-bottom: 5px;'>💖 Nota especial para ti:</p>
                <b>{st.session_state['mensaje_sorpresa_actual']}</b>
            </div>
            """, unsafe_allow_html=True)

    with col_foto:
        st.markdown("<div class='photo-card'><b>📸 Nuestro Rincón Especial</b></div>", unsafe_allow_html=True)
        st.write("")
        
        # Carga dinámica de foto de portada
        if os.path.exists("portada.jpg"):
            st.image("portada.jpg", caption="¡Siempre juntos, mi reina hermosa! ✨💖", use_container_width=True)
        elif os.path.exists("portada.jpeg"):
            st.image("portada.jpeg", caption="¡Siempre juntos, mi reina hermosa! ✨💖", use_container_width=True)
        elif os.path.exists("portada.png"):
            st.image("portada.png", caption="¡Siempre juntos, mi reina hermosa! ✨💖", use_container_width=True)
        else:
            st.image(
                "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
                caption="¡Brillando con tu luz propia donde vayas! ✨",
                use_container_width=True
            )
            
        st.markdown("""
        <div style='background: white; border-radius: 18px; padding: 18px; margin-top: 15px; border: 1px solid #ffb6c1; text-align: center;'>
            <p style='margin:0; color:#444; font-size: 1.05em;'>
                <b>Distancia:</b> Medellín ↔ Bucaramanga <br>
                <b>Estado:</b> Pensándote 24/7 💭❤️
            </p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: MI DIARIO INTERACTIVO (CON MENSAJES DE ÁNIMO DINÁMICOS Y AUTOMÁTICOS)
# ------------------------------------------
with tab2:
    st.markdown("<h3 style='color: #d63384;'>✍️ Mi Diario Personal e Interactivo</h3>", unsafe_allow_html=True)
    st.write("Escribe lo que viviste hoy, desahógate o guarda un lindo recuerdo.")
    
    tz_colombia = pytz.timezone("America/Bogota")
    fecha_hoy = datetime.now(tz_colombia).strftime("%d/%m/%Y %I:%M %p")
    
    st.write("---")
    st.markdown("#### **¿Cómo te sientes en este momento, mi reina?**")
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
        Por favor regálate una ducha tibia, ponte ropa cómoda y permite que tu mente descanse. ¡Hiciste un trabajo fabuloso hoy y estoy muy orgulloso de ti!""",
        
        "🙂 Tranquila": """☕ **Paz para tu corazón:** Qué dicha saber que estás disfrutando de un momento de calma. 
        Tómate un café o té, escucha una bonita canción y disfruta esta serenidad. Te mereces cada segundo de tranquilidad.""",
        
        "😊 Motivada": """🚀 **¡Esa es la actitud, mi reina!**: Tu energía positiva contagia y mueve montañas. 
        Aprovecha este impulso para avanzar en tus metas de Administración o proyectos personales. ¡Vas con toda!""",
        
        "⭐ Excelente": """🌟 **¡Qué felicidad verte así!**: Tu alegría ilumina todo a tu alrededor. 
        Guarda este momento de satisfacción en tu diario y celebra cada logro, por pequeño o grande que sea.""",
        
        "💖 Imparable": """👑 **¡Eres una mujer poderosa e invencible!**: No hay reto laboral ni examen de universidad que pueda contigo. 
        Tienes la berraquera y la inteligencia para devorarte el mundo. ¡A brillar!""",
        
        "🤯 Abrumada / Estresada": """🤗 **Respira profundo, mi cielo:** Cierra los ojos 5 segundos. No tienes que resolver todo en un solo día.
        Ve paso a paso. Recuerda que aquí estoy siempre para escucharte, apoyarte y sostenerte cuando sientas que la carga pesa."""
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
        height=180, 
        placeholder="Hoy me sentí... logré terminar mis pendientes y compartí tiempo con..."
    )
    
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
            st.success("¡Entrada guardada con éxito en tu diario personal! 📖✨")
            st.balloons()
        else:
            st.warning("Por favor escribe un título y el contenido antes de guardar.")

    st.write("---")
    st.markdown("### 📚 Tus Memorias y Notas Guardadas")
    
    entradas_guardadas = cargar_entradas()
    if entradas_guardadas:
        busqueda = st.text_input("🔍 Buscar en mis notas pasadas:", placeholder="Escribe palabras clave...")
        
        for item in entradas_guardadas:
            # Filtro simple
            if busqueda.lower() in item['titulo'].lower() or busqueda.lower() in item['contenido'].lower():
                cat = item.get('categoria', '💖 Pensamientos')
                with st.expander(f"📅 {item['fecha']} — {item['titulo']} ({item['animo']}) [{cat}]"):
                    st.markdown(f"**Categoría:** {cat}")
                    st.markdown(f"**Estado de ánimo:** {item['animo']}")
                    st.write(item['contenido'])
    else:
        st.info("Aún no tienes entradas guardadas. ¡Inaugura tu diario escribiendo la primera arriba! ✨")

# ------------------------------------------
# TAB 3: NUESTROS DETALLES & GUSTOS
# ------------------------------------------
with tab3:
    st.markdown("<h3 style='color: #d63384;'>🍕 Nuestros Detalles, Gustos & Momentos</h3>", unsafe_allow_html=True)
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
                <li><b>Premio acordado:</b> Una cena deliciosa pagada por el perdedor 😉</li>
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
            <p><b>La Finca los fines de semana:</b> El espacio perfecto para desconectar del trabajo de TQ, respirar aire puro, recargar energías y compartir risas con tu hijita. ✨🌳</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 4: GENERADOR DE CARTAS EN PDF
# ------------------------------------------
with tab4:
    st.markdown("<h3 style='color: #d63384;'>📜 Redactar y Generar Carta Elegante en PDF</h3>", unsafe_allow_html=True)
    st.write("Escribe una reflexión, carta o nota importante para descargarla en formato PDF profesional con sellos de fecha y hora.")
    
    col_pdf1, col_pdf2 = st.columns(2)
    with col_pdf1:
        titulo_carta = st.text_input("Título o Asunto de la carta:", "Mis reflexiones y metas ✨")
        remitente_carta = st.text_input("Firma / Remitente:", "Laura Sofía 💖")
    
    contenido_carta = st.text_area(
        "Escribe aquí el cuerpo de tu carta:", 
        height=240, 
        placeholder="Hoy quiero dejar por escrito lo agradecida que me siento por los avances en mi vida profesional y personal..."
    )
    
    tz_colombia = pytz.timezone("America/Bogota")
    fecha_hora_actual = datetime.now(tz_colombia).strftime("%d/%m/%Y a las %I:%M %p")
    
    st.caption(f"🕒 **Sello de fecha y hora automática:** {fecha_hora_actual} (Hora oficial de Colombia)")
    
    if st.button("🎨 Generar y Preparar Archivo PDF"):
        if contenido_carta.strip():
            pdf_bytes = generar_pdf_carta(titulo_carta, remitente_carta, contenido_carta, fecha_hora_actual)
            st.success("¡Tu carta PDF se ha generado correctamente con un diseño elegante! 💖")
            
            st.download_button(
                label="📥 Descargar Carta en Formato PDF",
                data=pdf_bytes,
                file_name=f"Carta_LauraSofia_{datetime.now().strftime('%d_%m_%Y')}.pdf",
                mime="application/pdf"
            )
            st.balloons()
        else:
            st.warning("Escribe algo en el campo de texto antes de generar el documento PDF.")
