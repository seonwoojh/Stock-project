from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBHandler:
    def __init__(self, influx_url: str, influx_token: str, influx_org: str, influx_bucket: str):

        ## InfluxDB client 정보
        self.influx_client = InfluxDBClient(
            url=influx_url,
            token=influx_token,
            org=influx_org
        )
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
        self.bucket = influx_bucket
        
    
    def send_to_influxdb(self, partition_key: str, data: dict):
        if partition_key == "HOSTASP0":
            measurement = 'realtime_hoka'
            stockcode = data.pop("MKSC_SHRN_ISCD", None)  # Remove Stock code from data and use it as a tag
            hour_cls_code = data.pop("HOUR_CLS_CODE", None)  # Remove HOUR_CLS_CODE from data and use it as a tag
            fields = data

            point = Point(measurement)
            if stockcode:
                point.tag("STOCKCODE", stockcode)
            if hour_cls_code:
                point.tag("HOUR_CLS_CODE", hour_cls_code)

            for field_key, field_value in fields.items():
                point.field(field_key, field_value)
        
            self.write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

        elif partition_key == "H0STCNT0":
            measurement = 'realtime_purchase'
            TRHT_YN = data.pop("TRHT_YN", None)
            hour_cls_code = data.pop("HOUR_CLS_CODE", None)
            mrkt_trtm_cls_code = data.pop("MRKT_TRTM_CLS_CODE", None)
            fields = data

            point = Point(measurement)
            if TRHT_YN:
                point.tag("TRHT_YN", TRHT_YN)
            if hour_cls_code:
                point.tag("HOUR_CLS_CODE", hour_cls_code)
            if mrkt_trtm_cls_code:
                point.tag("MRKT_TRTM_CLS_CODE", mrkt_trtm_cls_code)
            for field_key, field_value in fields.items():
                point.field(field_key, field_value)

            self.write_api.write(bucket=self.bucket, org=self.org, record=point)