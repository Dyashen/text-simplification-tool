from flask import Flask, request, render_template_string
from summarizer import Summarizer

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    """"""
    text = request.json['text']
    number = request.json['n']
    summarizer = Summarizer()

    if number is None or not str(number).isnumeric():
        number = summarizer.calculate_optimal_k(text, k_max=10)

    print(text)
    print(number)

    """extracting key sentences"""
    result = summarizer(
        body=text,
        max_length=700,
        min_length=5,
        num_sentences=number,
        return_as_list=True
    )

    return render_template_string(f'{result}')


if __name__ == '__main__':
    app.run()