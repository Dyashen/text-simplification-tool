import configparser, openai, requests, json, spacy
from langdetect import detect

dict = {
    'nl':'nl_core_news_sm',
    'en':'en_core_word_sm'
}

""""""
class Lexicala:

    """
    @sets openai.api_key
    """
    def __init__(self, key):
        if key is None:
            config = configparser.ConfigParser()
            config.read('config.ini')

            global rapidapikey
            try:
                rapidapikey = config['rapidapi']['api_key']
            except:
                rapidapikey = 'no_key_submitted'

    """
    Lexicala is een multilinguaal woordenboek die beschikbaar wordt gesteld via een online API. In principe kan deze API volledig in JavaScript worden gedraaid, al De keuze om de PoS-tagging te baseren op de zin en niet het woord maakt het systeem minder vatbaar op afwisselend taalgebruik. Echter het gebruik van afwisselende woordenschat, wat prevalent is bij informatica-gerelateerde wetenschappelijke papers, maakt het systeem wel vatbaar op het niet kunnen terugvinden van deze woorden. Er wordt gesuggereerd om een valnet aan te maken, door ofwel de taal te veranderen naar Engels of Frans, ofwel door het GPT-3 model aan te spreken om een alternatieve definitie op te halen.
    """
    def look_up_word_rapidapi(self, word, sentence):
        try:

            """PoS-tag determination"""
            url = "https://lexicala1.p.rapidapi.com/search"
            lang = detect(sentence)
            
            """"""
            nlp = spacy.load(dict.get(lang, 'en'))
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
                "X-RapidAPI-Key": str(rapidapikey),
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
        