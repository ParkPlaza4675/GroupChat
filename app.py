from flask import Flask, request
from twilio.rest import Client
import os

app = Flask(__name__)

# Twilio credentials
ACCOUNT_SID = os.environ['AC59f356c3053a5c1cc3b4a1462fe44864']
AUTH_TOKEN = os.environ['972249e79c988f7561770bd8cc7e528b']
TWILIO_NUMBER = os.environ['+18335530340']

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# In-memory store of users: {phone_number: name}
participants = {}

@app.route('/sms', methods=['POST'])
def sms():
    from_number = request.form['From']
    msg = request.form['Body'].strip()

    if msg.upper().startswith("JOIN"):
        name = msg[5:].strip()
        if name:
            participants[from_number] = name
            return f"Hello {name}, you're now in the group chat."
        return "Please include your name: JOIN John"

    elif msg.upper() == "STOP":
        if from_number in participants:
            participants.pop(from_number)
            return "You’ve left the group chat."
        return "You're not currently in the chat."

    elif from_number in participants:
        sender_name = participants[from_number]
        broadcast_msg = f"[{sender_name}]: {msg}"
        for number in participants:
            if number != from_number:
                client.messages.create(
                    body=broadcast_msg,
                    from_=TWILIO_NUMBER,
                    to=number
                )
        return "Message sent to group."

    return "You're not in the chat. Text JOIN yourname to join."

