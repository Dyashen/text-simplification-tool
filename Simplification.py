import configparser, openai
""""""
COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

""""""
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    openai.api_key = config['openai']['api_key']
except:
    openai.api_key = 'demo'

"""
@returns prompt, result from gpt 
"""
def look_up_word(word, context):
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
@returns prompt, result
"""
def syntactic_simplify(text):
    try:
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

    
