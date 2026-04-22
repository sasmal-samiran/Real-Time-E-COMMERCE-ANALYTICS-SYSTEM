from datetime import datetime
import random, json, time
from kafka import KafkaProducer, errors
from Synthetic_Data_Generator.Generators.session_generator import generate_sessions
from Synthetic_Data_Generator.Generators.User_Generator import get_user
from Synthetic_Data_Generator.Generators.log_Data_generator import format_log
from config import KAFKA_BOOTSTRAP

producer = None
i = 1
initial_time = datetime.now()

while True:
    try:
        if producer is None:
            producer = KafkaProducer(
                bootstrap_servers= KAFKA_BOOTSTRAP,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Producer initialized successfully.")

        user_id = get_user()
        session = generate_sessions(user_id)

        for event in session:
            log = format_log(event) 
            # if log.get("event_type") in ["add_to_cart", "view_product"] or \
            # log.get("action_details", {}).get("is_purchase", False):

            #     print(f"Produced log for user {user_id}: {json.dumps(log, indent=2)}")
            future=producer.send("clickstream_events", value=log)
            elapsed = datetime.now() - initial_time   # this is a timedelta
            print(f"Message {i}, Time: {elapsed}", end="\r")
            i+=1
            future.get(timeout=5) 
            time.sleep(random.uniform(0.5, 1.5))

    except KeyboardInterrupt:
        print("\nStopping producer...")
        if producer:
            producer.close()
        break
        
    except errors.NoBrokersAvailable:
        print("Producer not initialized. Retrying in 5 seconds...")
        if producer:
            producer.close()
        producer = None
        time.sleep(5)
    
    except Exception as e:
        print("\nKafka connection lost. Stopping producer...")
        if producer:
            producer.close()
            producer = None
        continue