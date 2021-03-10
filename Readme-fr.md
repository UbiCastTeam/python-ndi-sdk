# Wrapper python du Capture SDK Magewell

## Description
python-ndi-sdk fourni un wrapper python permettant d'exploiter la librairie 
libMWCapture mise à disposition par le Capture SDK Magewell (http://www.magewell.com/files/sdk/Magewell_Capture_SDK_Linux_3.3.1.1313.tar.gz).  
python-ndi-sdk met à disposition l'ensemble des définitions des structures
transtypées C++ -> Python.  
python-ndi-sdk donne un accès à ces ressources à travers un service D-Bus.

## Installation
### Prérequis
Vous devez préalablement générer les librairies dynamiques à partir des 
librairies statiques fournies par le Capture SDK Magewell.
Vous trouverez dans l'archive un script réalisant cela (Magewell_Capture_SDK_Linux_3.3.1.1313/Lib/gen_shared.sh).
Copiez les librairies dynamiques générées dans votre dossier lib (généralement 
/usr/lib) et exécutez la commande ldconfig.
### Procédure
Effectuez les commandes suivantes:
```
git clone https://github.com/UbiCastTeam/python-ndi-sdk.git
cd python-ndi-sdk/
sed -i 's/\/bin/\/local\/bin/g' dbus-1/system-services/com.magewell.MWCapture.service
sudo ./setup.py install
```

## Utilisation
Après installation effectuez la commande suivante:
```
mc-magewell-signal 
A209180830030 HDMI 1920x1080p 60.00 Hz RGB
```
Ceci est un client D-Bus qui affiche les caractéristiques des périphériques
vidéos connectés sur le Capture Magewell.
