from PyPDF2 import PdfFileReader
pdfObject = open('C:\\_hogeschool-gent\\bachelorproef-nlp-tekstvereenvoudiging\\scripts\\pdf\\Manual_AISurveillance.pdf', 'rb')
pdfReader = PdfFileReader(pdfObject)
text=''
for i in range(0,pdfReader.numPages):
    pageObject = pdfReader.getPage(i)
    text += pageObject.extractText()
print(text)