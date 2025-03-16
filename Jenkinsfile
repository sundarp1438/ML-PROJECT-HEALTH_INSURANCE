pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "insurance-api"
        MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
    }
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Setup Environment') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Run DVC Pipeline') {
            steps {
                sh '. venv/bin/activate && dvc repro'
            }
        }
        stage('Track Data Loading in MLflow') {
            steps {
                sh '. venv/bin/activate && python data_load.py --config=params.yaml'
            }
        }
        stage('Track Featurization in MLflow') {
            steps {
                sh '. venv/bin/activate && python featurize.py --config=params.yaml'
            }
        }
        stage('Track Data Splitting in MLflow') {
            steps {
                sh '. venv/bin/activate && python data_split.py --config=params.yaml'
            }
        }
        stage('Track Model Training in MLflow') {
            steps {
                sh '. venv/bin/activate && python train.py --config=params.yaml'
            }
        }
        stage('Track Model Evaluation in MLflow') {
            steps {
                sh '. venv/bin/activate && python mlflow_insurance.py --config=params.yaml'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials']) {
                    sh 'docker tag $DOCKER_IMAGE yourdockerhubusername/$DOCKER_IMAGE:latest'
                    sh 'docker push yourdockerhubusername/$DOCKER_IMAGE:latest'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
            }
        }
    }
}
