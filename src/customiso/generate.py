"""
Programme secondaire qui récupère des données utilisateur et les serializes en YAML,
avec une structure bien définie.
"""

import sys
import os
import tempfile
from pathlib import Path
from getpass import getpass

import yaml

from constants import *

class Generator:
    def __init__(self, quiet, output):
        self.quiet = quiet
        self.output = output
        self.yaml_file = ""
        self.data = {}

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
        self.printer("\nQuel sera le nom de votre fichier de configuration ?", 
                    "Vous pouvez spécifier un chemin complet, ou relatif.")
        self.yaml_file = Path(input(": ") or "/tmp/customiso.yaml")

        self.yaml_file = self.yaml_file.resolve()

        # On ajoute un suffixe .yaml s'il n'y est pas
        if self.yaml_file.suffix != "yaml" or self.yaml_file.suffix != "yml":
            self.yaml_file = self.yaml_file.with_suffix(".yaml")

        while self.yaml_file.exists():
            self.yaml_file = Path(input(f"{fCwarning}Le fichier spécifié existe déjà{rC}, veuillez faire un choix alternatif : "))

        self.yaml_file.touch()


    def config_preseed(self):
        self.printer("\n🔹 CONFIGURATION DE L'INSTALLATION SILENCIEUSE", 
                    "Pour toutes les questions, si vous laissez vide, vous serez interrogé par l'installateur au moment de l'installation.")

        # Localization
        self.printer("\nQuelle sera la langue pour l'installation (format ISO 639-1) ?", 
                    "Par exemple : en, fr, es, ...")
        language = input(": ") or None
        
        self.printer("\nQuelle sera le pays (format ISO 3166-1 alpha-2) ?", 
                    "Par exemple : UK, FR, ES, ...")
        county = input(": ") or None

        self.printer("\nQuelle sera la langue (format <ISO 639-1>_<ISO 3166-1 alpha-2>.<encodage>) ?", 
                    "Par exemple : en_US.UTF-8, fr_FR.UTF-8, ...")
        locale = input(": ") or None

        self.printer("\nQuelle sera la disposition du clavier ?", 
                    "Par exemple : fr(latin9), ...")
        keymap = input(": ") or None

        # Clock & Time zone
        self.printer("\nQuelle sera la zone de temps ?", 
                    "Par exemple : Europe/Paris, ...")
        timezone = input(": ") or None

        # Network
        self.printer("\nQuel sera le nom d'hôte ?", 
                    "Par exemple : customiso-computer.")
        hostname = input(": ") or None

        self.printer("\nQuel sera le nom de domaine ?", 
                    "Par exemple : local, u-picardie.fr, ...")
        domain = input(": ") or None

        self.printer("\nSouhaitez-vous effectuer la configuration IP ?", 
                    "Si vous ne disposerez pas d'une connexion réseau, choisissez non.")
        ip_config = input("[o/n] : ")
        
        if (ip_config.lower() in ("y", "o")):
            ip_config = True
        elif (ip_config.lower() in ("n")):
            ip_config = False
        else:
            ip_config = None

        # Mirror
        self.printer("\nQuel sera le miroir pour l'installation des paquets ?", 
                    "Par exemple : http.fr.debian.org, http.us.debian.org, ...")
        http_hostname = input(": ") or None

        self.printer("\nDans quel répertoire ?????", 
                    "Recommandé : /debian")
        http_directory = input(": ") or None

        self.printer("\nQuel est l'adresse du proxy HTTP pour l'installation des paquets ?", 
                    "Laissez vide si aucun.")
        http_proxy = input(": ") or None

        # Accounting
        self.printer("\nSouhaitez-vous activer le compte root ?", 
                    "Il est recommandé de laisser vide. Dans ce cas, sudo sera utilisé pour l'élévation de privilèges.")
        root_enable = input("[o/n] : ")
        
        if (root_enable.lower() in ("y", "o")):
            root_enable = True
            self.printer("\nQuel sera le mot de passe de root ?", 
                        "Choisissez un mot de passe sécurisé ! Laissez vide si vous souhaitez le demander au moment de l'installation.")
            root_password = getpass(": ") or None
        elif (root_enable.lower() in ("y", "o")):
            root_enable = False
        else:
            root_enable = None

        self.printer("\nQuel sera le nom complet de l'utilisateur principal ?", 
                    "Par exemple : Utilisateur Customiso")
        user_fullname = input(": ") or None

        self.printer("\nQuel sera le nom d'utilisateur de l'utilisateur principal ?", 
                    "Par exemple : user-customiso")
        user_username = input(": ") or None

        self.printer("\nQuel sera le mot de passe de l'utilisateur principal ?", 
                    "Choisissez un mot de passe sécurisé ! Laissez vide si vous souhaitez le demander au moment de l'installation.")
        user_password = getpass(": ") or None

        # Partitionning
        self.printer("\nQuel mode de partitionnement souhaitez-vous utiliser ?", 
                    """Par exemple 1, 2 ou 3.
        1 = Tout dans une même partition
        2 = Partition /homme séparée
        3 = Partition /home, /var et /tmp séparées.""")
        partitionning_mode = input(": ") or None

        # Packages
        self.printer("\nQuels paquets souhaitez-vous installer sur votre système ?", 
                    "Par exemple : standard, ssh-server, ...")
        tasksel = input(": ") or None

        self.printer("\nSouaitez-vous participer à l'étude sur les paquets ?", 
                    "")
        popularity_contest = input(": ") or None

        # Finishing
        self.printer("\nSouhaitez-vous faire apparaître le message de fin d'installation ?", 
                    "Si non, le système redémarrera sans afficher de message.")
        reboot_message = input(": ") or None

        self.printer("\nSouhaitez-vous que le support d'installation soit éjecté à la fin de l'installation ?", 
                    "Généralement c'est ce que vous souhaitez pour éviter de démarrer une nouvelle fois sur le support d'installation.")
        device_eject = input(": ") or None


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
