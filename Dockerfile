FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt \
    && python3 -m spacy download nl_core_news_md \
    && python3 -m spacy download en_core_web_sm \
    && pip3 install bert-extractive-summarizer torch \
    && apt-get install -y wget



COPY . .

RUN if [ ! -f "pytorch_model.bin" ]; then \
    echo "Downloading model" && wget https://huggingface.co/xlm-roberta-base/resolve/main/pytorch_model.bin; \
fi

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]