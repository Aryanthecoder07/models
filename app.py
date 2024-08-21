import streamlit as st
from PIL import Image
import google.generativeai as gen
import os

# Configure the API key for the model
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
st.set_page_config(page_title="My Personal Nutritionist", page_icon="🍏", layout="centered")

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

# Carousel Simulation with Streamlit
st.subheader("🎠 Food Carousel ")
food_options = {
    "Salmon": "Rich in Omega-3 fatty acids, great for heart health.",
    "Broccoli": "Packed with vitamins C and K, fiber, and antioxidants.",
    "Quinoa": "A complete protein source, high in fiber and minerals.",
    "Blueberries": "Loaded with antioxidants, supports brain health.",
    "Avocado": "High in healthy fats, supports heart health."
}

# Create a selectbox to simulate carousel navigation
selected_food = st.selectbox("Select a food item to see details:", list(food_options.keys()))

# Display details of the selected food
st.write(f"**{selected_food}**")
st.write(food_options[selected_food])

# Placeholder for displaying the uploaded image



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
            
          image = Image.open(file)
          st.image(image, caption="Uploaded Meal Image", use_column_width=True, clamp=True)
            

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
