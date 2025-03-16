import os
import yaml
import pandas as pd
import json
import joblib
import mlflow
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset, TargetDriftPreset
from evidently import ColumnMapping

def detect_drift(config_path):
    """Detects data drift, data quality issues, and target drift using Evidently AI."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    train_path = config["data_split"]["trainset_path"]
    test_path = config["data_split"]["testset_path"]
    drift_report_path = config["evaluate"]["drift_report_path"]
    target_column = config["featurize"]["target_column"]

    # Load train and test datasets
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        raise FileNotFoundError("🚨 Train or test dataset not found! Run data processing first.")
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    # Separate features from target
    X_train = train_df.drop(columns=[target_column])
    X_test = test_df.drop(columns=[target_column])

    # Define column mapping
    column_mapping = ColumnMapping()
    column_mapping.target = target_column
    column_mapping.prediction = "prediction"
    column_mapping.numerical_features = X_train.select_dtypes(include=["number"]).columns.tolist()
    column_mapping.categorical_features = X_train.select_dtypes(include=["object"]).columns.tolist()

    # Generate Evidently AI reports
    drift_report = Report(metrics=[
        DataDriftPreset(),
        DataQualityPreset(),
        TargetDriftPreset()
    ])
    drift_report.run(reference_data=X_train, current_data=X_test, column_mapping=column_mapping)

    # Save report
    os.makedirs(os.path.dirname(drift_report_path), exist_ok=True)
    drift_report.save_html(drift_report_path)
    print(f"✅ Data drift, data quality, and target drift report saved at {drift_report_path}")

    # Log report to MLflow
    mlflow.set_experiment("Insurance Data Drift Monitoring")
    with mlflow.start_run():
        mlflow.log_artifact(drift_report_path)
        print("✅ Drift report logged to MLflow")

if __name__ == "__main__":
    detect_drift("params.yaml")
