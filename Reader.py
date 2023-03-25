from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from io import BytesIO

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