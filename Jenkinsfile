// 애플리케이션 이름을 초기화한다.
def APP_NAME = "${name.split("/")[2]}"

pipeline {
    // 기본 환경 변수를 설정한다.
    environment {
        TIME_ZONE = 'Asia/Seoul'
        PROFILE = 'local'
        REPOSITORY_URL = 'https://github.com/seonwoojh/Stock-project.git'
        IMAGE_TAG = 'latest'     
    }
    
    agent {
        // 이미지 빌드와 배포를 위한 jenkins agent pod를 생성한다.
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
        // 이미지 빌드와 배포에 사용할 환경변수를 설정하고 소스코드 변경 내역이 아닌 경우 스테이지를 종료한다.
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

        // 레포지토리의 코드를 fetch 하고 배포할 브랜치로 checkout 한다.
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

        // 이미지를 빌드하고 ECR에 업로드한다.
        stage('Build Image') {
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

        // 템플릿을 활용해 DEV 브랜치의 파드를 배포한다. 추후 테스트 완료 후 Helm Chart로 패키징한다.
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