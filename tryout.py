from pdfminer.high_level import extract_text, extract_pages
import TextAnalysis as tu
import Reader as ra
from pdfminer.layout import LTTextContainer, LTChar
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from io import BytesIO
import io, os, spacy, numpy, configparser, fnmatch
from langdetect import detect
import unicodedata
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from fpdf import FPDF
from os.path import exists

import openai

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"
config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['openai']['api_key']


dutch_spacy_model = "nl_core_news_md"
english_spacy_model = "en_core_web_sm"


""""""
def unicode_normalize(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')


""""""
pdf_w=210
pdf_h=297
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        w = self.get_string_width('') + 6
        self.set_x((210 - w) / 2)
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        self.set_line_width(1)
        self.cell(w, 9, '', 1, 1, 'C', 1)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        self.set_font('Arial', '', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        txt = text
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 5, txt)
        self.ln()
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)


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


def get_full_clean_text(full_text):
    cleaned_text = []
    for i in full_text:
        nlp = spacy.load(dutch_spacy_model) if detect(i) == 'nl' else spacy.load(english_spacy_model)
        doc = nlp(i)
        sentences = doc.sents
        for s in sentences:
            if(len(s)>=6):
                cleaned_text.append(str(s).strip() \
                                    .replace('\n',' '))
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
        max_length=700,
        min_length=100,
        num_sentences=30,
        return_as_list=True
        )
    return result

def main_extractive_summary():
    from pdfminer.high_level import extract_text, extract_pages
    from pdfminer.layout import LTTextContainer, LTChar


    import os
    import fnmatch

    folder_path = "C:/hogeschool-gent/bachelorproef-nlp-tekstvereenvoudiging/scripts/experimenten/pdf/"
    file_list = os.listdir(folder_path)
    pdf_files = [f for f in file_list if fnmatch.fnmatch(f, "Original*.pdf")]

    for file in pdf_files:

        all_pages = extract_pages(
            pdf_file=folder_path + file,
            page_numbers=None,
            maxpages=999
        )

        t = get_full_text_dict(all_pages=all_pages)
        t = get_full_clean_text(t)
        t = extractive_summarization(' '.join(t))

        sublist = [t[n:n+5] for n in range(0, len(t), 5)]

        """
        pdf = PDF(orientation='P', unit='mm', format='A4')
        pdf.set_title('test')
        pdf.set_author('test')
        for i in range(0, len(sublist)):
            data = io.StringIO()
            data.write(unicode_normalize(' '.join(sublist[i])))
            pdf.print_chapter(i+1, '', data)
        pdf.set_author('Simply Flied')
        pdf.output('test.pdf','F')
        """

        fname = 'ExtractiveSum_' + str(file).split('_')[1]\
                                            .split('.')[0]\
                                            + '.txt'

        with open(fname, "w") as file:
            for element in sublist:
                file.write(" ".join(element) + "\n")

def prompt_gpt(text):
    prompt = f"""
    Prompt: 
    Parafraseer de zinnen in het Nederlands met eenvoudige woordenschat. De output moet aan volgende regels voldoen: zinnen zijn niet langer dan tien woorden, regelmatige woordenschat, schrijf cijfermateriaal voluit, schrijf acroniemen voluit vermijd tangconstructies, voorzetsel- en verwijswoorden
    Zinnen:
    {text}
    """

    return openai.Completion.create(
            prompt=prompt,
            temperature=0,
            max_tokens=1000,
            model=COMPLETIONS_MODEL,
            top_p=0.9,
            stream=False
    )["choices"][0]["text"].strip(" \n")

def main_abstractive_summary():
    folder_path = "C:/hogeschool-gent/bachelorproef-nlp-tekstvereenvoudiging/scripts/experimenten/pdf/"
    file_list = os.listdir(folder_path)
    pdf_files = [f for f in file_list if fnmatch.fnmatch(f, "Original*.pdf")]

    for file in pdf_files:
        fname = 'AbstractiveSumm_' + str(file).split('_')[1]\
                                        .split('.')[0]\
                                        + '.txt'
        print(f'starting ... {folder_path + fname} ...')
        
        all_pages = extract_pages(
                pdf_file=folder_path + file,
                page_numbers=None,
                maxpages=999
        )

        t = get_full_text_dict(all_pages=all_pages)
        t = get_full_clean_text(t)
        
        sublist = [t[n:n+5] for n in range(0, len(t), 5)]

        total = ""
        for p in sublist:
            r = prompt_gpt(' '.join(p))
            total += r + '\n'
        
        with open(fname, "w", encoding="utf-8") as file:
            file.write(str(total))



def main_hybrid_summary():
    folder_path = "C:/hogeschool-gent/bachelorproef-nlp-tekstvereenvoudiging/scripts/experimenten/pdf/"
    file_list = os.listdir(folder_path)
    pdf_files = [f for f in file_list if fnmatch.fnmatch(f, "Original*.pdf")]

    for file in pdf_files:
        fname = 'HybridSum_' + str(file).split('_')[1]\
                                        .split('.')[0]\
                                        + '.txt'
        
        print(f'starting ... {folder_path + fname} ...')

        if not exists(folder_path + file):
            all_pages = extract_pages(
                pdf_file=folder_path + file,
                page_numbers=None,
                maxpages=999
            )

            t = get_full_text_dict(all_pages=all_pages)
            t = get_full_clean_text(t)
            t = extractive_summarization(' '.join(t))

            sublist = [t[n:n+5] for n in range(0, len(t), 5)]

            total = ""

            for i in range(0, len(sublist)):
                result = prompt_gpt(sublist[i])
                total += result + '\n'
            
            with open(fname, "w", encoding="utf-8") as file:
                file.write(str(total))
    
# main_extractive_summary()
# main_hybrid_summary()
main_abstractive_summary()