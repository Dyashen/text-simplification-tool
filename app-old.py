# Web-app imports
from flask import Flask, render_template,request,jsonify

# PDF Miner
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from io import BytesIO

# 
from langdetect import detect
import openai, configparser, os, spacy, re, yake
from summarizer import Summarizer
from spacy.matcher import PhraseMatcher

app = Flask(__name__)

"""
used gpt-3 models
"""
# COMPLETIONS_MODEL = "gpt-3.5-turbo"
COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"
config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['openai']['api_key']

dutch_spacy_model = "nl_core_news_md"


"""
TODO
Data-cleaning
"""
def text_cleaning(text_from_pdf):
    text_from_pdf = str(text_from_pdf).replace('\n',' ')
    text_from_pdf = str(text_from_pdf).strip(' ')
    text_from_pdf = str(text_from_pdf).strip('.')
    return text_from_pdf

"""
Returns full-text without stopwords assigned by SpaCy's dutch library
"""
def remove_stopwords(text_with_stopwords):
    nlp = spacy.load(dutch_spacy_model) if detect(text_with_stopwords) == 'nl' else spacy.load("en_core_word_md")
    doc = nlp(text_with_stopwords)
    words_without_stopwords = [token.text for token in doc if not token.is_stop]
    return " ".join(words_without_stopwords)


"""
Return ten keywords
"""
def get_keywords(text_without_stopwords):
    lang = detect(" ".join(text_without_stopwords))
    max_ngram_size = 1
    deduplication_threshold = 0.9
    numOfKeywords = 10
    custom_kw_extractor = yake.KeywordExtractor(lan=lang, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text_without_stopwords)
    return keywords

"""
"""
def get_keyword_related_sentences(keywords, text):
    nlp = spacy.load(dutch_spacy_model)
    phrase_matcher = PhraseMatcher(nlp.vocab)
    phrases = ['Cupere','Natuurwetenschappen']
    patterns = [nlp(text) for text in phrases]
    for kw in keywords:
        phrase_matcher.add(kw, None, *patterns)

    doc = nlp(text)
    sentences = []
    for sent in doc.sents:
        for match_id, start, end in phrase_matcher(nlp(sent.text)):
            if nlp.vocab.strings[match_id] in keywords:
                sentences.append(sent.text)


"""

"""
def get_full_text(all_pages):
    total = ""
    for page_layout in all_pages:
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    total += text_line.get_text()
                    # total = re.sub('(.{0})-\s*', '', total) # sommige lijnen worden afgebroken door een liggend streepje --> preventie
    nlp = spacy.load(dutch_spacy_model) if detect(total) == 'nl' else spacy.load("en_core_word_md")

    total = text_cleaning(total)
    
    doc = nlp(total)
    word_arrays = []

    for sent in doc.sents:
        word_array = [token.text for token in sent]
        word_arrays.append(word_array)

    return word_arrays

"""
"""
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

"""

"""
def get_summary_of_abstract(all_pages):
    total = ""
    for page_layout in all_pages:
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    total += text_line.get_text()
                    total = re.sub('(.{0})-\s*', '', total)
    total = "".join(total)
    print(total[:400])
    prompt = f"""
    Schrijf dit zo eenvoudig mogelijk. Gebruik eenvoudige woordenschat en zinnen die niet langer dan 12 woorden zijn. Vermeld zeker de probleemstelling, resultaten en conclusie.
    context:
    {total[:400]}
    """
    return [total, prompt_gpt(prompt=prompt, model=COMPLETIONS_MODEL, max_tokens=999, temperature=0)]


"""
todo
"""
def get_toc(document):
    arr_outlines = []
    if "Outlines" in document.catalog:
        outlines = document.get_outlines()
        for (level,title,dest,a,se) in outlines:
            arr_outlines.append([level, title])

"""

"""
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

"""
"""
@app.route('/view-pdf', methods=['GET','POST'])
def show_pdf():
    pdf = request.files['pdf']
    pdf_data = BytesIO(pdf.read())

    all_pages = extract_pages(
        pdf_data,
        page_numbers=None,
        maxpages=5
    )

    sentences = get_full_text(all_pages)
    # text = " ".join(sentences)

    keywords = ""

    return render_template(
        'pdf-viewer.html',
        full_text = sentences,
        keywords  = keywords
    )

"""
"""
@app.route('/for-teachers', methods=['GET','POST'])
def summarize_abstract():
    pdf = request.files['pdf']
    pdf_data = BytesIO(pdf.read()) 
    all_pages = extract_pages(
        pdf_data,
        page_numbers=None,
        maxpages=100
    )

    sentences = get_full_text(all_pages)

    return render_template('for-teachers.html', original=sentences, lang='nl', title='voorbeeld titel', subject='voorbeeld van onderwerp')


"""
"""
@app.route('/summarise-with-presets', methods=['GET','POST'])
def summarize_with_presets():
    presets = request.args
    print(presets)
    print(jsonify(presets))
    return render_template('index.html')

"""
TODO: 'eenvoudig' toevoegen
"""
@app.route('/look-up-word',methods=['GET'])
def look_up_word():
    word = request.args.get('word')
    context = request.args.get('context')
    prompt = f"""
    Leg het begrip '{word}' eenvoudig uit in de context van "{context}"? 
    Lengte: max. 1 zin. Geef 3 eenvoudigere synoniemen.
    """

    result = prompt_gpt(
            prompt=prompt,
            max_tokens=200,
            model=COMPLETIONS_MODEL,
            temperature=0)
    return jsonify(result=result, prompt=prompt)


@app.route('/summarize',methods=['GET'])
def summarize():
    text = request.args.get('text')
    sentences = 5
    max_words = 10
    prompt = f"""
    Samenvat deze tekst: 
    Lengte: max {sentences} zinnen en max {max_words} woorden per zin.
    context:
    {text}
    """
    text = prompt_gpt(
        model=COMPLETIONS_MODEL,
        max_tokens=500,
        prompt=prompt,
        temperature=0
    )

    return jsonify(result=text, prompt=prompt)

@app.route('/extract-text', methods=['GET'])
def extract():
    text = request.args.get('text')   
    summarizer = Summarizer()
    result = summarizer(
        #algorithm=...,
        body=text,
        #max_length=460,
        min_length=100,
        num_sentences=10,
        #ratio=...,
        #return_as_list=...,
        #use_first=...,
    )
    return jsonify(result=result)


@app.route('/syntactic-simplify', methods=['GET'])
def syntactic_simplify():
    text = request.args.get('text')
    max_words = 10
    prompt = f"""
    Breek zinnen langer dan {max_words} woorden op. Verander verwijswoorden naar de oorspronkelijke naam.
    Vervang tangconstructies door de bijzin naar het begin of het einde te plaatsen. 
    Vervang voorzetseluitdrukkingen en samengestelde werkwoorden.
    context:
    {text}
    """
    text = prompt_gpt(
        model=COMPLETIONS_MODEL,
        max_tokens=500,
        prompt=prompt,
        temperature=0
    )
    return jsonify(result=text, prompt=prompt)

@app.route('/foo', methods=['GET'])
def foo():
    return render_template('tryout.html')

if __name__ == "__main__":
    app.run()