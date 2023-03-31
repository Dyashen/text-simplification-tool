from pdfminer.high_level import extract_pages
import TextAnalysis as tu
import Reader as ras

text = ra.get_full_text_dict(all_pages)

stats = tu.get_statistics(' '.join(text))

ra.get_full_text()

keywords  = tu.get_key_words(text)

print(stats)

exit(0)

tu.get_key_sentences()