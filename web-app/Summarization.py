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
    'nl':'nl_core_news_sm',
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
                result = self.query({"inputs": str(i),"parameters": {"repetition_penalty": 4.0,"max_length": length*ratio,"min_length":1},"options":{"wait_for_model":True}}, API_URL)

                try:
                    if 'generated_text' in result[0]:
                        text = result[0].get('generated_text')

                    if 'summary_text' in result[0]:
                        text = result[0].get('summary_text')
                except:
                    print('server outage')

                try:
                    if origin_lang != 'en':
                        text = gt.translate(text=str(text),src="en", dest=origin_lang).text 
                except TypeError as e:
                    text = ''

                output.append(text)

            result_dict[key] = output

        return(result_dict)
        


    """
    1) translate to english
    2) extract/abstractive summarization
    3) translate to original language
    """
    def summarize_old(self, text, key):
        
        ratio = 0.5

        soup = BeautifulSoup(text, 'html.parser')

        text = soup.get_text().replace('\n',' ').strip(' ')

        origin_lang = detect(text)
        nlp = spacy.load(languages.get(origin_lang, 'en'))
        doc = nlp(text)

        sentences = []

        gt = Translator()

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

        API_URL = huggingfacemodels.get(key)

        sentences = np.array(sentences)
        pad_size = 3 - (sentences.size % 3)
        padded_a = np.pad(sentences, (0, pad_size), mode='empty')
        paragraphs = padded_a.reshape(-1, 3)
        
        output = []
        text = ""
        for i in paragraphs:
            length = len(str(i))
            result = self.query({"inputs": str(i),"parameters": {"repetition_penalty": 4.0,"max_length": length*ratio,"min_length":1},"options":{"wait_for_model":True}}, API_URL)

            try:
                if 'generated_text' in result[0]:
                    text = result[0].get('generated_text')

                if 'summary_text' in result[0]:
                    text = result[0].get('summary_text')
            except:
                print('server outage')

            try:
                if origin_lang != 'en':
                    text = gt.translate(text=str(text),src="en", dest=origin_lang).text 
            except TypeError as e:
                text = ''

            output.append(text)                    
        return output
    

    def generate_glossary(self, list):
        # [ [woord, betekenis], [woord, betekenis], ... [woord, betekenis] ]
        url = "https://lexicala1.p.rapidapi.com/search-entries"
        result = []
        for word in list:
            querystring = {"text":str(word[0]),"language":"nl","pos":str(word[1])}

            headers = {
                "X-RapidAPI-Key": str(rapidapi_api_key),
                "X-RapidAPI-Host": "lexicala1.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            try:
                # definition = response.json()['results'][0]['senses'][0]['definition']
                definition = response.json()
            except Exception as e:
                definition = e

            result.append([word, definition])
        return result
    


    """
    @retuns full-text
    """
    def summarize_with_presets(self, full_text, presets):
        try:    
            prompt = f"""
            Samenvat de volgende tekst in {presets[0]} paragrafen met elk {presets[1]} zinnen van max {presets[2]} lang.
            {full_text}
            """

            result = openai.Completion.create(
                    prompt=prompt,
                    temperature=0,
                    max_tokens=1000,
                    model=COMPLETIONS_MODEL,
                    top_p=0.9,
                    stream=False
            )["choices"][0]["text"].strip(" \n")
            return prompt, result
        
        except Exception as e:
            return 'Open AI outage of problemen met API-sleutel', e
            

    """
    @returns 
    """
    def translate_sentence(self, sentence):
        translator  = Translator()
        result = translator.translate(
            text=sentence,
            dest='nl')
        return result.text # result.origin

class GPT():

    """
    @sets openai.api_key
    """
    def __init__(self, key=None):
        global gpt_api_key
        try:
            gpt_api_key = os.getenv('OPENAI')
        except:
            gpt_api_key = 'no_key_submitted'

    """
    @returns prompt, result from gpt 
    """
    def look_up_word_gpt(self, word, context):
        try:
            prompt = f"""
            Write a 10-word Dutch easy-to-read definition for the word: {word}
            context:
            {context}
            format:
            Definition. \n Bron: 
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
        Paraphrase this Dutch text. Avoid using {", ".join(personalisation)}
        Sentence:
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

class Lexicala():

    """
    @sets openai.api_key
    """
    def __init__(self, key=None):
        global rapidapi_api_key
        try:
            rapidapi_api_key = os.getenv('RAPIDAPI')
        except:
            rapidapi_api_key = 'no_key_submitted'

    """
    Lexicala is een multilinguaal woordenboek die beschikbaar wordt gesteld via een online API. In principe kan deze API volledig in JavaScript worden gedraaid, al De keuze om de PoS-tagging te baseren op de zin en niet het woord maakt het systeem minder vatbaar op afwisselend taalgebruik. Echter het gebruik van afwisselende woordenschat, wat prevalent is bij informatica-gerelateerde wetenschappelijke papers, maakt het systeem wel vatbaar op het niet kunnen terugvinden van deze woorden. Er wordt gesuggereerd om een valnet aan te maken, door ofwel de taal te veranderen naar Engels of Frans, ofwel door het GPT-3 model aan te spreken om een alternatieve definitie op te halen.
    """
    def look_up_word_rapidapi(self, word, sentence):
        try:

            """PoS-tag determination"""
            url = "https://lexicala1.p.rapidapi.com/search"
            lang = detect(sentence)
            
            """"""
            nlp = spacy.load(languages.get(lang, 'en'))
            doc = nlp(sentence)
            for token in doc:
                if word == token.text:
                    tag = token.pos_
                    lemma = token.lemma_ 

            """building up querystring"""
            querystring = {
                "text":str(lemma),
                "monosemous": "true",
                "language": lang,
                "pos":str(tag).lower()
            }

            headers = {
                "X-RapidAPI-Key": str(rapidapi_api_key),
                "X-RapidAPI-Host": "lexicala1.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)            

            """
            example resppnse output:
            {'id': 'NL_DE00001303', 'language': 'nl', 'headword': {'text': 'appel', 'pos': 'noun'}, 'senses': [{'id': 'NL_SE00001712', 'definition': 'ronde, harde, zoetzure vrucht met een klokhuis waarin donkere pitjes zitten'}]}
            {'id': 'NL_DE00001304', 'language': 'nl', 'headword': {'text': 'appel', 'pos': 'noun'}, 'senses': [{'id': 'NL_SE00001713', 'definition': 'bijeenkomst om te zien of iedereen er is'}]}
            """

            return response.json()
            # return response.json()['results'][0]['senses'][0]['definition']
        except Exception as e:
            return e
        


"""
text = "Within stutter therapy, transfer of learned skills to everyday life is not evident. Virtual Reality (VR) offers the opportunity to bring everyday life into into the safety of the therapy room. In this way, the feared situation can be practiced several times before moving into everyday life. An initial prototype of VR was tested by a group of 13 (young) adults who stutter. Based on their experiences and feedback, this was optimized with a more elaborated scenario and a more high-tech design. This second prototype was tested by 2 (young) adults who stutter. Young) adults who stutter indicated they see potential in using VR during the transfer phase. The first prototype had a greater impact than expected. A more high-tech elaboration with 360° images was perceived as more realistic."
for k in huggingfacemodels.keys():
    result = HuggingFaceModels().summarize(text=text, key=k)
    print(" ".join(result))
"""
    