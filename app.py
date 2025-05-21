
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

# Suggestions intelligentes de combos
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
    "with a drone shot circling the scene", "with a slow-motion dolly zoom",
    "with a handheld shaking camera", "in a smooth panoramic shot"
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
        "Pull Out + Tilt Down", "Orbit Right + Handheld", "Elevator Doors + Dolly Zoom",
        "Aerial Drone", "Zoom In", "Tiny Planet"
    ],
    "Runway": [
        "Horizontal (X-Axis Movement)", "Vertical (Y-Axis Movement)", "Pan", "Tilt", "Zoom", "Roll"
    ],
    "Minimax": [
        "Dolly In/Out", "Pan", "Tilt", "Handheld", "Tracking Shot", "Rack Focus"
    ],
    "Pika": [
        "Zoom", "Pan (up/down/left/right)", "Rotate"
    ],
    "Vidu Q1": [
        "Pedestal Shot", "Tilt Shot", "Dolly Shot", "Arc Shot"
    ],
    "Pixverse 4.5": [
        "Dynamic Pan", "Zoom", "Push-Pull Lenses", "Tracking Shots", "Dramatic Pans"
    ],
    "Kling 1.6": [
        "Horizontal (left/right)", "Vertical (up/down)", "Zoom", "Pan", "Tilt", "Roll",
        "Move Left and Zoom In", "Move Right and Zoom In", "Move Forward and Zoom Up", "Move Down and Zoom Out"
    ]
}

camera_moves = [
    "static frame", "subtle handheld movement", "slow dolly zoom forward",
    "drone shot circling the subject", "vertical tilt from bottom to top"
]




st.set_page_config(page_title="🎬 FX Prompt Timeline Generator", layout="wide")
st.title("🎬 Générateur de Timeline d’Effets Spéciaux Vidéo IA")

# Options dans la sidebar
num_scenes = st.sidebar.slider("📽️ Nombre de scènes", 1, 5, 3)
use_smart_combo = st.sidebar.checkbox("🧠 Activer les suggestions intelligentes de FX", value=False)
camera_all_toggle = st.sidebar.checkbox("🔄 Afficher tous les mouvements de caméra")

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
            platform = st.selectbox(f"Plateforme IA", list(platforms.keys()), index=0, key=f"plat_{i}")
            camera = st.selectbox(f"Mouvement caméra", camera_moves if camera_all_toggle else camera_moves_by_platform.get(platform, camera_moves), index=random.randint(0, len(camera_moves)-1), key=f"camera_{i}")
            style = st.selectbox(f"Style visuel", styles, index=random.randint(0, len(styles)-1), key=f"style_{i}")
            inspiration = st.selectbox(f"Référence cinéma", inspirations, index=random.randint(0, len(inspirations)-1), key=f"inspiration_{i}")

        fx_desc = " and ".join(fx_list) if fx_list else "a mysterious phenomenon occurs"
        base_prompt = f"{fx_desc} {location}, {camera}, {style} style, {inspiration}."
        timeline.append((f"Scène {i + 1}", base_prompt))

# Affichage des scènes
st.subheader("📜 Timeline des Scènes Générées")
for scene_title, base_prompt in timeline:
    st.markdown(f"## 🎬 {scene_title}")
    st.code(base_prompt)
    for platform, desc in platforms.items():
        full_prompt = f"{base_prompt} Adapted for {platform}: {desc}."
        st.markdown(f"**🔹 {platform}**")
        st.code(full_prompt)

# Export Markdown
if st.button("📝 Exporter la timeline en Markdown (.md)"):
    md_lines = ["# 🎬 FX Video Prompt Timeline", ""]
    for scene_title, base_prompt in timeline:
        md_lines.append(f"## {scene_title}")
        md_lines.append("")
        md_lines.append("**Prompt principal :**")
        md_lines.append("")
        md_lines.append(f"> {base_prompt}")
        md_lines.append("")
        for platform, desc in platforms.items():
            full_prompt = f"{base_prompt} Adapted for {platform}: {desc}."
            md_lines.append(f"**🔹 {platform}**")
            md_lines.append("")
            md_lines.append(f"> {full_prompt}")
            md_lines.append("")

    markdown_text = "\n".join(md_lines)
    file_path = "fx_timeline.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)

    with open(file_path, "rb") as f:
        st.download_button(
            label="📥 Télécharger le fichier Markdown",
            data=f,
            file_name="fx_timeline.md",
            mime="text/markdown"
        )

    os.remove(file_path)

# Export PDF
def split_text(text, max_length):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= max_length:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())
    return lines

def create_pdf(timeline):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "🎬 FX Video Prompt Timeline")
    y -= 30

    for scene_title, base_prompt in timeline:
        if y < 120:
            c.showPage()
            c.setFont("Helvetica", 12)
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

        for platform, desc in platforms.items():
            full_prompt = f"{base_prompt} Adapted for {platform}: {desc}."
            y -= 10
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y, f"{platform}")
            y -= 16
            c.setFont("Helvetica", 11)
            for line in split_text(full_prompt, 90):
                c.drawString(50, y, line)
                y -= 14

            y -= 8

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
