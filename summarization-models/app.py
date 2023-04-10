from flask import Flask, request, render_template_string, jsonify
from summarizer import Summarizer
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from googletrans import Translator
from summarizer import Summarizer
import spacy


app = Flask(__name__)


@app.before_first_request
def load_model():
    print('--- first load ---')
    
    """"""
    global summarizer
    summarizer = Summarizer()
    tryout = summarizer(body='test')
    
    """"""
    global model, tokenizer, translator
    tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
    
    """"""
    translator = Translator()


@app.route('/', methods=['GET'])
def tryout():
    return jsonify(result='Connection works!')

@app.route('/extractive-summarize', methods=['POST'])
def ext_sum():
    """"""
    try:
        text = request.json['text']
        number = request.json['n']
    except Exception as e:
        return jsonify(result=e)

    try:
        if number is None or not str(number).isnumeric():
            number = summarizer.calculate_optimal_k(text, k_max=10)
    except Exception as e:
        return jsonify(result=e)

    """extracting key sentences"""
    try:
        result = summarizer(
            body=text,
            max_length=700,
            min_length=5,
            num_sentences=number,
            return_as_list=True
        )
    except Exception as e:
        return jsonify(result=e)

    return jsonify(
        result=result
    )

@app.route('/abstractive-summarize', methods=['POST'])
def abs_sum():
    """"""
    try:
        text = request.json['text']
        length = request.json['n']
        language = request.json['lang']
    except Exception as e:
        return jsonify(result=e)

    try:
        translated_text = translator.translate(text=text,dest='en').text
    except Exception as e:
        return jsonify(result=e)
        
    try:
        tokens = tokenizer(
            translated_text, 
            truncation=True, 
            padding="longest", 
            return_tensors="pt",
            max_length=length
        )
    except Exception as e:
        return jsonify(result=e)

    try:
        summary = model.generate(**tokens)
        summary = tokenizer.decode(summary[0])
    except Exception as e:
        return jsonify(result=e)

    try:
        if (language != 'en'):
            summary = translator.translate(text=text,dest=language).text
    except Exception as e:
        return jsonify(result=e)
        
    return jsonify(
        result=summary
    )


if __name__ == '__main__':
    app.run()