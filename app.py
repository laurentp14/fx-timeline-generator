
import streamlit as st
import random
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

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

locations = [
    "in a medieval castle", "on a floating island", "in a neon-lit cyberpunk city",
    "inside an ancient forest", "in an underwater city"
]

styles = ["cinematic", "dreamlike", "hyper-realistic", "stylized anime", "dark sci-fi"]

camera_moves = [
    "static frame",
    "subtle handheld movement",
    "slow dolly zoom forward",
    "drone shot circling the subject",
    "vertical tilt from bottom to top"
]

fx_options = [
    "particles floating around",
    "light rays breaking through clouds",
    "portal opening behind the subject",
    "energy surging from the ground",
    "environment slowly collapsing",
    "scene gradually shifting to another dimension"
]

inspirations = [
    "like in Inception",
    "inspired by Blade Runner 2049",
    "with the atmosphere of Interstellar",
    "like a Marvel final battle",
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

# Config de page
st.set_page_config(page_title="🎬 FX Prompt Generator - Dual Mode", layout="wide")
st.title("🎬 Générateur Vidéo IA : Texte vers Vidéo 🎞️ ou Image vers Vidéo 🖼️")

# Choix du mode
st.sidebar.header("⚙️ Mode de génération")
image_mode = st.sidebar.checkbox("🖼️ Activer le mode Image-to-Video", value=False)

if image_mode:
    # Mode image-to-video
    st.subheader("🖼️ Mode Image vers Vidéo (1 seule scène)")
    uploaded_image = st.file_uploader("📸 Uploade une image :", type=["jpg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Image source", width=350)
        st.divider()

        st.markdown("### 🎬 Paramètres d'animation")

        col1, col2, col3 = st.columns(3)

        with col1:
            style = st.selectbox("🎨 Style visuel", styles)
            inspiration = st.selectbox("🎞️ Référence cinéma", inspirations)

        with col2:
            camera = st.selectbox("🎥 Mouvement de caméra", camera_moves)
            fx_main = st.selectbox("✨ Effet principal", fx_options)

        with col3:
            fx_extra = st.selectbox("🔮 Effet secondaire", ["Aucun"] + fx_options)
            platform = st.selectbox("🎯 Moteur cible", list(platforms.keys()))

        # Prompt final
        prompt = f"{fx_main}"
        if fx_extra != "Aucun":
            prompt += f" and {fx_extra}"

        full_prompt = f"{prompt}, using a {camera}, {style} style, {inspiration}. Adapted for {platform}."

        st.markdown("### 📝 Prompt d'animation généré :")
        st.code(full_prompt)
    else:
        st.info("🖼️ Veuillez uploader une image pour commencer.")
else:
    # Mode texte-to-video multi-scène
    num_scenes = st.sidebar.slider("📽️ Nombre de scènes", 1, 5, 3)
    use_smart_combo = st.sidebar.checkbox("🧠 Activer les suggestions FX intelligentes", value=False)

    timeline = []

    for i in range(num_scenes):
        with st.expander(f"🎞️ Scène {i + 1}"):
            col1, col2 = st.columns(2)

            with col1:
                if use_smart_combo:
                    fx1 = st.selectbox(f"Effet principal (scène {i + 1})", list(combo_fx.keys()), key=f"fx1_{i}")
                    suggested = combo_suggestions.get(fx1, [])
                    fx2 = st.selectbox(f"Effet complémentaire suggéré", ["Aucun"] + suggested, key=f"fx2_{i}")
                    fx_list = [combo_fx[fx1]]
                    if fx2 != "Aucun" and fx2 in combo_fx:
                        fx_list.append(combo_fx[fx2])
                else:
                    fx_keys = st.multiselect(f"Effets spéciaux (scène {i + 1})", list(combo_fx.keys()),
                                             default=random.sample(list(combo_fx.keys()), 2), key=f"fx_{i}")
                    fx_list = [combo_fx[k] for k in fx_keys if k in combo_fx]

                location = st.selectbox(f"Lieu", locations, index=random.randint(0, len(locations)-1), key=f"location_{i}")

            with col2:
                camera = st.selectbox(f"Mouvement caméra", camera_moves, index=random.randint(0, len(camera_moves)-1), key=f"camera_{i}")
                style = st.selectbox(f"Style visuel", styles, index=random.randint(0, len(styles)-1), key=f"style_{i}")
                inspiration = st.selectbox(f"Référence cinéma", inspirations, index=random.randint(0, len(inspirations)-1), key=f"inspiration_{i}")

            fx_desc = " and ".join(fx_list) if fx_list else "a mysterious phenomenon occurs"
            base_prompt = f"{fx_desc} {location}, {camera}, {style} style, {inspiration}."
            timeline.append((f"Scène {i + 1}", base_prompt))

    st.subheader("📜 Timeline des Scènes Générées")
    for scene_title, base_prompt in timeline:
        st.markdown(f"## 🎬 {scene_title}")
        st.code(base_prompt)
        for platform, desc in platforms.items():
            full_prompt = f"{base_prompt} Adapted for {platform}: {desc}."
            st.markdown(f"**🔹 {platform}**")
            st.code(full_prompt)
