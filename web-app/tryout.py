import spacy
from spacy.matcher import PhraseMatcher
import Reader as re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import StringIO

def read_pdf(file_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(file_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text

full_text = read_pdf('PRINCE2_tijdelijke_tekst.pdf')

nlp = spacy.load("nl_core_news_sm")

phrase_matcher = PhraseMatcher(nlp.vocab)
phrases = ['business', 'analysis']
patterns = [nlp(text) for text in phrases]
phrase_matcher.add('BUSINESS_ANALYSIS', None, *patterns)

kernzinnen = []
doc = nlp(full_text)
for sent in doc.sents:
    matches = phrase_matcher(nlp(sent.text))
    if matches:
        kernzinnen.append(sent.text)

print(kernzinnen)
