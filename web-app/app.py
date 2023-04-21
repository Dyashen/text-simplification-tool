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
from Summarization import HuggingFaceModels, GPT, Lexicala, WordScraper
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
    global simplifier, lexi, wap
    simplifier = HuggingFaceModels()
    lexi = Lexicala(None)
    wap = WordScraper()

    

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
        
        settings = dict(request.form)
        fonts = (settings['titleFont'], settings['regularFont'])

        if 'personalized' not in settings:        
            title = settings['titleOfPaper']
            wordlist = settings['glossaryList']
            wordlist = wordlist.strip(' ').split('\n')
            
            glossary = {}
            for word in wordlist:
                try:
                    word_text = str(word).split(':')[0]
                    word_type = str(word).split(':')[2]
                    word_definition = wap.look_up(str(word_text))[0]
                    glossary[word_text] = {'type':word_type, 'definition':str(word_definition)}
                except Exception as e:
                    print(e)

            
            full_text = settings['fullText']            
            full_text = simplifier.summarize(text=full_text, lm_key='bart') # pegasus model --> dict structure

            
            chosen_options = []
            if 'saveToPDF' in settings:
                chosen_options.append('PDF')

            if 'saveToWord' in settings:
                chosen_options.append('Word')                            


            Creator().create_pdf(title=title, list=glossary, full_text=full_text, fonts=fonts, options=chosen_options)

            if 'PDF' in chosen_options and 'Word' in chosen_options:
                return send_file(path_or_file='saved_files/simplified_docs.zip', as_attachment=True)

            if 'PDF' in chosen_options:
                return send_file(path_or_file='saved_files/output.pdf', as_attachment=True)

            if 'Word' in chosen_options:
                return send_file(path_or_file='saved_files/output.docx', as_attachment=True)
            
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
    result = simplifier.scientific_simplify(text=text, lm_key=key)
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
    word = request.json['word']
    try:
        word_definition = wap.look_up(str(word))[0]
    except Exception as e:
        print(e)
    return jsonify(result=word_definition, source='Woorden.org', word=word)

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

""""""
@app.route('/get-background-color', methods=['POST'])
def get_color():
    try:
        color = session['color']
        return jsonify(color=color)
    except:
        return jsonify(color='white')


@app.route('/set-gpt-api-key', methods=['GET'])
def set_gpt_api_key():
    try:
        api_key = request.args.get('key')
        session['gpt3'] = api_key
        return jsonify(result=api_key)
    except:
        return jsonify(result='notgood')



""""""
@app.route('/get-session-keys', methods=['GET'])
def get_session_keys():
    try:
        return jsonify(dict(session))
    except:
        return jsonify(result='didnt work')
        


# Flask-App RunTime-related
app.permanent_session_lifetime = timedelta(minutes=20)
if __name__ == "__main__":
    app.run()