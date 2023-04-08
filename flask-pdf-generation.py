import subprocess, pypandoc, io
from flask import Flask, send_file
import os
import pypandoc, lorem

os.environ['PYPANDOC_PANDOC_ARGS'] = '--pdf-engine=xelatex'


def create_header(title):
    with open('file.md', 'w') as f:
        f.write("---\n")
        f.write(f"title: Simplified version of {title}\n")
        f.write("mainfont: Montserrat-Regular.ttf\n")
        f.write("titlefont: Montserrat-Black.ttf\n")
        f.write("---\n")


def generate_glossary(list):
    with open('file.md', 'a') as f:
        f.write("# Glossary\n")
        f.write("| Woord | Definitie |\n")
        f.write("| --- | --- |\n")
        for word, definition in list: 
            f.write(f"| {word} | {definition} |\n")

def generate_text(full_text):
    with open('file.md','a') as f:
        f.write("# Title\n")
        for i in full_text:
            f.write(f"{i}\n")


create_header('AI voor tekstvereenvoudiging')
generate_glossary([['test','foo'],['foo','bar'], ['bar','test']])


full_text = []
for i in range(5):
    full_text.append(lorem.paragraph())

generate_text(full_text=full_text)

output = pypandoc.convert_file('file.md', 'pdf', outputfile='output.pdf')

app = Flask(__name__)

@app.route('/convert')
def convert():
    output = io.BytesIO()
    output = pypandoc.convert_file('file.md', 'pdf', outputfile='output.pdf')
    return send_file(path_or_file='output.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run()