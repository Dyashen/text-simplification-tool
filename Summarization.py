import configparser, openai, re
from googletrans import Translator
from langdetect import detect
import requests

""""""
COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    openai.api_key = config['openai']['api_key']
except:
    openai.api_key = 'demo'


""""""
try:
    LANG = 'nl'
except:
    LANG = 'nl'

class Summarization:
    """
    @sets openai.api_key
    """
    def __init__(self, key):
        if key is None:
            config = configparser.ConfigParser()
            config.read('config.ini')
            openai.api_key = config['openai']['api_key']
        else:
            openai.api_key = key

        global rapidapikey
        try:
            rapidapikey = config['rapidapi']['api_key']
        except:
            rapidapikey = 'no_key_submitted'

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
        result = translator.translate(text=sentence, dest=LANG)
        return result.text # result.origin


    """
    """
    def abstractive_summarization_rapidapi(self, text, num_sentences):
        try:
            url = "https://gpt-summarization.p.rapidapi.com/summarize"
            payload = {
	            "text": text,
	            "num_sentences": num_sentences
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": str(rapidapikey),
                "X-RapidAPI-Host": "gpt-summarization.p.rapidapi.com"
            }
            response = requests.request("POST", url, json=payload, headers=headers)
            return response.json()['summary']
        except Exception as e:
            return f'{e}'


    """
    @returns list of sentences
    """
    def extractive_summarization(self, full_text, summarizer):

        try:    
            """determining optimal number of sentences based on MMR"""
            res = summarizer.calculate_optimal_k(
                full_text, 
                k_max=10
            )

            """extracting key sentences"""
            result = summarizer(
                body=full_text,
                max_length=700,
                min_length=100,
                num_sentences=res,
                return_as_list=True
            )

            new = []
            try:
                for i in result:
                    if detect(i) != 'nl':
                        new.append(self.translate_sentence(i))
                    else:
                        new.append(i)
                return ' '.join(new)
            except Exception as e:
                return f'Problemen met Google Translate {e}'

        
        except Exception as e:
            return f'Problemen met BERT {e}'
            

    def generate_summary(self, fullText, summarizer):
        fullText = str(fullText)
        fullText = fullText.encode('ascii', 'ignore').decode('ascii')

        """cleaning"""
        patterns = {
            '<h1>': '',
            '</h1>': '',
            '<div class="page">':'',
            '</div>':'',
            '<span class="word">': ' ',
            '</span>' : '',
            '\n' : '',
            ' ' : '',
            '<p>': '',
            '</p><p>':'',
            '</p>':'',
            '<span class="sentence">':' ',
            '[':'',
            ']':''
        }
        regex = re.compile('|'.join(map(re.escape, patterns.keys())))
        fullText = fullText.strip('\n')
        text = regex.sub(lambda match : patterns[match.group(0)], fullText)


        """per gekozen titel"""
        text = text.split('<h3>')
        new_text = []

        for i in range(len(text)):
            try:

                title = text[i].split('</h3>')[0],
                paragraph = text[i].split('</h3>')[1]
                
                if (len(paragraph) > 3000):
                    # extractive
                    paragraph = self.extractive_summarization(
                        full_text=paragraph, 
                        summarizer=summarizer
                    )

                    # abstractive
                    paragraph = self.abstractive_summarization_rapidapi(
                        text=paragraph,
                        num_sentences=5
                    )

                else:
                    # abstractive
                    paragraph = self.abstractive_summarization_rapidapi(
                        text=paragraph,
                        num_sentences=5
                    )

                new_text.append([
                    title, paragraph
                ])

            except:
                new_text.append(text[i])
        return new_text


    def generate_glossary(self, list):
        # [ [woord, betekenis], [woord, betekenis], ... [woord, betekenis] ]
        url = "https://lexicala1.p.rapidapi.com/search-entries"
        result = []
        for word in list:
            querystring = {"text":str(word[0]),"language":"nl","pos":str(word[1])}

            headers = {
                "X-RapidAPI-Key": str(rapidapikey),
                "X-RapidAPI-Host": "lexicala1.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            try:
                definition = response.json()['results'][0]['senses'][0]['definition']
            except Exception as e:
                definition = e

            result.append([word, definition])
        return result



    def generate_glossary_for_set(self, set):
        words = ", ".join(set)
        prompt = f"""
        Geef voor de volgende woorden een eenvoudige uitleg van hoogstens twee zinnen: {words}.
        formaat:
        woord: uitleg. synoniemen: ...\n
        """

        result = openai.Completion.create(
                prompt=prompt,
                temperature=0,
                max_tokens=1000,
                model=COMPLETIONS_MODEL,
                top_p=0.9,
                stream=False
                
        )["choices"][0]["text"].strip(" \n")
        return result.split('\n')
