import os
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import datetime
from pandas_ods_reader import read_ods

load_dotenv(".env")

SENDER = os.environ.get("GMAIL_USER")
PASSWORD = os.environ.get("GMAIL_PASSWORD")


def send_email(recipient, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = recipient
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    server.quit()

dt = datetime.datetime.today()
num_mes_passat = dt.month - 1
path = "trens2020-2021.ods"
sheet_idx = 1
df = read_ods(path, sheet_idx)

mesos = ["Gener", "Febrer", "Març", "Abril", "Maig", "Juny", "Juliol", "Agost", "Setembre", "Octubre", "Novembre", "Desembre"]
preus = {
    "AVE" : 13.9,
    "MD"  : 9
}
num_aves = num_mds = preu_total = 0
try:
    trens_mes = df[mesos[num_mes_passat].upper()].values
    for tren in trens_mes:
        if (tren == "AVE"):
            num_aves += 1
        else:
            num_mds += 1
        preu_total += preus[tren]
    subject = "Pressupost Trens d'en Marc Garcia Massaneda del mes de " + mesos[num_mes_passat] + " del curs 2020-2021."
    agraiment = "\n\nEt recordo que el preu per cada Ave és 13,9 euros i el preu per cada tren de Mitja Distància és 9 euros.\n\nGRÀCIES PER TOT EL QUE FAS PER MI MAMA! ET DEIXO AMB AQUESTA FRASE PERQUÈ COMENCIS EL DIA D'AVUI AMB MOLTES GANES:\n\"CADA MAÑANA AL DESPERTAR COMIENZA UNA NUEVA OPORTUNIDAD\""
    body = "Nombre d'Aves: " +  str(num_aves) + "\nNombre de Trens de Mitja Distància: " + str(num_mds) + "\nPreu total: " + str(preu_total) +  agraiment
    send_email("receiver@mail.com", subject, body)

except:
    subject = "Pressupost Trens d'en Marc Garcia Massaneda del mes de " + mesos[num_mes_passat] + " del curs 2020-2021."
    body = "AQUEST MES NO S'HA DE PAGAR RES!!!!! EN MARC S'HA QUEDAT A CASETA AMB LA MANTETA.\n\nPASSA UN GRAN DIA!"
    send_email("receiver@mail.com", subject, body)
