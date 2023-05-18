# Customiso
<img src="https://placehold.co/160x10/137c8b/137c8b.png"><img src="https://placehold.co/80x10/e1a624/e1a624.png">
<img src="src/customiso/assets/img/logo_customiso.png"  width="25%" align="right">

Projet universitaire (UPJV) - M1 INFO 2023
<br />

Modifiez votre image ISO Debian facilement ! Ajoutez lui des paquets (.deb), configurez l'installation silencieuse (preseed), et ajoutez votre propre script de post-installation ; le tout hors-ligne !
<br />

## Présentation
Customiso est un programme avec une interface en ligne de commande (CLI).
<br />

Une commande de base : `customiso`. Cette commande a deux commandes enfants, à savoir `customiso generate` et `customiso make`.
<br />

L’objectif est d’automatiser le processus de modification d’une image ISO Linux Debian afin de :
- Configurer de l’installation silencieuse ;
- Ajouter de paquets « .deb » et installer automatiquement ces derniers ;
- Ajouter des fichiers personnalisés à des emplacements spécifiques de l’arborescence ;
- Ajouter un script de post installation personnalisé.
La simplicité d’usage est la devise de Customiso !
<br />

## Customiso Generate
Permet de générer un fichier YAML avec un ensemble d’informations relatives à la modification souhaitée de l’image ISO.
Exemple d'utilisation :
```bash
python src/customiso generate -c /tmp/customiso-generate
```
<br />

## Customiso Make
Permet, avec un fichier YAML correctement formaté en entrée (comme celui généré par Customiso Generate), de modifier l’image ISO en conséquence du fichier passé en paramètre.
Exemple d'utilisation :
```bash
python src/customiso make -c "yaml_file.yaml" -i "debian-11.7.0-amd64-DVD-1.iso" -o "debian_custom"
```
<br />

## Documentation
En plus de cette documentation, utilisez les options `--help` sur chaque commande.

Une page `man` est également disponnible.

<br />

## Setup du projet (pour les utilisateurs)
```bash
curl -LO 
sudo apt install ./
```

Le programme est installé sur votre système suivant cette arborescence :
```
/
├── usr
│   ├── bin
│   ├── lib
│   │   └── customiso
│   └── share
│       └── man
└── var
    └── lib
        └── customiso
```

## Setup du projet (pour les développeurs)
### Dépendances
Vous devrez avoir Python3.10 (et pip) ainsi que git.
Les autres dépendances sont indiqués ci-après.

**Distributions Debian-based**

Acune dépendance.

**Distributions Arch-based**

```bash
yay -Sy apt dpkg 
```

### Setup
```bash
git clone git@github.com:Tanguy00/Customiso.git && cd Customiso

python -m venv .pyenv
source .pyenv/bin/activate  # On entre dans l'env

pip install -r requirements.txt
```
<br />

## Fichier de configuration Customiso
|Directive|Description                  |Valeur|
|---------|-----------------------------|------|
|preseed.localization.language|La langue parlée/écrite pour l'installation.|"ask", [string]|
|preseed.localization.country|Le pays de résidence.        |"ask", [string]|
|preseed.localization.locale|La langue parlée/écrite.     |"ask", [string]|
|preseed.localization.keymap|La langue du clavier.        |"ask", [string]|
|preseed.clock_time_zone.timezone|Le fuseau horaire.           |"ask", [string]|
|preseed.network.hostname|Le nom d'hôte.               |"ask", [string]|
|preseed.network.domain|Le domaine.                  |"ask", "none", [string]|
|preseed.network.advanced.ip_config|Si le système dispose ou non d'internet pour l'installation.|"ask", [boolean]|
|preseed.mirror.http_hostname|L'hôte HTTP pour le miroir.  |"ask", [string]|
|preseed.mirror.http_proxy|Le proxy HTTP pour le miroir.|"ask", "none", [string]|
|preseed.accounting.root.enable|Indique si le compte root est activé.|[boolean]|
|preseed.accounting.root.password|Le mot de passe chiffré du compte root.|"ask", [string]|
|preseed.accounting.user.fullname|Le nom complet de l'utilisateur.|"ask", [string]|
|preseed.accounting.user.username|Le nom d'utilisateur.        |"ask", [string]|
|preseed.accounting.user.password|Le mot de passe chiffré de l'utilisateur.|"ask", [string]|
|preseed.partitionning.predefined_mode|Le mode de partitionnement prédéfini.|"ask", 0, 1, 2, 3|
|preseed.packages.tasksel|Les composants du système à installer. Valeurs possibles : 'standard', 'desktop', 'gnome-desktop', 'kde-desktop', 'xfce-desktop', 'web-server', 'ssh-server'.|"ask", [list(string)]|
|preseed.packages.popularity_contest|Si vous souhaitez participer à popularity_contest.|"ask", [boolean]|
|preseed.finishing.reboot_message|Indique si un message de redémarrage est affiché.|"ask", [boolean]|
|preseed.finishing.device_eject|Indique si l'éjection du support est activée.|"ask", [boolean]|
|additional_packages|Les packages additionnels à installer.|"none", [list(string)]|
|additional_files|Les fichiers additionnels à ajouter et leur futur emplacement.|"none", [list("from": [string], "to": [string])]|
|post_install_script|Le script exécuté après l'installation.|"none", [string]|

