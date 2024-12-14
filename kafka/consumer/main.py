from confluent_kafka import Consumer, KafkaException
from influx_handler import InfluxDBHandler
import json

## InfluxDB를 초기화한다.
influx_handler = InfluxDBHandler(influx_url = '', influx_token = '', influx_org = 'project', influx_bucket = 'stock')


## Consumer를 초기화한다.
consumer_config = {
    'bootstrap.servers': '',
    'group.id' : '',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_config)
consumer.subscribe(['']) ## 토픽이름 지정

try:
    print("Consuming messages from Kafka and writing to InfluxDB...")
    while True:
        msg = consumer.poll(timeout=1.0)  # Poll messages from Kafka

        if msg is None:
            continue  # No message available, retry
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                # End of partition event
                print(f"Reached end of partition: {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
            else:
                raise KafkaException(msg.error())
        else:
            # Process the valid message
            try:
                measurements = msg.key().decode('utf-8') if msg.key() else None
                data = json.loads(msg.value().decode('utf-8'))

                ## 파티션 키에 따라 measurements를 지정해서 인서트 한다.
                influx_handler.send_to_influxdb(partition_key=measurements, data=data)
                print(f"Data written to InfluxDB: {data}")

            except Exception as e:
                print(f"Error processing message: {e}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connections gracefully
    consumer.close()
    influx_handler.close()