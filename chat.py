import openai

import os

def create_message(content, role):
    message = {"role": role, "content": content}
    return message

if __name__=='__main__':
    openai_key_var_name = "OPENAI_KEY"
    openai.api_key = os.getenv(openai_key_var_name)

    log = []
    while True:
        user_message_content = str(input('user: '))
        print('---------------------------------------')
        log.append(create_message(user_message_content, 'user'))
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=log[-2000:])
        system_message_content = (response['choices'][0]['message']['content']).strip()
        log.append(create_message(system_message_content, 'system'))
        print(f'system: {system_message_content}')
        print('---------------------------------------')