"""
Programme secondaire qui récupère des données utilisateur et les serializes en YAML,
avec une structure bien définie.
"""

import sys
import os
import tempfile
from pathlib import Path
import yaml

from constants import *

class Generator:
    def __init__(self, quiet, output):
        self.quiet = quiet
        self.output = output

    def printer(self, normal_str, verbose_str):
        print(normal_str)
        if self.quiet == False: print(f"{fCinfo}{verbose_str}{rC}")

    def start_generate(self):
        want_generate = input("⛽ Souaitez-vous générer un fichier de configuration pour Customiso Make ?\n[O/n] : ")
        if (not want_generate) or (want_generate.lower() in ("y", "o")):
            print("\n🚀 C'est parti.\n")
            print("=" * os.get_terminal_size().columns)
            
            self.init_config()
            self.config_preseed()
            self.config_additionnal_packages()
            self.config_additional_files()
            self.config_post_install_script()
        else:
            print("\n🤨 À bientôt.")
            sys.exit(1)

    def init_config(self):
        global f, content

        self.printer("\nQuel sera le nom de votre fichier de configuration ?", 
                    "Vous pouvez spécifier un chemin complet, ou relatif.")
        f = Path(input(": "))

        # On ajoute un suffixe .yaml s'il n'y est pas
        if f.suffix != "yaml" or f.suffix != "yml":
            f = f.with_suffix(".yaml")

        while f.exists():
            f = Path(input(f"{fCwarning}Le fichier spécifié existe déjà{rC}, veuillez faire un choix alternatif : "))

        f.touch()
        with open(f, "r") as customiso_yaml:
            content = yaml.safe_load(customiso_yaml)

    def config_preseed(self):
        self.printer("\n🔹 CONFIGURATION DE L'INSTALLATION SILENCIEUSE", 
                    "Pour toutes les questions, si vous laissez vide, vous serez interrogé par l'installateur au moment de l'installation.")

        self.printer("\nQuelle sera la langue sur le système (format ISO 639-1) ?", 
                    "Par exemple : en, fr, es, ...")
        language = input(": ")
        content["preseed"]["localization"] = "OOOOOOO"

        print(f)
        #with open(f, "w") as f:
        #    yaml.safe_dump(content, f, sort_keys=False)




    def config_additionnal_packages(self):
        pass

    def config_additional_files(self):
        pass

    def config_post_install_script(self):
        pass


#def printer(quiet: bool, normal_str: str, verbose_str: str):
#    print(normal_str)
#    if quiet == False: print(verbose_str)

#def ask_user(quiet: bool = False, path: str = "./"):
#
#    printer(quiet,
#        "\nQuel sera le nom d'hôte de votre machine ?",
#        "teeest")
#    hostname = input(": ")
#
#    print("\nQuel sera le nom complet de votre utilisateur (hors root) ?")
#    fullname = input(": ")
#
#    print("\nQuel sera l'identifiant de votre utilisateur (hors root) ?")
#    username = input(": ")
#
#    print("\nQuel sera le mot de passe de votre utilisateur (hors root) ?")
#    password = input(": ")
#
#    # Charger le fichier YAML
#    with open("somefile.yaml", "r") as f:
#        contenu = yaml.safe_load(f)
#
#    # Ajouter la liste dans la clé "markup"
#    contenu["languages"]["markup"] = ["YAML", "JSON", "XML"]
#
#    # Écrire les données modifiées dans le fichier YAML
#    with open("somefile.yaml", "w") as f:
#        yaml.safe_dump(contenu, f, sort_keys=False)
