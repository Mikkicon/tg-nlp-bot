import json
import requests
import openai
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from bs4 import BeautifulSoup

openai_token = os.environ['OPENAI_TOKEN']
telegram_token = os.environ['TG_BOT_TOKEN']

BASE_URL = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
print('openai_token len', len(openai_token))
print('telegram_token len', len(telegram_token))

# ./briefr/bin/pip3 install -r requirements.txt
# source ./source.sh

def webhook(request):
    print('request', request)
    print('request.json', request.json)

    body = request.json
    message = get_message(body)
    chat_id = body['message']['chat']['id']

    if 'MY_MODEL' in os.environ:
        my_t5_prediction = get_my_t5_prefiction(message)
        print(my_t5_prediction)
        send_to_bot(my_t5_prediction, chat_id)
    if 'T5_MODEL' in os.environ:
        t5_prediction = get_t5_prefiction(message)
        print(t5_prediction)
        send_to_bot(t5_prediction, chat_id)
    if 'OPENAI_MODEL' in os.environ:
        openai_prediction = get_openai_prediction(message)
        print(openai_prediction)
        send_to_bot(openai_prediction, chat_id)

    response_body = {"message": "SUCCESS", "request_data": str(request.data), "message": message}
    response = { "statusCode": 200, "body": json.dumps(response_body)}
    return response

def get_message(body):
    text = body['message']['text']
    if text[:8] == "https://":
        resonse = requests.get(text)
        return BeautifulSoup(resonse.text).text.replace("\n", " ").replace("\t", " ")
    return text

def get_my_t5_prefiction(input_text):
    my_model = AutoModelForSeq2SeqLM.from_pretrained(f"mikkicon/t5-small_tuned_on_billsum")
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    input_ids = tokenizer(get_prompt(input_text), return_tensors="pt").input_ids  
    outputs = my_model.generate(input_ids)
    return "MY MODEL:\n\n" + tokenizer.decode(outputs[0], skip_special_tokens=True)

def get_t5_prefiction(input_text):
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    input_ids = tokenizer(get_prompt(input_text), return_tensors="pt").input_ids  
    outputs = model.generate(input_ids)
    return "T5 MODEL:\n\n" + tokenizer.decode(outputs[0], skip_special_tokens=True)

def get_openai_prediction(input_text):
    openai.api_key=openai_token
    completion = openai.Completion.create(model="text-davinci-003", prompt=get_prompt(input_text), max_tokens=1024)
    return "OPENAI MODEL:\n\n" + completion.choices[0].text

def send_to_bot(text, chat_id):
    requests.post(BASE_URL, data= { 'text': text, 'chat_id': chat_id })

def get_prompt(input_text):
    return f"summarize: {input_text}"
