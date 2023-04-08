import subprocess, io, os, pypandoc

class Creator():

    """"""
    def create_header(self, title):
        with open('file.md', 'w') as f:
            f.write("---\n")
            f.write(f"title: Simplified version of {title}\n")
            f.write("mainfont: Montserrat-Regular.ttf\n")
            f.write("titlefont: Montserrat-Black.ttf\n")
            f.write("---\n")

    """"""
    def generate_glossary(self, list):
        with open('file.md', 'a') as f:
            f.write("# Glossary\n")
            f.write("| Woord | Definitie |\n")
            f.write("| --- | --- |\n")
            for word, definition in list: 
                f.write(f"| {word} | {definition} |\n")

    """"""
    def generate_text(self, full_text):
        with open('file.md','a') as f:
            f.write("# Title\n")
            for i in full_text:
                f.write(f"{i}\n")


    def create_pdf(self, title, list, full_text):
        """"""
        if title is not None:
            self.create_header(title=title)
        else:
            self.create_header('Simplified text')

        """"""
        if len(list) is not 0:
            self.generate_glossary(list=list)

        """"""
        self.generate_text(full_text=full_text)

        """"""
        pypandoc.convert_file('file.md', 'pdf', outputfile='output.pdf')