import configparser, openai

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"
config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['openai']['api_key']

def look_up_word(word, context):
    prompt = f"""
    Leg het begrip '{word}' eenvoudig uit in de context van "{context}"? 
    Lengte: max. 1 zin. Geef 3 eenvoudigere synoniemen.
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