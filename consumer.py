from kafka import KafkaConsumer
import json

from config import KAFKA_BOOTSTRAP

consumer = KafkaConsumer(
    "clickstream_events",
    bootstrap_servers= KAFKA_BOOTSTRAP,
    auto_offset_reset='earliest',   # start from beginning
    enable_auto_commit=True,
    group_id='clickstream-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer started... Listening for events\n")

try:
    for i, message in enumerate(consumer, start=1):
        log = message.value
        print(f"Received Log: {json.dumps(log, indent=2)}")
        print("-" * 80)
        # print(f"Message {i}", end='\r')

except KeyboardInterrupt:
    print("\nStopping consumer...")

finally:
    consumer.close()