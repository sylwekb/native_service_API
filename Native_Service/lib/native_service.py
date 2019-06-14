import os
import random
import string
from django.conf import settings
from django.core.mail import send_mail

os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.settings_module"

LOCAL_HOST_URL = "http://127.0.0.1:8000"
HOST_URL = "https://api.nativeservice.pl"
SENDER = "nativeservice@nativeservice.pl"
PERFORMERS_LIST = ["lukasz.gasiorowski92@gmail.com"]


class ProgressStages:
    """ Basic logic of email alert system. """

    STAGES = ("in_queue", "accepted", "in_progress", "done")

    def __init__(self, data, files, url):
        self.current_stage = None
        self.data = data
        self.files = files
        self.url = url
        self.in_queue_stage()

    def in_queue_stage(self):
        self.current_stage = self.STAGES[0]
        performer_queue_alert_email(self.data, self.files, self.url)
        customer_queue_alert_email(self.data, self.files)

    def accepted_stage(self):
        self.current_stage = self.STAGES[1]
        pass

    def in_progress_stage(self):
        self.current_stage = self.STAGES[2]
        pass

    def done_stage(self):
        self.current_stage = self.STAGES[3]
        pass


def secret_key_generator():
    letters, numbers = string.ascii_lowercase, string.digits
    return "".join(random.choice(letters + numbers) for i in range(12))


def files_urls_list_creating(file_data):
    files_list = []
    [
        files_list.append(f"{HOST_URL}{settings.MEDIA_URL}{f}\n".replace(" ", "_"))
        for f in file_data
    ]
    return files_list


def final_pricing_url_genrator(secret_key):
    return f"{LOCAL_HOST_URL}/final_pricing/{secret_key}/"


def performer_queue_alert_email(data, files="No files.", url="No url."):
    recipients_list = PERFORMERS_LIST

    send_mail(
        f"Nowe zlecenie!",
        f"Wejdź na https://nativeservice.pl/admin/ i sprawdź co na Ciebie czeka.\n"
        f"Imię: {data['name']}\n"
        f"Nazwisko: {data['last_name']}\n"
        f"Nazwa zlecenia: {data['title']}\n"
        f"Email: {data['email']}\n"
        f"Telefon: {data['phone']}\n"
        f"Data najpóźniejszej realizacji: {data['date_to_be_done']}\n"
        f"Opis: {data['description']}\n"
        f"{''.join(files_urls_list_creating(files))}"
        f"\n\nTen email został'wygenerowany automatycznie. Prosimy o nie odpowiadanie na wiadomość.\n"
        f"Wejdź na {url} i dokonaj wyceny.",
        SENDER,
        recipients_list,
        fail_silently=False,
    )


def customer_queue_alert_email(data, files="No files."):
    recipients_list = [data["email"]]

    send_mail(
        f"Native Service - wycena zlecenia.",
        f"Witaj {data['name']}\n"
        f"Twój unikalny kod do dalszej realizacji zlecenia to: {data['secret_key']}.\n"
        f"Twoja wycena '{data['title']}' oczekuje w kolejce! \n"
        f"Wyceny zleceń wysłanych w godzinach od 8 rano do 20 realizujemy w ciągu 15 minut!\n"
        f"Oto Twoje dane: \n"
        f"Imię: {data['name']}\n"
        f"Nazwisko: {data['last_name']}\n"
        f"Nazwa zlecenia: {data['title']}\n"
        f"Email: {data['email']}\n"
        f"Telefon: {data['phone']}\n"
        f"Data najpóźniejszej realizacji {data['date_to_be_done']}\n"
        f"Opis: {data['description']}\n"
        f"{''.join(files_urls_list_creating(files))}"
        f"\n\nTen email został'wygenerowany automatycznie. Prosimy o nie odpowiadanie na wiadomość.",
        SENDER,
        recipients_list,
        fail_silently=False,
    )
