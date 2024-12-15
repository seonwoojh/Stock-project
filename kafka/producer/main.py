from confluent_kafka import Producer
import asyncio
import connection
import json
import os

## Init ENV for Container
kafka_server = os.environ['KAFKA_SERVER']
hoka_topic = os.environ['HOKA_TOPIC']
conclusion_topic = os.environ['CONCLUSION_TOPIC']

## Kafka Producer를 생성한다.
producer_config = {
    'bootstrap.servers': kafka_server,
    'acks': '1'
}

producer = Producer(producer_config)

## 한국투자증권 API 데이터를 Kafka 브로커에 전송한다.
async def handle_data():
    try:
        ## connection.connect()에서 비동기적으로 데이터를 가져온다.
        async for data in connection.connect():
            ## 데이터를 Kafka에 전송
            if 'OVTM_TOTAL_BIDP_RSQN' in data:  # 호가 데이터
                producer.produce(f'{hoka_topic}', key='H0STASP0', value=json.dumps(data))
                print(f"호가 데이터 전송: {data}")
            elif 'STCK_OPRC' in data:  # 실시간 체결가 데이터
                producer.produce(f'{conclusion_topic}', key='H0STCNT0', value=json.dumps(data))
                print(f"체결가 데이터 전송: {data}")

            producer.flush()

    except Exception as e:
        print('Exception Raised!')
        print(e)

## 메인 이벤트 루프 실행
asyncio.run(handle_data())