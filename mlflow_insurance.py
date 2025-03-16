import os
import yaml
import json
import psutil
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error, r2_score

def evaluate_model(config_path):
    """Evaluates the trained model, logs metrics to MLflow, and collects system metrics."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    test_path = config['data_split']['testset_path']
    model_path = config['train']['model_path']
    metrics_path = config['evaluate']['metrics_path']
    system_metrics_path = config['evaluate']['system_metrics_path']
    target_column = config['featurize']['target_column']

    # Load test dataset
    df = pd.read_csv(test_path)
    X_test = df.drop(columns=[target_column])
    y_test = df[target_column]

    # Load trained model
    model = joblib.load(model_path)

    # Make predictions
    y_pred = model.predict(X_test)

    # Compute model performance metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    model_metrics = {
        "mse": mse,
        "rmse": rmse,
        "r2_score": r2
    }
    
    # Save model metrics
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    with open(metrics_path, 'w') as f:
        json.dump(model_metrics, f)
    print(f"✅ Model metrics saved at {metrics_path}")

    # Collect system metrics
    system_metrics = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    
    # Save system metrics
    os.makedirs(os.path.dirname(system_metrics_path), exist_ok=True)
    with open(system_metrics_path, 'w') as f:
        json.dump(system_metrics, f)
    print(f"✅ System metrics saved at {system_metrics_path}")

    # Log metrics to MLflow
    mlflow.set_experiment("Insurance Model Evaluation")
    with mlflow.start_run():
        mlflow.log_metrics(model_metrics)
        mlflow.log_dict(system_metrics, "system_metrics.json")
        mlflow.sklearn.log_model(model, "insurance_model")
        print("✅ Metrics and model logged to MLflow")

if __name__ == "__main__":
    evaluate_model("params.yaml")
