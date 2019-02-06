
Serveur pour mettre en ligne un contenu static avec mot de passe
================================================================

Le tutoriel s'adresse à ceux qui utilisent :epkg:`Linux`
qui la distribution la plus courante pour les serveur
en ligne car opensource. Il existe de nombreuses solutions.
La difficulté ici est de protéger le contenu avec un mot de passe.

.. contents::
    :local:

Installer un serveur SFTP
+++++++++++++++++++++++++

La première consiste à lancer un serveur SFTP
pour pouvoir publier le contenu en transférant des
fichiers depuis son ordinateur local vers la machine
distance. Pour le transfert de fichiers,
:epkg:`FileZilla` est souvent utilisé.
Ensuite, il faut mettre en place le serveur
SFTP. Le blog post suivant explique comment :
`Install FTP server on debian <http://www.xavierdupre.fr/app/pymyinstall/helpsphinx/blog/2018/2019-01-13_ftp_linux.html>`_.

Installer un serveur pour le contenu static
+++++++++++++++++++++++++++++++++++++++++++

L'idée retenue ici est de donner accès au contenu à quiconque
a le mot de passe, donc unique pour tous. Le code est encore
en développement, seul le protocol :epkg:`HTTP` a été implémenté.
Il vaudrait mieux pour ce type d'usage d'utiliser le protocol
:epkg:`HTTPS`. L'implémentation actuelle utilise :epkg:`starlette`
et :epkg:`uvicorn`. Le service se lance avec la commande suivante :

::

    nohup python3.7 -m mathenjeu static_local --cookie_domain "addresse ip de la machine" --cookie_key "mot de passe" --start=1 --port=<port> --userpwd "<quelquechose>" --content "2A,/home/ftpuser/ftp/quelquechose" > webapp.log &

Arrêter le serveur
++++++++++++++++++

Le plus simple est de rechercher le processus qui
exécute le serveur.

::

    ps -ef | grep mathenjeu

Il suffit ensuite de le tuer.

::

    kill <process id>

Il est possible qu'il existe un processus résiduel
associé au port de la machine utilisé pour lancer le site.
Pour le trouver, il suffit de remplacer *3000* par le port
utilisé puis de tuer le processus trouvé par ce biais.

::

    lsof -i tcp:3000
