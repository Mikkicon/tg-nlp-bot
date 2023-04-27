import json
import requests
import openai
import os
# from datasets import load_dataset


def webhook(event, context):
    openai_token = os.environ['OPENAI_TOKEN']
    telegram_token = os.environ['TG_BOT_TOKEN']
    
    print('event', event)
    print('openai_token len', len(openai_token))
    print('telegram_token len', len(telegram_token))

    BASE_URL = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    body = json.loads(event['body'])
    message = body['message']['text']
    chatId = body['message']['chat']['id']

    # list models
    # models = openai.Model.list()

    # print the first model's id
    # print(models.data[0].id)

    openai.api_key=openai_token
    # create a completion
    # completion = openai.Completion.create(model="ada", prompt=message)
    # print(completion.choices[0].text)

    form_data = { 'text': 'chatGPTResponse', 'chat_id': chatId }
    server = requests.post(BASE_URL, data=form_data)

    response_body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
