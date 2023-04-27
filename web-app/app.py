"""flask"""
from flask import Flask, render_template, render_template_string, request, jsonify, session, send_file, flash
from langdetect import detect_langs, detect
import spacy


"""pdf"""
from Reader import Reader
from pdf2image import convert_from_bytes
from pdfminer.pdfpage import PDFPage
from io import BytesIO
from pdfminer.high_level import extract_pages

""""""
from datetime import timedelta

""""""
from Summarization import HuggingFaceModels, GPT, WordScraper
from Writer import Creator
import Analysis as an

""""""
app = Flask(__name__)
app.secret_key = "super secret key"
GPT_API_KEY_SESSION_NAME = 'gpt3'
HF_API_KEY_SESSION_NAME = 'hf_api_key'
PER_SET_SESSION_NAME = 'personalized_settings'


def setup_scholars_teachers(request):
    settings = request.form
    if 'fullText' in request.form:
            text = request.form['fullText']
            langs = detect_langs(text)
            reader = Reader()
            dict_text = reader.get_full_text_site(text)                
    elif 'pdf' in request.files:
            if 'advanced' not in settings:
                pdf = request.files['pdf']
                pdf_data = BytesIO(pdf.read())
                all_pages = extract_pages(pdf_data,page_numbers=None,maxpages=999)
                langs = detect_langs(str(all_pages))
                reader = Reader()
                full_text = reader.get_full_text_dict(all_pages)
                dict_text = reader.get_full_text_site(full_text)
            else:
                pdf = request.files['pdf']
                pdf_data = pdf.read()
                pages = convert_from_bytes(pdf_data)
                reader = Reader()
                img_text = reader.get_full_text_from_image(pages)
                langs = detect_langs(img_text)
                dict_text = reader.get_full_text_site(img_text)                            
    return dict_text, langs, 'voorbeeldtitel', 'voorbeeldonderwerp'




""""""
@app.before_request
def pre_boot_up():
    session.permanent=True
    global simplifier, wap
    simplifier = HuggingFaceModels()
    wap = WordScraper()


""""""
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


""""""
@app.route('/for-scholars', methods=['GET','POST'])
def teaching_tool():
    try:
        dict_text, langs, title, subject = setup_scholars_teachers(request)
        return render_template('for-scholars.html', pdf=dict_text, lang=langs, title=title, subject=subject)
    except Exception as e:
        return render_template('error.html',error=str(e))


""""""
@app.route('/for-teachers', methods=['GET','POST'])
def analysing_choosing_for_teachers():
    try:
        dict_text, langs, title, subject = setup_scholars_teachers(request)
        return render_template('for-teachers.html', pdf=dict_text, lang=langs, title=title, subject=subject)
    except Exception as e:
        return render_template('error.html',error=str(e))

"""
"""
@app.route('/generate-summary', methods=['GET','POST'])
def generate_summary():
    try:
        settings = dict(request.form)
        fonts = (settings['titleFont'], settings['regularFont'])

        title = settings['titleOfPaper']
        wordlist = settings['glossaryList']
        wordlist = wordlist.strip(' ').split('\n')
            
        glossary = {}
        for word in wordlist:
            try:
                word_text = str(word).split(':')[0]
                word_type = str(word).split(':')[2]
            except Exception as e:
                print(str(e))
                pass
            
            try:
                word_definition = wap.look_up(str(word_text))[0]
                glossary[word_text] = {'type':word_type, 'definition':str(word_definition)}
            except:
                try:
                    api_key = session[GPT_API_KEY_SESSION_NAME]
                    gpt = GPT(api_key)
                    word_definition, word_text, prompt = gpt.look_up_word_gpt(word=word_text, context=word_text)
                    glossary[word_text] = {'type':word_type, 'definition': str(word_definition).replace('\n',' ').strip(' ')}
                except:
                    glossary[word_text] = {'type':word_type, 'definition':'Definitie kon niet gevonden worden.'}

        full_text = settings['fullText']  

        if 'personalizedSummary' not in settings:        
            full_text = simplifier.summarize(text=full_text, lm_key='bart') # pegasus model --> dict structure
        else:
            try:
                api_key = session[GPT_API_KEY_SESSION_NAME]
            except:
                api_key = None

            blacklisted_keys = ['fullText', 'glossary', 'titleOfPaper','subjectOfPaper','actions', 'titleFont','regularFont', 'personalizedSummary']
            for key in settings.keys():
                if key not in blacklisted_keys:
                    pass

            gpt = GPT(api_key)
            personalization_array = []
            full_text = gpt.summarize(full_text_dict=full_text, personalisation=personalization_array)
            
        Creator().create_pdf(title=title, list=glossary, full_text=full_text, fonts=fonts)
        return send_file(path_or_file='saved_files/simplified_docs.zip', as_attachment=True)
    except Exception as e:
        return jsonify(error_msg = str(e))

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
        return jsonify(pos=str(e))

"""
"""
@app.route('/personalized-simplify', methods=['POST'])
def personalized_simplify():
    try:
        api_key = session[GPT_API_KEY_SESSION_NAME]
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
    return jsonify(result=word_definition, source='Vertalen.nu', word=word)


"""
@ TODO combine these two
"""
@app.route('/change-settings', methods=['GET', 'POST'])
def return_personal_settings_page():
    return render_template('settings.html')

@app.route('/get-settings-user',methods=['POST'])
def return_personal_settings_dict():
    if PER_SET_SESSION_NAME in session:
        return jsonify(session[PER_SET_SESSION_NAME])
    else:
        return jsonify(result='session does not exist')

@app.route('/change-settings-user', methods=['POST'])
def change_personal_settings():
    try:
        session[PER_SET_SESSION_NAME] = dict(request.form)
        msg = 'Succesvol aangepast!'
    except Exception as e:
        msg = str(e)
    flash(msg)
    return render_template('settings.html')


"""
@app.route('/change-color', methods=['POST'])
def change_color():
    try:
        data = request.get_json()
        color = data['color']
        session[COLOR_SESSION_NAME] = color
        return jsonify(color=session[COLOR_SESSION_NAME])
    except Exception as e:
        return jsonify(color='white')


@app.route('/get-background-color', methods=['POST'])
def get_color():
    try:
        color = session[COLOR_SESSION_NAME]
        return jsonify(color=color)
    except:
        return jsonify(color='white')
"""

"""
"""
@app.route('/set-gpt-api-key', methods=['GET'])
def set_gpt_api_key():
    try:
        api_key = request.args.get('key')
        session[GPT_API_KEY_SESSION_NAME] = api_key
        return jsonify(result=api_key)
    except Exception as e:
        return jsonify(result=str(e))
    
"""
"""
@app.route('/set-hf-api-key', methods=['GET'])
def set_hf_api_key():
    try:
        api_key = request.args.get('key')
        session[HF_API_KEY_SESSION_NAME] = api_key
        return jsonify(result=api_key)
    except Exception as e:
        return jsonify(result=str(e))

""""""
@app.route('/get-session-keys', methods=['GET'])
def get_session_keys():
    try:
        return jsonify(dict(session))
    except:
        return jsonify(result='didnt work')
        

# Flask-App RunTime-related
app.permanent_session_lifetime = timedelta(minutes=30)
if __name__ == "__main__":
    app.run()