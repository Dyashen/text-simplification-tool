import openai, configparser

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

class GPT():

    """
    @sets openai.api_key
    """
    def __init__(self, key):
        if key is None:
            config = configparser.ConfigParser()
            config.read('config.ini')
            global gpt_api_key
            try:
                openai.api_key = config['openai']['api_key']
            except:
                gpt_api_key = 'no_key_submitted'
        else:
            openai.api_key = key

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
