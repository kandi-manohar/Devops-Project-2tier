pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/kandi-manohar/Devops-Project-2tier.git'
            }
        }

        stage('Create .env') {
            steps {
                withCredentials([string(credentialsId: 'flask-env', variable: 'ENV_FILE')]) {
                    sh '''
                    echo "$ENV_FILE" > .env
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'sudo docker build -t flask-app .'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                sudo docker compose down || true
                sudo docker compose up -d --build
                '''
            }
        }
    }
}
