import re
from Creator import Creator
from Summarization import Summarization
from summarizer import Summarizer

sum = Summarization('test')

summarizer = Summarizer(
        #MODEL_PATH
)


with open('output.txt', 'r', encoding='latin-1') as f:
    fullText = f.read()


list_of_words = [
    ['appel','noun'],
    ['reviseren','verb']
]


glossary = sum.generate_glossary(list=list_of_words)
result = sum.generate_summary(fullText=fullText, summarizer=summarizer)


Creator().create_pdf(
    title='Test text simplification', 
    list=glossary, 
    full_text=result # formaat: [ titel, tekst ]
)

# start
fullText = str(fullText)
fullText = fullText.encode('ascii', 'ignore').decode('ascii')

"""cleaning"""
patterns = {
    '<h1>': '',
    '</h1>': '',
    '<div class="page">':'',
    '</div>':'',
    '<span class="word">': ' ',
    '</span>' : '',
    '\n' : '',
    ' ' : '',
    '<p>': '',
    '</p><p>':'',
    '</p>':'',
    '<span class="sentence">':' ',
    '[':'',
    ']':''
}
regex = re.compile('|'.join(map(re.escape, patterns.keys())))
fullText = fullText.strip('\n')
text = regex.sub(lambda match : patterns[match.group(0)], fullText)


"""per gekozen titel"""
text = text.split('<h3>')
new_text = []

for i in range(len(text)):
    try:

        title = text[i].split('</h3>')[0],
        paragraph = text[i].split('</h3>')[1]
        
        if (len(paragraph) > 3000):
            # extractive
            paragraph = sum.extractive_summarization(
                full_text=paragraph, 
                summarizer=summarizer
            )

            # abstractive
            paragraph = sum.abstractive_summarization_rapidapi(
                text=paragraph,
                num_sentences=5
            )

        else:
            # abstractive
            paragraph = sum.abstractive_summarization_rapidapi(
                text=paragraph,
                num_sentences=5
            )


        new_text.append([
            title, paragraph
        ])
    except:
        new_text.append(text[i])

Creator().create_pdf(
    title='test', 
    list=[['foo','bar']], 
    full_text=new_text # formaat: [ titel, tekst ]
    )










