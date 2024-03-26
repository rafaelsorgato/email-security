import win32com.client
import pythoncom
import pywintypes
import datetime
import os
import django
import pytz

# Configurar as configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emailsecurity.settings")  
django.setup()

from aplication.models import emails

if __name__ == "__main__":
    timezone = pytz.timezone('America/Sao_Paulo')
    pythoncom.CoInitialize()
    outlook = win32com.client.Dispatch('Outlook.Application')
    mapi = outlook.GetNamespace("MAPI")
    inbox = mapi.GetDefaultFolder(6)
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)
    last_email_sentondate = emails.objects.latest('sentondatetime').sentondatetime if emails.objects.exists() else datetime.datetime(1970, 1, 1, 0, 0, 0,  tzinfo=timezone)
    print("starting email search")
    for message in messages:
        try:
            message_sent_on = datetime.datetime(message.SentOn.year, message.SentOn.month, message.SentOn.day,message.SentOn.hour, message.SentOn.minute, message.SentOn.second, tzinfo=timezone)
            if message_sent_on > last_email_sentondate:
                try:
                    if hasattr(message ,'HTMLBody'):
                        objeto_modelo = emails.objects.create(sender=message.SenderEmailAddress, body=message.HTMLBody, subject=message.Subject, sentondatetime=message_sent_on)
                    elif hasattr(message ,'Body'):
                        objeto_modelo = emails.objects.create(sender=message.SenderEmailAddress, body=message.Body, subject=message.Subject, sentondatetime=message_sent_on)
                except Exception as e:
                    print("error in getting one email")
            else:
                continue
        except Exception as e:
            print("error in getting senton from email")
    print("email search finished")

    pythoncom.CoUninitialize()
