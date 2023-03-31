from pdfminer.high_level import extract_text, extract_pages
import TextAnalysis as tu
import Reader as ra
from pdfminer.layout import LTTextContainer, LTChar
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from io import BytesIO
import spacy
import numpy
from langdetect import detect


dutch_spacy_model = "nl_core_news_md"
english_spacy_model = "en_core_word_md"


def get_full_text_dict(all_pages):
    full_text = []
    for page_layout in all_pages:
        total_page = ""
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    total_page += text_line.get_text()
        full_text.append(total_page)

    return full_text


def get_full_clean_text(full_text):
    cleaned_text = []
    for i in full_text:
        nlp = spacy.load(dutch_spacy_model) if detect(i) == 'nl' else spacy.load(english_spacy_model)
        doc = nlp(i)
        sentences = doc.sents
        for s in sentences:
            if(len(s)>=6):
                cleaned_text.append(str(s).strip().replace('\n',' '))
    return cleaned_text

    

def get_sentence_length():
    pass

def get_stats_per_sentence(sentence):
    pass

def extractive_summarization(full_text):
    from summarizer import Summarizer
    from transformers import AutoTokenizer, AutoModel, TFAutoModel
    model = Summarizer()
    result = model(
        body=full_text,
        max_length=500,
        min_length=100,
        num_sentences=20,
        return_as_list=True
        )
    return result

def foo():
    from pdfminer.high_level import extract_text, extract_pages
    from pdfminer.layout import LTTextContainer, LTChar

    all_pages = extract_pages(
        pdf_file='lectoren-vives-bijdrage-onderzoek-ai-taalmodel.pdf',
        page_numbers=None,
        maxpages=999
    )

    t = get_full_text_dict(all_pages=all_pages)
    t = get_full_clean_text(t)
    t = extractive_summarization(' '.join(t))

    print(t)
    
foo()