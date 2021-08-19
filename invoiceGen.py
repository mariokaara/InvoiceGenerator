import tkinter
from tkinter import messagebox

from datetime import *


todayTime = datetime.now()

aeg = str(todayTime.strftime("%d-%b-%YT%H-%M"))

with open("arve.csv") as a:
    a.readline()
    csv = []
    
    for i in a:
        elem = i.split(";")
        csv.append(elem)
        
def recordType(arve, f):
    if arve[7] == "arve":
        f.write('{:<2}'.format("FA"))
    else:
        f.write('{:<2}'.format("CN"))

def filler1(f):
    f.write('{:<1}'.format("0"))
        
def clientNumber(f):
    f.write('{:<7}'.format("ClientX"))
        
def debtorNumber(f):
    f.write('{:0>10}'.format('SEBOrklaNo'))

def filler10(f):
    f.write('{:0<10}'.format(""))

def invoiceAmount(arve, f):
    summaSõne = str(arve[27])
    summaFloat = float(summaSõne.replace(",", "."))
    sendidPanka = summaFloat*10000
    sendidPanka = sendidPanka/100
    sendidPankaStr = str(int(sendidPanka))
    f.write('{:0>11}'.format(sendidPankaStr))
    return sendidPanka

def invoiceDate(arve, f):
    kuupäevArvel = str(arve[3])
    kuupäev = kuupäevArvel[0:2]
    kuu = kuupäevArvel[3:5]
    aasta = kuupäevArvel[6:10]
    f.write('{:<10}'.format(aasta+"-"+kuu+"-"+kuupäev))

def dueDate(arve, f):
    kuupäevArvel = str(arve[3])
    kuupäev = kuupäevArvel[0:2]
    kuu = kuupäevArvel[3:5]
    aasta = kuupäevArvel[6:10]
    f.write('{:<10}'.format(aasta+"-"+kuu+"-"+kuupäev))

def currencyCode(arve, f):
    f.write('{:<3}'.format(str(arve[6].upper())))
    
def approvedDate(f):
    f.write('{: <10}'.format(""))

def assignedDate(f):
    f.write('{: <10}'.format(""))
        
def notifiedDate(f):
    f.write('{: <10}'.format("")) 

def invoiceNumber(arve, f):
    f.write('{:<15}'.format(str(arve[1])))

def blank(f):
    f.write('{: <20}'.format("") + "\n")


def reaPikkuseTest(txtFail):
    lüliti = True
    with open(txtFail) as a:
        rida = 1
        for i in a:
            if len(i) != 130:
                with open ("ERROR REPORT " + aeg + ".txt", "a") as e:
                    e.write(str(rida) + ". rida ei ole nõutud pikkusega: rea pikkuseks on " + str(len(i)) + " tähemärki, kuid lubatud on 129\n")
                lüliti = False
            rida += 1
    if lüliti == False:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror("Error", "Genereeritud väljundfaili pikkus ei ole õige (nõutud täpselt 129 tähemärki)! Kirja ei saadetud!")
    return lüliti

def filler10PositsiooniTest(txtFail):
    lüliti = True
    with open(txtFail) as a:
        rida = 1
        for i in a:
            if i[20:30] != "0000000000":
                with open ("ERROR REPORT " + aeg + ".txt", "a") as e:
                    e.write(str(rida) + ". real ei ole 10 täidise nulli õigel kohal või on seal midagi muud. Peab olema '0000000000' aga on " + i[20:30]+"\n")
                lüliti = False
            rida += 1
    if lüliti == False:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror("Error", "Nullide arv (10tk) või asukoht pole õiged (kohtadel 21-30)! Kirja ei saadetud!")
    return lüliti


fail = open("OrkEE" + aeg + ".txt", "a")

summa = 0

for i in range(len(csv)):
    recordType(csv[i], fail)
    filler1(fail)
    clientNumber(fail)
    debtorNumber(fail)
    filler10(fail)
    n = invoiceAmount(csv[i], fail)
    invoiceDate(csv[i], fail)
    dueDate(csv[i], fail)
    currencyCode(csv[i], fail)
    approvedDate(fail)
    assignedDate(fail)
    notifiedDate(fail)
    invoiceNumber(csv[i],fail)
    blank(fail)
    summa += n

fail.close()

messagebox.showinfo("Information", "Arvete summa on: " + str(summa/100)+" EUR")

x = filler10PositsiooniTest("OrkEE" + aeg + ".txt")
y = reaPikkuseTest("OrkEE" + aeg + ".txt")

'''
if x == True and y == True:

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    mail_content = ''Tere,
    See on e-kirja ja genereeritud manuse saatmise test.
    Kirja manus on genreeritud sisendina saadud CSV failist
    ning kiri ise on saadetud peale väljundfaili (txt) korrektsuse
    kontrolli automaatselt. Kiri kasutab Püütoni SMTP library't.
    ''
    sender_address = "eesnimi.perenimi@kcf.ee"
    sender_pass = "parool"
    receiver_address = 'eesnimi.perenimi@orkla.ee'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Test e-kiri, mis on saadetud Püütoni poolt. Sisaldab manust.'
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = "OrkEE" + aeg + ".txt"
    attach_file = open(attach_file_name, 'rb')
    payload = MIMEBase('application', 'octet-stream')
    payload.set_payload((attach_file).read())
    payload.add_header('Content-Disposition', 'attachment', filename = attach_file_name)
    message.attach(payload)
    session = smtplib.SMTP('10.25.32.13', 465)
    #session.connect("10.25.32.13", 465)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo("Information", "Kiri saadeti aadressile: " + receiver_address)
    '''
