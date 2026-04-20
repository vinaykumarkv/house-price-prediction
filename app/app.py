import gradio as gr
import pandas as pd
import numpy as np
import pickle
import os

# 1. Correct Path to your model
model_path = os.path.join("models", "house_model.pkl")
#API_URL = "http://127.0.0.1:8000/predict"

with open(model_path, 'rb') as f:
    model = pickle.load(f)

def predict_price(sq_ft, rooms, age, dist):
    input_df = pd.DataFrame({
        'square_feet': [sq_ft],
        'num_rooms': [rooms],
        'age': [age],
        'distance_to_city(km)': [dist]
    })
    
    prediction = model.predict(input_df)
    print(f"Model prediction output: {prediction}")  # Debugging line
    price = float(prediction[0][0]) # Assuming array output
    return f"${round(price, 2):,}"

interface = gr.Interface(
    fn=predict_price,
    inputs=[
        gr.Number(label="Square Feet", value=1500),
        gr.Slider(1, 10, step=1, label="Rooms", value=3),
        gr.Number(label="Age", value=10),
        gr.Number(label="Distance (km)", value=5)
    ],
    outputs=gr.Textbox(label="Estimated Price"),
    title="House Price Predictor"
)

if __name__ == "__main__":
    interface.launch(server_name="127.0.0.1", server_port=7860)
