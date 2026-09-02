from basic_agent import get_genai_response

def get_dev_prompt(): 
    return f"""
    You are an email classification agent.

    You will recieve email data from the user. Based on that data, you will choose exactly one of these actions:
    - MARK_AS_SPAM
    - ADD_LABEL
    - RESPOND_TO_EMAIL
    - DO_NOTHING  

    Respond with ONLY the action name. Do not include any explanation.
    """

def get_user_prompt(email_data):
    return f"""
    From: {email_data['from']}
    Sender description: {email_data['sender_desc']}
    Subject: {email_data['subject']}
    Body: {email_data['text']}
    """

#Brain
def make_decision(input_data):
    user_prompt = get_user_prompt(input_data)
    print(user_prompt)
    response = get_genai_response(
        get_dev_prompt(), 
        user_prompt,
    )
    return response
    # from_email = input_data['from']
    # subject = input_data['subject']
    # email_text = input_data['text']

    # if 'big sale' in email_text:
    #     return 'MARK_AS_SPAM'
    # elif from_email.endswith('@xyzcorp.com'):
    #     return 'ADD_LABEL'
    # elif 'ASAP' in email_text:
    #     return 'RESPOND_TO_EMAIL'
    # else:
    #     return 'DO_NOTHING'

#Tools
def respond_to_email(response_text):
    print(f'Responding to email with message: {response_text}')

def add_label(label):
    print(f'Adding Label ro email: {label}')

def mark_as_spam():
    print(f'Marking email as spam...')

# Additional Knowledge
def describe_sender(email_address):
    if email_address == "bob@xyzcorp.com":
        return "The user's boss, highly value quick response to email"
    elif email_address == "awais@gmail.com":
        return "The user's friend, generally doesn't expect a quick response"
    else:
        return "No decription found"


#plumbing
def execute_decision(decision):
    if decision == 'RESPOND_TO_EMAIL':
        respond_to_email('This is just an auto-respoonse...')
    elif decision == 'ADD_LABEL':
        add_label('Filter Label')
    elif decision == 'MARK_AS_SPAM':
        mark_as_spam()
    elif decision == 'DELETE_EMAIL':
        approval = input('Do you realy want to let the agent to delete this email? (Y/n): ')
        if approval == 'Y':
            print('Deleting email...')
        else: 
            print('Not deleting email...')
    else:
        print('Doing Nothing...')

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