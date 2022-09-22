import datetime

def date():
    annee=datetime.date.today().year
    mois=datetime.date.today().month
    mois2=str(mois)
    if mois<10 :
     mois2=str(0)+mois2
    jour=datetime.date.today().day
    annee2=str(annee)
    jour2=str(jour)
    date=annee2+mois2+jour2
    print(date)
    return date

def dateminus():
    annee=datetime.date.today().year
    mois=datetime.date.today().month
    mois2=str(mois)
    if mois<10 :
     mois2=str(0)+mois2
    jour=datetime.date.today().day
    jour=jour-1
    jour2=str(jour)
    annee2=str(annee)
    dateminus=annee2+mois2+jour2
    print(dateminus)
    return dateminus





