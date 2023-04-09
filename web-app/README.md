# Prototype for multilingual text simplification and summarization of research articles with GPT-3 and BERT.

Docker instructions:

```bash
docker build -t text-app .
docker run --name text-application-prototype -d -p 5000:5000 text-app
```