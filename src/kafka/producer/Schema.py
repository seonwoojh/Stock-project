from dataclasses import dataclass, asdict
import faust

# realtime_hoka 데이터 클래스 정의1123
@dataclass
class realtime_hoka(faust.Record, serializer='json'):
    MKSC_SHRN_ISCD: str ## 유가증권 단축 종목 코드
    HOUR_CLS_CODE: str          ## 시간 구분코드
    ASKP1: float                  ## 매도호가 1
    ASKP2: float                  ## 매도호가 2
    ASKP3: float                  ## 매도호가 3
    ASKP4: float                  ## 매도호가 4
    ASKP5: float                  ## 매도호가 5
    ASKP6: float                  ## 매도호가 6
    ASKP7: float                  ## 매도호가 7
    ASKP8: float                  ## 매도호가 8
    ASKP9: float                  ## 매도호가 9
    ASKP10: float                 ## 매도호가 10
    BIDP1: float                  ## 매수호가 1
    BIDP2: float                  ## 매수호가 2
    BIDP3: float                  ## 매수호가 3
    BIDP4: float                  ## 매수호가 4
    BIDP5: float                  ## 매수호가 5
    BIDP6: float                  ## 매수호가 6
    BIDP7: float                  ## 매수호가 7
    BIDP8: float                  ## 매수호가 8
    BIDP9: float                  ## 매수호가 9
    BIDP10: float                 ## 매수호가 10
    ASKP_RSQN1: float             ## 매도호가 잔량 1
    ASKP_RSQN2: float
    ASKP_RSQN3: float
    ASKP_RSQN4: float
    ASKP_RSQN5: float
    ASKP_RSQN6: float
    ASKP_RSQN7: float
    ASKP_RSQN8: float
    ASKP_RSQN9: float
    ASKP_RSQN10: float
    BIDP_RSQN1: float            ## 매수호가 잔량 1
    BIDP_RSQN2: float
    BIDP_RSQN3: float
    BIDP_RSQN4: float
    BIDP_RSQN5: float
    BIDP_RSQN6: float
    BIDP_RSQN7: float
    BIDP_RSQN8: float
    BIDP_RSQN9: float
    BIDP_RSQN10: float
    TOTAL_ASKP_RSQN: float # 총 매도호가 잔량
    TOTAL_BIDP_RSQN: float # 총 매수호가 잔량
    OVTM_TOTAL_ASKP_RSQN: float # 시간 외 총 매도호가 잔량
    OVTM_TOTAL_BIDP_RSQN: float # 시간 외 총 매수호가 잔량
    ANTC_CNPR: float ## 예상 체결가
    ANTC_CNQN: float ## 예상 체결량
    ANTC_VOL: float ## 예상 거래량
    ANTC_CNTG_VRSS: float ## 예상 체결 대비
    ANTC_CNTG_VRSS_SIGN: str ## 예상 체결대비 부호
    ANTC_CNTG_PRDY_CTRT: float ## 예상 체결 대비율
    ACML_VOL: float ## 누적 거래량
    TOTAL_ASKP_RSQN_ICDC: float ## 총 매도호가 잔량 증감
    TOTAL_BIDP_RSQN_ICDC: float ## 총 매수호가 잔량 증감
    OVTM_TOTAL_ASKP_ICDC: float ## 시간 외 총 매도호가 증감
    OVTM_TOTAL_BIDP_ICDC: float ## 시간 외 총 매tn호가 증감
    STCK_DEAL_CLS_CODE: str     ## 주식 매매 구분 코드(사용x)


# realtime_purchase 데이터 클래스 정의
@dataclass
class realtime_purchase(faust.Record, serializer='json'):
    TRHT_YN: str # 거래 정지 여부
    HOUR_CLS_CODE: str          ## 시간 구분코드
    MRKT_TRTM_CLS_CODE: str ## 임의종료구분코드
    MKSC_SHRN_ISCD: str ## 유가증권 단축 종목 코드
    STCK_CNTG_HOUR: str ## 주식 체결 시간
    STCK_PRPR: float ## 주식 현재가
    PRDY_VRSS_SIGN: str ## 전일 대비 부호
    PRDY_VRSS: float ## 전일 대비
    PRDY_CTRT: float ## 전일 대비율 
    WGHN_AVRG_STCK_PRC: float ## 가중 평균 주식 가격
    STCK_OPRC: float ## 주식 시가
    STCK_HGPR: float ## 주식 최고가
    STCK_LWPR: float ## 주식 최저가
    ASKP1: float ## 매도호가1
    BIDP1: float ## 매수호가1
    CNTG_VOL: float ## 체결 거래량
    ACML_VOL: float ## 누적 거래량
    ACML_TR_PBMN: float ## 누적 거래 대금
    SELN_CNTG_CSNU: float ## 매도 체결 건수
    SHNU_CNTG_CSNU: float ## 매수 체결 건수
    NTBY_CNTG_CSNU: float ## 순매수 체결 건수
    CTTR: float ## 체결 강도
    SELN_CNTG_SMTN: float ## 총 매도 수량
    SHNU_CNTG_SMTN: float ## 총 매수 수량
    CCLD_DVSN: str ## 체결 구분
    SHNU_RATE: float ## 매수 비율
    PRDY_VOL_VRSS_ACML_VOL_RATE: float ## 전일 거래량 대비 등락률
    OPRC_HOUR: str ## 시가 시간
    OPRC_VRSS_PRPR_SIGN: str ## 시가 대비 구분
    OPRC_VRSS_PRPR: float ## 시가대비
    HGPR_HOUR: str ## 최고가 시간
    HGPR_VRSS_PRPR_SIGN: str ## 고가 대비 구분
    HGPR_VRSS_PRPR: float ## 고가 대비
    LWPR_HOUR: str ## 최저가 시간
    LWPR_VRSS_PRPR_SIGN: str ## 저가대비구분
    LWPR_VRSS_PRPR: float ## 저가 대비
    BSOP_DATE: str ## 영업 일자
    NEW_MKOP_CLS_CODE: str ## 신 장운영 구분 코드
    ASKP_RSQN1: float ## 매도호가 잔량 1
    BIDP_RSQN1: float ## 매수호가 잔량 1
    TOTAL_ASKP_RSQN: float ## 총 매도호가 잔량
    TOTAL_BIDP_RSQN: float ## 총 매수호가 잔량
    VOL_TNRT: float ## 거래량 회전율
    PRDY_SMNS_HOUR_ACML_VOL: float ## 전일 동시간 누적 거래량
    PRDY_SMNS_HOUR_ACML_VOL_RATE: float ## 전일 동시간 누적 거래량 비율
    VI_STND_PRC: float ## 정적VI발동기준가
