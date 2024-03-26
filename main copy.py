import win32com.client
import pythoncom
import pywintypes
import datetime
import os
import django

# Configurar as configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emailsecurity.settings")  
django.setup()

from aplication.models import emails

if __name__ == "__main__":
    pythoncom.CoInitialize()
    outlook = win32com.client.Dispatch('Outlook.Application')
    mapi = outlook.GetNamespace("MAPI")
    inbox = mapi.GetDefaultFolder(6)
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)
    last_email_sentondate = emails.objects.latest('sentondatetime').sentondatetime if emails.objects.exists() else datetime.datetime(1970, 1, 1)
    
    for message in messages:
        message_sent_on = datetime.datetime(message.SentOn.year, message.SentOn.month, message.SentOn.day,message.SentOn.hour, message.SentOn.minute, message.SentOn.second)
        if message_sent_on > last_email_sentondate:
            objeto_modelo = emails.objects.create(sender=message.SenderEmailAddress, body=message.HTMLBody, subject=message.Subject, sentondatetime=datetime.datetime.fromtimestamp(message.SentOn))
        else:
            continue

    pythoncom.CoUninitialize()
