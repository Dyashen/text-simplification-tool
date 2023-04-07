# Web-app imports
from flask import Flask, render_template,request,jsonify,session

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
from Simplification import Simplification
import TextAnalysis as ta

MODEL_PATH = "pytorch_model.bin"
API_KEY_SESSION_NAME = 'api_key'
COLOR_SESSION_NAME = 'color'

app = Flask(__name__)
app.secret_key = "super secret key"

"""
returns homepage
"""
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/change-color', methods=['GET'])
def change_color():
    try:
        color = request.args.get(COLOR_SESSION_NAME)
        session['color'] = color
        return jsonify(color=session[COLOR_SESSION_NAME])
    except Exception as e:
        return jsonify(color='white')

"""
"""
@app.route('/set-gpt-api-key', methods=['GET'])
def change_api_key():
    try:
        api_key = request.args.get('key')
        session[API_KEY_SESSION_NAME] = api_key
        return jsonify(api_key=session[API_KEY_SESSION_NAME])
    except Exception as e:
        return jsonify(error=e)


"""
"""
@app.before_first_request
def load_model():
    print('--- first load ---')
    global summarizer
    summarizer = Summarizer(
        #MODEL_PATH
    )

"""
returns webpage
"""
@app.route('/for-teachers', methods=['GET','POST'])
def analysing_choosing_for_teachers():
    pdf = request.files['pdf']
    pdf_data = BytesIO(pdf.read()) 
    all_pages = extract_pages(
        pdf_data,
        page_numbers=None,
        maxpages=999
    )

    """[page, page, page, ..., page]"""
    full_text = read.get_full_text_dict(all_pages)
    full_text_new = read.get_full_text_site(full_text)

    """
    f = read.get_full_text_plain(all_pages)
    stats = ta.get_statistics(f)
    """

    return render_template(
        'for-teachers.html', 
        pdf=full_text_new, 
        lang='nl', 
        title='voorbeeld titel', 
        subject='voorbeeld van onderwerp'
        #, statistics=test
        #, statistieken=stats
    )

"""
@return 
"""
@app.route('/for-scholars', methods=['GET','POST'])
def teaching_tool():
    try:    
        """"""
        pdf = request.files['pdf']
        pdf_data = BytesIO(pdf.read())
        all_pages = extract_pages(
            pdf_data,
            page_numbers=None,
            maxpages=999
        )

        """"""
        full_text = read.get_full_text_dict(all_pages)
        full_text_new = read.get_full_text_site(full_text)

        """"""
        return render_template(
            'for-scholars.html',
            pdf=full_text_new, 
            lang='nl', 
            title='voorbeeld titel', 
            subject='voorbeeld van onderwerp',
            statistieken=''
        )
    except Exception as e:
        return render_template(
            'error.html',
            error=e
        )

"""
@returns prompt and word explanation from gpt-result
"""
@app.route('/look-up-word',methods=['GET'])
def look_up_word():
    try:
        api_key = session.get(API_KEY_SESSION_NAME, None) 

        word = request.args.get('word')
        context = request.args.get('context')
        result, prompt = lu.look_up_word(
            word=word, 
            context=context, 
            api_key=api_key
        )
        return jsonify(result=result, prompt=prompt)
    except Exception as e:
        return jsonify(
            result=f'Error {e}.',
            prompt=e
        )

"""
@returns prompt and simplified text from gpt-result
"""
@app.route('/syntactic-simplify', methods=['GET'])
def syntactic_simplify():
    try:
        api_key = session.get(API_KEY_SESSION_NAME, None) 
        text = request.args.get('text')

        sim = Simplification(api_key)
        result = sim.syntactic_simplify(text)
        return jsonify(
            result=result
        )
    except Exception as e:
        return jsonify(
            result=f'Error: {e}'
        )

"""
"""
@app.route('/extract-text', methods=['GET'])
def extract_sentences():
    text = request.args.get('text')
    result = sum.extractive_summarization(
        full_text=text, 
        summarizer=summarizer
    )
    return jsonify(result=result)

"""
"""
@app.route('/generate-summary', methods=['GET', 'POST'])
def generate_summary():
    try:
        full_text = request.args.get('fullText')
        if True or len(full_text) > 1900:
            result = sum.extractive_summarization(full_text=full_text)
        else:
            extracted_text = sum.extractive_summarization(full_text=full_text)
            result = sum.summarize_with_presets(full_text=extracted_text)
        return jsonify(
            original=full_text,
            result=result
            )
    except Exception as e:
        return jsonify(
            result='Je aanvraag kon niet verwerkt worden :(',
            prompt=e
        )


"""
"""
@app.route('/generate-glossary', methods=['GET','POST'])
def generate_glossary():
    glossary = request.form.get('glossaryList')

    words = glossary.split('\n')
    grouped_words = [words[i:i+5] for i in range(0, len(words), 5)]

    arr = []
    for set in grouped_words:
        arr.append(sum.generate_glossary_for_set(set))

    return jsonify( 
        glossary=arr
    )

"""
"""
if __name__ == "__main__":
    app.run()