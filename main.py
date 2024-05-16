import subprocess
import multiprocessing
import time
from imap_tools import MailBox, AND
import joblib


def run_custom_script():
    # Configurações de login
    print("oi")


if __name__ == "__main__":
    # Execute o script personalizado em um processo separado
    custom_process = multiprocessing.Process(target=run_custom_script)
    custom_process.start()

    # Inicie o servidor Django em outro processo
    django_process = subprocess.Popen(["python", "manage.py", "runserver"])
    django_process.wait()  # Aguarde o término do processo do servidor Django
