# 카프카 스트림을 활용한 사용자 맞춤 주식 알림 서비스

이 Helm 차트는 카프카 스트림을 기반으로 사용자가 설정한 조건에 맞는 주식 알림 서비스를 제공합니다. 사용자는 다양한 알림 타입을 설정하고, 주식 시장의 변동에 따라 실시간 알림을 받을 수 있습니다.

## 사용법

### 1. 프로듀서 및 컨슈머 활성화

프로듀서와 컨슈머는 서브 차트에 포함되어 있으며, 기본적으로 비활성화되어 있습니다. 이를 활성화하려면 `values.yaml` 파일에서 관련 항목을 **Enable**로 설정하세요.

### 2. 알림 서비스 설정

알림은 아래와 같은 다양한 타입으로 제공됩니다. 원하는 알림 타입을 설정하여 조건에 맞는 알림을 받을 수 있습니다.

- **상/하한가 알림** (`price_limit`)
- **등락률 알림** (`fluctuation`)
- **목표가 알림** (`goal`)
- **전일대비 알림** (`compared_previous`)

#### 알림 설정 방법

1. **알림 타입 선택**: 위의 알림 타입 중 하나를 선택하고, `values.yaml` 파일에서 `notiType` 항목에 해당 타입을 입력하세요.
2. **조건 설정**: 원하는 조건을 선택하여 `values.yaml` 파일의 `userCondition` 항목에 입력하세요.
3. **Helm 차트 설치**: 설정이 완료되면 Helm 차트를 설치하여 서비스를 실행합니다.

#### 예시

예를 들어, **목표가 알림**을 설정하고, 삼성전자의 주가가 53,200원 미만일 경우 알림을 받으려면:

```yaml
notiType: goal
userCondition: "53200|미만"
```

### 3. 프로듀서 설정

1. **API 키 발급**: 한국투자증권 Open API 홈페이지에서 가입 후 API 키를 발급받습니다.
2. `values.yaml` 파일에서 **producer 항목을 Enable**하고, 발급받은 API 키와 원하는 종목 코드를 입력하세요.

### 4. 컨슈머 설정

1. **InfluxDB 토큰 발급**: InfluxDB API 키를 발급 받습니다.
2. `values.yaml` 파일에서 **consumer 항목을 Enable**하고, DB URL과 발급 받은 API 키와 원하는 종목 코드를 입력하세요.

## 차트 구조
```
├── Chart.yaml
├── README.md
├── charts
│   ├── consumer
│   │   ├── Chart.yaml
│   │   ├── templates
│   │   │   ├── configMap.yaml
│   │   │   ├── deployment.yaml
│   │   │   └── secret.yaml
│   │   └── values.yaml
│   └── producer
│       ├── Chart.yaml
│       ├── templates
│       │   ├── configMap.yaml
│       │   ├── deployment.yaml
│       │   └── secret.yaml
│       └── values.yaml
├── templates
│   ├── NOTES.txt
│   ├── _helpers.tpl
│   ├── configMap.yaml
│   └── deployment.yaml
└── values.yaml
```