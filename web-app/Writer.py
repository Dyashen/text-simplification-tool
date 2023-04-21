import subprocess, io, os, pypandoc
from datetime import date
import zipfile


markdown_file = "web-app/saved_files/file.md"
zip_filename = 'web-app/saved_files/simplified_docs.zip'
pdf_file = "web-app/saved_files/output.pdf"
docx_file = "web-app/saved_files/output.docx"
DEFAULT_FONT = "Montserrat-Regular.ttf"
DEFAULT_TITLE_FONT = "Montserrat-Black.ttf"
DATE_NOW = str(date.today())


class Creator():
    
    """"""
    def create_header(self, title, margin=0.5, fontsize=14, chosen_font=DEFAULT_FONT, chosen_title_font=DEFAULT_TITLE_FONT):
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f"title: Simplified version of {title}\n") 
            f.write(f"mainfont: {chosen_font}\n")
            f.write(f"titlefont: {chosen_title_font}\n")
            f.write(f'date: {DATE_NOW}\n')
            f.write(f'document: article\n')
            f.write(f'geometry: margin={margin}in\n')
            f.write(f'fontsize: {fontsize}pt\n')
            f.write("---\n")

    """"""
    def generate_glossary(self, list):
        with open(markdown_file, 'a', encoding='utf-8') as f:
            f.write("---\n")
            f.write("# Glossary\n")
            f.write("| Woord | Soort | Definitie |\n")
            f.write("| --- | --- | --- |\n")
            for word in list.keys(): 
                f.write(f"| {word} | {list[word]['type']} | {list[word]['definition']} |\n")

    """"""
    def generate_summary(self, full_text):
        with open(markdown_file,'a', encoding="latin-1", errors="surrogateescape") as f:
            for key in full_text.keys():
                title = str(key).replace('\n',' ')
                text = full_text[key]
                f.write('\n\n')
                f.write(f'## {title}')
                f.write('\n\n')
                f.write(" ".join(text))
                f.write('\n\n')


    def create_pdf(self, title, list, full_text, fonts, options):
        """"""
        if title is not None:
            self.create_header(title=title, chosen_font=fonts[0], chosen_title_font=fonts[1])
        else:
            self.create_header(title='Simplified text', chosen_font=fonts[0], chosen_title_font=fonts[1])
        
        """"""
        print(list)
        if len(list) != 0:
            self.generate_glossary(list=list)

        """"""
        self.generate_summary(full_text=full_text)
        
        """"""
        if 'Word' in options:
            pypandoc.convert_file(source_file=markdown_file, to='docx', outputfile=docx_file)

        if 'PDF' in options:
            pypandoc.convert_file(source_file=markdown_file, to='pdf', outputfile=pdf_file, extra_args=['--pdf-engine=xelatex'])

        if len(options) > 1:
            with zipfile.ZipFile(zip_filename, 'w') as myzip:
                myzip.write(pdf_file)
                myzip.write(docx_file)
