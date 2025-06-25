from flask import Flask, request
import requests
import os
from refund_logic import refund_policy_helper
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, headers=headers, json=data)
    print("Send message response:", response.text)

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Verification token mismatch", 403

@app.route('/webhook', methods=['POST'])
def handle_messages():
    data = request.get_json()
    print("Received webhook event:", data)

    if 'entry' in data:
        for entry in data['entry']:
            for messaging_event in entry.get('messaging', []):
                sender_id = messaging_event['sender']['id']
                if 'message' in messaging_event and 'text' in messaging_event['message']:
                    user_message = messaging_event['message']['text']
                    bot_reply = refund_policy_helper(user_message)
                    send_message(sender_id, bot_reply)

    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
