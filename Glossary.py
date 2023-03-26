import pandoc, openai

COMPLETIONS_MODEL = "text-davinci-003"

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
