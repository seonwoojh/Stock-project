def APP_NAME = "${name.split("/")[2]}"

pipeline {
    environment {
        TIME_ZONE = 'Asia/Seoul'
        PROFILE = 'local'
        REPOSITORY_URL = 'https://github.com/seonwoojh/Stock-project.git'
        IMAGE_TAG = 'latest'     
    }
    
    agent {
        kubernetes {
            defaultContainer 'kaniko'
            yaml """
            apiVersion: v1
            kind: Pod
            metadata:
              name: jenkins-agent
              labels:
                app: kaniko-builder
            spec:
              containers:
              - name: kubectl
                image: gcr.io/cloud-builders/kubectl
                command: ['cat']
                tty: true

              - name: kaniko
                image: gcr.io/kaniko-project/executor:debug
                command: ['sleep']
                args: ['infinity']
                volumeMounts:
                - name: kaniko-credentials
                  mountPath: /kaniko/.docker
              volumes:
              - name: kaniko-credentials
                secret:
                  secretName: stock-${APP_NAME}
                  items:
                  - key: .dockerconfigjson
                    path: config.json
"""
        }
    }
    stages{
        stage('Prepare') {
            steps {
                
                echo 'Set Environment'
                script{
                    env.IMAGE_NAME = "${name.split("/")[2]}"
                    env.CONTEXT = "${name.split('/')[0..-2].join('/')}"
                    env.ECR_PATH = "${ecr_number}.dkr.ecr.ap-northeast-2.amazonaws.com/stock/${IMAGE_NAME}"
                }
                
                echo 'Verify Environment'
                script{
                    if (!env.CONTEXT.contains('src')) {
                        error('Environment Variable Validation Failed: Changes must be in the src directory')
                    }
                }
            }
            post {
                success {
                    echo 'success init in pipeline'
                }
                failure {
                    error 'fail init in pipeline' // exit pipeline
                }
            }
        }

        stage('Checkout') {
            steps {
                git branch: "${branch.split("/")[2]}",
                url : "$REPOSITORY_URL";
                
                sh "ls -al"
            }
            post {
                success {
                    echo 'success Checkout Project'
                }
                failure {
                    echo 'fail Checkout Project'
                }
            }
        }

        stage('Build and Tag Docker Image') {
            steps {
                container('kaniko') {
                    sh '''executor \
                    --verbosity debug \
                    --context=${CONTEXT} \
                    --dockerfile=Dockerfile \
                    --cache=true \
                    --cleanup \
                    --destination=${ECR_PATH}:${IMAGE_TAG}
                    '''
                }
            }
            post {
                success {
                    echo 'success dockerizing project'
                }
                failure {
                    error 'fail dockerizing project' // exit pipeline
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    withKubeConfig([credentialsId: 'kube', serverUrl: 'https://kubernetes.default', namespace: 'stock']) {
                        container('kubectl') {
                            sh "sed -i 's/xxxx.dkr.ecr.ap-northeast-2.amazonaws.com\\/stock\\/xxxx:latest/${ecr_number}.dkr.ecr.ap-northeast-2.amazonaws.com\\/stock\\/${IMAGE_NAME}:latest/g' manifest-dev/stock/${IMAGE_NAME}-deployment.yaml"
                            sh 'kubectl apply -f manifest-dev/stock/${IMAGE_NAME}-deployment.yaml'
                        }
                    }
                }
            }
            post {
                success { 
                    echo 'Deploy success'
                }
                failure {
                     echo 'Deploy fail'
                }
            }
        }
    }
}