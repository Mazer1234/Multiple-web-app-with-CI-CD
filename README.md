# 🎬 Movie Database - Full Stack Kubernetes Application

Полнофункциональное веб-приложение для управления базой данных фильмов, развернутое в Kubernetes.

## 🏗️ Архитектура


## 🛠️ Технологический стек

### Frontend
- **React** - пользовательский интерфейс
- **Axios** - HTTP клиент для API
- **Nginx** - раздача статики и прокси

### Backend  
- **FastAPI** - современный Python фреймворк
- **Pydantic** - валидация данных
- **Redis** - кэширование и метрики
- **PostgreSQL** - база данных

### Infrastructure
- **Docker** - контейнеризация
- **Kubernetes** - оркестрация
- **Minikube** - локальный кластер
- **Ingress Nginx** - маршрутизация трафика

## 🚀 Быстрый старт

### Предварительные требования
- Docker
- Kubernetes (Minikube)
- kubectl

### Запустите Minikube

bash
minikube start
minikube addons enable ingress
Соберите и загрузите образы

### Соберите образы и добавьте их в minikube
bash
# Backend
docker build -t movie-backend:latest ./backend
minikube image load movie-backend:latest

# Frontend
docker build -t movie-frontend:latest ./frontend  
minikube image load movie-frontend:latest
Разверните в Kubernetes

### Запустите скрипты
bash
kubectl apply -f k8s/redis/
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/ingress.yaml

### Доступ к приложению
# Терминал 1 - фронтенд
kubectl port-forward service/frontend-service 8080:80

# Терминал 2 - бэкенд (для API)
kubectl port-forward service/backend-service 8000:8000

📁 Структура проекта
text
devops-project/
├── backend/                 # FastAPI приложение
│   ├── app/
│   │   ├── main.py         # Основное приложение
│   │   └── models.py       # Модели Pydantic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React приложение
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── services/       # API клиент
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
└── k8s/                    # Kubernetes манифесты
    ├── backend/
    │   ├── deployment.yaml
    │   └── service.yaml
    ├── frontend/
    │   ├── deployment.yaml  
    │   └── service.yaml
    ├── redis/
    │   ├── deployment.yaml
    │   └── service.yaml
    └── ingress.yaml

🎯 Функциональность
Frontend
📋 Просмотр списка фильмов

🔍 Поиск и фильтрация по жанру, году

⭐ Система рейтингов и отзывов

📊 Статистика базы данных

Backend
REST API с документацией Swagger

Валидация данных через Pydantic

Кэширование через Redis

Health checks для Kubernetes
