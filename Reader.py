from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from io import BytesIO
import spacy
from langdetect import detect



dutch_spacy_model = "nl_core_news_md"
english_spacy_model = "en_core_word_md"

# assert spacy.util.is_package(dutch_spacy_model)
# assert spacy.util.is_package(english_spacy_model)

"""
"""
def get_full_text_plain(all_pages):
    full_text = ""
    for page_layout in all_pages:
        total_page = ""
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    total_page += text_line.get_text()
        full_text += total_page
    return full_text


""""""
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


def get_full_text(full_text):
    full_text_new = []

    # opbreken pagina --> paragraaf         [ptekst, pnummer]
    
    for i in range (len(full_text)):

        page = []
        nlp = spacy.load(dutch_spacy_model) if detect(full_text[i]) == 'nl' else spacy.load(english_spacy_model)
        doc = nlp(full_text[i])

        sentences = doc.sents

        paragraph = []
        for sent in sentences:
            sentence = []
            for token in sent:
                sentence.append(token.text)

            if len(paragraph) > 4:
                page.append(paragraph)
                paragraph = []
                paragraph.append(sentence)
            else:
                paragraph.append(sentence)

        page.append(paragraph)
        full_text_new.append([page, i])

    return full_text_new