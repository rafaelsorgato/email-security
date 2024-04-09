import win32com.client
import pythoncom
import pywintypes
import datetime
import os
import django
import pytz
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup

# List of strings
texts = ["This is a sample text.", "Another sample text."]

# Creating a CountVectorizer instance
vectorizer = CountVectorizer()

# Fitting the vectorizer with the list of strings
vectorizer.fit(texts)


# Configurar as configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emailsecurity.settings")  
django.setup()

from aplication.models import emails

def analyse_emails():
    timezone = pytz.timezone('America/Sao_Paulo')
    for email in emails.objects.all():
        print('oi')


def train_model():
    # Carregar dados
    df = pd.read_csv('training_files/spam.csv', encoding='latin1')
    data = df.fillna('')  # Preencher valores nulos com string vazia

    # Preparar dados
    x = data["v2"]
    y = data["v1"]
    X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=3)

    # Vetorizar texto
    feature_extraction = TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)
    X_train_features = feature_extraction.fit_transform(X_train)
    X_test_features = feature_extraction.transform(X_test)

    # Treinar modelo
    model = LogisticRegression()
    model.fit(X_train_features, Y_train)

    joblib.dump(model, 'modelo_treinado.pkl')
    #modelo_carregado = joblib.load('modelo_treinado.pkl')

    # Prever para novos dados
    for email in emails.objects.all()[:10]:
        input_data_features = feature_extraction.transform([email.body])
        prediction = model.predict(input_data_features)
        print(prediction)

train_model()