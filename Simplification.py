import configparser, openai, requests, json

""""""
COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

class Simplification:

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
    @returns prompt, result from gpt 
    """
    def look_up_word_gpt(self, word, context):
        try:
            prompt = f"""
            Provide a 10-word Dutch definition and 3 Dutch synonyms for the Dutch word: {word}
            context:
            {context}
            """

            result = openai.Completion.create(
                    prompt=prompt,
                    temperature=0,
                    max_tokens=1000,
                    model=COMPLETIONS_MODEL,
                    top_p=0.9,
                    stream=False
                    )["choices"][0]["text"].strip(" \n")    
            return result, prompt
        
        except Exception as e:
            return 'Open AI outage of problemen met API-sleutel', e 
        

    """
    """
    def look_up_word_rapidapi(word, sentence, nlp_model):
        try:
            url = "https://lexicala1.p.rapidapi.com/search"
            doc = nlp_model(sentence)
            for token in doc:
                if word == token.text:
                    tag = token.pos_

            querystring = {
                "text":str(word),
                "monosemous":"true",
                "language":"nl",
                "pos":str(tag).lower()
            }

            headers = {
                "X-RapidAPI-Key": str(rapidapikey),
                "X-RapidAPI-Host": "lexicala1.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            data = json.loads(json.dumps(response))
            return data['results'][0]['senses'][0]['definition']
        except:
            return None
        
    

        
    """
    @returns prompt, result
    """
    def syntactic_simplify(self, text):
        try:
            print(text)
            max_words = 10
            prompt = f"""
            prompt:
            Simplify this sentence by removing tangential constructions, proverbs, separable words, and pronouns, and ensure that the resulting sentence is under {max_words} words. Afterwards, translate this sentence to Dutch.
            context:
            {text}
            """
            result = openai.Completion.create(
                    prompt=prompt,
                    temperature=0,
                    max_tokens=500,
                    model=COMPLETIONS_MODEL,
                    top_p=0.9,
                    stream=False
            )["choices"][0]["text"].strip(" \n")
            return result
        except Exception as e:
            return f'Open AI outage of problemen met API-sleutel {e}'