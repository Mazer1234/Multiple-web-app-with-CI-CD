pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "localhost:5000"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Mazer1234/Multiple-web-app-with-CI-CD.git'
            }
        }

        stage('Build Frontend') {
            steps {
                sh '''
                cd frontend
                npm install
                npm run build
                '''
            }
        }

        stage('Build Backend') {
            steps {
                sh '''
                cd backend
                npm install || true
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                docker build -t movie-backend:latest ./backend
                docker build -t movie-frontend:latest ./frontend
                minikube image load movie-backend:latest
                minikube image load movie-frontend:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f k8s/ --recursive --force
                kubectl get pods,services,ingress
                '''
            }
        }
    }

    post {
        always {
            echo "=== Pipeline completed ==="
            sh 'kubectl get pods'
        }
    }
}