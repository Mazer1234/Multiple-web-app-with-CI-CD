pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Mazer1234/Multiple-web-app-with-CI-CD.git'
            }
        }

        stage('Install Tools') {
            steps {
                sh '''
                    echo "=== Installing necessary tools ==="
                    
                    # Update package list
                    apt-get update
                    
                    # Install Node.js and npm
                    apt-get install -y nodejs npm
                    
                    # Install kubectl
                    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
                    rm kubectl
                    
                    # Check installed tools
                    echo "Node.js version: $(node --version)"
                    echo "npm version: $(npm --version)"
                    echo "kubectl version: $(kubectl version --client --short)"
                '''
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

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    echo "=== Deploying to Kubernetes ==="
                    kubectl apply -f k8s/ --recursive --force
                    kubectl get pods,services,ingress
                '''
            }
        }
    }

    post {
        always {
            echo "=== Pipeline completed ==="
            sh 'kubectl get pods || echo "kubectl not available"'
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}