import uvicorn
import joblib
import yaml
import os
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.tools import Tool

# ✅ Load Config
with open("params.yaml", "r") as file:
    config = yaml.safe_load(file)

MODEL_PATH = config["train"]["model_path"]

# ✅ Load Model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"🚨 Model file not found at {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

# ✅ Initialize FastAPI
app = FastAPI(title="Insurance Prediction Agent", description="An AI-powered assistant for insurance charge predictions.")

# ✅ Define Request Body
class InsuranceInput(BaseModel):
    age: int
    bmi: float
    children: int
    smoker: str
    region: str

# ✅ Define the prediction function
def predict_insurance(data: InsuranceInput):
    input_data = pd.DataFrame([data.dict()])
    input_data["smoker"] = input_data["smoker"].map({"no": 0, "yes": 1})
    input_data = pd.get_dummies(input_data, columns=["region"], drop_first=True)
    model_columns = model.feature_names_in_
    missing_cols = set(model_columns) - set(input_data.columns)
    for col in missing_cols:
        input_data[col] = 0  # Add missing columns with default value
    input_data = input_data[model_columns]
    prediction = model.predict(input_data)[0]
    return round(float(prediction), 2)

# ✅ LangChain Agent Setup
llm = OpenAI()
tools = [
    Tool(
        name="Insurance Calculator",
        func=lambda x: predict_insurance(InsuranceInput(**x)),
        description="Calculates estimated insurance charges based on user details."
    )
]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

@app.get("/")
def home():
    return {"message": "Welcome to the Insurance Prediction Agent! Use /predict to get insurance charge predictions."}

@app.post("/predict")
def predict(data: InsuranceInput):
    """Predicts insurance charges based on input features."""
    prediction = predict_insurance(data)
    return {
        "predicted_charge": prediction,
        "message": "Insurance charge predicted successfully."
    }

@app.post("/agent")
def agent_interact(data: dict):
    """Uses an AI agent to process insurance-related queries."""
    response = agent.run(data["query"])
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
