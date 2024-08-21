import streamlit as st
import google.generativeai as gen
import os
from PIL import Image

# Configure the API key
gen.configure(api_key="AIzaSyB9y3zCzpzNKzFq7LOWMn7d3SirCDtDYUI")

# Function to get the response from the model
def res(input_prompt, image):
    model = gen.GenerativeModel("gemini-1.5-pro")
    resp = model.generate_content([input_prompt, image[0]])
    return resp.text

# Function to process the uploaded file
def inp(file):
    if file is not None:
        bytes_data = file.getvalue()
        image_parts = [
            {
                "mime_type": file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app setup
st.set_page_config(page_title="My Personal Nutritionist", page_icon="🍎", layout="centered")

# Custom CSS and JavaScript for styling, carousel, and background color
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
        }
        .main {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .carousel-container {
            width: 100%;
            overflow: hidden;
            background-color: #e0e7ff;
            padding: 10px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .carousel-content {
            display: flex;
            animation: moveBelt 20s linear infinite;
        }
        .carousel-item {
            min-width: 200px;
            margin-right: 20px;
            flex-shrink: 0;
            text-align: center;
            background-color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        @keyframes moveBelt {
            0% { transform: translateX(0); }
            100% { transform: translateX(-100%); }
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            text-align: center;
        }
        .stButton>button {
            background-color: #e74c3c;
            color: white;
            border-radius: 8px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #c0392b;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.header("🍏 My Personal Nutritionist")
st.markdown("Learn about the nutritional value of your meals with a quick analysis!")

# Section: Importance of a Healthy Diet
st.subheader("🥗 Importance of a Healthy Diet")
st.markdown("""
    Maintaining a healthy diet is crucial for overall well-being. It helps in:
    - **Boosting immunity**: Proper nutrition strengthens the immune system.
    - **Maintaining a healthy weight**: Balanced meals prevent obesity.
    - **Improving mental health**: A nutritious diet can enhance mood and mental clarity.
    - **Reducing chronic diseases**: Healthy eating lowers the risk of heart disease, diabetes, and other chronic conditions.
""")

# Moving Belt Carousel
st.subheader("🍲 Discover Various Types of Food")
st.markdown("""
    <div class="carousel-container">
        <div class="carousel-content">
            <div class="carousel-item">
                <strong>Salmon</strong><br>
                Rich in Omega-3 fatty acids, great for heart health.
            </div>
            <div class="carousel-item">
                <strong>Broccoli</strong><br>
                Packed with vitamins C and K, fiber, and antioxidants.
            </div>
            <div class="carousel-item">
                <strong>Quinoa</strong><br>
                A complete protein source, high in fiber and minerals.
            </div>
            <div class="carousel-item">
                <strong>Blueberries</strong><br>
                Loaded with antioxidants, supports brain health.
            </div>
            <div class="carousel-item">
                <strong>Avocado</strong><br>
                High in healthy fats, supports heart health.
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Instructions for the user
st.subheader("🔽 Follow the steps below to get your meal analysis:")

# Instructions at the end
st.markdown("""
    1. **Upload an image of your meal**: Use the uploader below to choose an image of your meal.
    2. **Submit**: Click the submit button to get your detailed nutritional analysis.
""")

# File uploader in Streamlit
file = st.file_uploader("Choose an image of your meal", type=["jpg", "png", "jpeg"])
image = ""

# Display uploaded image
if file is not None:
    image = Image.open(file)
    st.image(image, caption="Uploaded Meal Image", use_column_width=True, clamp=True)

# Button to submit and get the analysis
input_prompt = (
    "You are an expert in nutrition where you need to see the food items from the image and calculate the total calories,"
    "also provide the details of every food item with calorie intake in the below format:\n\n"
    "1. Item 1 - no. of calories\n"
    "2. Item 2 - no. of calories\n"
    "...\n\n"
    "Finally, mention whether the food is healthy or not and also mention the percentage split of the ratio of carbohydrates, fats, fiber, sugar, and other essential nutrients in our diet."
)

submit = st.button("Tell Me About My Food 🍽️")

# Process the image and display the results
if submit:
    if file is not None:
        try:
            with st.spinner("Analyzing the image..."):
                image_data = inp(file)
                r = res(input_prompt, image_data)
            st.success("Analysis Complete! Here's your report:")
            st.markdown("---")
            st.write(r)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload an image before submitting.")
