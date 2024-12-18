from Schema import realtime_purchase
from datetime import datetime, timedelta
import pytz
import faust
import os

## Init ENV for Container
kafka_server = os.environ['KAFKA_SERVER']
source_topic = os.environ['SOURCE_TOPIC']
destination_topic = os.environ['DESTINATION_TOPIC']
stock_code = os.environ['STOCK_CODE']

## 어떤 알림 받을건지 변수 추가 예정

# KST 시간대 설정
KST = pytz.timezone('Asia/Seoul')

## Faust 앱을 정의한다.
app = faust.App('stock_conclusion_app', broker=f'kafka://{kafka_server}', serializer='json', value_serializer='json',key_type=str, value_type=realtime_purchase)

## 데이터를 불러올 원본 토픽을 지정한다.
stock_conclusion_topic = app.topic(
    f'{source_topic}',
    key_type=str,
    value_type=realtime_purchase
)

## 조건에 맞는 데이터를 저장할(알람 발송용) 토픽을 지정한다.
new_topic = app.topic(f'{destination_topic}', key_type=str, value_type=dict)

@app.agent(stock_conclusion_topic, sink=[new_topic])
async def stock_fluctuation_rate(stream):
    ## 정상 거래중이면서 주식 코드가 사용자가 설정한 종목인 경우를 필터링 한다.
    async for data in stream.filter(lambda x: str(x.MKSC_SHRN_ISCD) == stock_code and x.TRHT_YN == "N"):
        try:
            ### 등락률 알림
            match data.PRDY_VRSS_SIGN:
                
                ## 상한
                case 1:
                    alert_data = {
                        "Stock Code": data.MKSC_SHRN_ISCD, ## 주식코드
                        "PRDY_VRSS_SIGN": "상한", ## 부호 여부
                        "STCK_PRPR": data.PRDY_VRSS, ## 현재가
                        "PRDY_VRSS": data.PRDY_VRSS, ## 전일대비 상승 가격
                        "PRDY_CTRT": data.PRDY_CTRT ## 등락률
                    }
                    print(alert_data)
                    yield alert_data
                
                ## 상승
                case 2:
                    if data.PRDY_CTRT >= 0.5:
                        alert_data = {
                            "Stock Code": data.MKSC_SHRN_ISCD, ## 주식코드
                            "PRDY_VRSS_SIGN": "상승", ## 부호 여부
                            "STCK_PRPR": data.PRDY_VRSS, ## 현재가
                            "PRDY_VRSS": data.PRDY_VRSS, ## 전일대비 상승한 가격
                            "PRDY_CTRT": data.PRDY_CTRT ## 등락률
                        }
                        print(alert_data)
                        yield alert_data

                ## 보합
                case 3:
                    continue

                ## 하한
                case 4:
                    alert_data = {
                        "Stock Code": data.MKSC_SHRN_ISCD, ## 주식코드
                        "PRDY_VRSS_SIGN": "하한", ## 부호 여부
                        "STCK_PRPR": data.PRDY_VRSS, ## 현재가
                        "PRDY_VRSS": data.PRDY_VRSS, ## 전일대비 상승 가격
                        "PRDY_CTRT": data.PRDY_CTRT ## 등락률
                    }
                    print(alert_data)
                    yield alert_data

                ## 하락
                case 5:
                    if data.PRDY_CTRT >= 0.5:
                        alert_data = {
                            "Stock Code": data.MKSC_SHRN_ISCD, ## 주식코드
                            "PRDY_VRSS_SIGN": "하락", ## 부호 여부
                            "STCK_PRPR": data.PRDY_VRSS, ## 현재가
                            "PRDY_VRSS": data.PRDY_VRSS, ## 전일대비 상승한 가격
                            "PRDY_CTRT": data.PRDY_CTRT ## 등락률
                        }
                        print(alert_data)
                        yield alert_data
        except:
            print("조건에 맞지 않는 데이터")
            continue

if __name__ == '__main__':
    app.main()
