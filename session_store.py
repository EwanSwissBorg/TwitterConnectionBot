import json
import os

def save_session(token, chat_id, request_token=None):
    sessions = load_sessions()
    sessions[token] = {
        'chat_id': chat_id,
        'request_token': request_token
    }
    with open('sessions.json', 'w') as f:
        json.dump(sessions, f)

def load_sessions():
    if os.path.exists('sessions.json'):
        with open('sessions.json', 'r') as f:
            return json.load(f)
    return {}

def get_session(token):
    sessions = load_sessions()
    return sessions.get(token) 