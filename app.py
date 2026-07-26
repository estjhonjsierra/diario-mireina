import streamlit as st
import json
import os
from datetime import datetime
import pytz
import io

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

# Estilos CSS Avanzados
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff5f7 0%, #ffe6ee 100%);
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .main-header {
        text-align: center;
        color: #d63384;
        font-family: 'Poppins', cursive, sans-serif;
        animation: pulse 3s infinite ease-in-out;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .photo-card {
        border: 3px solid #ff85a1;
        border-radius: 20px;
        padding: 8px;
        background: white;
        box-shadow: 0px 8px 20px rgba(255, 133, 161, 0.25);
        text-align: center;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 18px;
        padding: 22px;
        border-left: 6px solid #ff4d6d;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }

    .daily-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
        border: 2px solid #ffb6c1;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 6px 18px rgba(214, 51, 132, 0.12);
        margin-top: 10px;
    }
    </style>
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
    },
    "2026-08-11": {
        "fecha_str": "Martes, 11 de Agosto",
        "titulo": "✨ La ternura de tu voz",
        "poema": """Escuchar tu voz me cambia el día. Tienes esa calidez que contagia alegría y paz. Deseo que hoy en tu entorno laboral todo fluya con armonía y que encuentres motivos para sonreír a cada rato."""
    },
    "2026-08-12": {
        "fecha_str": "Miércoles, 12 de Agosto",
        "titulo": "🇳🇴 El espíritu competitivo",
        "poema": """Mitad de semana... ¿Se vale apostar hoy? 😄 Siempre me hace sonreír recordar tus gustos y hasta tu apoyo a Noruega. Me encanta descubrir cada faceta tuya. Que tengas un día excelente, mi administradora estrella."""
    },
    "2026-08-13": {
        "fecha_str": "Jueves, 13 de Agosto",
        "titulo": "🌷 Pequeños detalles",
        "poema": """Las grandes historias se construyen de pequeños momentos diarios. Gracias por dejarme acompañar tus días a través de este rinconcito virtual. Nunca olvides lo valiosa e importante que eres para mí."""
    },
    "2026-08-14": {
        "fecha_str": "Viernes, 14 de Agosto",
        "titulo": "🎉 ¡Fin de semana a la vista!",
        "poema": """Cerrando otra semana de victorias. Cumpliste con tus deberes, avanzaste en tus materias y diste lo mejor en el trabajo. Ahora es momento de cambiar la mente a modo descanso. ¡Te mando un beso enorme!"""
    },
    "2026-08-15": {
        "fecha_str": "Sábado, 15 de Agosto",
        "titulo": "🏡 El lugar donde eres feliz",
        "poema": """Nada se compara a ver la paz que sientes cuando estás en la finca. Que este sábado sea para disfrutar de los tuyos, tomar el sol y olvidar cualquier pendiente de trabajo. Disfrútalo al máximo."""
    },
    "2026-08-16": {
        "fecha_str": "Domingo, 16 de Agosto",
        "titulo": "👑 Reina de tu propio destino",
        "poema": """Estás construyendo exactamente la vida que sueñas a base de esfuerzo propio y constancia. Esa independencia y berraquera tuya me enamoran cada día más. Que tengas un domingo hermoso y sereno."""
    },
    "2026-08-17": {
        "fecha_str": "Lunes, 17 de Agosto",
        "titulo": "⚡ Energía renovada",
        "poema": """Un lunes más para conquistar objetivos. Que no te falte la paciencia ni el entusiasmo hoy en la oficina. Recuerda que cada paso te acerca a tus metas profesionales. ¡Te amo mucho!"""
    },
    "2026-08-18": {
        "fecha_str": "Martes, 18 de Agosto",
        "titulo": "🌸 Dulzura que enamora",
        "poema": """Incluso en los días más acelerados, tu esencia dulce se mantiene intacta. Gracias por ser esa mujer tan especial, por cuidar con tanto amor de tu hijita y por regalarme tu compañía. Que hoy sea un día brillante."""
    },
    "2026-08-19": {
        "fecha_str": "Miércoles, 19 de Agosto",
        "titulo": "📈 Paso a paso",
        "poema": """Llegamos al ombligo de la semana. Visualiza tus metas de la universidad y del trabajo, pero disfruta también el proceso. Vas por un camino impecable mi reina. ¡Sigue así!"""
    },
    "2026-08-20": {
        "fecha_str": "Jueves, 20 de Agosto",
        "titulo": "💖 Siempre en mi corazón",
        "poema": """No importa cuántos correos o tareas tengas hoy en TQ, tómate un minuto para respirar y sentir que desde Medellín te estoy enviando todo mi amor y la mejor energía. Eres maravillosa."""
    },
    "2026-08-21": {
        "fecha_str": "Viernes, 21 de Agosto",
        "titulo": "🌭 Un perrito caliente de recompensa",
        "poema": """¡Llegó el viernes mi niña! Te mereces consentirte hoy con algo delicioso, quizás ese perrito caliente nocturno que tanto nos gusta. Disfruta la tarde y la satisfacción del deber cumplido."""
    },
    "2026-08-22": {
        "fecha_str": "Sábado, 22 de Agosto",
        "titulo": "🌿 Magia en lo simple",
        "poema": """Un paseo, una conversación sincera, la naturaleza... Ahí está la verdadera magia. Deseo que tu sábado esté lleno de estos instantes bonitos que recargan el corazón."""
    },
    "2026-08-23": {
        "fecha_str": "Domingo, 23 de Agosto",
        "titulo": "✨ La bendición de tenerte",
        "poema": """Agradezco infinitamente por haber cruzado nuestros caminos. Eres una luz inmensa en mi vida. Que este domingo sea tranquilo, reparador y lleno de amor familiar."""
    },
    "2026-08-24": {
        "fecha_str": "Lunes, 24 de Agosto",
        "titulo": "🔥 Imparable en tus metas",
        "poema": """Última semana completa de Agosto. Entra con toda la actitud ganadora. Tu determinación es capaz de mover montañas. ¡Que tengas un inicio de semana fenomenal!"""
    },
    "2026-08-25": {
        "fecha_str": "Martes, 25 de Agosto",
        "titulo": "🎓 Futura Administradora brillante",
        "poema": """Falta cada vez menos para que celebres el título que tanto has sudado. Nunca pierdas de vista la gran profesional que eres y en la que te estás convirtiendo. Orgulloso de ti siempre."""
    },
    "2026-08-26": {
        "fecha_str": "Miércoles, 26 de Agosto",
        "titulo": "💖 Un mes juntos en este diario y siempre",
        "poema": """Mi reina hermosa, hoy cumplimos un mes desde que abrimos este rinconcito especial. Gracias por permitirme estar a tu lado en la distancia, apoyarte y recordarte a diario lo infinitamente especial que eres para mí. ¡Te amo con el alma, hoy y siempre!"""
    }
}

