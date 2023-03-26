# Web-app imports
from flask import Flask, render_template,request,jsonify

# PDF Miner
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from io import BytesIO

# 
from langdetect import detect
from summarizer import Summarizer
from spacy.matcher import PhraseMatcher

#
import Reader as read
import Summarization as sum
import Glossary as gloss
import LookUp as lu

app = Flask(__name__)

dutch_spacy_model = "nl_core_news_md"


"""
returns homepage
"""
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

"""
returns webpage
"""
@app.route('/for-teachers', methods=['GET','POST'])
def teaching_tool():
    pdf = request.files['pdf']
    pdf_data = BytesIO(pdf.read()) 

    all_pages = extract_pages(
        pdf_data,
        page_numbers=None,
        maxpages=100
    )

    """[page, page, page, ..., page]"""
    full_text = read.get_full_text_dict(all_pages)
    full_text_new = read.get_full_text(full_text)
    
    return render_template(
        'for-teachers.html', 
        pdf=full_text_new, 
        lang='nl', 
        title='voorbeeld titel', 
        subject='voorbeeld van onderwerp',
        statistieken=''
    )

"""
@return 
"""
@app.route('/for-scholars', methods=['GET','POST'])
def show_pdf():
    pdf = request.files['pdf']
    pdf_data = BytesIO(pdf.read())

    all_pages = extract_pages(
        pdf_data,
        page_numbers=None,
        maxpages=100
    )

    full_text = read.get_full_text_dict(all_pages)
    full_text_new = read.get_full_text(full_text)

    return render_template(
        'for-scholars.html',
        pdf=full_text_new, 
        lang='nl', 
        title='voorbeeld titel', 
        subject='voorbeeld van onderwerp',
        statistieken=''
    )


"""
"""
@app.route('/look-up-word',methods=['GET'])
def look_up_word():
    word = request.args.get('word')
    context = request.args.get('context')
    result, prompt = lu.look_up_word(word, context)
    return jsonify(result=result, prompt=prompt)



"""
Only for tryout purposes
return
"""
@app.route('/foo', methods=['GET'])
def foo():
    return render_template('tryout.html')


"""
"""
@app.route('/generate-glossary', methods=['GET','POST'])
def generate_glossary():
    glossary = request.form.get('glossaryList')

    words = glossary.split('\n')
    grouped_words = [words[i:i+5] for i in range(0, len(words), 5)]

    arr = []
    for set in grouped_words:
        arr.append(gloss.generate_glossary_for_set(set))

    gloss.generate_pdf()
    return render_template(
        'download-pdf.html', 
        glossary=arr
        )


"""
"""
if __name__ == "__main__":
    app.run()