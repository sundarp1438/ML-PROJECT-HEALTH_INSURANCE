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
        stage('Python Installation') {
            steps {
                sh 'sudo apt install python3 -y'
                sh 'sudo apt install python3-pip -y'
                sh 'sudo apt install python3-venv -y'
            }
        }
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh 'bash -c "source venv/bin/activate && pip install --upgrade pip"'
                sh 'bash -c "source venv/bin/activate && pip install -r requirements.txt"' 
                
            }
        }
        stage('Initialize DVC') {
            steps {
                sh '. venv/bin/activate && dvc init'
                sh '. venv/bin/activate && dvc add data'
                sh '. venv/bin/activate && git add .dvc data.dvc'
                sh '. venv/bin/activate && git commit -m "Initialize DVC and track data"'
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
                sh '. venv/bin/activate && python mlflow_evaluate.py --config=params.yaml'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'DockerHubPass']) {
                    sh 'docker tag $DOCKER_IMAGE sundarp1985/$DOCKER_IMAGE:latest'
                    sh 'docker push sundarp1985/$DOCKER_IMAGE:latest'
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
