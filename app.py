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
    font_size = int(width * (size / 100))
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except:
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(text, font)

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
    else:
        x = (width - text_width) // 2
        y = (height - text_height) // 2

    # Shadow
    draw.text((x+2, y+2), text, fill=(0, 0, 0, opacity), font=font)
    # Main text
    draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)

    return Image.alpha_composite(img, overlay)

# -----------------------
# UI
# -----------------------
uploaded = st.file_uploader("Upload an image (PNG or JPG)", type=["png", "jpg", "jpeg"])

if uploaded:
    image = Image.open(uploaded)

    st.image(image, caption="Original Image", use_container_width=True)

    st.subheader("Watermark Settings")
    text = st.text_input("Watermark text", "© My Art – Do Not Repost")
    position = st.selectbox(
        "Position",
        ["Bottom Right", "Bottom Left", "Top Right", "Top Left", "Center"]
    )
    size = st.slider("Text size", 2, 15, 6)
    opacity = st.slider("Opacity", 50, 255, 160)

    if st.button("Apply Watermark"):
        result = add_watermark(image, text, position, opacity, size)
        st.image(result, caption="Watermarked Image")

        buf = BytesIO()
        result.save(buf, format="PNG")

        st.download_button(
            "Download Image",
            buf.getvalue(),
            file_name="watermarked.png",
            mime="image/png"
        )
