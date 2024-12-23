from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import smtplib
import re 
import json
import base64
import datet

def lambda_handler(event, context):
    ## smpt 서버와 연결을 설정한다.
    gmail_smtp = ""
    gmail_port = 465
    smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
    
    ## 로그인 정보를 설정한다.
    my_account = ""
    my_password = ""
    smtp.login(my_account, my_password)
    
    ## 이벤트 중에서 토픽의 메시지 정보만 가져온다.
    if event:
        message = json.loads(base64.b64decode(event["records"]["topic_name-0"][0]["value"]).replace(b'\n', b'').replace(b'\t', b''))

    to_mail = message["address"]
    if message["Stock Code"] == 5930.0:
        stock = "삼성전자"

    ## 메일 기본 정보를 설정한다.(거래량 추가 여부 확인)
    noti_time = datetime.now().strftime('%H시%M분')
    msg = MIMEMultipart()
    msg["Subject"] = f"[등락률 알림] {noti_time} - {stock}"
    msg["From"] = my_account
    msg["To"] = to_mail

    ## 메시지 발송 템플릿을 설정한다.
    content = f"""
    {noti_time}
    
    종목 {stock} 이/가 {message["PRDY_CTRT"]}% {message["PRDY_VRSS_SIGN"]} 했습니다.

    (현재가 {message["Price"]}, 전일대비 {message["PRDY_VRSS"]})
    """

    content_part = MIMEText(content, "plain", "utf-8")
    msg.attach(content_part)

    ## 유효성 검사를 진행한 후 메일을 발송한다.
    reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"
    if re.match(reg, to_mail):
        smtp.sendmail(my_account, to_mail, msg.as_string())
        print("정상적으로 메일이 발송되었습니다.")
    else:
        print("받으실 메일 주소를 정확히 입력하십시오.")
    
    smtp.quit()