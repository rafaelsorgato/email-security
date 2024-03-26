import subprocess
import multiprocessing
import time
from imap_tools import MailBox, AND

# Server is the address of the IMAP server

def run_custom_script():
    # Configurações de login
    server = 'imap-mail.outlook.com'
    email = 'rafaelsorgato@hotmail.com'
    password = 'iu&KbPYN2F6v^B'

    # Faça login na caixa de correio do Outlook
    with MailBox(server).login(email, password, 'INBOX') as mailbox:
        # Exemplo de uso: imprimir os assuntos dos últimos 10 e-mails
        for msg in mailbox.fetch(reverse=True, limit=10):
            print(msg.subject)


if __name__ == "__main__":
    # Execute o script personalizado em um processo separado
    custom_process = multiprocessing.Process(target=run_custom_script)
    custom_process.start()

    # Inicie o servidor Django em outro processo
    django_process = subprocess.Popen(["python", "manage.py", "runserver"])
    django_process.wait()  # Aguarde o término do processo do servidor Django
