import pandas as pd

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
import spacy
from langdetect import detect
import pandas as pd
import os
import readability


folder_path = 'scripts\experimenten\pdf'
dutch_spacy_model = "nl_core_news_md"
english_spacy_model = "en_core_web_sm"

dict = {
    'nl':'nl_core_news_md',
    'en':'en_core_web_md'
}

"""
"""
def get_sentence_length(sentence):
    nlp = spacy.load(english_spacy_model)
    doc = nlp(sentence)
    return len(doc)


"""
"""
def text_clean(text):    
    full_text = text.strip()
    full_text = text.replace('\n', ' ')
    
    return full_text

"""
"""
def get_sentences(text):
    nlp = spacy.load(dutch_spacy_model) if detect(text) == 'nl' else spacy.load('en_core_web_sm')
    doc = nlp(text)
    sentences = []
    for sentence in doc.sents:
        sentences.append(str(sentence))
    return sentences

"""
TODO
"""
def get_key_sentences():
    pass


"""
TODO
"""
def get_key_words():
    pass


"""
Dataframe opbouwen voor een pdf. Hieronder wordt de zin, bron en zinlengte opgeslaan.
"""
def get_statistics(full_text):
    full_text = text_clean(full_text)
    lang = detect(full_text)
    sentences = get_sentences(full_text)
    df = pd.DataFrame(sentences, columns=['sentence'])
    df['sentence_length'] = df['sentence'].apply(get_sentence_length)

    """
    Filteren. Zinnen kleiner dan 3 woord-tokens zijn niet mogelijk. Deze worden verworpen.
    """
    df = df[df['sentence_length'] > 3]   


    """
    """
    for key in readability.getmeasures("test")['readability grades'].keys():
        df[key] = df['sentence'].apply(lambda x: readability.getmeasures(x)['readability grades'][key])

    """
    """
    word_usage_cols = readability.getmeasures("test")['word usage'].keys()
    for key in word_usage_cols:
        df[key] = df['sentence'].apply(lambda x: readability.getmeasures(x, lang=lang)['word usage'][key])

    """
    """
    sentence_beginnings_cols = readability.getmeasures("test")['sentence beginnings'].keys()
    for key in sentence_beginnings_cols:
        df[key] = df['sentence'].apply(lambda x: readability.getmeasures(x, lang=lang)['sentence beginnings'][key])

    """
    """
    avg = df[word_usage_cols].avg()
    sum = df[sentence_beginnings_cols].sum()
    return (avg, sum)
