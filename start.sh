#!/usr/bin/env bash

# Start FastAPI on port 8000 (background)
uvicorn app.api:app --host 0.0.0.0 --port 8000 --workers 1 &

# Wait a few seconds for API to be ready
sleep 5

# Start Streamlit on port 7860 (Hugging Face default exposed port)
python app/app.py