# Encabezado Principal
st.markdown("<h1 class='main-header'>✨ El Diario de Laura Sofía 💖</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.05em;'>De Medellín a Bucaramanga 🏔️✈️🌳 | Un rincón hecho con mucho cariño</p>", unsafe_allow_html=True)
st.write("---")

# Menú por pestañas (Con la nueva pestaña de Cartas PDF)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👑 Bienvenida & Portada", 
    "✍️ Mi Diario", 
    "🍕 Nuestros Detalles", 
    "🌟 Sorpresas & Ánimo",
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

# Función para construir el PDF bonitamente decorado
def generar_pdf_carta(titulo, remitente, contenido, fecha_hora_str):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor("#d63384"),
        alignment=1, # Centrado
        spaceAfter=15
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        textColor=colors.HexColor("#888888"),
        alignment=1,
        spaceAfter=20
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.HexColor("#222222"),
        leading=18,
        spaceAfter=15
    )

    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor("#ff4d6d"),
        alignment=2, # Derecha
        spaceBefore=20
    )

    # Elementos del PDF
    story.append(Paragraph("💖 CARTA DE PENSAMIENTOS 💖", title_style))
    story.append(Paragraph(f"🌸 ✨ 🌸 ✨ 🌸", title_style))
    story.append(Paragraph(f"<b>Fecha y Hora de Creación:</b> {fecha_hora_str} (Hora Colombia)", meta_style))
    story.append(Paragraph(f"<b>Asunto:</b> {titulo}", ParagraphStyle('Sub', parent=title_style, fontSize=14, textColor=colors.HexColor("#ff85a1"))))
    story.append(Spacer(1, 10))
    
    # Formatear saltos de línea para el PDF
    contenido_formateado = contenido.replace('\n', '<br/>')
    story.append(Paragraph(contenido_formateado, body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Con todo el amor,<br/><b>{remitente}</b> ✨", footer_style))
    story.append(Paragraph("🌸 ✨ 🌸 ✨ 🌸", title_style))

    # Generar el documento
    doc.build(story)
    buffer.seek(0)
    return buffer

# TAB 1: BIENVENIDA Y PORTADA
with tab1:
    col_texto, col_foto = st.columns([1.1, 0.9], gap="large")
    
    with col_texto:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #d63384; margin-bottom: 8px;'>¡Bienvenida, mi Reina! 👋✨</h3>
            <p style='color: #444; font-size: 1em;'>Este espacio fue diseñado especialmente para ti, para acompañarte en tus jornadas de trabajo en <b>TQ</b>, tus estudios de <b>Administración</b> y tus momentos de relax.</p>
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
            <span style='background-color: #ff85a1; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 0.85em;'>
                📅 {mensaje_hoy['fecha_str']}
            </span>
            <h4 style='color: #c2185b; margin-top: 12px; margin-bottom: 8px;'>{mensaje_hoy['titulo']}</h4>
            <p style='color: #333; font-size: 0.96em; line-height: 1.6; white-space: pre-line;'>
                {mensaje_hoy['poema']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🎉 ¡Lanzar animación de celebración!"):
            st.balloons()

    with col_foto:
        st.markdown("<div class='photo-card'><b>📸 Nuestro Rincón Especial</b></div>", unsafe_allow_html=True)
        st.write("")
        
        if os.path.exists("portada.jpg"):
            st.image("portada.jpg", caption="¡Siempre contigo, mi reina! ✨💖", use_container_width=True)
        elif os.path.exists("portada.jpeg"):
            st.image("portada.jpeg", caption="¡Siempre contigo, mi reina! ✨💖", use_container_width=True)
        elif os.path.exists("portada.png"):
            st.image("portada.png", caption="¡Siempre contigo, mi reina! ✨💖", use_container_width=True)
        else:
            st.image(
                "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
                caption="¡Siempre brillando con tu luz propia! ✨",
                use_container_width=True
            )

# TAB 2: MI DIARIO INTERACTIVO
with tab2:
    st.subheader("✍️ Escribe cómo estuvo tu día")
    
    tz_colombia = pytz.timezone("America/Bogota")
    fecha_hoy = datetime.now(tz_colombia).strftime("%d/%m/%Y %I:%M %p")
    
    estado_animo = st.select_slider(
        "¿Cómo te sentiste hoy?",
        options=["😴 Cansada", "🙂 Tranquila", "😊 Motivada", "⭐ Excelente", "💖 Imparable"]
    )
    
    titulo = st.text_input("Título del día:", placeholder="Ej: Un gran día en el trabajo / Finde en la finca...")
    contenido = st.text_area("Tus pensamientos:", height=150, placeholder="Hoy logré avanzar en el trabajo, compartí tiempo especial...")
    
    if st.button("💾 Guardar en mi Diario"):
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
            st.warning("Escribe un título y contenido antes de guardar.")

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

# TAB 4: MENSAJES DE ÁNIMO
with tab4:
    st.subheader("🌟 Un mensaje sorpresivo para ti")
    import random
    frases = [
        "Recordatorio: Tienes una sonrisa preciosa que transmite muchísima tranquilidad. 😊✨",
        "Vas a ser una Administradora de Empresas brillante. ¡Orgullo total de tu disciplina! 🎓💪",
        "Disfruta cada segundo del fin de semana en la finca con tu hijita. 🏡💖",
        "¡Muchos éxitos hoy en TQ! Que tengas una jornada genial. 💼🌟",
        "Desde Medellín te mando toda la buena energía del mundo. 🏔️✈️"
    ]
    if st.button("🎲 Recibir mensaje aleatorio"):
        st.balloons()
        st.info(random.choice(frases))

# TAB 5: CREADOR DE CARTAS EN PDF
with tab5:
    st.subheader("📜 Escribe una Carta o Pensamiento y Descárgalo en PDF")
    st.write("Un espacio hermoso para redactar reflexiones o cartas con formato elegante, figuras y sello de fecha/hora de Colombia.")
    
    col_pdf1, col_pdf2 = st.columns(2)
    with col_pdf1:
        titulo_carta = st.text_input("Título de la carta/reflexión:", "Mis pensamientos de hoy ✨")
        remitente_carta = st.text_input("Firma / De parte de:", "Laura Sofía 💖")
    
    contenido_carta = st.text_area(
        "Escribe aquí lo que desees expresar:", 
        height=200, 
        placeholder="Hoy quiero plasmar en este documento mis agradecimientos, aprendizajes y metas..."
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
