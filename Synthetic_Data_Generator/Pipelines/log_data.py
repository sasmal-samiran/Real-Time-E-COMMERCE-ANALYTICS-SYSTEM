from Generators.session_generator import generate_sessions
from Generators.User_Generator import get_user

while True:
    user_id = get_user()
    sessions = generate_sessions(user_id)
    


