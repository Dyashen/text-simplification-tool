import pandoc, openai

COMPLETIONS_MODEL = "text-davinci-003"

"""
@retuns full-text
"""
def summarize_with_presets(full_text, presets):
    prompt = f"""
    Samenvat de volgende tekst in {presets[0]} paragrafen met elk {presets[1]} zinnen van max {presets[2]} lang.
    {full_text}
    """

    result = 'foo'

    return prompt, result

    result = openai.Completion.create(
            prompt=prompt,
            temperature=0,
            max_tokens=1000,
            model=COMPLETIONS_MODEL,
            top_p=0.9,
            stream=False
    )["choices"][0]["text"].strip(" \n")


"""
@returns list of sentences
"""
def extractive_summarization(full_text):
    from summarizer import Summarizer
    model = Summarizer()
    result = model(
        body=full_text,
        max_length=700,
        min_length=100,
        num_sentences=30,
        return_as_list=True
    )

    return result


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
