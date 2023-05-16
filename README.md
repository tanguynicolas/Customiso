# Customiso
<img src="https://placehold.co/160x10/137c8b/137c8b.png"><img src="https://placehold.co/80x10/e1a624/e1a624.png">
<img src="src/customiso/assets/img/logo_customiso.png"  width="25%" align="right">

Projet universitaire (UPJV) - M1 INFO 2023
<br />

Modifiez votre image ISO Debian facilement ! Ajoutez lui des paquets (.deb), configurez l'installation silencieuse (preseed), et ajoutez votre propre script de post-installation ; le tout hors-ligne !

## Présentation
Customiso est un programme avec une interface en ligne de commande (CLI).
<br />
Une commande de base : `customiso`. Cette commande a deux commandes enfants, à savoir `customiso generate` et `customiso make`
<br />
L’objectif est d’automatiser le processus de modification d’une image ISO Linux Debian afin de :
- Configurer de l’installation silencieuse ;
- Ajouter de paquets « .deb » et installer automatiquement ces derniers ;
- Ajouter des fichiers personnalisés à des emplacements spécifiques de l’arborescence ;
- Ajouter un script de post installation personnalisé.
La simplicité d’usage est la devise de Customiso !


## Customiso Generate
Permet de générer un fichier YAML avec un ensemble d’informations relatives à la modification souhaitée de l’image ISO.
Exemple d'utilisation :
```bash
python src/customiso generate -c /tmp/customiso-generate
```

## Customiso Make
Permet, avec un fichier YAML correctement formaté en entrée, de modifier l’image ISO en conséquence du fichier passé en paramètre.
Exemple d'utilisation :
```bash
python src/customiso make -c "yaml_file.yaml" -i "debian-11.7.0-amd64-DVD-1.iso" -o "debian_custom"
```

## Setup projet
```bash
python -m venv .pyenv
source .pyenv/bin/activate  # On entre dans l'env

pip install -r requirements.txt

deactivate                  # On sort de l'env
```

Require: yaml
