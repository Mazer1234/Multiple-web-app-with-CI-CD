pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
    containers:
    - name: node
      image: node:16-alpine
      command: ['cat']
      tty: true
      volumeMounts:
      - name: docker-sock
        mountPath: /var/run/docker.sock
    - name: docker
      image: docker:20.10
      command: ['cat']
      tty: true
      volumeMounts:
      - name: docker-sock
        mountPath: /var/run/docker.sock
    - name: kubectl
      image: bitnami/kubectl:latest
      command: ['cat']
      tty: true
    volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
            '''
        }
    }

    environment: {
        DOCKER_REGISTRY = "localhost:5000"
        KUBECONFIG = "/home/jenkins/.kube/config"
    }

    stages{
        stage('Checkout'){
            steps{
                git branch: 'master', url: 'https://github.com/Mazer1234/Multiple-web-app-with-CI-CD.git'
            }
        }

        stage('Test Backend'){
            steps{
                constainer('node'){
                    sh '''
                    cd backend
                    npm install || true
                    '''
                }
            }
        }

        stage('Build Frontend'){
            steps{
                container('node'){
                    sh '''
                    cd frontend
                    npm install
                    npm run build
                    '''
                }
            }
        }

        stage('Build Docker Images'){
            steps{
                container('docker'){
                    sh '''
                    docker build -t movie-backend:lates ./backend

                    docker build -t movie-frontend:latest ./frontend

                    minikube image load movie-backend:latest
                    minikube image load movie-frontend:latest
                    '''
                }
            }
        }

        stage('Deploy to kubernetes'){
            steps{
                container('kubectl'){
                    sh '''
                    kubectl apply -f k8s/redis/ --force
                    kubectl apply -f k8s/backend/ --force
                    kubectl apply -f k8s/frontend/ --force
                    kubectl apply -f k8s/ingress.yaml

                    kubectl port-forward service/backend-service 8000:8000
                    kubectl port-forward service/frontend-service 8081:80
                    '''
                }
            }
        }
    }
}