import pandoc, openai

COMPLETIONS_MODEL = "text-davinci-003"

def prompt_gpt(prompt, model, max_tokens, temperature):
    # https://platform.openai.com/docs/api-reference/completions
    return openai.Completion.create(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
            top_p=0.9,
            stream=False
        )["choices"][0]["text"].strip(" \n")

def generate_glossary_for_set(set):
    words = ", ".join(set)
    prompt = f"""
    Geef voor de volgende woorden een eenvoudige uitleg van hoogstens twee zinnen: {words}.
    formaat:
    woord: uitleg. synoniemen: ...\n
    """

    result = prompt_gpt(
            prompt=prompt,
            max_tokens=200,
            model=COMPLETIONS_MODEL,
            temperature=0,
            top_p=0.25
    )
    
    print(result)

    return result.split('\n')

def generate_pdf():
    return 'foo'
