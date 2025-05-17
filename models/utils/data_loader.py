import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(excel_path):
    df = pd.read_excel(excel_path)
    df = df[['review_id', 'review_text', 'Genel Duygu', 'Grafik', 'AI', 'Oynanis',
        'Ses ve Muzik', 'Oyun Dunyasi', 'Topluluk ve Sosyal',
        'Hikaye ve Senaryo', 'Performans ve Teknik']]

    return df

def split_data(df):
    train, temp = train_test_split(df, test_size=0.2, stratify=df['Genel Duygu'], random_state=42)
    val, test = train_test_split(temp, test_size=0.5, stratify=temp['Genel Duygu'], random_state=42)
    return train, val, test
