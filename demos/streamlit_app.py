import streamlit as st
import requests
import time

API_KEY = "4cf557b1-fee5-467b-812d-9f7c8889bc38"

def call_akkio_api(message):
    create_task_url = "https://api.akkio.com/api/v1/chat-explore/new"
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    data = {"project_id": "VJQA1flvZ2meAFxMic0w", "messages": [{"role": "user", "content": message}]}
    response = requests.post(create_task_url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('task_id')
    else:
        return 'Error: ' + str(response.status_code)

def query_task_status(task_id):
    status_url = f"https://api.akkio.com/api/v1/chat-explore/status/{task_id}"
    headers = {"X-API-Key": API_KEY}
    response = requests.get(status_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return 'Error: ' + str(response.status_code)

def retrieve_chat_results(chat_id):
    results_url = f"https://api.akkio.com/api/v1/chat-explore/chats/{chat_id}"
    headers = {"X-API-Key": API_KEY}
    response = requests.get(results_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return 'Error: ' + str(response.status_code)

st.title("AI Data Chat")

message = st.text_input("Enter your message:")
if st.button("Send"):
    task_id = call_akkio_api(message)
    if task_id.startswith('Error'):
        st.error(task_id)
    else:
        while True:
            status_response = query_task_status(task_id)
            if isinstance(status_response, str) and status_response.startswith('Error'):
                st.error(status_response)
                break
            if status_response.get('status') == 'completed':
                chat_id = status_response.get('chat_id')
                results = retrieve_chat_results(chat_id)
                st.write(results)
                break
            time.sleep(5)