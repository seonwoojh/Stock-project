from generate_key import get_approval
from subscribe_data import stockhoka, stockspurchase
import websockets
import asyncio
import datetime
import json
import os

key = os.environ['APP_KEY']
secret = os.environ['APP_SECRET']
stock_code = os.environ['STOCK_CODE']

async def connect():
    ## API 키와 URL, 주식 코드를 입력한다.
    g_appkey = key
    g_appsecret = secret
    url = 'ws://ops.koreainvestment.com:21000'

    ## Websocket 키를 생성한다.
    g_approval_key = get_approval(g_appkey, g_appsceret)

    ## 가져올 데이터를 정의한다.
    ## H0STASP0 실시간 호가 /// H0STCNT0 실시간 체결가
    code_list = [['1','H0STASP0', stock_code],['1','H0STCNT0', stock_code]]
    senddata_list = []

    ## API 서버에 보낼 데이터 리스트를 생성한다.(TR_ID, 데이터 타입, 주식 코드)
    for i,j,k in code_list:
        temp = '{"header":{"approval_key": "%s","custtype":"P","tr_type":"%s","content-type":"utf-8"},"body":{"input":{"tr_id":"%s","tr_key":"%s"}}}'%(g_approval_key,i,j,k)
        senddata_list.append(temp)

    ## Websocket을 생성한다.
    async with websockets.connect(url, ping_interval=None) as websocket:

        ## 생성된 WebSocket에 데이터 리스트를 보내 증권 데이터를 호출한다.
        for senddata in senddata_list:
            await websocket.send(senddata)
            await asyncio.sleep(0.5)
        
        while True:
            ### API 서버와 Websocket을 통해 데이터를 받아온다.
            print("Recev Start : ",datetime.datetime.now())
            data = await websocket.recv()
            if data[0] == '0' or data[0] == '1':  
                trid = jsonObject["header"]["tr_id"]

                if data[0] == '0':
                    recvstr = data.split('|') 
                    trid0 = recvstr[1]
                    if trid0 == "H0STASP0":  
                        hoka_data = stockhoka(recvstr[3], 'H0STASP0')

                        print(hoka_data)

                        yield hoka_data

                    elif trid0 == "H0STCNT0":  
                        data_cnt = int(recvstr[2])  
                        purchase_data = stockspurchase(data_cnt, recvstr[3], 'H0STCNT0')

                        print(hoka_data)

                        yield purchase_data
            
            ## 데이터가 없는 경우
            else:
                jsonObject = json.loads(data)
                trid = jsonObject["header"]["tr_id"]

                if trid != "PINGPONG":
                    rt_cd = jsonObject["body"]["rt_cd"]
                    if rt_cd == '1':    
                        print("### ERROR RETURN CODE [ %s ] MSG [ %s ]" % (rt_cd, jsonObject["body"]["msg1"]))
                        break
                    elif rt_cd == '0':  
                        print("### RETURN CODE [ %s ] MSG [ %s ]" % (rt_cd, jsonObject["body"]["msg1"]))
                        if trid == "H0STCNI0" or trid == "H0STCNI9":
                            aes_key = jsonObject["body"]["output"]["key"]
                            aes_iv = jsonObject["body"]["output"]["iv"]
                            print("### TRID [%s] KEY[%s] IV[%s]" % (trid, aes_key, aes_iv))

                elif trid == "PINGPONG":
                    print("### RECV [PINGPONG] [%s]" % (data))
                    await websocket.pong(data)
                    print("### SEND [PINGPONG] [%s]" % (data))
