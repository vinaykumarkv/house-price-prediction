from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import pandas as pd
import numpy as np
from typing import Literal

app = FastAPI(
    title="House Price Prediction API",
    description="Predicts house prices based on various features.",
    version="1.0.0"
)

# ────────────────────────────────────────────────
# Load model once at startup (very efficient)
# ────────────────────────────────────────────────
MODEL_PATH = "models/house_model.joblib"

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# ────────────────────────────────────────────────
# Pydantic model – matches Telco dataset columns exactly
# ────────────────────────────────────────────────
class House(BaseModel):
    square_feet: int = Field(..., description="Total square footage of the house")
    num_rooms: int = Field(..., description="Number of rooms in the house")
    age: int = Field(..., description="Age of the house in years")
    distance_to_city: int = Field(..., description="Distance to the city center in kilometers")
    

    class Config:
        json_schema_extra = {
            "example": {
                'square_feet': 1500,
                'num_rooms': 3,
                'age': 10,
                'distance_to_city': 5,
            }
        }

# ────────────────────────────────────────────────
# Prediction endpoint
# ────────────────────────────────────────────────
@app.post("/predict", response_model=dict)
async def predict_price(house: House):
    try:
        # Convert input to DataFrame (exactly what the pipeline expects)
        input_df = pd.DataFrame([house.model_dump()])

        # Predict
        price = model.predict(input_df)

        prediction = model.predict(input_df)
        message = f"Model prediction output: {prediction}"  # Debugging line
        price = float(prediction[0][0]) # Assuming array output
        
        return {
            "price": f"${round(price, 2):,}",
            "message": message,
            "model_version": "Neural Network based house price prediction model v1.0"
        }

    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Prediction error: {str(e)}")


# ────────────────────────────────────────────────
# Health check (useful for deployment / monitoring)
# ────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}