import streamlit as st
import json
import os
from datetime import datetime
import pytz
import io
import random

# Librerías para generar el PDF bonito
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuración de página
st.set_page_config(
    page_title="Diario Especial | Laura Sofía 💖",
    page_icon="👑",
    layout="wide"
)

# Efecto de bienvenida inicial
if "bienvenida" not in st.session_state:
    st.balloons()
    st.session_state["bienvenida"] = True

# CSS Avanzado con letras más grandes, animaciones de corazones flotantes y diseño elegante
st.markdown("""
    <style>
    /* Tipografía general más grande y legible */
    html, body, [class*="css"] {
        font-size: 18px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #fff0f3 0%, #ffe3ec 100%);
        position: relative;
        overflow-x: hidden;
    }

    /* Animación de corazones y estrellas flotando en el fondo */
    @keyframes floatingElements {
        0% { transform: translateY(0px) rotate(0deg); opacity: 0.8; }
        50% { transform: translateY(-20px) rotate(10deg); opacity: 1; }
        100% { transform: translateY(0px) rotate(0deg); opacity: 0.8; }
    }

    .floating-heart-1 {
        position: fixed;
        top: 15%;
        left: 3%;
        font-size: 32px;
        animation: floatingElements 4s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }
    .floating-heart-2 {
        position: fixed;
        top: 60%;
        right: 4%;
        font-size: 38px;
        animation: floatingElements 5s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }
    .floating-star-1 {
        position: fixed;
        bottom: 10%;
        left: 5%;
        font-size: 30px;
        animation: floatingElements 3.5s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }

    @keyframes pulseHeader {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    .main-header {
        text-align: center;
        color: #d63384;
        font-size: 2.5em !important;
        font-weight: 800;
        animation: pulseHeader 3s infinite ease-in-out;
        margin-bottom: 5px;
    }
    
    .photo-card {
        border: 4px solid #ff85a1;
        border-radius: 20px;
        padding: 10px;
        background: white;
        box-shadow: 0px 10px 25px rgba(255, 133, 161, 0.3);
        text-align: center;
        font-size: 1.1em;
    }

    .card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 24px;
        border-left: 8px solid #ff4d6d;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        font-size: 1.05em;
    }

    .daily-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
        border: 2px solid #ffb6c1;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 22px rgba(214, 51, 132, 0.15);
        margin-top: 15px;
    }

    .mood-box {
        background: white;
        border-radius: 16px;
        padding: 18px;
        border: 2px solid #ff85a1;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(255, 133, 161, 0.15);
    }
    
    /* Botones más llamativos y grandes */
    .stButton>button {
        font-size: 1.05em !important;
        border-radius: 14px !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
    }
    </style>
    
    <!-- Elementos flotantes decorativos -->
    <div class="floating-heart-1">💖</div>
    <div class="floating-heart-2">✨</div>
    <div class="floating-star-1">🌸</div>
""", unsafe_allow_html=True)

# Diccionario con mensajes y poemas diarios
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
Sábado de tranquilidad, de aire fresco en la finca y de regalarte el tiempo que tanto trabajas en la semana. Deseo que tu corazón se llene de risas, de desconexión y de ese amor puro de hogar. Disfruta tu fin de semana mi reina bella, te pienses donde estés."""
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
Recuerda que en cada reto laboral en TQ demuestra la mujer capaz, inteligente y estructurada que eres. No te achiquopales ante ningún obstáculo; tienes la capacidad y la berraquera para resolver lo que sea. ¡Estoy muy orgulloso de ti!"""
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
    }
}

# Encabezado Principal
st.markdown("<h1 class='main-header'>✨ El Diario de Laura Sofía 💖</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.15em; font-weight: 500;'>De Medellín a Bucaramanga 🏔️✈️🌳 | Un rincón hecho con mucho cariño</p>", unsafe_allow_html=True)
st.write("---")

# Menú simplificado por 4 pestañas (Sorpresas integrado en la portada)
tab1, tab2, tab3, tab4 = st.tabs([
    "👑 Bienvenida & Portada", 
    "✍️ Mi Diario", 
    "🍕 Nuestros Detalles", 
    "📜 Carta en PDF ✨"
])

DB_FILE = "diario_laura.json"

def cargar_entradas():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_entradas(entradas):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(entradas, f, ensure_ascii=False, indent=4)

