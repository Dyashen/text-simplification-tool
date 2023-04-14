import configparser
import time, json, requests
from langdetect import detect
from googletrans import Translator

dict = {
    'sc':"https://api-inference.huggingface.co/models/haining/scientific_abstract_simplification",
    'bart':"https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
    'bart-sc': "https://api-inference.huggingface.co/models/sambydlo/bart-large-scientific-lay-summarisation",
    't5':"https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-summarize-news",
    'kis': "https://api-inference.huggingface.co/models/philippelaban/keep_it_simple",
    'gpt-2':'https://api-inference.huggingface.co/models/gpt2',
    'gpt-2-ft': "https://api-inference.huggingface.co/models/gavin124/gpt2-finetuned-cnn-summarization-v2"
}

max_length = 2000

class HuggingFaceModels:
    def __init__(self):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            global huggingface_api_key
            huggingface_api_key = config['huggingface']['api_key']
        except Exception as e:
            huggingface_api_key = 'not_submitted'


    """
    
    """
    def query(self, payload, API_URL):
        headers = {"Authorization": f"Bearer {huggingface_api_key}"}
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    

    """
    1) translate to english
    2) extract/abstractive summarization
    3) translate to original language
    """
    def summarize(self, text, key):
        origin_lang = detect(text)

        if origin_lang in ['fr','nl','de']:
            text = Translator().translate(text=text,src=origin_lang,dest='en').text
        elif origin_lang not in ['fr','nl','de','en']:
            text = Translator.translate(text=text,src='en',dest='en').text

        length = len(text)

        API_URL = dict.get(key)
        i = 0
        while True and i < 3:
            output = self.query({
                "inputs": text,
                "parameters": {
                    "repetition_penalty": 4.0,
                    "max_length": length+10
                }
            }, API_URL)

            response = output
            
            if 'error' not in response:
                break
            else:
                i += 1
                try:
                    time.sleep(float(response.get('estimated_time')))
                except:
                    time.sleep(20)
        
        response = output[0]
                
        if 'generated_text' in output[0]:
            text = output[0].get('generated_text')

        if 'summary_text' in output[0]:
            text = output[0].get('summary_text')

        if origin_lang != 'en':
            text = Translator().translate(text=text,src="en", dest=origin_lang).text

        return text