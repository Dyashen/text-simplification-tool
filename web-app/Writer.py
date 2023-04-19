import subprocess, io, os, pypandoc

markdown_file = "web-app/saved_files/file.md"
pdf_file = "web-app/saved_files/output.pdf"

class Creator():

    """"""
    def create_header(self, title, margin=0.5, fontsize=14):
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f"title: Simplified version of {title}\n") 
            f.write("mainfont: Montserrat-Regular.ttf\n")
            f.write("titlefont: Montserrat-Black.ttf\n")
            f.write(f'date: June 1, 2022\n')
            f.write(f'document: article\n')
            f.write(f'geometry: margin={margin}in\n')
            f.write(f'fontsize: {fontsize}pt\n')
            f.write("---\n")

    """"""
    def generate_glossary(self, list):
        with open(markdown_file, 'a', encoding='utf-8') as f:
            f.write("---\n")
            f.write("# Glossary\n")
            f.write("| Woord | Definitie |\n")
            f.write("| --- | --- |\n")
            for word, definition in list: 
                f.write(f"| {word} | {definition} |\n")

    """"""
    def generate_summary(self, full_text):
        with open(markdown_file,'a', encoding="latin-1", errors="surrogateescape") as f:
            for key in full_text.keys():
                title = key
                text = str(full_text[key])
                f.write('\n\n')
                f.write(f'## {title}')
                f.write('\n\n')
                f.write(text)
                f.write('\n\n')


    def create_pdf(self, title, list, full_text):
        """"""
        if title is not None:
            self.create_header(title=title)
        else:
            self.create_header(title='Simplified text')
        
        """"""
        print(list)
        if len(list) != 0:
            self.generate_glossary(list=list)

        """"""
        self.generate_summary(full_text=full_text)
        
        """"""
        pypandoc.convert_file(source_file=markdown_file, 
                              to='pdf', 
                              outputfile=pdf_file, 
                              extra_args=['--pdf-engine=xelatex'])
        