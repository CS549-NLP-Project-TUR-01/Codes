import torch
from torch.utils.data import DataLoader, Dataset
from transformers import Trainer, TrainingArguments
from torch.optim import AdamW
from utils.data_loader import load_data, split_data
from process.preprocess import get_tokenizer, tokenize_data
import os

import pandas as pd
from models.instances import get_bert_model, get_ngram_model


class ReviewDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __len__(self):
        return len(self.encodings['input_ids'])

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

def train_bert_model(train_df, val_df, num_labels):
    # Robust NaN/unmapped label check for 'Genel Duygu'
    unmapped = train_df['Genel Duygu'][train_df['Genel Duygu'].isna()]
    if not unmapped.empty:
        problematic = train_df.loc[train_df['Genel Duygu'].isna(), 'Genel Duygu']
        raise ValueError(f"Unmapped or NaN labels found in 'Genel Duygu' in train set. Please check your label mapping. Problematic values: {problematic.value_counts()}")
    unmapped_val = val_df['Genel Duygu'][val_df['Genel Duygu'].isna()]
    if not unmapped_val.empty:
        problematic_val = val_df.loc[val_df['Genel Duygu'].isna(), 'Genel Duygu']
        raise ValueError(f"Unmapped or NaN labels found in 'Genel Duygu' in validation set. Please check your label mapping. Problematic values: {problematic_val.value_counts()}")

    tokenizer = get_tokenizer()
    train_enc = tokenize_data(tokenizer, train_df['review_text'], train_df['Genel Duygu'])
    val_enc = tokenize_data(tokenizer, val_df['review_text'], val_df['Genel Duygu'])

    train_dataset = ReviewDataset(train_enc)
    val_dataset = ReviewDataset(val_enc)

    model = get_bert_model(num_labels=num_labels)

    training_args = TrainingArguments(
        output_dir='output/sentiment_model',
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        save_strategy="epoch",
        logging_dir='output/logs',
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    trainer.train()
    model.save_pretrained("sentiment_model")

    return model




def train_ngram_model(train_df, val_df, output_dir, aspect_cols=None, ngram_range=(1,1), max_features=2000):
    if aspect_cols is None:
        # Default: all columns except review_text
        aspect_cols = [col for col in train_df.columns if col not in ['review_text']]
    model = get_ngram_model(ngram_range=ngram_range, max_features=max_features)
    X_train = train_df['review_text'].astype(str)
    Y_train = train_df[aspect_cols]
    model.fit(X_train, Y_train)
    model.save(output_dir)
    return model