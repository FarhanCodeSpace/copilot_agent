"""Email agent implemented with the reusable AgentFramework."""

from agentic_framework import AgentFramework


def respond_to_email(email_data):
    print(f"Responding to email from {email_data['from']} with an automatic response...")


def add_label(email_data):
    print(f"Adding Filter Label to email from {email_data['from']}")


def mark_as_spam(email_data):
    print(f"Marking email from {email_data['from']} as spam...")


def delete_email(email_data):
    print(f"Deleting email from {email_data['from']}...")


def do_nothing(email_data):
    print("Doing nothing...")


def describe_sender(email_address):
    if email_address == "bob@xyzcorp.com":
        return "The user's boss; respond quickly"
    if email_address == "awais@gmail.com":
        return "The user's friend; a quick response is usually not expected"
    return "No description found"


def get_user_prompt(email_data):
    return f"""
From: {email_data['from']}
Sender description: {email_data['sender_desc']}
Subject: {email_data['subject']}
Body: {email_data['text']}
"""


def build_email_agent():
    actions = [
        {
            "action_name": "MARK_AS_SPAM",
            "action_description": "Mark suspicious or unwanted email as spam.",
            "action_function": mark_as_spam,
            "require_permission": False,
        },
        {
            "action_name": "ADD_LABEL",
            "action_description": "Add the Filter Label when the email should be organized for later review.",
            "action_function": add_label,
            "require_permission": False,
        },
        {
            "action_name": "RESPOND_TO_EMAIL",
            "action_description": "Send an automatic response when the email needs a reply.",
            "action_function": respond_to_email,
            "require_permission": False,
        },
        {
            "action_name": "DO_NOTHING",
            "action_description": "Take no action when the email does not need processing.",
            "action_function": do_nothing,
            "require_permission": False,
        },
        {
            "action_name": "DELETE_EMAIL",
            "action_description": "Permanently delete the email; use only when it is clearly unwanted.",
            "action_function": delete_email,
            "require_permission": True,
        },
    ]

    return AgentFramework(
        actions,
        developer_prompt_elements={
            "role": "You are an email classification agent.",
            "objective": "Choose the safest and most useful action for the email data provided by the user.",
            "instructions": [
                "Choose exactly one available action.",
                "Consider the sender description, subject, and body.",
                "Never delete an email unless it is clearly unwanted.",
            ],
            "output_format": "Respond with ONLY the action name. Do not include any explanation.",
        },
    )


def run_email_agent(email_data):
    email_agent = build_email_agent()
    user_prompt = get_user_prompt(email_data)
    print(user_prompt)
    return email_agent.run(user_prompt, email_data)


if __name__ == "__main__":
    while True:
        from_email = input("What email address is this from?: ")
        email_data = {
            "from": from_email,
            "sender_desc": describe_sender(from_email),
            "subject": input("What is the subject line?: "),
            "text": input("Enter the email text: "),
        }
        run_email_agent(email_data)
