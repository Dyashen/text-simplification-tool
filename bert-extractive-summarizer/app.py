from flask import Flask, request, render_template_string, jsonify
from summarizer import Summarizer

app = Flask(__name__)


@app.before_first_request
def load_model():
    print('--- first load ---')
    global summarizer
    summarizer = Summarizer()
    tryout = summarizer(body='test')

@app.route('/summarize', methods=['POST'])
def summarize():
    """"""
    text = request.json['text']
    number = request.json['n']

    if number is None or not str(number).isnumeric():
        number = summarizer.calculate_optimal_k(text, k_max=10)

    """extracting key sentences"""
    result = summarizer(
        body=text,
        max_length=700,
        min_length=5,
        num_sentences=number,
        return_as_list=True
    )

    return jsonify(
        result=result
    )


if __name__ == '__main__':
    app.run()