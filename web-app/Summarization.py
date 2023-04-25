import openai, configparser, time, json, requests, spacy, os, numpy as np
import time, json, requests
from langdetect import detect
from googletrans import Translator
from bs4 import BeautifulSoup

huggingfacemodels = {
    'sc':"https://api-inference.huggingface.co/models/haining/scientific_abstract_simplification",
    'bart':"https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
    'bart-sc': "https://api-inference.huggingface.co/models/sambydlo/bart-large-scientific-lay-summarisation",
    't5':"https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-summarize-news",
    'kis': "https://api-inference.huggingface.co/models/philippelaban/keep_it_simple",
    'gpt-2':'https://api-inference.huggingface.co/models/gpt2',
    'gpt-2-ft': "https://api-inference.huggingface.co/models/gavin124/gpt2-finetuned-cnn-summarization-v2",
    'peg':'https://api-inference.huggingface.co/models/google/pegasus-xsum',
    'peg-par':'https://api-inference.huggingface.co/models/tuner007/pegasus_paraphrase'
}

from dotenv import load_dotenv
load_dotenv()

max_length = 2000

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

languages = {
    'nl':'nl_core_news_md',
    'en':'en_core_web_md'
}

class HuggingFaceModels:
    def __init__(self, key=None):
        try:
            global huggingface_api_key
            huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
        except:
            huggingface_api_key = 'not_submitted'

    """
    """
    def query(self, payload, API_URL):
        headers = {"Authorization": f"Bearer {huggingface_api_key}"}
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    

    def scientific_simplify(self, text, lm_key):
        length = len(text)
        API_URL = huggingfacemodels.get(lm_key)
        gt = Translator()
        translated_text = gt.translate(text=text,src='nl',dest='en').text
        result = self.query({"inputs": str(translated_text),"parameters": {"max_length": length},"options":{"wait_for_model":True}}, API_URL)[0]['generated_text']
        result = gt.translate(text=result,src='en',dest='nl').text
        return result


    def summarize(self, text, lm_key):
        ratio = 0.5
        soup = BeautifulSoup(text, 'html.parser')
        gt = Translator()
        
        h3_tags = soup.find_all('h3')

        split_text = {}
        for i, tag in enumerate(h3_tags):
            key = tag.text
            value = ""
            for sibling in tag.next_siblings:
                if sibling.name == 'h3':
                    break
                value += str(sibling.get_text()).replace('\n',' ')
            split_text[key] = value

        result_dict = {}
        for key in split_text.keys():
            text = split_text[key]
            origin_lang = detect(text)
            nlp = spacy.load(languages.get(origin_lang, 'en'))
            doc = nlp(text)

            sentences = []
            for s in doc.sents:
                try:
                    if origin_lang in ['fr','nl','de']:
                        text = gt.translate(text=str(s),src=origin_lang,dest='en').text
                    elif origin_lang not in ['fr','nl','de','en']:
                        text = gt.translate(text=s,src='en',dest='en').text
                    else:
                        text = s
                    sentences.append(text)
                except Exception as e:
                    continue

            API_URL = huggingfacemodels.get(lm_key)
            sentences = np.array(sentences)
            pad_size = 3 - (sentences.size % 3)
            padded_a = np.pad(sentences, (0, pad_size), mode='empty')
            paragraphs = padded_a.reshape(-1, 3)


            output = []
            text = ""
            for i in paragraphs:
                length = len(str(i))
                result = self.query({"inputs": str(i),"parameters": {"max_length": length},"options":{"wait_for_model":True}}, API_URL)

                try:
                    if 'generated_text' in result[0]:
                        text = result[0].get('generated_text')

                    if 'summary_text' in result[0]:
                        text = result[0].get('summary_text')
                except Exception as e:
                    print(e)
                    

                try:
                    if origin_lang != 'en':
                        text = gt.translate(text=str(text),src="en", dest=origin_lang).text 
                except TypeError as e:
                    text = ''

                output.append(text)

            result_dict[key] = output

        return(result_dict)            

    """
    @returns 
    """
    def translate_sentence(self, sentence):
        translator  = Translator()
        result = translator.translate(
            text=sentence,
            dest='nl')
        return result.text

class GPT():

    """
    @sets openai.api_key
    """
    def __init__(self, key=None):
        global gpt_api_key
        if key is None:
            gpt_api_key = 'not-submitted'
            openai.api_key = key
        else:
            gpt_api_key = key
            openai.api_key = key

    """
    @returns prompt, result from gpt 
    """
    def look_up_word_gpt(self, word, context):
        try:
            prompt = f"""
            Give for this word a Dutch definition considering the context: {word}
            context:
            {context}
            """
            result = openai.Completion.create(
                    prompt=prompt,
                    temperature=0,
                    max_tokens=100,
                    model=COMPLETIONS_MODEL,
                    top_p=0.9,
                    stream=False
                    )["choices"][0]["text"].strip(" \n")    
            return result, prompt
        except Exception as e:
            return 'Open AI outage of problemen met API-sleutel', str(e)
        
    def personalised_simplify(self, sentence, personalisation):
        prompt = f"""
        Simplify this text in Dutch and remove {", ".join(personalisation)}
        ///
        {sentence}
        """

        try:
            result = openai.Completion.create(
                    prompt=prompt,
                    temperature=0,
                    max_tokens=100,
                    model=COMPLETIONS_MODEL,
                    top_p=0.9,
                    stream=False
            )["choices"][0]["text"].strip(" \n")
            return result, prompt

        except Exception as e:
            return str(e), prompt 
        
    def summarize(self, full_text_dict, personalisation):

        print(personalisation)

        for title in full_text_dict.keys():
            prompt = f"""
            Rewrite this text without {", ".join(personalisation)}
            ///
            {full_text_dict[title]}
            """

            full_text_dict[title] = prompt

        return full_text_dict
        
        
class WordScraper():
    def look_up(self, woord):
        url = f"https://www.vertalen.nu/betekenis?woord={woord}&taal=nl"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        def_blocks = soup.find_all('ul', class_='def-block')
        definities = []
        for card in def_blocks:
            card_text = str(card.get_text()).strip(' ')
            definities.append(card_text)
        return definities

"""
text = "Within stutter therapy, transfer of learned skills to everyday life is not evident. Virtual Reality (VR) offers the opportunity to bring everyday life into into the safety of the therapy room. In this way, the feared situation can be practiced several times before moving into everyday life. An initial prototype of VR was tested by a group of 13 (young) adults who stutter. Based on their experiences and feedback, this was optimized with a more elaborated scenario and a more high-tech design. This second prototype was tested by 2 (young) adults who stutter. Young) adults who stutter indicated they see potential in using VR during the transfer phase. The first prototype had a greater impact than expected. A more high-tech elaboration with 360° images was perceived as more realistic."
for k in huggingfacemodels.keys():
    result = HuggingFaceModels().summarize(text=text, key=k)
    print(" ".join(result))
"""
    