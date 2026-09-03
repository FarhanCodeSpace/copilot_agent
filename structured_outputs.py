from dotenv import load_dotenv
import os
import requests
from pydantic import BaseModel

load_dotenv()


def get_genai_response(dev_prompt, user_prompt, structure):
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "moonshotai/kimi-k3")

    messages = [
        {
            "role": "developer",
            "content": dev_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": messages,
            "max_tokens": 256,
            "text_format": structure
        }
    )

    data = response.json()

    if "error" in data:
        return "Error: " + data["error"]["message"]

    return data["choices"][0]["message"]["content"]

def get_dev_prompt():
    return f"""
    You are an email classification agent.

    You will recieve email data from the user. Based on that data, you will choose exactly one of these actions:
    - MARK_AS_SPAM
    - ADD_LABEL
    - RESPOND_TO_EMAIL
    - DO_NOTHING

    When responding, action_name should be one of the above, and the additional_details will depend on the action, for ADD_LABEL, it should be the label name, for RESPOND_TO_EMAIL, it should be a draft of the email response.
    """
def get_user_prompt(email_data):
    return f"""
    From: {email_data['from']}
    Sender description: {email_data['sender_desc']}
    Subject: {email_data['subject']}
    Body: {email_data['text']}
    """

if __name__ == '__main__':
    while True:
     from_email = input('What email address is this from?: ')
     additional_sender_info = describe_sender(from_email)
     subject = input('What is the subject line?: ')
     email_text = input('Enter the email text: ')

     email_data = {
        'from': from_email,
        'sender_desc': additional_sender_info,
        'subject': subject,
        'text': email_text
     }

     decision = make_decision(email_data)
     execute_decision(decision)

class ToolActivation(BaseModel):
    action_name: str
    additional_details: str

response = get_genai_response(
    get_dev_prompt,
    """
    from: bob@xyzcorp.com
    subject: URGENT EMERGENCY
    text: I believe the site is down! Please check into it immediately!!
    """,
    ToolActivation,
)

print(response)