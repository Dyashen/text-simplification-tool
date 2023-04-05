import configparser, openai
from googletrans import Translator
from langdetect import detect

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

"""
@retuns full-text
"""
def summarize_with_presets(full_text, presets):
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
def translate_sentence(sentence):
    translator  = Translator()
    result = translator.translate(text=sentence, dest=LANG)
    return result.text # result.origin


"""
@returns list of sentences
"""
def extractive_summarization(full_text, summarizer):

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
                    new.append(translate_sentence(i))
                else:
                    new.append(i)
            return ' '.join(new)
        except Exception as e:
            return f'Problemen met Google Translate {e}'

    
    except Exception as e:
        return f'Problemen met BERT {e}'
        


def generate_glossary_for_set(set):
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
