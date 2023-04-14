"""flask"""
from flask import Flask, render_template, render_template_string, request, jsonify, session, send_file


"""pdf"""
from Reader import Reader
from io import BytesIO
from pdfminer.high_level import extract_pages

""""""
from datetime import timedelta


""""""
from Summarization import HuggingFaceModels
from Lexicala import Lexicala
from GPT import GPT


""""""
app = Flask(__name__)
app.secret_key = "super secret key"
COLOR_SESSION_NAME = 'color'

""""""
@app.before_request
def pre_boot_up():
    session.permanent = True
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