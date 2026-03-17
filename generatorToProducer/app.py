# # from fastapi import FastAPI,WebSocket
# from kafka import KafkaProducer
# from Synthetic_Data_Generator.Generators.session_generator import generate_sessions
# from Synthetic_Data_Generator.Generators.User_Generator import get_user
# import json
# import asyncio

# # app = FastAPI(title='PBL-proj')
# # @app.get('/')
# # def home():
# #     return {'message':'Wecome Section C project...'}
# producer = KafkaProducer(
#     bootstrap_servers = 'localhost:9092',
#     api_version = (0,10),
#     value_serializer = lambda v:json.dumps(v).encode('utf-8')
# )

# # @app.websocket("/stream_log_data")
# # async def websocket_stream(websocket: WebSocket):
# #     await websocket.accept()
# #     while True:
# #         user_id = get_user()
# #         session = generate_sessions(user_id)
# #         for event in session:
# #             await websocket.send_json(event)
# #             producer.send(topic="clickstream_events", value=event)
# #             await asyncio.sleep(1)
# #         producer.flush()


# # async def simulate_user(websocket: WebSocket): 
# #     user_id = get_user() 
# #     session = generate_sessions(user_id) 
# #     for event in session: 
# #         await websocket.send_json(event) 
# #         producer.send("clickstream_events", value=event) 
# #         await asyncio.sleep(1) 
# # @app.websocket("/stream_log_data") 
# # async def websocket_stream(websocket: WebSocket): 
# #     await websocket.accept() 
# #     while True: 
# #         tasks = []
# #         for _ in range(3):
# #             tasks.append(asyncio.create_task(simulate_user(websocket)))
# #         await asyncio.gather(*tasks)
# #         producer.flush()

# async def simulate_user(): 
#     user_id = get_user() 
#     session = generate_sessions(user_id) 
#     for event in session: 
#         producer.send("clickstream_events", value=event) 
#         await asyncio.sleep(1) 

# async def bal():
#     pass
# async def main(): 
#     while True: 
#         tasks = []  
#         for _ in range(5): 
#             tasks.append(asyncio.create_task(simulate_user()))               
#             await asyncio.gather(*tasks) 
#             producer.flush() 
# asyncio.run(main())












import sys
sys.path.append('/home/asim/workspace/projects/PBL')
from kafka import KafkaProducer
from Synthetic_Data_Generator.Generators.session_generator import generate_sessions
from Synthetic_Data_Generator.Generators.User_Generator import get_user
from Synthetic_Data_Generator.Generators.log_Data_generator import format_log
import json
import asyncio


producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    api_version=(0, 10),
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
)
async def simulate_user():
    user_id = get_user()
    session = generate_sessions(user_id)
    for event in session:
        log = format_log(event)          # flat event → nested log dict
        producer.send("clickstream_events", value=log)
        await asyncio.sleep(1)

async def main():
    while True:
        tasks = [asyncio.create_task(simulate_user()) for _ in range(5)]
        await asyncio.gather(*tasks)     # 5 users stream concurrently
        producer.flush()
 
asyncio.run(main())