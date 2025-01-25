# Real-time Data Processing Architecture

> **EKS와 Kafka, Jenkins를 활용한 실시간 데이터 처리 아키텍처와 주식 알림 서비스**

- 투자 입문자가 간편하게 원하는 종목의 알림을 받아볼 수 있도록 프로젝트를 진행했습니다.
- 실시간 주가 API 데이터를 **스트림 서브 토폴로지를 통해 처리**하여 **다양한 타입을 알림**을 제공합니다.
- **Terraform 프로비저닝**, **Kafka Application 개발**, **CI/CD Pipeline**, **Helm 차트 패키징**을 담당했습니다.

<br/>

[🙋‍ Helm Chart 확인하기](https://github.com/seonwoojh/Stock-project/tree/main/helm-chart)

## 1.1. 사용자 제공 서비스 예시

> **현재가, 등락률, 매도/매수 호가, 일봉 차트 등 종목 관련 정보를 확인할 수 있습니다.**

![대시보드](https://github.com/seonwoojh/img-source/blob/main/img/image.png?raw=true)

- 주식 관련 데이터는 InfluxDB에 저장되며, Grafana Dashboard를 통해 시각화되어 제공됩니다.
- 이를 통해 주식 알림 뿐만 아니라 현재 관심 종목의 정보도 손쉽게 확인 가능합니다.
- 알림 메시지는 종목코드, 상승 하락 여부, 현재가, 등락률, 전일대비 상승 가격등이 포함되어있습니다.

<br/>

## 1.2. 전체 프로젝트 아키텍처

> **모든 AWS 리소스는 Terraform으로 프로비저닝, 관리됩니다.**

![전체 프로젝트 구조](https://github.com/seonwoojh/img-source/blob/main/img/stock-%EC%A0%84%EC%B2%B4%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EA%B5%AC%EC%A1%B0.drawio.png?raw=true)

- AWS EKS와 EC2에 배포되며 Kafka, InfluxDB, Grafana, Jenkins, AWS Lambda, ECR을 사용했습니다.
- Kafka Cluster를 EKS에 포함하지 않고 EC2에 배포하여 **한 달 운영 비용을 약 77.62달러 절감**했습니다.
- ECR는 프라이빗 레포지토리로 운영되며, 이미지들은 **라이프 사이클에 의해 관리**됩니다.
- 보다 간결한 액세스 관리를 위해 SSM을 사용하고, **IAM 계정별로 접근 기록이 로깅**됩니다.

<br/>

## 1.3. 서비스 플로우

> **상/하한가, 등락률, 목표가, 전일 대비 알림 중 한 가지를 선택해 제공합니다.**

![서비스 플로우](https://github.com/seonwoojh/img-source/blob/main/img/stock-%EC%84%9C%EB%B9%84%EC%8A%A4%20%ED%94%8C%EB%A1%9C%EC%9A%B0.drawio.png?raw=true)

- 사용자는 원하는 종목과 알림 조건값을 설정해 엔지니어에게 전달합니다.
- 엔지니어는 사용자의 설정 값에 맞게 애플리케이션을 배포합니다.
- 종목 관련 대시보드를 통해 현황을 확인하고 조건에 맞는 알림을 메일로 발송 받습니다.

<br/>

## 1.4. 기능 플로우

> **프로젝트의 기능 플로우는 아래와 같습니다.**

![기능 플로우.drawio.png](https://github.com/seonwoojh/img-source/blob/main/img/stock-%EA%B8%B0%EB%8A%A5%20%ED%94%8C%EB%A1%9C%EC%9A%B0.drawio.png?raw=true)

- Helm 차트는 Main Chart(Streams)와 API 호출 및 적재를 담당하는 SubChart로 구성되어 있습니다.
- 실시간 데이터를 프로세싱해 별도 토픽에 저장하고 AWS Lambda를 통해 알림을 발송합니다.

<br/>

## 1.5. CI/CD Pipeline

> **Main / develop Branch는 각각 다른 프로젝트로 관리됩니다.**

![CI_CD 파이프라인](https://github.com/seonwoojh/img-source/blob/main/img/stock-CI_CD%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8.drawio.png?raw=true)

1. **SCM:** Git으로 애플리케이션 코드를 관리하며 Gitflow 전략을 사용합니다.

<br/>

2. **Develop Branch:**
    - **Prepare**
        - Set Environment
            - 브랜치별 Github Webhook의 파라미터를 이미지 빌드와 배포에 사용할 환경변수로 설정합니다.
        - Verify Environment
            - 환경변수를 검증하는 단계로 소스코드 변경 내역이 아닌경우 스테이지를 종료합니다.
    - **Checkout**
        - Git Repository의 코드를 fetch 하고 배포할 브랜치로 checkout 합니다.
    - **Build Image**
        - Kaniko로 Docker Image를 생성하여 AWS ECR에 Push 합니다.
    - **Deploy**
        - manifest 템플릿을 통해 애플리케이션을 배포합니다.
            
            관리자는 여러 테스트를 진행하고 정리가 되면 Helm chart로 패키징하여 관리합니다.
            

<br/>


3. **Main Branch:**
    - **Prepare**
        - Set Environment & Verify Environment
            - Develop 브랜치 파이프라인과 동일한 환경변수 설정 및 검증 과정을 거칩니다.
    - **Deploy**
        - Helm을 사용하여 애플리케이션을 배포합니다.


<br/>

## 1.6. Kafka Streams Topology

> **Python Faust-Streaming을 활용해 토폴로지를 구현했습니다.**

![서비스 플로우-스트림 토폴로지.drawio (5).png](https://github.com/seonwoojh/img-source/blob/main/img/stock-%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80.drawio.png?raw=true)

- 4개의 서브 토폴로지로 구성되며, 토픽을 읽어 1차 필터링한 후 알림 타입별 스트림 프로세서로 포워딩합니다.
- 사용자 조건과 알림 발송 여부를 확인 후 데이터를 토픽에 적재하고, 구독 중인 컨슈머가 메시지를 발송합니다.
- 레코드의 중복 방지를 위해 알림 발송 여부를 **1시간 간격의 Tumbling window** changelog에 저장합니다.
