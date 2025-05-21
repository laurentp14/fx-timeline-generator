
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

story_roles = [
    "An introduction to the world or situation",
    "A tension rises as the environment starts to change",
    "A spectacular climax with major effects or destruction",
    "A twist or unexpected transformation",
    "A resolution, collapse or return to calm"
]

st.set_page_config(page_title="🎬 Timeline FX Generator", layout="wide")
st.title("🎬 Générateur de Timeline d’Effets Spéciaux Vidéo IA")
st.markdown("Crée une **suite de scènes FX** avec transitions, effets et ambiance. Idéal pour vidéos narratives multi-étapes.")

# Nombre de scènes
num_scenes = st.sidebar.slider("📽️ Nombre de scènes", min_value=1, max_value=5, value=3)

# Génération automatique d'un arc narratif
st.sidebar.markdown("---")
if st.sidebar.button("🎬 Générer un arc narratif automatique"):
    num_scenes = min(len(story_roles), num_scenes)
    timeline = []

    for i in range(num_scenes):
        role = story_roles[i]

        fx = random.sample(list(combo_fx.values()), k=random.choice([1, 2]))
        location = random.choice(locations)
        camera = random.choice(camera_moves)
        style = random.choice(styles)
        inspiration = random.choice(inspirations)

        scene_title = f"Scène {i + 1} – {role}"
        fx_desc = " and ".join(fx)
        base_prompt = f"{fx_desc} {location}, {camera}, {style} style, {inspiration}."
        timeline.append((scene_title, base_prompt))

    st.session_state["auto_timeline"] = timeline
else:
    timeline = []

# Construction manuelle
if "auto_timeline" not in st.session_state:
    for i in range(num_scenes):
        with st.expander(f"🎞️ Scène {i + 1} : personnaliser ou générer aléatoirement"):
            col1, col2 = st.columns(2)

            with col1:
                fx_keys = st.multiselect(f"Effets spéciaux (scène {i + 1})", list(combo_fx.keys()),
                                         default=random.sample(list(combo_fx.keys()), 2), key=f"fx_{i}")
                location = st.selectbox(f"Lieu", locations, index=random.randint(0, len(locations)-1), key=f"location_{i}")

            with col2:
                camera = st.selectbox(f"Mouvement caméra", camera_moves, index=random.randint(0, len(camera_moves)-1), key=f"camera_{i}")
                style = st.selectbox(f"Style visuel", styles, index=random.randint(0, len(styles)-1), key=f"style_{i}")
                inspiration = st.selectbox(f"Référence cinéma", inspirations, index=random.randint(0, len(inspirations)-1), key=f"inspiration_{i}")

            fx_parts = [combo_fx[k] for k in fx_keys if k in combo_fx]
            fx_desc = " and ".join(fx_parts) if fx_parts else "a mysterious phenomenon occurs"
            base_prompt = f"{fx_desc} {location}, {camera}, {style} style, {inspiration}."
            timeline.append((f"Scène {i + 1}", base_prompt))

# Affichage des scènes
if "auto_timeline" in st.session_state:
    timeline = st.session_state["auto_timeline"]

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
