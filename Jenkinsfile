
pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Flask Application and Selenium Tests') {
            steps {
                sh '''
                    nohup python3 app.py > app.log 2>&1 &
                    echo $! > app.pid

                    for i in $(seq 1 30); do
                        if curl -fsS http://127.0.0.1:5000/ > /dev/null; then
                            echo "Flask application is ready"
                            break
                        fi
                        sleep 2
                    done

                    curl -fsS http://127.0.0.1:5000/ > /dev/null
                    python3 -m pytest -v tests/test_register.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t seleniumdemo:v1 .'
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'nisha1310',
                    passwordVariable: 'Gsnisha2023'
                )]) {
                    sh '''
                        echo "$Gsnisha2023" | docker login \
                            -u "$nisha1310" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'nisha1310',
                    passwordVariable: 'Gsnisha2023'
                )]) {
                    sh '''
                        docker tag seleniumdemo:v1 \
                            "$DH_USER/simple-demo:seleniumimage1"

                        docker push "$DH_USER/simple-demo:seleniumimage1"
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml --validate=false'
                sh 'kubectl apply -f service.yaml'
                sh 'kubectl rollout status deployment --timeout=120s'
            }
        }
    }

    post {
        always {
            sh '''
                if [ -f app.pid ]; then
                    kill "$(cat app.pid)" 2>/dev/null || true
                    rm -f app.pid
                fi
            '''
        }

        success {
            echo 'W12 pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
