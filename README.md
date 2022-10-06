# Utilitaire d'archivage 2022.

_Projet de scripting système réalisé par Anthony Desousa, Arthur Rigaudière et Mattéo FIRRONE._

## Rôle

Le script permet de récupérer une archive sur serveur web https, d'extraire le fichier qu'il contient puis de l'archiver sur un serveur sftp distant avec une durée de conservation paramétrable.<br/>
Ce script possède diverses fonctionnalités comme :
* Un suivit des sauvegardes par envoi d'emails.
* Une journalisation des étapes effectuées pendant la sauvegarde dans un fichier d'extension **'.log'**.

## Doc utilisateur

### Installation


Le script bash **deZipScript.sh** va permettre à l’utilisateur d’installer tout ce qui est utile pour le bon fonctionnement du programme.
Il faut lancer ce script en super utilisateur. Ensuite, il va :

* vérifier les dernières mises à jour sur l’environnement de travail
* installer le programme git
* installer le programme python
* installer le gestionnaire de package pip
* installer la librairie paramiko sur python
* installer le programme cron

Toutes ces installations automatiques vont permettre à l’utilisateur de gagner du temps et de ne pas avoir de problème au moment de l’exécution.<br/>
Ensuite, nous avons mis notre projet github en public pour que le script le récupère avec la commande git clone. Le projet est enregistré dans une dossier qui s’appelant Scripting System qui sera créé dans **~/** (ce qui signifie /home/user/).<br/>

Maintenant que le programme est téléchargé, il faut planifier le lancement automatique grâce au cron. Le script va écrire dans le fichier cron de sorte à ce que le programme Python se lance chaque jour à 8h00.<br/>
La seule partie manuelle à réaliser par l’utilisateur est de déposer son fichier de configuration dans le dossier **ScripingSystem**. Nous n’avons pas choisi de mettre le fichier de configuration avec le code en public sur github car ce n’est pas du tout sécurisé.<br/>
Ensuite, le code s’exécutera automatiquement chaque jour pour récupérer le fichier sur le serveur.<br/>

### Configuration

Le fichier de configuration **databaseconfig.json** contient un ensemble de champs éditables afin d'utiliser le script :
* L'objet **FileRequest** permet de spécifier l'URL sur laquelle se trouve l'archive à travers l'attribut _URLtoRequest_, il permet de plus de définir le nom du fichier à extraire dans cette archive avec _filename_.
* L'objet **SFTP** permet de configurer la connexion au serveur SFTP distant avec :
     * Le nom d'utilisateur _username_.
     * Le mot de passe : _password_. 
     * L'adresse du serveur et son port: _server_, _port_.
     * Chemin d'accès : **ANTHONY ICI**
     * La durée de conservation des fichiers sur le serveur distant : _daysOfPersistence_.
* L'objet **SMTP** permet de configurer l'adresse du serveur SMTP, son port ainsi que les identifiants de connexion : _server_, _port_, _senderEmail_ , _password_.
* L'objet **EMAILS** permet d'ajouter les adresses mails qui recevront les emails à chaque sauvegarde. Le format de la chaîne de caractère est libre et il n'y a pas de limite d'emails à ajouter.


### Exploitation

Le script d'installation configure par défaut l'automatisation de lancement du script avec CRON. Par défaut le script est exécuté tous les jours à 8H.

Si l'utilisateur souhaite configurer lui même l'automatisation de lancement du script. Il suffit d'ajouter la ligne suivante dans la crontable du root : <br/>
> 0 8 * * * python3 /chemin-absolue-vers-le-script/deZipFromWeb.py

Pour une utilisation manuelle, il suffit d'exécuter le script :
> python3 ./deZipFromWeb.py

