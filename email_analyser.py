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

# Configurar as configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emailsecurity.settings")  
django.setup()
from aplication.models import emails
from googletrans import Translator



def analyse_emails():
    tfidf_vectorizer = joblib.load('training_files/tfidf_vectorizer.pkl')
    model = joblib.load('training_files/spam_model.pkl')

    translator = Translator()
    for email in emails.objects.all()[:10]:
        translated_email = translator.translate(email.body, dest='en')
        input_data_features = tfidf_vectorizer.transform([translated_email.text])
        if(model.predict_proba(input_data_features)[0][1] > 0.7):
            print("é spam")
            print(model.predict_proba(input_data_features)[0][1])
            print(translated_email.text)
            print("\n\n\n")

        else:
            print("não é spam")
            print(model.predict_proba(input_data_features)[0][1])
            print(translated_email.text)
            print("\n\n\n")



    #timezone = pytz.timezone('America/Sao_Paulo')


    
analyse_emails()