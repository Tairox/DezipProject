# Utilitaire d'archivage 2022.

_Projet de scripting système réalisé par Anthony Desousa, Arthur Rigaudière et Mattéo FIRRONE._

## Rôle

Le script permet de récupérer une archive sur serveur web https, d'extraire le fichier qu'il contient puis de l'archiver sur un serveur sftp distant avec une durée de conservation paramétrable.<br/>
Ce script possède diverses fonctionnalités comme :

- Un suivit des sauvegardes par envoi d'emails.
- Une journalisation des étapes effectuées pendant la sauvegarde dans un fichier d'extension **'.log'**.

## Doc utilisateur

### Installation

Le script bash **deZipScript.sh** permet à l’utilisateur d’installer le script et les dépendances pour le bon fonctionnement du programme.
Il faut lancer ce script en super utilisateur. Ensuite, il va :

- Vérifier les derniers paquets disponibles et les installer sur la machine.
- Installer les dernières versions de _git_, _python_ et son gestionnaire de paquets _pip_.
- Installer la librairie paramiko sur python (pour l'envoi SMTP).
- Cloner le dépot GitHub dans le répertoire **~**.
- Installer CRON et planifier l'exécution du script tous les jours à 8H.

Ce script fonctionne bien évidemment que sur linux, pour les utilisateurs windows il sagira de réaliser l'installation des dépendances manuellement :

- Installer Python puis la librairie _paramiko_.
- Télécharger les scripts python et le fichier de configuration présent dans le repository.

Pour finir, l'utilisateur doit ajouter l'ensemble des informations nécéssaires dans le fichier de configuration. Pour cela, se référer à la section **exploitation**.

### Configuration

Le fichier de configuration **databaseconfig.json** contient un ensemble de champs éditables afin d'utiliser le script :

- L'objet **FileRequest** permet de spécifier l'URL sur laquelle se trouve l'archive à travers l'attribut _URLtoRequest_, il permet de plus de définir le nom du fichier à extraire dans cette archive avec _filename_.
- L'objet **SFTP** permet de configurer la connexion au serveur SFTP distant avec :
  - Le nom d'utilisateur _username_.
  - Le mot de passe : _password_.
  - L'adresse du serveur et son port: _server_, _port_.
  - Chemin d'accès : **ANTHONY ICI**
  - La durée de conservation des fichiers sur le serveur distant : _daysOfPersistence_.
- L'objet **SMTP** permet de configurer l'adresse du serveur SMTP, son port ainsi que les identifiants de connexion : _server_, _port_, _senderEmail_ , _password_.
- L'objet **EMAILS** permet d'ajouter les adresses mails qui recevront les emails à chaque sauvegarde. Le format de la chaîne de caractère est libre et il n'y a pas de limite d'emails à ajouter.

### Exploitation

Le script d'installation configure par défaut l'automatisation de lancement du script avec CRON. Par défaut le script est exécuté tous les jours à 8H.

Si l'utilisateur souhaite configurer lui même l'automatisation de lancement du script. Il suffit d'ajouter la ligne suivante dans la crontable du root : <br/>

> 0 8 \* \* \* python3 /chemin-absolue-vers-le-script/deZipFromWeb.py

Pour une utilisation manuelle, il suffit d'exécuter le script (script dans le répertoire courant)

> python3 ./deZipFromWeb.py
