import re #module for tianematches

def tianematches(text):
    text = text.lower()
    textlist = re.split("\s", text)
    for index, word in enumerate(textlist):
        if index > 1:
            if re.search(r"feld|felder|platz|plätze|stab|stäbe", word):
                try:
                    k = int(textlist[index-1])
                except:
                    print("no number of fields")
            if re.search(r"scheibe|scheiben|klotz|klötze", word):
                try:
                    n = int(textlist[index-1])
                except:
                    print("no number of disks")
    else:
        return False

def movetime(text):
    text = text.lower()
    textlist = re.split("\s", text)
    nosuccess = False
    for index, word in enumerate(textlist):
        if index > 1:
            if re.search(r"feld|felder|platz|plätze|stab|stäbe", word):
                try:
                    k = int(textlist[index-1]
                except:
                    nosuccess = True
            if re.search(r"scheibe|scheiben|klotz|klötze", word):
                try:
                    n = int(textlist[index-1])
                except:
                    nosuccess = True
    if not nosuccess:
        m = M(n,k)
        years = int(m/(3600*24*365))
        remaining = m-years *3600*24*365
        months = int(remaining/(3600*24*(365/12)))
        remaining -= months * 3600*24*(365/12)
        days = int(remaining/(3600*24))
        remaining -= days *3600*24
        hours = int(remaining/(3600))
        remaining -= hours * 3600
        minutes = int(remaining/60)
        remaining -= minutes * 60
        seconds = remaining

        time_string = ""
        if years > 0:
            if years ==1:
                time_string += "1 Jahr"
            else:
                time_string += str(years) + " Jahre"
        
        if months > 0:
            time_string += ","
            if months == 1:
                time_string += "1 Monat"
            else:
                time_string += str(months) + " Monate"
        
        if days > 0:
            time_string += ","
            if months == 1:
                time_string += "1 Tag"
            else:
                time_string += str(days) + "Tage"
        
        if days > 0:
            time_string += ","
            if days == 1:
                time_string += "1 Tag"
            else:
                time_string += str(days) + "Tage"

        if hours > 0:
            time_string += ","
            if hours == 1:
                time_string += "1 Stunde"
            else:
                time_string += str(hours) + "Stunden"
        
        if minutes > 0:
            time_string += ","
            if minutes == 1:
                time_string += "1 Minute"
            else:
                time_string += str(minutes) + "Minuten"
        
        if seconds > 0:
            time_string += ","
            if seconds == 1:
                time_string += "1 Sekunde"
            else:
                time_string += str(seconds) + "Sekunden"

        ret = "Wenn man pro Sekunde einen Zug macht, benötigt man für {} Scheiben und {} Felder {}.".format(n, k , timestring)
    else:
        ret = "Ich konnte leider keine Zugzahl ermitteln"
    sucess = not nosuccess
    return ret, sucess

def possibilitynumber(n,k):
    text = text.lower()
    textlist = re.split("\s", text)
    success = True
    for index, word in enumerate(textlist):
        if index > 1:
            if re.search(r"feld|felder|platz|plätze|stab|stäbe", word):
                try:
                    k = int(textlist[index-1]
                except:
                    success = False
            if re.search(r"scheibe|scheiben|klotz|klötze", word):
                try:
                    n = int(textlist[index-1])
                except:
                    success = False
    if success:
        ret = "Um die Türme von Hanoi mit {} Scheiben und {} Felder optimal zu lösen, gibt es {} Möglichkeiten.".format(n, k , upsilon(n,k))
    else:
        ret = "Ich konnte die Anzahl der Möglichkeiten leider nicht ermitteln"
    return ret, success


print(tianematches("Felder"))



def faculty(x):
    if x == 0:
        return 1
    value = 1
    for i in range(1, x+1):
        value *= i
    return int(value)


def bk(n, k):
    if n == k:
        return 1
    if k < 0 or k > n:
        return 0
    value = faculty(n) / (faculty(k) * faculty(n - k))
    return int(value)


def t_(n, k):
    t = -1
    x = 0
    while n > x:
        t += 1
        x = bk(k-2+t, k-2)
    return t


def formula(n, k, t):
    """berechnet die Mindestzugzahl bei "n" Knickpunkten, "m" Plätzen und "AS" Scheiben"""
    if k == 3:
        return 2**(n)-1
    x = 0
    for i in range(0, t+1):
        x = x + 2**i*bk(i+k-3, k-3)
    correction = 2**t*(n-bk(t+k-2, k-2))
    return x + correction


def M(n, k):
    """berechnet die Mindestanzahl von Zügen, die für "As" Scheiben bei "m" Plätzen benötigt werden"""
    t = t_(n, k)
    x = formula(n, k, t)
    return x


def upsilon(n,k):
    s = t_(n,k)
    above = bk(s+k-3,k-3)
    below = bk(s+k-2,k-2)-n
    result = bk(above,below)
    return result
