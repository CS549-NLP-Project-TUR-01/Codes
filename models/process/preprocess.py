from transformers import AutoTokenizer

def get_tokenizer(model_name='dbmdz/bert-base-turkish-cased'):
    return AutoTokenizer.from_pretrained(model_name)

def tokenize_data(tokenizer, texts, labels=None, max_length=128):
    encodings = tokenizer(texts.tolist(), truncation=True, padding=True, max_length=max_length)
    if labels is not None:
        encodings['labels'] = labels.tolist()
    return encodings
