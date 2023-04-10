from googletrans import Translator
from transformers import pipeline

# Importing model and tokenizer
from transformers import GPT2Tokenizer,GPT2LMHeadModel
# Instantiating the model and tokenizer with gpt-2
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = GPT2LMHeadModel.from_pretrained('gpt2')
translator = Translator()



text = """
HR-beleid van Belgische kmo’s nauwelijks veranderd sinds corona
Het HR-beleid van Belgische kmo’s is nagenoeg onveranderd gebleven sinds de stat van de coronacrisis. Datis de conclusie van de eerste resultaten van de HR-scan, een onderzoek van HOGENT, KU Leuven, UGent enSecurex.
De coronaperiode stelde werkgevers én werknemers voor ongeziene uitdagingen. Met de HR-scan, eenlopend onderzoek, tracht de impact van deze periode op HR-beleid in kaart te worden gebracht. Dat blijktminiem. 86 procent van de werknemers van Belgische kmo’s geeft aan sinds corona helemaal geenverandering te merken. 14 procent merkt minstens enige verandering. De scan richt zich op drie belangrijkepijlers die samen het beleid vormen: HR-praktijken, job design en stijl van leidinggevenden. 86 procent zietop deze vlakken dus een status quo. Maar nog meer van hen wijzen ook op een stilstand van elkeafzonderlijke pijler.
"""

text = translator.translate(text=text,dest='en').text


# Encoding text to get input ids & pass them to model.generate()
inputs = tokenizer.encode_plus(text, return_tensors='pt', truncation=True, padding='longest')
input_ids, attention_mask = inputs['input_ids'], inputs['attention_mask']

# pad the input_ids and attention_mask with the new padding token
max_length = 512
padded_input_ids = input_ids[:, :max_length].reshape(-1, max_length)
padded_attention_mask = attention_mask[:, :max_length].reshape(-1, max_length)

summary_ids = model.generate(padded_input_ids, attention_mask=padded_attention_mask, early_stopping=False, min_length=90, max_length=max_length, pad_token_id=tokenizer.eos_token_id)

GPT_summary=tokenizer.decode(summary_ids[0],skip_special_tokens=True)
#print(GPT_summary)


# Importing model and tokenizer
from transformers import GPT2Tokenizer,GPT2LMHeadModel

# Instantiating the model and tokenizer with gpt-2
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

model = GPT2LMHeadModel.from_pretrained('gpt2')

# Set up the parameters for generating the summary
max_length = len(text.split()) # subtract 1 to match the size of input tensor
min_length = 32
temperature = 0.7
num_beams = 5

# Encoding text to get input ids & pass them to model.generate()
inputs = tokenizer.encode_plus(text, return_tensors='pt', truncation=True, padding='longest')
input_ids, attention_mask = inputs['input_ids'], inputs['attention_mask']

# pad the input_ids and attention_mask with the new padding token
padded_input_ids = input_ids[:, :max_length].reshape(-1, max_length)
padded_attention_mask = attention_mask[:, :max_length].reshape(-1, max_length)

# Generate the summary
summary_ids = model.generate(
    padded_input_ids,
    attention_mask=padded_attention_mask,
    early_stopping=False,
    min_length=min_length,
    max_length=max_length+1,
    pad_token_id=tokenizer.eos_token_id,
    temperature=temperature,
    num_beams=num_beams,
    no_repeat_ngram_size=2,
    length_penalty=1.0
)

# Decode the summary and print it
GPT_summary=tokenizer.decode(summary_ids[0],skip_special_tokens=True)
print(GPT_summary)