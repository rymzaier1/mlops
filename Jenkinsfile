
// Jenkinsfile : le pipeline est décrit dans un fichier versionné
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Installer') {
            steps {
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install -r requirements.txt -r requirements-dev.txt'
            }
        }

        stage('Entrainer') {
            steps {
                sh 'venv/bin/python entrainer_ci.py'
            }
        }

        stage('Tests') {
            steps {
                sh 'venv/bin/pytest test_ci.py -v --junitxml=rapport.xml'
            }
            post {
                always {
                    junit 'rapport.xml'
                }
            }
        }

        stage('Image Docker') {
            steps {
                sh 'docker build -t churn-api:$BUILD_NUMBER .'
            }
        }

        stage('Publier sur GHCR') {
            when {
                branch 'develop'
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-pat',
                    usernameVariable: 'GH_USER',
                    passwordVariable: 'GH_TOKEN'
                )]) {
                    sh '''
                    echo "$GH_TOKEN" | docker login ghcr.io -u "$GH_USER" --password-stdin
                    IMAGE=ghcr.io/$(echo "$GH_USER" | tr A-Z a-z)/churn-api:jenkins-$BUILD_NUMBER
                    docker tag churn-api:$BUILD_NUMBER $IMAGE
                    docker push $IMAGE
                    '''
                }
            }
            post {
                always {
                    sh 'docker logout ghcr.io'
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline termine avec succes"
        }
        failure {
            echo "Pipeline en echec : ouvrez le journal de l'etape en rouge"
        }
    }
}
