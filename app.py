
import streamlit as st
import random
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

combo_fx = {
    "explosion": "a giant explosion shatters the ground",
    "portal": "a magical portal opens in the sky",
    "storm": "a supernatural storm tears the air",
    "transformation": "a person transforms into pure light",
    "collapse": "the city collapses like a vortex",
    "lava": "lava rapidly rises from the earth",
    "disintegration": "everything slowly disintegrates into particles"
}

combo_suggestions = {
    "explosion": ["collapse", "disintegration"],
    "portal": ["storm", "transformation"],
    "storm": ["lava", "collapse"],
    "transformation": ["portal", "disintegration"],
    "collapse": ["explosion", "storm"],
    "lava": ["storm", "collapse"],
    "disintegration": ["explosion", "transformation"]
}

locations = [
    "in a medieval castle", "on a floating island", "in a cyberpunk city",
    "in an ancient forest", "in an underwater city"
]

styles = ["cinematic", "dreamlike", "hyper-realistic", "stylized anime", "dark sci-fi"]

camera_moves = [
    "with a drone shot circling the scene", "with a slow-motion dolly zoom",
    "with a handheld shaking camera", "in a smooth panoramic shot"
]

inspirations = [
    "like in Inception", "inspired by Blade Runner 2049",
    "with the atmosphere of Interstellar", "like a Marvel final battle",
    "reminiscent of The Witcher"
]


platform_styles = {
    "LumaLabs": lambda p: f"A realistic cinematic view of {p}, with dramatic lighting and dynamic camera movements.",
    "Runway": lambda p: f"Hyper-detailed and naturalistic rendering of {p}, with soft transitions and organic textures.",
    "Minimax": lambda p: f"Stylized animation showing {p}, featuring fluid transitions and strong emotional atmosphere.",
    "Pika": lambda p: f"High-impact VFX of {p}, with sharp effects and fast-paced camera action.",
    "Vidu Q1": lambda p: f"Cinematic storytelling shot of {p}, with smooth camera motion and rich visual transitions.",
    "Pixverse 4.5": lambda p: f"Animated and colorful depiction of {p}, full of energetic motion effects.",
    "Kling 1.6": lambda p: f"Ultra-realistic capture of {p}, with physical light simulation and advanced camera tracking."
}

st.set_page_config(page_title="🎬 Générateur de Timeline FX", layout="wide")
st.title("🎬 Générateur de Timeline d’Effets Spéciaux Vidéo IA")

num_scenes = st.sidebar.slider("📽️ Nombre de scènes", 1, 5, 1)
use_smart_combo = st.sidebar.checkbox("🧠 Activer les suggestions intelligentes de FX", value=False)

timeline = []

for i in range(num_scenes):
    with st.expander(f"🎞️ Scène {i + 1}"):
        col1, col2 = st.columns(2)
        with col1:
            fx_list = []


import streamlit as st
import random
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

combo_fx = {
    "explosion": "a giant explosion shatters the ground",
    "portal": "a magical portal opens in the sky",
    "storm": "a supernatural storm tears the air",
    "transformation": "a person transforms into pure light",
    "collapse": "the city collapses like a vortex",
    "lava": "lava rapidly rises from the earth",
    "disintegration": "everything slowly disintegrates into particles"
}

combo_suggestions = {
    "explosion": ["collapse", "disintegration"],
    "portal": ["storm", "transformation"],
    "storm": ["lava", "collapse"],
    "transformation": ["portal", "disintegration"],
    "collapse": ["explosion", "storm"],
    "lava": ["storm", "collapse"],
    "disintegration": ["explosion", "transformation"]
}

locations = [
    "in a medieval castle", "on a floating island", "in a cyberpunk city",
    "in an ancient forest", "in an underwater city"
]

styles = ["cinematic", "dreamlike", "hyper-realistic", "stylized anime", "dark sci-fi"]

camera_moves = [
    "with a drone shot circling the scene", "with a slow-motion dolly zoom",
    "with a handheld shaking camera", "in a smooth panoramic shot"
]

inspirations = [
    "like in Inception", "inspired by Blade Runner 2049",
    "with the atmosphere of Interstellar", "like a Marvel final battle",
    "reminiscent of The Witcher"
]


