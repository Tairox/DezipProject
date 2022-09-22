import tarfile,os,filecmp

def formatDate(daynumber : int ,monthnumber : int,yearnumber : int) -> str :
    '''Takes in the number of the day,month and year and returns it in a AAAADDMM format'''
    if monthnumber<10 :
        monthnumber="0"+str(monthnumber)

    if daynumber<10 :
        daynumber="0"+str(daynumber)

    final_date=str(yearnumber)+str(daynumber)+str(monthnumber)
    return final_date

def tgzMyFile(filenameOfTgz : str,filenameOfSource : str):
    '''Takes in the desired name of your .tgz file (without extension) and the filename (or path) of your source file, creates the archive in your current directory'''
    with tarfile.open(filenameOfTgz+".tgz","w:gz") as tar:
        tar.add(os.path.basename(filenameOfSource))
    if os.path.exists(filenameOfTgz+".tgz") :
        print("L'archive .tgz avec le bon nom a bien été créé.")
    else :
        print("Erreur : L'archive .tgz n'a pas pu être créé.")