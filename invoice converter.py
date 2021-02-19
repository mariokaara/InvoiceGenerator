from datetime import *
todayTime = datetime.now()

aeg = str(todayTime.strftime("%d-%b-%Y kell %H-%M-%S")) #aeg error report faili nimesse identifikaatoriks

with open("arve.csv") as arveFail:
    arveFail.readline() #loe faili päis eest ära
    failiRead = [] #loo tühi list failis olevate ridade salvestamiseks
    
    for rida in arveFail: #käi järjest läbi kõik arvete faili (arveFail) read
        reaElement = rida.split(";") #erista arvel olevaid elemente üksteisest nende vahel oleva semikooloni järgi
        failiRead.append(reaElement) #lisa read listi. Iga rida on oma indeksiga listi liige.

def pangaFailiGeneraator(arve):
    with open (str(arve[1].strip("'")) + ".txt", "a") as pangaFail:
       
        if arve[7] == "arve": #kui arve tüüp on "arve" siis lisa faili tähis "FA"
            pangaFail.write("FA")
        else:
            pangaFail.write("CN") #eeldab, et kui arve tüüp ei ole "arve" siis on ta ALATI "kreeditarve" ning faili lisatakse tähis "CN"
   
        pangaFail.write("0")
        pangaFail.write("???????") #kliendi nr. ainult 7 tähemärki lubatud
        pangaFail.write("??????????") #10 tähemärki lubatud. kui vähem tähemärke siis täida vasakult nullidega
        pangaFail.write("0000000000") #filler (kohustuslikud 10 nulli)
        
        #summa korrutatakse 100ga ja leitakse sentide arv, mis sisestatakse panga faili
        summaSõne=str(arve[5])
        if "," not in summaSõne:
            summaInt = int(summaSõne) #muuda failist saadud summa ujukomaarvuks
            sendidPanka = str(summaInt*100) #muuda summa sentideks, sest pank tahab saada sentide arvu
            sendidPanka = str(sendidPanka)
            summaPikkus = len(sendidPanka) #arvutab muutuja sendidPanka pikkuse
            nullideArv = 11-summaPikkus #leiab mitu nulli peaks lisama enne summat: 11st kohustuslikust tähemärgist lahutatakse summa tähemärkide arv
            pangaFail.write("0"*nullideArv) #lisatakse kõigepealt nullid...
            pangaFail.write(sendidPanka) #...ja seejärel summa sentide arvu tähemärgid
            
        #summas asendatakse punkt komaga ja leitakse sentide arv, mis sisestatakse panga faili
        else:
            summaFloat = float(summaSõne.replace(",", ".")) #asenda summas olev koma punktiga ja tee ujukomaarvuks
            sendidPanka = summaFloat*100 #muuda summa sentideks, sest pank tahab saada sentide arvu
            sendidPanka = str(int(sendidPanka))
            summaPikkus = len(sendidPanka) #arvuta muutuja summaPankaPunktita pikkus
            nullideArv = 11-summaPikkus #lahuta 11st kohustuslikust tähemärgist maha sendidPanka tähemärkide arv
            pangaFail.write("0"*nullideArv) #lisa kõigepealt faili nullid, mis täidavad summast üle jäävaid kohustuslikke kohti panga failis...
            pangaFail.write(sendidPanka) #...ja seejärel summa sentide arvu tähemärgid
                
        arvekuupäev = str(arve[3])  #formaaditakse arve kuupäeva kuju ja lisatakse faili
        kuupäev1 = arvekuupäev[0:2]
        kuu1 = arvekuupäev[3:5]
        aasta1 = arvekuupäev[6:10]
        pangaFail.write(aasta1+"-"+kuu1+"-"+kuupäev1)
        
        maksetähtaeg = str(arve[4]) #formaaditakse arve kuupäeva kuju ja lisatakse faili
        kuupäev2 = maksetähtaeg[0:2]
        kuu2 = maksetähtaeg[3:5]
        aasta2 = maksetähtaeg[6:10]
        pangaFail.write(aasta2+"-"+kuu2+"-"+kuupäev2)
        
        pangaFail.write(arve[6]) #lisa faili valuuta tähis (alati 3 kohta)
        
        pangaFail.write("                               ") #mittekohustuslikud väljad täidetud 10*3 tühikut
        
        pangaFail.write(str(arve[1])) #arve number sõnena
        
        arveNrPikkus = len(str(arve[1])) #arve numbri pikkus
        järelTühikuteArv = 15-arveNrPikkus #arve numbrist allesjäävate kohtade arv
        pangaFail.write(" " * järelTühikuteArv) #arve numbrist alles jäävate kohtade arv täidetuna tühikutega
        
        pangaFail.write(" " * 20) #20 viimast kohustuslikku tühikut


def failiPikkuseTest(failinimi): #funktsioon mis saab argumendiks faili nime ning kontrollib selle faili ridade pikkust (kas on täpselt 129 tähemärki)
    with open(failinimi) as fail:
        for i in fail:
            if len(i) != 129:
                with open ("ERROR REPORT " + aeg + ".txt", "a") as error:
                    error.write("Fail tähisega " + failinimi + " ei ole nõutud pikkuses\n")

def nulliFillerTest(failinimi): #kontrollib kas panga standardis olevad filler nullid kohtadel 21-30 asuvad ikka omal kohal
    with open(failinimi) as fail:
        for i in fail:
            if i[20:30] != "0000000000":
                with open ("ERROR REPORT " + aeg + ".txt", "a") as error:
                    error.write("Failis tähisega " + failinimi + " ei ole kohtadel 21-30 nullid nii nagu nõuab panga standard\n")

def tühikuFillerTest(failinimi): #kontrollib kas panga standardis olevad filler tühikud kohtadel 21-30 asuvad ikka omal kohal
    with open(failinimi) as fail:
        for i in fail:
            if i[64:94] != "                              ":
                with open ("ERROR REPORT " + aeg + ".txt", "a") as error:
                    error.write("Failis tähisega " + failinimi + " ei ole kohtadel 65-94 tühikud nii nagu nõuab panga standard\n")

for i in range(len(failiRead)): #loe sisse kõik read CSV failist
    pangaFailiGeneraator(failiRead[i]) #genereeri iga CSV failis oleva arve rea kohta panga txt fail ja vajadusel error report
    failiPikkuseTest(failiRead[i][1]+".txt") #testib kohe ka äsja loodud txt faili pikkuse nõude täidetust (129 tähemärki pikk)
    nulliFillerTest(failiRead[i][1]+".txt") #testib, kas loodud panga failis on täidiseks pandud nullid nõutud kohtadel 21-30 (-1 Pythonis ehk sõne viil 20:30)
    tühikuFillerTest(failiRead[i][1]+".txt") #testib, kas loodud panga failis on täidiseks pandud tühikud nõutud kohtadel 65-94 (-1 pythonis ehk sõne viil 64:94)