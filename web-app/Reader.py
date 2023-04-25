from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from io import BytesIO
import spacy, re
from langdetect import detect

dict = {
    'nl':'nl_core_news_md',
    'en':'en_core_web_md'
}

class Reader():
    """
    input: generator-object
    output: format used for site
    """
    def get_full_text_dict(self, all_pages):
        full_text = []
        for page_layout in all_pages:
            total_page = ""
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        total_page += text_line.get_text()
                        total_page = re.sub(r'[^a-zA-Z0-9\s.,;]', '', total_page)
            full_text.append(total_page)
        return full_text
    

    def get_full_text_site(self, full_text):
        full_text_new = []

        # opbreken pagina --> paragraaf [ptekst, pnummer]
        for i in range (len(full_text)):
            page = []
            try:
                lang = detect(full_text[i])
            except:
                pass

            if lang in dict:
                nlp = spacy.load(dict.get(lang))
            else:
                nlp = spacy.load(dict.get('en'))

            doc = nlp(full_text[i])
            sentences = doc.sents

            paragraph = []
            for sent in sentences:
                sentence = {}
                for token in sent:
                    sentence[token.text] = str(token.pos_).lower()

                if len(paragraph) > 4:
                    page.append(paragraph)
                    paragraph = []
                    paragraph.append(sentence)
                else:
                    paragraph.append(sentence)

            page.append(paragraph)
            full_text_new.append([page, i])
        return full_text_new