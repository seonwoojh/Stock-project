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
noti_type = os.environ['NOTI_TYPE'] ## 어떤 타입의 알람을 받을 것인지 설정
user_condition = os.getenv('USER_CONDITION') ## 사용자가 지정한 목표 변수 EX) 등락률이 20% 이상 / 목표가가 30,000원 이하 ## 없을 경우 None으로 예외 처리

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
            ## 유저가 지정한 알림 타입에 따라서 하위 스트림 프로세서로 분기처리한다.
            match noti_type:

################################################### 상/하한가 알림 Stream processor ################################################################
                case 'price_limit': ## 상한 / 하한가 알림(1:상한, 4:하한)
                    if str(data.PRDY_VRSS_SIGN) in ["1.0", "4.0"]:
                        noti_data = {
                            "Stock Code": data.MKSC_SHRN_ISCD, ## 주식코드
                            "PRDY_VRSS_SIGN": "상한" if data.PRDY_VRSS_SIGN == 1 else "하한",  # 부호 여부
                            "STCK_PRPR": data.STCK_PRPR, ## 현재가
                            "PRDY_VRSS": data.PRDY_VRSS, ## 전일대비 상승 가격
                            "PRDY_CTRT": data.PRDY_CTRT ## 등락률
                        }
                        print(f"상/하한 데이터 발송 완료 {noti_data}")
                        yield noti_data ## Sink processor 알람 발송 토픽으로 전송한다.

                    else:
                        continue

################################################### 등락률 알림 Stream processor ################################################################
                case 'fluctuation':
                    value, condition = user_condition.split("|")
                    sign = ">" if condition in ["초과", "미만"] else ">="

                    ## 사용자가 지정한 값과 비교해 알림 데이터를 전송한다.
                    if eval(f"{abs(data.PRDY_CTRT)} {sign} {value}"):
                        noti_data = {
                            "Stock Code": data.MKSC_SHRN_ISCD, ## 주식코드
                            "PRDY_VRSS_SIGN": condition,
                            "STCK_PRPR": data.STCK_PRPR, ## 현재가
                            "PRDY_VRSS": data.PRDY_VRSS, ## 전일대비 상승 가격
                            "PRDY_CTRT": data.PRDY_CTRT ## 등락률
                        }
                        print(f"등락률 데이터 발송 완료 {noti_data}")
                        yield noti_data ## Sink processor 알람 발송 토픽으로 전송한다.

################################################### 목표가 알림 Stream processor ################################################################
                case 'goal': 
                    value, condition = user_condition.split("|")
                    condition_to_sign = {
                        "초과": ">",
                        "이상": ">=",
                        "미만": "<",
                        "이하": "<="
                    }
                    sign = condition_to_sign.get(condition)

                    ## 사용자가 지정한 값과 비교해 알림 데이터를 전송한다.
                    if eval(f"{data.STCK_PRPR} {sign} {value}"):
                        noti_data = {
                            "Stock Code": data.MKSC_SHRN_ISCD, ## 주식코드
                            "PRDY_VRSS_SIGN": condition,
                            "STCK_PRPR": data.STCK_PRPR, ## 현재가
                        }
                        print(f"목표가 데이터 발송 완료 {noti_data}")
                        yield noti_data ## Sink processor 알람 발송 토픽으로 전송한다.

################################################### 전일 대비 알림 Stream processor ################################################################
                case 'compared_previous': 
                    value, condition = user_condition.split("|")
                    sign = ">" if condition in ["초과", "미만"] else ">="

                    ## 사용자가 지정한 값과 비교해 알림 데이터를 전송한다.
                    if eval(f"{abs(data.PRDY_VRSS)} {sign} {value}"):
                        noti_data = {
                            "Stock Code": data.MKSC_SHRN_ISCD, ## 주식코드
                            "PRDY_VRSS_SIGN": condition,
                            "STCK_PRPR": data.STCK_PRPR, ## 현재가
                            "PRDY_VRSS": data.PRDY_VRSS, ## 전일대비 상승 가격
                            "PRDY_CTRT": data.PRDY_CTRT ## 등락률
                        }
                        print(f"전일대비 데이터 발송 완료 {noti_data}")
                        yield noti_data ## Sink processor 알람 발송 토픽으로 전송한다.

        except:
            print("조건에 맞지 않는 데이터")
            continue

if __name__ == '__main__':
    app.main()
