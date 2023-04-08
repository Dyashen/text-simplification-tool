import pypandoc

output = pypandoc.convert_file('test.md', 'pdf', outputfile='tryout.pdf', extra_args=['--pdf-engine=xelatex'])