import subprocess, io, os, pypandoc

class Creator():

    """"""
    def create_header(self, title):
        with open('file.md', 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f"title: Simplified version of {title}\n")
            f.write("mainfont: Montserrat-Regular.ttf\n")
            f.write("titlefont: Montserrat-Black.ttf\n")
            f.write("---\n")

    """"""
    def generate_glossary(self, list):
        with open('file.md', 'a', encoding='utf-8') as f:
            f.write("# Glossary\n")
            f.write("| Woord | Definitie |\n")
            f.write("| --- | --- |\n")
            for word, definition in list: 
                f.write(f"| {word} | {definition} |\n")

    """"""
    def generate_text(self, full_text):
        with open('file.md','a', encoding='utf-8') as f:
            for i in range(len(full_text)):
                if len(full_text[i]) > 1:
                    title = full_text[i][0]
                    text = full_text[i][1]
                    f.write('\n\n')
                    f.write(f'## {title}')
                    f.write('\n\n')
                    f.write(text)
                    f.write('\n\n')
                else:
                    f.write('\n\n')
                    f.write(f'{full_text[i]}')
                    f.write('\n\n')


    def create_pdf(self, title, list, full_text):
        """"""
        if title is not None:
            self.create_header(title=title)
        else:
            self.create_header(title='Simplified text')
        
        """"""
        if len(list) != 0:
            self.generate_glossary(list=list)

        """"""
        self.generate_text(full_text=full_text)
        
        """"""
        pypandoc.convert_file('file.md', 
                                'pdf', 
                                outputfile='output.pdf', 
                                extra_args=['--pdf-engine=xelatex'])