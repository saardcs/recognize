import streamlit as st
from openai import OpenAI
from PIL import Image
import io, base64

st.title("Find the Object Challenge!")

# Load API key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

target_word = st.text_input("Word students must find:", "banana")

image_data = st.camera_input("Take a picture")

if image_data:
    image = Image.open(image_data)

    st.image(image, caption="Your picture")
    
    # Convert to base64
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    b64_image = base64.b64encode(buf.getvalue()).decode()

    with st.spinner("Analyzing the image..."):
        response = client.responses.create(
            model="gpt-4.1-vision",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Describe what you see."},
                        {"type": "input_image", "image_url": f"data:image/jpeg;base64,{b64_image}"},
                    ]
                }
            ]
        )

    description = response.output_text

    st.write("### AI Description:")
    st.write(description)

    if target_word.lower() in description.lower():
        st.success(f"Nice! The description contains **{target_word}**.")
    else:
        st.error(f"Not quite — I didn’t detect **{target_word}** in the description.")
