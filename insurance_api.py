import uvicorn
import joblib
import yaml
import os
import pandas as pd
import mlflow
import mlflow.sklearn
from fastapi import FastAPI
from pydantic import BaseModel

# ✅ Load Config
with open("params.yaml", "r") as file:
    config = yaml.safe_load(file)

MODEL_PATH = config["train"]["model_path"]
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("Insurance Prediction API")

# ✅ Load Model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"🚨 Model file not found at {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

# ✅ Initialize FastAPI
app = FastAPI(title="Insurance Prediction API", description="Predicts insurance charges based on customer features.")

# ✅ Define Request Body
class InsuranceInput(BaseModel):
    age: int
    bmi: float
    children: int
    smoker: str
    region: str

@app.get("/")
def home():
    return {"message": "Welcome to the Insurance Prediction API! "}

@app.post("/predict")
def predict(data: InsuranceInput):
    """Predicts insurance charges based on input features and logs results to MLflow."""
    input_data = pd.DataFrame([data.dict()])

    # Convert categorical features to numerical
    input_data["smoker"] = input_data["smoker"].map({"no": 0, "yes": 1})
    input_data = pd.get_dummies(input_data, columns=["region"], drop_first=True)

    # Ensure columns match training data
    model_columns = model.feature_names_in_
    missing_cols = set(model_columns) - set(input_data.columns)
    for col in missing_cols:
        input_data[col] = 0  # Add missing columns with default value
    input_data = input_data[model_columns]  # Reorder columns to match model

    # Make Prediction
    prediction = model.predict(input_data)[0]
    predicted_charge = round(float(prediction), 2)

    # ✅ Log input & output to MLflow
    with mlflow.start_run():
        mlflow.log_params(data.dict())
        mlflow.log_metric("predicted_charge", predicted_charge)

    return {
        "predicted_charge": predicted_charge,
        "message": "Insurance charge predicted successfully and logged to MLflow."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
