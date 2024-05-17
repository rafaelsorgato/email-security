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
from aplication.models import emails,rule_settings
from googletrans import Translator



def analyse_emails():
    spam_tfidf_vectorizer = joblib.load('training_files/spam_tfidf_vectorizer.pkl')
    phishing_tfidf_vectorizer = joblib.load('training_files/phishing_tfidf_vectorizer.pkl')

    spam_model = joblib.load('training_files/spam_model.pkl')
    phishing_model = joblib.load('training_files/phishing_model.pkl')
    rule_settings_data = rule_settings.objects.first()
    spam_level = rule_settings_data.antispam
    phishing_level = rule_settings_data.antiphishing
    if spam_level == 'low':
        spam_level = 0.90
    elif spam_level == 'medium':
        spam_level = 0.80
    elif spam_level == 'high':
        spam_level = 0.73
    if phishing_level == 'low':
        phishing_level = 0.90
    elif phishing_level == 'medium':
        phishing_level = 0.80
    elif phishing_level == 'high':
        phishing_level = 0.73
    translator = Translator()

    queued_emails = emails.objects.filter(category='Queued') | emails.objects.filter(action=0)

    for email in queued_emails[:10]:
        translated_email = translator.translate(email.body, dest='en')
        email_spam_data = spam_tfidf_vectorizer.transform([translated_email.text])
        email_phishing_data = phishing_tfidf_vectorizer.transform([translated_email.text])
        is_phishing = 0
        is_spam = 0
        if spam_model.predict_proba(email_spam_data)[0][1] > spam_level:
            is_spam = 1
        if phishing_model.predict_proba(email_phishing_data)[0][1] > phishing_level: 
            is_phishing = 1
        if is_phishing and is_spam:
            if spam_model.predict_proba(email_spam_data)[0][1] > phishing_model.predict_proba(email_phishing_data)[0][1]:
                is_phishing = 0
            else:
                is_spam = 0
        if is_spam:
            email.category = 'Spam'
        elif is_phishing:
            email.category = 'Phishing'
        else:
            email.category = 'Safe'
        
        email.save()


    
analyse_emails()