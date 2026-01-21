import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import streamlit.components.v1 as components

# -----------------------
# Page setup
# -----------------------
st.set_page_config(
    page_title="Cyber-Art Protector",
    page_icon="🛡️",
    layout="centered"
)

# -----------------------
# Fonts + Styling
# -----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Dancing+Script:wght@400;600&family=Inter:wght@300;400&display=swap');

/* ---------- BACKGROUND ---------- */
.stApp {
    background: #EAF2FF;
}

section.main > div {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 2.5rem 2rem 3rem 2rem;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

.block-container {
    padding-top: 2rem;
}

/* ---------- STREAMLIT TOP HEADER ---------- */

/* Main header bar */
header[data-testid="stHeader"] {
    background: #EAF2FF;
    border-bottom: none;
}

/* Optional: soften the shadow if present */
header[data-testid="stHeader"]::after {
    box-shadow: none;
}

/* Make header buttons/icons subtle but visible */
header[data-testid="stHeader"] button,
header[data-testid="stHeader"] svg {
    color: #1F2937;
}


/* ---------- TEXT ---------- */
.title {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    letter-spacing: 0.25em;
    text-align: center;
    margin-bottom: 0.3rem;
    color: #1F2937;
}

.script {
    font-family: 'Dancing Script', cursive;
    font-size: 2.3rem;
    text-align: center;
    margin-bottom: 1rem;
    color: #374151;
}

.description {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    line-height: 1.65;
    max-width: 560px;
    margin: 0 auto;
    text-align: center;
    letter-spacing: 0.02em;
    color: #1F2937;
    text-transform: uppercase;
}

.label {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    text-align: center;
    margin-top: 1.4rem;
    color: #4B5563;
}

/* ---------- FILE UPLOADER ---------- */
.stFileUploader {
    border: 2px solid #C7D7F5;
    border-radius: 16px;
    padding: 1.4rem;
    background: #F9FBFF;
}

/* Upload label text */
.stFileUploader label {
    color: #1F2937 !important;
    font-weight: 500;
}

/* Drag & drop text */
.stFileUploader div {
    color: #374151;
}

/* ---------- BUTTONS ---------- */
.stButton > button,
.stDownloadButton > button {
    background-color: #E6EFFF;
    color: #1E3A8A;
    border-radius: 14px;
    padding: 0.65rem 1.3rem;
    border: 1px solid #C7D7F5;
    font-weight: 500;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #D7E6FF;
}

/* ---------- SPACING ---------- */
.upload-spacer {
    height: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# Header
# -----------------------
st.markdown('<div class="title">CYBER-ART<br>PROTECTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="script">upload an image</div>', unsafe_allow_html=True)

st.markdown("""
<div class="description">
Scared that someone will steal YOUR artwork or YOUR image? <b>FEAR NOT!</b>  
<i>The Cyber Art Protector</i> has come to the rescue. With this tool, you can upload your image.
The algorithm will add a watermark, letting everybody on the Internet know exactly what's yours.
</div>

<div class="label">
Back off, copycats!
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

# -----------------------
# Helper function
# -----------------------
def add_watermark(image, text, position, opacity, size):
    img = image.convert("RGBA")
    width, height = img.size

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = max(12, int(width * (size / 100)))

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=4)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 20
    positions = {
        "Bottom Right": (width - text_width - padding, height - text_height - padding),
        "Bottom Left": (padding, height - text_height - padding),
        "Top Right": (width - text_width - padding, padding),
        "Top Left": (padding, padding),
        "Center": ((width - text_width) // 2, (height - text_height) // 2),
    }

    x, y = positions[position]
    x = max(padding, min(x, width - text_width - padding))
    y = max(padding, min(y, height - text_height - padding))

    draw.multiline_text((x + 2, y + 2), text, fill=(0, 0, 0, opacity), font=font)
    draw.multiline_text((x, y), text, fill=(255, 255, 255, opacity), font=font)

    return Image.alpha_composite(img, overlay)

# -----------------------
# UI
# -----------------------
uploaded = st.file_uploader("Upload an image (PNG or JPG)", type=["png", "jpg", "jpeg"])

if "result_bytes" not in st.session_state:
    st.session_state.result_bytes = None

if uploaded:
    image = ImageOps.exif_transpose(Image.open(uploaded))
    st.image(image, caption="Original Image", use_container_width=True)

    st.subheader("Watermark Settings")
    text = st.text_area("Watermark text", "© My Art – Do Not Repost")
    position = st.selectbox(
        "Position",
        ["Bottom Right", "Bottom Left", "Top Right", "Top Left", "Center"]
    )
    size = st.slider("Text size (% of image width)", 2, 15, 6)
    opacity = st.slider("Opacity", 50, 255, 160)

    if st.button("Apply Watermark"):
        result = add_watermark(image, text, position, opacity, size)
        buf = BytesIO()
        result.save(buf, format="PNG")
        buf.seek(0)
        st.session_state.result_bytes = buf.getvalue()

    if st.session_state.result_bytes:
        st.image(st.session_state.result_bytes, caption="Watermarked Image", use_container_width=True)
        st.download_button(
            "Download Image",
            st.session_state.result_bytes,
            file_name="watermarked.png",
            mime="image/png"
        )
