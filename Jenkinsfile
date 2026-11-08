
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Week 12 Registration project checked out from GitHub'
            }
        }

        stage('Run Selenium Tests with pytest') {
            steps {
                echo 'Running Selenium Tests using pytest'

                bat 'pip install -r requirements.txt'

                bat 'start /B python app.py'

                bat 'ping 127.0.0.1 -n 5 > nul'

                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t w12-registration:v1 .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
               
                   bat 'docker login -u nisha1310 -p <Gsnisha2023>'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                bat 'docker tag w12-registration:v1 nisha1310/simple-demo:w12-registration'
                bat 'docker push nisha1310/simple-demo:w12-registration'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
