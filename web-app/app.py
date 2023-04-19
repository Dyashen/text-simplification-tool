"""flask"""
from flask import Flask, render_template, render_template_string, request, jsonify, session, send_file

from langdetect import detect_langs, detect


"""pdf"""
from Reader import Reader
from io import BytesIO
from pdfminer.high_level import extract_pages

""""""
from datetime import timedelta


""""""
from Summarization import HuggingFaceModels, GPT, Lexicala
from Writer import Creator
import Analysis as an



""""""
app = Flask(__name__)
app.secret_key = "super secret key"
API_KEY_SESSION_NAME = 'api_key'
COLOR_SESSION_NAME = 'color'

""""""
@app.before_request
def pre_boot_up():
    session.permanent=True
    global simplifier, lexi
    simplifier = HuggingFaceModels()
    lexi = Lexicala(None)

    

""""""
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


""""""
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
        reader = Reader()
        full_text = reader.get_full_text_dict(all_pages)
        full_text_new = reader.get_full_text_site(full_text)

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


""""""
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
    reader = Reader()
    full_text = reader.get_full_text_dict(all_pages)
    full_text_new = reader.get_full_text_site(full_text)

    return render_template(
        'for-teachers.html', 
        pdf=full_text_new, 
        lang='lang',
        title='Test', 
        subject='Test'
    )

"""
"""
@app.route('/generate-summary', methods=['GET','POST'])
def generate_summary():
        api_key = session.get(API_KEY_SESSION_NAME, None) 

        personalized = request.form.get('personalizedSummary')

        if personalized is None:        
            title = request.form.get('title')
            wordlist = request.form.get('glossaryList')
            wordlist = wordlist.strip(' ').split('\n')

            print(wordlist)
            print('-'*100)

            """

            if len(wordlist) != 0:
                arr = []
                for field in wordlist:
                    if len(field.split(':'))>1:
                        word = field.split(':')[0]
                        pos = field.split(':')[2]
                        arr.append([word, pos])
                glossary = sum.generate_glossary(list=arr)
            else:
            """
            glossary = [['example','definition']]

            full_text = request.form.get('fullText')

            full_text = simplifier.summarize(text=full_text, lm_key='peg') # pegasus model --> dict structure

            Creator().create_pdf(title=title, list=glossary, full_text=full_text)

            return send_file(path_or_file='saved_files/output.pdf', as_attachment=True)

        else:
            return jsonify(result='aangevinkt')


# TEXT FUNCTIONS
@app.route('/extract-text', methods=['POST'])
def extract_sentences():
    text = request.json['text']
    key = request.json['key']
    result = simplifier.summarize(text=text, key=key)
    return jsonify(result=result)

"""
"""
@app.route('/simplify', methods=['POST'])
def scientific_simplify():
    text = request.json['text']
    key = request.json['key']
    result = simplifier.summarize(text=text, key=key)
    return jsonify(result=result)

"""
"""
@app.route('/get-pos-tag', methods=['GET','POST'])
def get_pos_tag():
    try:
        word = request.args.get('word')
        sentence = request.args.get('context')
        pos_tag = an.get_spacy_pos_tag(
            word=word,
            sentence=sentence
        ).lower()
        return jsonify(pos=pos_tag)
    except Exception as e:
        return jsonify(pos='noun')

"""
"""
@app.route('/personalized-simplify', methods=['POST'])
def personalized_simplify():
    try:
        api_key = session['api_key']
    except:
        api_key = None

    gpt = GPT(api_key)
    text = request.json['text']
    choices = request.json['choices']
    result, prompt = gpt.personalised_simplify(sentence=text, personalisation=choices)
    return jsonify(prompt=prompt, result=result)

"""
@returns prompt and word explanation from gpt-result
"""
@app.route('/look-up-word',methods=['POST'])
def look_up_word():
    
        sentence = request.json['sentence']
        word = request.json['word']
        
        result = lexi.look_up_word_rapidapi(
            sentence=sentence, 
            word=word
        )

        # if no result, try again here with gpt-3
        if 'n_results' in result:
            if False and result['n_results'] > 0:
                return jsonify(result=result, source='Lexicala')
        
        try:
            api_key = session['api_key']
        except:
            api_key = None

        gpt = GPT(api_key)
        result, prompt = gpt.look_up_word_gpt(word=word,context=sentence)
        return jsonify(result=result, source='gpt', prompt=prompt)

# Color changes
""""""
@app.route('/change-color', methods=['POST'])
def change_color():
    try:
        data = request.get_json()
        color = data['color']
        session['color'] = color
        return jsonify(color=session[COLOR_SESSION_NAME])
    except Exception as e:
        return jsonify(color='white')

@app.route('/get-background-color', methods=['POST'])
def get_color():
    try:
        color = session['color']
        return jsonify(color=color)
    except:
        return jsonify(color='white')



# Flask-App RunTime-related
app.permanent_session_lifetime = timedelta(minutes=20)
if __name__ == "__main__":
    app.run()