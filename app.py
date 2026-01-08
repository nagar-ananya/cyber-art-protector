import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# -----------------------
# Page setup
# -----------------------
st.set_page_config(
    page_title="Cyber-Art Protector",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Cyber-Art Protector")
st.write("Upload an image, add a watermark, and download the protected version.")

# -----------------------
# Helper function
# -----------------------
def add_watermark(image, text, position, opacity, size):
    img = image.convert("RGBA")
    width, height = img.size

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Font size based on image width
    # size slider is 2..15, treat it as "percent of width"
    font_size = max(12, int(width * (size / 100)))

    # Load a font (DejaVuSans is often available on Linux/Streamlit Cloud)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    # --- Measure text safely across Pillow versions ---
    # Use multiline bbox so "\n" works too
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=4, align="left")
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 20
    if position == "Bottom Right":
        x = width - text_width - padding
        y = height - text_height - padding
    elif position == "Bottom Left":
        x = padding
        y = height - text_height - padding
    elif position == "Top Right":
        x = width - text_width - padding
        y = padding
    elif position == "Top Left":
        x = padding
        y = padding
    else:  # Center
        x = (width - text_width) // 2
        y = (height - text_height) // 2

    # Keep it on-screen if text is huge
    x = max(padding, min(x, width - text_width - padding))
    y = max(padding, min(y, height - text_height - padding))

    # Shadow + main text
    shadow_offset = 2
    draw.multiline_text(
        (x + shadow_offset, y + shadow_offset),
        text,
        fill=(0, 0, 0, opacity),
        font=font,
        spacing=4,
        align="left",
    )
    draw.multiline_text(
        (x, y),
        text,
        fill=(255, 255, 255, opacity),
        font=font,
        spacing=4,
        align="left",
    )

    return Image.alpha_composite(img, overlay)

# -----------------------
# UI
# -----------------------
uploaded = st.file_uploader("Upload an image (PNG or JPG)", type=["png", "jpg", "jpeg"])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Original Image", use_container_width=True)

    st.subheader("Watermark Settings")
    text = st.text_area("Watermark text", "© My Art – Do Not Repost")  # text_area helps if you want newlines
    position = st.selectbox(
        "Position",
        ["Bottom Right", "Bottom Left", "Top Right", "Top Left", "Center"]
    )
    size = st.slider("Text size (% of image width)", 2, 15, 6)
    opacity = st.slider("Opacity", 50, 255, 160)

    if st.button("Apply Watermark"):
        result = add_watermark(image, text, position, opacity, size)
        st.image(result, caption="Watermarked Image", use_container_width=True)

        buf = BytesIO()
        result.save(buf, format="PNG")
        st.download_button(
            "Download Image",
            buf.getvalue(),
            file_name="watermarked.png",
            mime="image/png"
        )