# Generador de PDF
def generar_pdf_carta(titulo, remitente, contenido, fecha_hora_str):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
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
        leading=20,
        spaceAfter=15
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
    story.append(Paragraph(f"<b>Asunto:</b> {titulo}", ParagraphStyle('Sub', parent=title_style, fontSize=15, textColor=colors.HexColor("#ff85a1"))))
    story.append(Spacer(1, 10))
    
    contenido_formateado = contenido.replace('\n', '<br/>')
    story.append(Paragraph(contenido_formateado, body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Con todo el amor,<br/><b>{remitente}</b> ✨", footer_style))
    story.append(Paragraph("🌸 ✨ 🌸 ✨ 🌸", title_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# TAB 1: BIENVENIDA Y PORTADA (CON SORPRESAS INCLUIDO)
with tab1:
    col_texto, col_foto = st.columns([1.1, 0.9], gap="large")
    
    with col_texto:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #d63384; margin-bottom: 8px; font-size: 1.4em;'>¡Bienvenida, mi Reina! 👋✨</h3>
            <p style='color: #333; font-size: 1.05em; line-height: 1.6;'>Este espacio fue diseñado especialmente para ti, para acompañarte en tus jornadas de trabajo en <b>TQ</b>, tus estudios de <b>Administración</b> y tus momentos de relax.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
            <span style='background-color: #ff85a1; color: white; padding: 6px 14px; border-radius: 12px; font-weight: bold; font-size: 0.95em;'>
                📅 {mensaje_hoy['fecha_str']}
            </span>
            <h3 style='color: #c2185b; margin-top: 14px; margin-bottom: 10px; font-size: 1.3em;'>{mensaje_hoy['titulo']}</h3>
            <p style='color: #222; font-size: 1.05em; line-height: 1.7; white-space: pre-line;'>
                {mensaje_hoy['poema']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("### 🌟 Rinconcito de Alegría & Sorpresas")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🎉 Lanzar animación"):
                st.balloons()
                
        with col_btn2:
            if st.button("🎲 Mensaje Sorpresa"):
                st.balloons()
                frases = [
                    "Recordatorio: Tienes una sonrisa preciosa que me devuelve la paz. 😊✨",
                    "Vas a ser una Administradora de Empresas brillante. ¡Orgullo total! 🎓💪",
                    "Disfruta cada segundo del fin de semana en la finca con tu hijita. 🏡💖",
                    "¡Muchos éxitos hoy en TQ! Que tengas una jornada fenomenal. 💼🌟",
                    "Desde Medellín te mando toda la buena energía del mundo. 🏔️✈️",
                    "No olvides regalarte una pausa y tomar agua hoy, mi reina. ☕🌸"
                ]
                st.info(random.choice(frases))

    with col_foto:
        st.markdown("<div class='photo-card'><b>📸 Nuestro Rincón Especial</b></div>", unsafe_allow_html=True)
        st.write("")
        
        if os.path.exists("portada.jpg"):
            st.image("portada.jpg", caption="¡Siempre juntos mi reina hermosa! ✨💖", use_container_width=True)
        elif os.path.exists("portada.jpeg"):
            st.image("portada.jpeg", caption="¡Siempre juntos mi reina hermosa! ✨💖", use_container_width=True)
        elif os.path.exists("portada.png"):
            st.image("portada.png", caption="¡Siempre juntos mi reina hermosa! ✨💖", use_container_width=True)
        else:
            st.image(
                "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
                caption="¡Siempre brillando con tu luz propia! ✨",
                use_container_width=True
            )

# TAB 2: MI DIARIO INTERACTIVO (CON SELECTOR MEJORADO Y RESPUESTA DINÁMICA)
with tab2:
    st.subheader("✍️ Escribe cómo estuvo tu día")
    
    tz_colombia = pytz.timezone("America/Bogota")
    fecha_hoy = datetime.now(tz_colombia).strftime("%d/%m/%Y %I:%M %p")
    
    st.markdown("**¿Cómo te sientes hoy?** (Selecciona una opción para recibir un mensaje especial)")
    
    # Selector claro y fácil de seleccionar
    estado_animo = st.radio(
        "",
        options=["😴 Cansada", "🙂 Tranquila", "😊 Motivada", "⭐ Excelente", "💖 Imparable"],
        horizontal=True
    )
    
    # Respuestas personalizadas e inmediatas según el estado de ánimo elegido
    mensajes_animo = {
        "😴 Cansada": "💆‍♀️ **Mi vida:** Te has esforzado mucho hoy. Recuerda descansar la mente, tomar una ducha tibia y regalarte un espacio de paz. ¡Hiciste un trabajo excelente!",
        "🙂 Tranquila": "☕ **Que la paz te acompañe:** Disfruta esta calma tan bonita. Un té, una conversación tranquila o un respiro profundo para mantener el equilibrio.",
        "😊 Motivada": "🚀 **¡Aprovecha esa chispa!**: Tu energía contagia. Cada paso que das te acerca más a tu título de Administradora y a tus metas.",
        "⭐ Excelente": "🌟 **¡Qué alegría verte así!**: Me llena el corazón saber que tu día va genial. Disfruta cada instante y celebra tus logros.",
        "💖 Imparable": "👑 **¡Eres una reina poderosa!**: No hay meta que te quede grande ni reto que no puedas superar. ¡A devorarse el mundo!"
    }
    
    st.markdown(f"""
    <div class='mood-box'>
        {mensajes_animo[estado_animo]}
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    titulo = st.text_input("Título del día:", placeholder="Ej: Avances en TQ / Finde relajante en la finca...")
    contenido = st.text_area("Tus pensamientos:", height=160, placeholder="Escribe aquí lo que desees recordar o desahogar...")
    
    if st.button("💾 Guardar entrada en mi Diario"):
        if titulo and contenido:
            entradas = cargar_entradas()
            nueva = {
                "fecha": fecha_hoy,
                "animo": estado_animo,
                "titulo": titulo,
                "contenido": contenido
            }
            entradas.insert(0, nueva)
            guardar_entradas(entradas)
            st.success("¡Entrada guardada con éxito! 📖✨")
            st.balloons()
        else:
            st.warning("Escribe un título y el contenido antes de guardar.")

    st.write("---")
    st.subheader("📚 Tus Notas Guardadas")
    entradas_guardadas = cargar_entradas()
    if entradas_guardadas:
        for item in entradas_guardadas:
            with st.expander(f"📅 {item['fecha']} - {item['titulo']} ({item['animo']})"):
                st.write(item['contenido'])
    else:
        st.info("Aún no hay entradas guardadas. ¡Anímate a escribir la primera! ✨")

# TAB 3: DETALLES PERSONALIZADOS
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🍕 Antojitos & Favoritos
        * **Plato favorito:** Lasaña y Pasta 🍝
        * **El infaltable:** Perro caliente de medianoche 🌭
        * **Pelis:** Terror (*Evil Dead Rise*) 🍿👻
        """)
    with col2:
        st.markdown("""
        ### ⚽ La Apuesta
        * **Tu equipo:** ¡Noruega! 🇳🇴
        * **Mi equipo:** Francia / Argentina 🇫🇷🇦🇷
        * **Lugar de paz:** La finca los fines de semana 🏡
        """)

# TAB 4: CREADOR DE CARTAS EN PDF
with tab4:
    st.subheader("📜 Escribe una Carta o Pensamiento y Descárgalo en PDF")
    st.write("Redacta tus reflexiones o notas importantes con formato de carta elegante, firmas y sello de fecha/hora colombiana.")
    
    col_pdf1, col_pdf2 = st.columns(2)
    with col_pdf1:
        titulo_carta = st.text_input("Título de la carta/reflexión:", "Mis pensamientos de hoy ✨")
        remitente_carta = st.text_input("Firma / De parte de:", "Laura Sofía 💖")
    
    contenido_carta = st.text_area(
        "Escribe aquí lo que desees plasmar:", 
        height=220, 
        placeholder="Hoy quiero expresar..."
    )
    
    tz_colombia = pytz.timezone("America/Bogota")
    fecha_hora_actual = datetime.now(tz_colombia).strftime("%d/%m/%Y a las %I:%M %p")
    
    st.caption(f"🕒 **Fecha y Hora de firma automática:** {fecha_hora_actual} (Hora de Colombia)")
    
    if st.button("🎨 Generar y Preparar PDF"):
        if contenido_carta.strip():
            pdf_bytes = generar_pdf_carta(titulo_carta, remitente_carta, contenido_carta, fecha_hora_actual)
            st.success("¡Tu carta PDF ha sido generada con un estilo precioso! 💖")
            
            st.download_button(
                label="📥 Descargar Carta en PDF",
                data=pdf_bytes,
                file_name=f"Carta_LauraSofia_{datetime.now().strftime('%d_%m_%Y')}.pdf",
                mime="application/pdf"
            )
            st.balloons()
        else:
            st.warning("Escribe algo en la casilla de texto antes de generar el PDF.")