platform_styles = {
    "LumaLabs": lambda p: f"A realistic cinematic view of {p}, with dramatic lighting and dynamic camera movements.",
    "Runway": lambda p: f"Hyper-detailed and naturalistic rendering of {p}, with soft transitions and organic textures.",
    "Minimax": lambda p: f"Stylized animation showing {p}, featuring fluid transitions and strong emotional atmosphere.",
    "Pika": lambda p: f"High-impact VFX of {p}, with sharp effects and fast-paced camera action.",
    "Vidu Q1": lambda p: f"Cinematic storytelling shot of {p}, with smooth camera motion and rich visual transitions.",
    "Pixverse 4.5": lambda p: f"Animated and colorful depiction of {p}, full of energetic motion effects.",
    "Kling 1.6": lambda p: f"Ultra-realistic capture of {p}, with physical light simulation and advanced camera tracking."
}

st.set_page_config(page_title="🎬 Générateur de Timeline FX", layout="wide")
st.title("🎬 Générateur de Timeline d’Effets Spéciaux Vidéo IA")

num_scenes = st.sidebar.slider("📽️ Nombre de scènes", 1, 5, 1)
use_smart_combo = st.sidebar.checkbox("🧠 Activer les suggestions intelligentes de FX", value=False)

timeline = []

for i in range(num_scenes):
    with st.expander(f"🎞️ Scène {i + 1}"):
        col1, col2 = st.columns(2)
        with col1:
            fx_list = []

if use_smart_combo:
    fx1 = st.selectbox(f"Effet principal (scène {i + 1})", list(combo_fx.keys()), key=f"fx1_{i}")
    suggested = combo_suggestions.get(fx1, [])
    fx2 = st.selectbox("Effet complémentaire suggéré", ["Aucun"] + suggested, key=f"fx2_{i}")
    fx_list.append(combo_fx[fx1])
    if fx2 != "Aucun" and fx2 in combo_fx:
        fx_list.append(combo_fx[fx2])

def create_pdf(timeline):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "🎬 Timeline des Prompts FX")
    y -= 30

    for scene_title, base_prompt in timeline:
        if y < 140:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica-Bold", 14)

        c.drawString(40, y, scene_title)
        y -= 20
        c.setFont("Helvetica", 12)
        c.drawString(40, y, "Prompt principal :")
        y -= 16
        for line in split_text(base_prompt, 90):
            c.drawString(50, y, line)
            y -= 14

        for platform, modifier in platform_styles.items():
            full_prompt = modifier(base_prompt)
            y -= 10
            if y < 100:
                c.showPage()
                y = height - 40
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y, platform)
            y -= 16
            c.setFont("Helvetica", 11)
            for line in split_text(full_prompt, 90):
                c.drawString(50, y, line)
                y -= 14
            y -= 6

    c.save()
    buffer.seek(0)
    return buffer

if st.button("📄 Exporter la timeline en PDF"):
    pdf_file = create_pdf(timeline)
    st.download_button(
        label="📥 Télécharger le PDF",
        data=pdf_file,
        file_name="fx_timeline.pdf",
        mime="application/pdf"
    )
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "🎬 Timeline des Prompts FX")
    y -= 30

    for scene_title, base_prompt in timeline:
        if y < 140:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica-Bold", 14)

        c.drawString(40, y, scene_title)
        y -= 20
        c.setFont("Helvetica", 12)
        c.drawString(40, y, "Prompt principal :")
        y -= 16
        for line in split_text(base_prompt, 90):
            c.drawString(50, y, line)
            y -= 14

        for platform, modifier in platform_styles.items():
            full_prompt = modifier(base_prompt)
            y -= 10
            if y < 100:
                c.showPage()
                y = height - 40
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y, platform)
            y -= 16
            c.setFont("Helvetica", 11)
            for line in split_text(full_prompt, 90):
                c.drawString(50, y, line)
                y -= 14
            y -= 6

    c.save()
    buffer.seek(0)
    return buffer

if st.button("📄 Exporter la timeline en PDF"):
    pdf_file = create_pdf(timeline)
    st.download_button(
        label="📥 Télécharger le PDF",
        data=pdf_file,
        file_name="fx_timeline.pdf",
        mime="application/pdf"
    )