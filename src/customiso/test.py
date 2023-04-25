#import yaml
#
#### ÉTAPE 01
#
#language = "fr"
#country = "en"
#locale = "en_US.UTF-8"
#keymap = 12
#
#content = {
#    "preseed": {
#        "localization": {
#            "language": language,
#            "country": country,
#            "locale": locale,
#            "keymap": keymap
#        }
#    }
#}
#
## Écrire le fichier YAML
#with open("yaml_file.yaml", "w") as f:
#    yaml.safe_dump(content, f, sort_keys=False)
#
#
#### ÉTAPE 02
#
#timezone = "Europe/Paris"
#
## Lire le fichier YAML
#with open("yaml_file.yaml", "r") as f:
#    content = yaml.safe_load(f)
#
## Ajouter les deux dernières lignes
#content_add = { 
#    "clock_time_zone": {
#        "timezone": timezone
#    }
#}
#content["preseed"].update(content_add)
#
## Écrire le fichier YAML
#with open("yaml_file.yaml", "w") as f:
#    yaml.safe_dump(content, f, sort_keys=False)

import inquirer

keymap = { 'keymap': {'bonjour': 'français', 'hello': 'anglais' } }

print(keymap.get('keymap'))
