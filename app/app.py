import gradio as gr
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/predict"

def predict_price(sq_ft, rooms, age, dist):

    payload = {
        "square_feet": int(sq_ft),
        "num_rooms": int(rooms),
        "age": int(age),
        "distance_to_city": int(dist)
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            return result["price"]

        else:
            return f"API Error: {response.text}"

    except Exception as e:
        return f"Connection Error: {str(e)}"


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
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860
    )