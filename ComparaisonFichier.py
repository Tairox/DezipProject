import os,filecmp
from Date import *

def comparefichier(jour,jourminus):
   
    auj=os.path.isfile('c:/Users/arthr/OneDrive/Bureau/COURS/FISE2/S7/Scripting System/vscod/'+jour+'.sql')
    hier=os.path.isfile('c:/Users/arthr/OneDrive/Bureau/COURS/FISE2/S7/Scripting System/vscod/'+jourminus+'.sql')
    if auj==True:
        print('le fichier du jour, le ',jour,'existe')
    else:
        print('le fichier du jour, le ',jour,'n existe pas')
    if hier==True:
        print('le fichier d hier, le ',jourminus,' existe')
    else:
        print('le fichier d hier, le ',jourminus,' n existe pas')
   
    FichierDuJour = open('c:/Users/arthr/OneDrive/Bureau/COURS/FISE2/S7/Scripting System/vscod/'+jour+'.sql')
    ContenuJour = FichierDuJour.read()
    FichierDhier = open('c:/Users/arthr/OneDrive/Bureau/COURS/FISE2/S7/Scripting System/vscod/'+jourminus+'.sql')
    ContenuHier = FichierDhier.read()
    if ContenuJour==ContenuHier:
        print("Le fichier d'aujourd'hui est le meme que celui d'hier")
    else :
        print("Le fichier d'aujourd'hui est different de celui d'hier")



comparefichier("20220922","20220921")