pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'
        DOCKER_IMAGE = 'cithit/allame'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/miamioh-allame/lab-5-1.git'
        KUBECONFIG = credentials('allame-225')
    }

    stages {
        stage('Code Checkout') {
            steps {
                cleanWs()
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
            }
        }

        stage('Lint HTML') {
            steps {
                sh 'npm install htmlhint --save-dev'
                sh 'npx htmlhint *.html'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "-f Dockerfile.build .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy to Dev Environment') {
            steps {
                script {
                    sh 'kubectl delete --all deployments --namespace=default || true'
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }

stage('Init DB Schema') {
    steps {
        script {
            sleep 10
            def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
            sh "kubectl wait pod/${appPod} --for=condition=ready --timeout=60s"
            sh "kubectl exec ${appPod} -c flask -- sh -c 'python3 -c \"from main import init_db; init_db()\"'"
        }
    }
}

        
        stage('Generate Test Data') {
            steps {
                script {
                    sleep 10
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "kubectl wait pod/${appPod} --for=condition=ready --timeout=60s"
                    sh "kubectl exec ${appPod} -c flask -- python3 data-gen.py"
                }
            }
        }



        stage("Run Acceptance Tests") {
            steps {
                script {
                    sh 'docker stop qa-tests || true'
                    sh 'docker rm qa-tests || true'
                    sh 'docker build -t qa-tests -f Dockerfile.test .'
                    sh 'docker run -e TARGET_URL=http://10.48.10.127 qa-tests'
                }
            }
        }

        stage('Remove Test Data') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "kubectl wait pod/${appPod} --for=condition=ready --timeout=60s"
                    sh "kubectl exec ${appPod} -c flask -- python3 data-clear.py"
                }
            }
        }

        stage('Run Security Checks') {
            steps {
                sh 'docker pull public.ecr.aws/portswigger/dastardly:latest'
                sh '''
                    docker run --user $(id -u) -v ${WORKSPACE}:${WORKSPACE}:rw \
                    -e BURP_START_URL=http://10.48.10.127 \
                    -e BURP_REPORT_FILE_PATH=${WORKSPACE}/dastardly-report.xml \
                    public.ecr.aws/portswigger/dastardly:latest
                '''
            }
        }

        stage('Deploy to Prod Environment') {
            steps {
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-prod.yaml"
                    sh "kubectl apply -f deployment-prod.yaml"
                }
            }
        }

        stage('Check Kubernetes Cluster') {
            steps {
                sh 'kubectl get all'
            }
        }
    }

    post {
        success {
            slackSend(color: "good", message: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
        }
        unstable {
            slackSend(color: "warning", message: "⚠️ UNSTABLE: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
        }
        failure {
            slackSend(color: "danger", message: "❌ FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
        }
    }
}

