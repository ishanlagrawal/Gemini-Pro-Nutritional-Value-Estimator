### Health Management App
import os
import base64
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(image_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    image_blob = {
        "mime_type": "image/jpeg",
        "data": base64.b64encode(image_data).decode('utf-8')
    }
    response = model.generate_content([image_blob, prompt])
    return response.text

# Function to process uploaded image
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file.getvalue()
    raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="GeminiPro: Nutritional Value Estimator")
st.header("GeminiPro: Nutritional Value Estimator")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])
if uploaded_file:
    image_data = process_uploaded_file(uploaded_file)
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

input_prompt = """
You are an expert in nutritionist or dietitian where you need to identify name of each food items from the image
and considering average portion size for one person, provide the details of each food item with the estimated
general calories intake or general calorie ranges in the below format, :

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----
Finally, mention whether the food is healthy and the percentage split 
of carbohydrates, fats, fibers, sugar, and other important nutrients.
"""

if st.button("Click for Nutritional Information and Total Calories"):
    response = get_gemini_response(image_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)
