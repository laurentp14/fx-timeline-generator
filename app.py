# -*- coding: utf-8 -*-

import streamlit as st
import random

# Données
combo_fx = {
    "explosion": "a giant explosion shattering the ground",
    "portal": "a glowing magical portal opening in the sky",
    "storm": "a supernatural storm tearing the air",
    "transformation": "a person transforming into pure light",
    "collapse": "the city collapsing inward like a vortex",
    "lava": "lava rising rapidly from the earth",
    "disintegration": "everything slowly disintegrating into particles"
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
styles = ["cinematic", "dreamlike", "hyper-realistic", "stylized anime", "dark sci-fi"]
camera_moves = [
    "static frame", "subtle handheld movement", "slow dolly zoom forward",
    "drone shot circling the subject", "vertical tilt from bottom to top"
]
fx_options = [
    "particles floating around", "light rays breaking through clouds",
    "portal opening behind the subject", "energy surging from the ground",
    "environment slowly collapsing", "scene gradually shifting to another dimension"
]
effects_by_intention = {
    "Destruction": [
        "a giant explosion shattering the ground",
        "a collapsing city swallowed by the earth",
        "buildings crumbling in a dust storm"
    ],
    "Magie": [
        "a glowing magical portal opening in the sky",
        "a person transforming into pure light",
        "a swarm of enchanted sparks dancing in the air"
    ],
    "Peur": [
        "dark fog crawling over the ground",
        "shadows moving unnaturally",
        "a sudden burst of whispering voices"
    ],
    "Cataclysme": [
        "lava rising rapidly from the earth",
        "the sky tearing open with lightning",
        "a vortex consuming everything in its path"
    ],
    "Renaissance": [
        "a golden light emerging from ruins",
        "nature reclaiming a destroyed city",
        "flowers blooming from scorched earth"
    ],
    "Technologie": [
        "a swarm of drones forming patterns in the sky",
        "a holographic interface appearing in midair",
        "a robot assembling itself from scrap parts"
    ],
    "Rêve": [
        "floating islands above a sea of stars",
        "a staircase leading into the sky",
        "giant fish swimming through clouds"
    ]
}
intention_labels = {
    "Destruction": "💥 Destruction – Chaos, explosions, écroulements",
    "Magie": "✨ Magie – Portails, transformations, étincelles",
    "Peur": "😱 Peur – Brouillard, ombres, chuchotements",
    "Cataclysme": "🌪️ Cataclysme – Tremblements, vortex, fin du monde",
    "Renaissance": "🌱 Renaissance – Lumière, nature renaissante, espoir",
    "Technologie": "🤖 Technologie – IA, drones, hologrammes",
    "Rêve": "🌙 Rêve – Monde flottant, irréel, onirique"
}
locations = [
    "in a medieval castle", "on a floating island", "in a neon-lit cyberpunk city",
    "inside an ancient forest", "in an underwater city"
]
inspirations = [
    "like in Inception", "inspired by Blade Runner 2049",
    "with the atmosphere of Interstellar", "like a Marvel final battle",
    "reminiscent of The Witcher"
]
platforms = {
    "LumaLabs": "realistic and cinematic style with strong lighting and dynamic motion",
    "Runway": "hyper-detailed realism with soft transitions and natural textures",
    "Minimax": "stylized and expressive animation with fluid transitions and strong mood",
    "Pika": "bold and punchy visuals with sharp VFX and fast action flow",
    "Vidu Q1": "cinematic storytelling visuals with fluid camera movement and rich transitions",
    "Pixverse 4.5": "animated, colorful and fast-paced style with energetic motion effects",
    "Kling 1.6": "ultra-realistic rendering with advanced camera tracking and physical lighting simulation"
}



camera_moves_by_platform = {
    "LumaLabs": [
        "Pull Out + Tilt Down",
        "Orbit Right + Handheld",
        "Elevator Doors + Dolly Zoom",
        "Aerial Drone",
        "Zoom In",
        "Tiny Planet"
    ],
    "Runway": [
        "Horizontal (X-Axis Movement)",
        "Vertical (Y-Axis Movement)",
        "Pan",
        "Tilt",
        "Zoom",
        "Roll"
    ],
    "Minimax": [
        "Dolly In/Out",
        "Pan",
        "Tilt",
        "Handheld",
        "Tracking Shot",
        "Rack Focus"
    ],
    "Pika": [
        "Zoom",
        "Pan (up/down/left/right)",
        "Rotate"
    ],
    "Vidu Q1": [
        "Pedestal Shot",
        "Tilt Shot",
        "Dolly Shot",
        "Arc Shot"
    ],
    "Pixverse 4.5": [
        "Dynamic Pan",
        "Zoom",
        "Push-Pull Lenses",
        "Tracking Shots",
        "Dramatic Pans"
    ],
    "Kling 1.6": [
        "Horizontal (left/right)",
        "Vertical (up/down)",
        "Zoom",
        "Pan",
        "Tilt",
        "Roll",
        "Move Left and Zoom In",
        "Move Right and Zoom In",
        "Move Forward and Zoom Up",
        "Move Down and Zoom Out"
    ]
}

camera_moves = [
    "static frame",
    "subtle handheld movement",
    "slow dolly zoom forward",
    "drone shot circling the subject",
    "vertical tilt from bottom to top"
]

st.set_page_config(page_title=" FX Generator Tool", layout="wide")
st.title(" Générateur Vidéo IA : Texte 🎞️ ou Image 🖼️ vers Vidéo")

st.sidebar.header("⚙️ Mode de génération")
image_mode = st.sidebar.checkbox("🖼️ Mode Image-to-Video", value=False)

if image_mode:
    uploaded_image = st.file_uploader("📸 Uploade une image :", type=["jpg", "png"])
    if uploaded_image:
        st.image(uploaded_image, caption="Image source", width=350)
        st.divider()

        st.markdown("###  Paramètres d'animation")
        col1, col2, col3 = st.columns(3)
        with col1:
            style = st.selectbox("🎨 Style visuel", styles)
            inspiration = st.selectbox("🎞️ Référence cinéma", inspirations)
        with col2:
            camera = st.selectbox("🎥 Mouvement caméra", camera_moves)
            fx_main = st.selectbox("✨ Effet principal", fx_options)
        with col3:
            fx_extra = st.selectbox(" Effet secondaire", ["Aucun"] + fx_options)
            platform = st.selectbox(" Moteur cible", list(platforms.keys()))

        prompt = f"{fx_main}"
        if fx_extra != "Aucun":
            prompt += f" and {fx_extra}"
        desc = platforms[platform]
        full_prompt = f"{prompt}, using a {camera}, {style} style, {inspiration}. {desc}"

        st.markdown("### 📝 Prompt généré :")
        st.text_area(" Sélectionnez et copiez ce prompt :", full_prompt, height=120)

        summary = f"""Image-to-Video Scene
Image: {uploaded_image.name}
FX: {prompt}
Camera: {camera}
Style: {style}
Inspiration: {inspiration}
Platform: {platform} - {desc}
Prompt:
{full_prompt}