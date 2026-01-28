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

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                docker compose down || true
                docker compose up -d --build
                '''
            }
        }
    }
}
