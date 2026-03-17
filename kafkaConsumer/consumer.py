from kafka import KafkaConsumer
import json
 
consumer = KafkaConsumer(
    "clickstream_events",
    bootstrap_servers="localhost:9092",
    api_version=(0, 10),
    auto_offset_reset="earliest",        # start from beginning if no offset saved
    enable_auto_commit=True,             # auto-commit offset every 5s
    group_id="clickstream_consumer_group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)
 
print("Consumer started — waiting for messages...\n")
 
for message in consumer:
    log = message.value
 
    print(f"[{log['timestamp']}] "
          f"user={log['user']['user_id']} | "
          f"event={log['event_type']} | "
          f"page={log['session']['page']} | "
          f"ip={log['location']['ip_address']} | "
          f"city={log['location']['city']} | "
          f"device={log['session']['device']}")