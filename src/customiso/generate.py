"""
Programme secondaire qui récupère des données utilisateur et les serializes en YAML,
avec une structure bien définie.
"""

import sys
import os
from pathlib import Path
from getpass import getpass
import subprocess

import yaml
import inquirer
from inquirer.themes import BlueComposure

from constants import *

class Generator:
    def __init__(self, quiet, output):
        self.quiet = quiet
        self.output = output

    def printer(self, normal_str, verbose_str):
        print(normal_str)
        if self.quiet == False: print(f"{fCinfo}{verbose_str}{rC}")

    def start_generate(self):
        want_generate = input("⛽ Souaitez-vous générer un fichier de configuration pour Customiso Make ?\n(O/n) : ")
        if (not want_generate) or (want_generate.lower() in ("y", "o")):
            print("\n🚀 C'est parti.\n")
            print("=" * os.get_terminal_size().columns)
            
            self.init_config()
            self.config_preseed()
            self.config_additionnal_packages()
            self.config_additional_files()
            self.config_post_install_script()
            self.end_generate()
        else:
            print("\n🤨 À bientôt.")
            sys.exit(1)

    def init_config(self):
        if self.output:
            self.yaml_file = Path(self.output)
        else:
            self.printer("\nQuel sera le nom de votre fichier de configuration ?", 
                        "Vous pouvez spécifier un chemin complet, ou relatif.")
            self.yaml_file = Path(input(": ") or "/tmp/customiso.yaml")

        self.yaml_file = self.yaml_file.resolve()

        # On ajoute un suffixe .yaml s'il n'y est pas
        if self.yaml_file.suffix != "yaml" or self.yaml_file.suffix != "yml":
            self.yaml_file = self.yaml_file.with_suffix(".yaml")

        while self.yaml_file.exists():
            self.yaml_file = Path(input(f"{fCwarning}Le fichier de sortie spécifié existe déjà{rC}, veuillez faire un choix alternatif : "))

        self.yaml_file.touch()

    def config_preseed(self):
        self.printer("\n🔹 CONFIGURATION DE L'INSTALLATION SILENCIEUSE", 
                    "Pour toutes les questions, si vous répondez « ask », vous serez interrogé par l'installateur au moment de l'installation.\nSi vous répondez « none », l'installateur ignorera la configuration de l'option.\nAttention, toutes les questions n'acceptent pas forcément ces réponses.\nVoir documentation : https://github.com/Tanguy00/Customiso/blob/main/README.md.")
        print()

        ## Localization
        questions = [
        inquirer.List('language',
                        message="Quelle sera la langue pour l'installation (format ISO 639-1) ? ",
                        choices=['ask', 'fr', 'en', 'es']
                    )
        ]
        self.language = inquirer.prompt(questions, theme=BlueComposure())
        
        questions = [
        inquirer.List('country',
                        message="Quel sera le pays (format ISO 3166-1 alpha-2) ? ",
                        choices=['ask', 'FR', 'US', 'UK', 'ES']
                    )
        ]
        self.country = inquirer.prompt(questions, theme=BlueComposure())

        questions = [
        inquirer.List('locale',
                        message="Quelle sera la langue (format <ISO 639-1>_<ISO 3166-1 alpha-2>.<encodage>) ? ",
                        choices=['ask', 'fr_FR.UTF-8', 'en_US.UTF-8']
                    )
        ]
        self.locale = inquirer.prompt(questions, theme=BlueComposure())

        questions = [
        inquirer.List('keymap',
                        message="Quelle sera la disposition du clavier ? ",
                        choices=['ask', 'fr(latin9)']
                    )
        ]
        self.keymap = inquirer.prompt(questions, theme=BlueComposure())

        ## Clock & Time zone
        questions = [
        inquirer.List('timezone',
                        message="Quelle sera la zone de temps ? ",
                        choices=['ask', 'Europe/Paris']
                    )
        ]
        self.timezone = inquirer.prompt(questions, theme=BlueComposure())

        ## Network
        questions = [
        inquirer.Text('hostname', message="Quel sera le nom d'hôte ? ")
        ]
        hostname = inquirer.prompt(questions, theme=BlueComposure())
        self.hostname = hostname['hostname']
        if self.hostname == '':
            self.hostname = "ask"

        print()

        questions = [
        inquirer.Text('domain', message="Quel sera le nom de domaine ? ")
        ]
        domain = inquirer.prompt(questions, theme=BlueComposure())
        self.domain = domain['domain']
        if self.domain == '':
            self.domain = "ask"

        self.printer("\n[?] Souhaitez-vous effectuer la configuration IP ?", 
                    "Si vous ne disposerez pas d'une connexion réseau, choisissez non.")
        ip_config = input("(o/n/ASK) : ")
        
        if (ip_config.lower() in ("y", "o")):
            self.ip_config = True
        elif (ip_config.lower() == "n"):
            self.ip_config = False
        else:
            self.ip_config = "ask"

        print()

        # Mirror
        questions = [
        inquirer.List('http_hostname',
                        message="Quel sera le miroir pour l'installation des paquets ? ",
                        choices=['ask', 'http.fr.debian.org', 'http.us.debian.org', 'deb.debian.org']
                    )
        ]
        self.http_hostname = inquirer.prompt(questions, theme=BlueComposure())

        print("[?] Souhaitez-vous utiliser un mandataire HTTP ?")
        http_proxy = input("(o/n/ASK) : ")

        if (http_proxy.lower() in ("y", "o")):
            questions = [
            inquirer.Text('http_proxy', message="Quelle est son adresse ? ")
            ]
            self.http_proxy = inquirer.prompt(questions, theme=BlueComposure())
        elif (http_proxy.lower() == "n"):
            self.http_proxy = {'http_proxy': 'none'}
        else:
            self.http_proxy = {'http_proxy': 'ask'}

        # Accounting
        self.printer("\n[?] Souhaitez-vous activer le compte root ?", 
                    "Il est recommandé de ne pas l'utiliser. Dans ce cas, sudo sera utilisé pour l'élévation de privilèges.")
        root_enable = input("(o/N) : ")
        
        if (root_enable.lower() in ("y", "o")):
            self.root_enable = True
            self.printer("\nQuel sera le mot de passe de root ?", 
                        "Choisissez un mot de passe sécurisé ! Laissez vide si vous souhaitez le demander au moment de l'installation.")
            raw_root_password = getpass(": ") or "ask"

            if raw_root_password != "ask":
                tmp_root_password = subprocess.run(f"mkpasswd -m sha-512 {raw_root_password}", shell=True, stdout=subprocess.PIPE)
                self.root_password = tmp_root_password.stdout.decode().strip()
            else:
                self.root_password = raw_root_password

        else:
            self.root_enable = False
            self.root_password = "root_disabled"

        print()

        questions = [
        inquirer.Text('user_fullname', message="Quel sera le nom complet de l'utilisateur principal ? ")
        ]
        user_fullname = inquirer.prompt(questions, theme=BlueComposure())
        self.user_fullname = user_fullname['user_fullname']
        if self.user_fullname == '':
            self.user_fullname = "ask"

        print()

        questions = [
        inquirer.Text('user_username', message="Quel sera le nom d'utilisateur de l'utilisateur principal ? ")
        ]
        user_username = inquirer.prompt(questions, theme=BlueComposure())
        self.user_username = user_username['user_username']
        if self.user_username == '':
            self.user_username = "ask"

        self.printer("\n[?] Quel sera le mot de passe de l'utilisateur principal ?", 
                    "Choisissez un mot de passe sécurisé ! Laissez vide si vous souhaitez le demander au moment de l'installation.")
        raw_user_password = getpass(": ") or "ask"

        if raw_user_password != "ask":
            tmp_user_password = subprocess.run(f"mkpasswd -m sha-512 {raw_user_password}", shell=True, stdout=subprocess.PIPE)
            self.user_password = tmp_user_password.stdout.decode().strip()
        else:
            self.user_password = raw_user_password

        # Partitionning
        print("""\nListe des modes de partitionnement :
    0 = Laisse l'installateur demander
    1 = Tout dans une même partition
    2 = Partition /homme séparée
    3 = Partition /home, /var et /tmp séparées.""")

        questions = [
        inquirer.List('partitionning_mode',
                        message="Quel mode de partitionnement souhaitez-vous utiliser ? ",
                        choices=[0, 1, 2, 3]
                    )
        ]
        self.partitionning_mode = inquirer.prompt(questions, theme=BlueComposure())

        # Packages
        questions = [
        inquirer.Checkbox('tasksel',
                            message = "Quels paquets souhaitez-vous installer sur votre système (laisser vide vaudra « ask ») ? ",
                            choices = ['standard', 'desktop', 'gnome-desktop', 'kde-desktop', 'xfce-desktop', 'web-server', 'ssh-server'],
                            autocomplete = ['standard'],
                        )
        ]
        tasksel = inquirer.prompt(questions, theme=BlueComposure())
        self.tasksel = tasksel['tasksel']

        if self.tasksel == []:
            self.tasksel = "ask"


        print("[?] Souaitez-vous participer à l'étude sur les paquets ?")
        popularity_contest = input("(o/n/ASK) : ")

        if (popularity_contest.lower() in ("y", "o")):
            self.popularity_contest = True
        elif (popularity_contest.lower() == "n"):
            self.popularity_contest = False
        else:
            self.popularity_contest = "ask"

        # Finishing
        self.printer("\nSouhaitez-vous faire apparaître le message de fin d'installation ?", 
                    "Si non, le système redémarrera sans afficher de message.")
        reboot_message = input("(o/n/ASK) : ")

        if (reboot_message.lower() in ("y", "o")):
            self.reboot_message = True
        elif (reboot_message.lower() == "n"):
            self.reboot_message = False
        else:
            self.reboot_message = "ask"

        self.printer("\nSouhaitez-vous que le support d'installation soit éjecté à la fin de l'installation ?", 
                    "Généralement c'est ce que vous souhaitez pour éviter de démarrer une nouvelle fois sur le support d'installation.")
        device_eject = input("(o/n/ASK) : ")

        if (device_eject.lower() in ("y", "o")):
            self.device_eject = True
        elif (device_eject.lower() == "n"):
            self.device_eject = False
        else:
            self.device_eject = "ask"


    def config_additionnal_packages(self):
        self.printer("\n🔹 AJOUT DE PAQUETS ADDITIONNELS", 
                    "Ajoutez uniquement des paquets « .deb ».")

        add_packages = input("\nVoulez-vous ajouter des paquets ?\n(o/N) : ")

        self.additional_packages = []
        while (add_packages.lower() in ("y", "o")):
            package_name = input("Entrez le nom du paquet : ")

            if os.path.isfile(package_name) and package_name.endswith(".deb"):
                    self.additional_packages.append(package_name)
                    add_packages = input("Voulez-vous ajouter un autre paquet ? (O/n) ") or "o"
            else:
                print(f"{fCwarning}Le nom du paquet saisi n'est pas valide. Veuillez saisir un nom de fichier .deb valide.{rC}")

        if self.additional_packages == []:
            self.additional_packages = "none"


    def config_additional_files(self):
        self.printer("\n🔹 AJOUT DE FICHIERS ADDITIONNELS", 
                    "Ajoutez tous les fichiers que vous souhaitez, à l'endroit où vous le souhaitez.")

        add_files = input("\nVoulez-vous ajouter des fichiers ?\n(o/N) : ")

        self.additional_files = []
        while (add_files.lower() in ("y", "o")):
            from_file = input("Entrez le chemin du fichier source : ")
            if not os.path.isfile(from_file):
                print(f"{fCwarning}Le fichier spécifié n'existe pas.{rC}")
                continue

            to_file = input("Entrez l'emplacement de destination : ")

            self.additional_files.append({'from': from_file, 'to': to_file})
            add_files = input("Voulez-vous ajouter d'autres fichiers ? (O/n) : ") or "o"

        if self.additional_files == []:
            self.additional_files = "none"


    def config_post_install_script(self):
        self.printer("\n🔹 AJOUT D'UN SCRIPT DE POST INSTALLATION", 
                    "Indiquez simplement le chemin du script Bash que vous voudrez exécuter en fin d'installation.")

        add_script = input("\nVoulez-vous ajouter un script de post-installation ?\n(o/N) : ")

        self.post_install_script = "none"
        while (add_script.lower() in ("y", "o")):
            self.post_install_script = input("Entrez le chemin vers le script : ")
            if not os.path.isfile(self.post_install_script):
                print(f"{fCwarning}Le fichier spécifié n'existe pas.{rC}")
                continue
            else:
                break


    def end_generate(self):
        data =  {
            'preseed': {
                'localization': {
                    'language': getattr(self, 'language')['language'],
                    'country': getattr(self, 'country')['country'],
                    'locale': getattr(self, 'locale')['locale'],
                    'keymap': getattr(self, 'keymap')['keymap']
                },
                'clock_time_zone': {
                    'timezone': getattr(self, 'timezone')['timezone']
                },
                'network': {
                    'hostname': self.hostname,
                    'domain': self.domain,
                    'advanced': {
                        'ip_config': self.ip_config
                    },
                },
                'mirror': {
                    'http_hostname': getattr(self, 'http_hostname')['http_hostname'],
                    'http_proxy': getattr(self, 'http_proxy')['http_proxy']
                },
                'accounting': {
                    'root': {
                        'enable': self.root_enable,
                        'password': self.root_password
                    },
                    'user': {
                        'fullname': self.user_fullname,
                        'username': self.user_username,
                        'password': self.user_password
                    }
                },
                'partitionning': {
                    'predefined_mode': getattr(self, 'partitionning_mode')['partitionning_mode']
                },
                'packages': {
                    'tasksel': self.tasksel,
                    'popularity_contest': self.popularity_contest
                },
                'finishing': {
                    'reboot_message': self.reboot_message,
                    'device_eject': self.device_eject
                }
            },
            'additional_packages': self.additional_packages,
            'additional_files': self.additional_files,
            'post_install_script': self.post_install_script
        }

        info = """# Customiso - 2023"

# Toutes les valeurs à « ask », aux endroits où cela est pris en charge, se résulteront par une demande d'information au moment de l'installation.
# Les valeurs à « none », aux endroits où cela est pris en charge, se résulteront par un non déploiement de la fonctionnalité.\n\n
# Voir documentation : https://github.com/Tanguy00/Customiso/blob/main/README.md."""

        with open(self.yaml_file, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)
            
        with open(self.yaml_file, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(info.rstrip('\r\n') + '\n\n' + content + '\n')

        print("\n" + "=" * os.get_terminal_size().columns)
        print(f"\n{fCsuccess}{fB}Votre fichier a bien été généré !{rC}\nRetrouvez-le ici : {self.yaml_file}\n")
        print(f"Poursuivez la création de votre image ISO via la commande suivante : {fI}customiso make -c \"{self.yaml_file}\" -i \"<input_iso_file>\" -o \"<output_iso_name>\"{rC}\n")
