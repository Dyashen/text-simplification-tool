from flask import Flask, request, render_template_string, jsonify
from summarizer import Summarizer
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from googletrans import Translator
import spacy


app = Flask(__name__)

@app.before_first_request
def load_model():
    print('--- first load ---')
    global model, tokenizer, translator
    tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
    translator = Translator()

@app.route('/summarize', methods=['POST'])
def summarize():
    """"""
    text = request.json['text']
    length = request.json['n']
    language = request.json['lang']

    print(text, length, language)

    translated_text = translator.translate(text=text,dest='en').text

    print(translated_text)

    tokens = tokenizer(
        translated_text, 
        truncation=True, 
        padding="longest", 
        return_tensors="pt",
        max_length=length
    )

    print(tokens)

    summary = model.generate(**tokens)

    print(summary)

    summary = tokenizer.decode(summary[0])

    if (language != 'en'):
        summary = translator.translate(text=text,dest=language).text
        
    return jsonify(result=summary)

if __name__ == '__main__':
    app.run()


