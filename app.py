import streamlit as st
import json
import os
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Diario Especial | Laura Sofía 💖",
    page_icon="👑",
    layout="centered"
)

# Efecto de bienvenida (Animación inicial)
if "bienvenida" not in st.session_state:
    st.balloons()
    st.session_state["bienvenida"] = True

# Estilos CSS Avanzados (Efectos y diseño romántico)
st.markdown("""
    <style>
    /* Fondo con degradado suave */
    .stApp {
        background: linear-gradient(135deg, #fff5f7 0%, #ffe6ee 100%);
    }
    
    /* Título principal con efecto de pulso */
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
    }
    
    /* Marco brillante para fotos o GIFs */
    .photo-card {
        border: 3px solid #ff85a1;
        border-radius: 20px;
        padding: 12px;
        background: white;
        box-shadow: 0px 8px 20px rgba(255, 133, 161, 0.25);
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* Tarjetas de información */
    .card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        border-left: 6px solid #ff4d6d;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Principal
st.markdown("<h1 class='main-header'>✨ El Diario de Laura Sofía 💖</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.1em;'>De Medellín a Bucaramanga 🏔️✈️🌳 | Un rincón hecho con mucho cariño</p>", unsafe_allow_html=True)
st.write("---")

# Menú por pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "👑 Bienvenida & Foto", 
    "✍️ Mi Diario", 
    "🍕 Nuestros Detalles", 
    "🌟 Sorpresas & Ánimo"
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

# TAB 1: BIENVENIDA Y FOTO
with tab1:
    st.markdown("""
    <div class='card'>
        <h3>¡Bienvenida, mi Reina! 👋✨</h3>
        <p>Este espacio fue diseñado especialmente para ti, para acompañarte en tus jornadas de trabajo en <b>TQ</b>, tus estudios de <b>Administración</b> y tus momentos de relax.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='photo-card'><b>📸 Nuestro Rincón Especial</b></div>", unsafe_allow_html=True)
    
    # Imagen de portada (Pudiste cambiar este link por un GIF o foto subida)
    st.image(
        "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
        caption="¡Siempre brillando con tu luz propia y hermosa sonrisa! ✨",
        use_container_width=True
    )
    
    if st.button("🎉 ¡Lanzar animación de celebración!"):
        st.balloons()

# TAB 2: MI DIARIO INTERACTIVO
with tab2:
    st.subheader("✍️ Escribe cómo estuvo tu día")
    
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %I:%M %p")
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
        * **Pelis:** Terror (*Evil Dead Rise*) 🍿👻[cite: 1]
        """)
    with col2:
        st.markdown("""
        ### ⚽ La Apuesta
        * **Tu equipo:** ¡Noruega! 🇳🇴[cite: 1]
        * **Mi equipo:** Francia / Argentina 🇫🇷🇦🇷[cite: 1]
        * **Lugar de paz:** La finca los fines de semana 🏡[cite: 1]
        """)

# TAB 4: MENSAJES DE ÁNIMO
with tab4:
    st.subheader("🌟 Un mensaje para ti hoy")
    
    import random
    frases = [
        "Recordatorio: Tienes una sonrisa preciosa que transmite muchísima tranquilidad. 😊✨",
        "Vas a ser una Administradora de Empresas brillante. ¡Orgullo total de tu disciplina! 🎓💪",
        "Disfruta cada segundo del fin de semana en la finca con tu hijita. 🏡💖",
        "¡Muchos éxitos hoy en TQ! Que tengas una jornada genial. 💼🌟",
        "Desde Medellín te mando toda la buena energía del mundo. 🏔️✈️"
    ]
    
    if st.button("🎲 Recibir mensaje del día"):
        st.balloons()
        st.info(random.choice(frases))