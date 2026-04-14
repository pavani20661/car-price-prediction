# Generated from: narendra.ipynb
# Converted at: 2026-04-10T15:01:32.182Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

# ---------------- IMPORTS ----------------
import streamlit as st
import joblib
import pandas as pd
from datetime import datetime

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "users" not in st.session_state:
    st.session_state.users = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- LOAD MODEL ----------------
try:
    model = joblib.load("car_price_model.pkl")
except:
    model = None

# ---------------- APP CONFIG ----------------
st.set_page_config(page_title="Car Price Prediction", layout="centered")
st.title("🚗 Used Car Price Prediction System")

# ---------------- NAVIGATION ----------------
menu = ["Home", "Register", "Login", "Prediction", "Chatbot"]
choice = st.sidebar.selectbox("Navigation", menu)

# ---------------- HOME ----------------
if choice == "Home":
    st.subheader("🏠 Home")
    st.write("Welcome to the Used Car Price Prediction System")

    st.subheader("📄 About")
    st.write("""
    This project predicts used car prices using Machine Learning.
    Users must register and login to access prediction.
    """)

# ---------------- REGISTER ----------------
elif choice == "Register":
    st.subheader("📝 Register")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Create Password", type="password")
    phone = st.text_input("Phone")
    age = st.number_input("Age", 18, 100)
    address = st.text_area("Address")

    if st.button("Register"):
        if email in st.session_state.users:
            st.error("User already exists!")
        else:
            st.session_state.users[email] = {
                "name": name,
                "password": password
            }
            st.success("Registration Successful! Please Login.")

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email in st.session_state.users:
            if st.session_state.users[email]["password"] == password:
                st.session_state.logged_in = True
                st.success(f"Welcome {st.session_state.users[email]['name']} 🎉")
            else:
                st.error("Incorrect Password")
        else:
            st.error("User not found. Please Register.")

# ---------------- PREDICTION ----------------
elif choice == "Prediction":

    if not st.session_state.logged_in:
        st.warning("⚠️ Please login first to access Prediction page")
        st.stop()

    st.subheader("🚘 Car Price Prediction")

    uploaded_file = st.file_uploader("Upload Car Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Car Image", use_container_width=True)

    st.write("### Enter Car Details")

    present_price = st.number_input("Present Price (in lakhs)")
    kms_driven = st.number_input("Kilometers Driven")
    past_owners = st.selectbox("Past Owners", [0, 1, 2, 3])

    year = st.number_input("Year of Purchase", 2000, datetime.now().year)
    age_of_car = datetime.now().year - year

    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel"])
    fuel_petrol = 1 if fuel_type == "Petrol" else 0
    fuel_diesel = 1 if fuel_type == "Diesel" else 0

    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    seller_individual = 1 if seller_type == "Individual" else 0

    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    transmission_manual = 1 if transmission == "Manual" else 0

    if st.button("Predict Price"):

        input_data = pd.DataFrame({
            'Present_Price(lacs)': [present_price],
            'Kms_Driven': [kms_driven],
            'Past_Owners': [past_owners],
            'Age_of_car': [age_of_car],
            'Fuel_Type_Diesel': [fuel_diesel],
            'Fuel_Type_Petrol': [fuel_petrol],
            'Seller_Type_Individual': [seller_individual],
            'Transmission_Manual': [transmission_manual]
        })

        if model is not None:
            try:
                prediction = model.predict(input_data)
                st.success(f"💰 Estimated Price: ₹ {round(prediction[0], 2)} Lakhs")
            except Exception as e:
                st.error(f"Prediction Error: {e}")
        else:
            st.error("Model not loaded")

# ---------------- CHATBOT ----------------
elif choice == "Chatbot":

    st.subheader("🤖 AI Chatbot Assistant")

    st.write("Ask anything about cars, price prediction, or app usage!")

    # Display chat history
    for chat in st.session_state.chat_history:
        st.write(chat)

    user_input = st.text_input("You:")

    def chatbot_response(user_text):
        user_text = user_text.lower()

        if "price" in user_text:
            return "Car price depends on factors like age, kms driven, fuel type, and ownership."
        elif "model" in user_text:
            return "We use a Machine Learning regression model trained on car data."
        elif "hello" in user_text or "hi" in user_text:
            return "Hello! How can I help you?"
        elif "login" in user_text:
            return "Go to the Login page from sidebar and enter your credentials."
        elif "register" in user_text:
            return "Go to Register page and create your account."
        else:
            return "I'm here to help! Ask me about car prediction or this app."

    if st.button("Send"):
        if user_input:
            response = chatbot_response(user_input)

            st.session_state.chat_history.append(f"🧑 You: {user_input}")
            st.session_state.chat_history.append(f"🤖 Bot: {response}")