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
                script {
                    docker.image('node:16-alpine').inside {
                        sh '''
                            cd frontend
                            npm install
                            npm run build
                        '''
                    }
                }
            }
        }

        stage('Build Backend') {
            steps {
                script {
                    docker.image('node:16-alpine').inside {
                        sh '''
                            cd backend
                            npm install || true
                        '''
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Сборка frontend образа
                    sh 'docker build -t movie-frontend:latest ./frontend'
                    // Сборка backend образа  
                    sh 'docker build -t movie-backend:latest ./backend'
                    // Загрузка в Minikube
                    sh 'minikube image load movie-frontend:latest'
                    sh 'minikube image load movie-backend:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh 'kubectl apply -f k8s/ --recursive --force'
                    sh 'kubectl get pods,services,ingress'
                }
            }
        }
    }

    post {
        always {
            echo "=== Pipeline completed ==="
            script {
                sh 'kubectl get pods || true'
            }
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}