"""
Programme secondaire qui récupère des données utilisateur et les serializes en YAML,
avec une structure bien définie.
"""

import sys
import os
import shutil

import yaml

from constants import *

class Maker:
    def __init__(self, conf_file, in_iso, out_iso):
        self.conf_file = conf_file
        self.in_iso = in_iso
        self.out_iso = out_iso

#    def printer(self, normal_str, verbose_str):
#        print(normal_str)
#        if self.quiet == False: print(f"{fCinfo}{verbose_str}{rC}")

    def start_make(self):
        # Suppression du répertoire /tmp/customiso s'il existe déjà
        shutil.rmtree('/tmp/customiso', ignore_errors=True)
        # Création du répertoire /tmp/customiso
        os.makedirs('/tmp/customiso')

        # Création d'un fichier vide "build_pressed"
        open('/tmp/customiso/build_pressed', 'w').close()

        self.build_presseed()
        self.extract_iso()
        self.import_presseed()
        self.build_customiso_package()
        self.import_packages()
        self.pack_iso()

    def build_presseed(self):
        with open(self.conf_file, 'r') as f:
            try:
                yaml_data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)
                return False

        preseed_cfg = []

        # LOCALIZATION
        localization = yaml_data['preseed']['localization']

        if localization['language']:
            preseed_cfg.append(f"d-i debian-installer/language string {localization['language']}")
        else:
            preseed_cfg.append("d-i debian-installer/language string FAILED")

        if localization['country']:
            preseed_cfg.append(f" {localization['country']}")
        else:
            preseed_cfg.append(" FAILED")

        if localization['locale']:
            preseed_cfg.append(f" {localization['locale']}")
        else:
            preseed_cfg.append(" FAILED")

        if localization['keymap']:
            preseed_cfg.append(f" {localization['keymap']}")
        else:
            preseed_cfg.append(" FAILED")
        
        # CLOCK_TIME_ZONE
        clock_time_zone = yaml_data['preseed']['clock_time_zone']

        if clock_time_zone['timezone']:
            preseed_cfg.append(f" {clock_time_zone['timezone']}")
        else:
            preseed_cfg.append(" FAILED")

        # NETWORK
        network = yaml_data['preseed']['network']

        if network['hostname']:
            preseed_cfg.append(f" {network['hostname']}")
        else:
            preseed_cfg.append(" FAILED")

        if network['domain']:
            preseed_cfg.append(f" {network['domain']}")
        else:
            preseed_cfg.append(" FAILED")

        if network['advanced']['ip_config']:
            preseed_cfg.append(f" {network['advanced']['ip_config']}")
        else:
            preseed_cfg.append(" FAILED")

        # MIRROR
        mirror = yaml_data['preseed']['mirror']

        if mirror['http_hostname']:
            preseed_cfg.append(f" {mirror['http_hostname']}")
        else:
            preseed_cfg.append(" FAILED")

        if mirror['http_proxy']:
            preseed_cfg.append(f" {mirror['http_proxy']}")
        else:
            preseed_cfg.append(" FAILED")

        # ACCOUNTING
        accounting = yaml_data['preseed']['accounting']

        if accounting['root']['enable']:
            preseed_cfg.append(f" {accounting['root']['enable']}")
        else:
            preseed_cfg.append(" FAILED")

        if accounting['root']['password']:
            preseed_cfg.append(f" {accounting['root']['password']}")
        else:
            preseed_cfg.append(" FAILED")

        if accounting['user']['fullname']:
            preseed_cfg.append(f" {accounting['user']['fullname']}")
        else:
            preseed_cfg.append(" FAILED")

        if accounting['user']['username']:
            preseed_cfg.append(f" {accounting['user']['username']}")
        else:
            preseed_cfg.append(" FAILED")

        if accounting['user']['password']:
            preseed_cfg.append(f" {accounting['user']['password']}")
        else:
            preseed_cfg.append(" FAILED")

        # PARTITIONNING
        partitionning = yaml_data['preseed']['partitionning']

        if partitionning['predefined_mode']:
            preseed_cfg.append(f" {partitionning['predefined_mode']}")
        else:
            preseed_cfg.append(" FAILED")

        # PACKAGES
        packages = yaml_data['preseed']['packages']

        if packages['tasksel']:
            tasksel_list = ', '.join(packages['tasksel'])
            preseed_cfg.append(f"tasksel tasksel/first multiselect {tasksel_list}")
        else:
            preseed_cfg.append(" FAILED")

        if packages['popularity_contest']:
            preseed_cfg.append(f" {packages['popularity_contest']}")
        else:
            preseed_cfg.append(" FAILED")

        # FINISHING
        if yaml_data['additional_packages']:
            pass

        if yaml_data['post_install_script']:
            pass

        finishing = yaml_data['preseed']['finishing']

        if finishing['reboot_message']:
            preseed_cfg.append(f" {finishing['reboot_message']}")
        else:
            preseed_cfg.append(" FAILED")
        
        if finishing['device_eject']:
            preseed_cfg.append(f" {finishing['device_eject']}")
        else:
            preseed_cfg.append(" FAILED")



        #if 'preseed' in yaml_data and 'packages' in yaml_data['preseed'] and 'tasksel' in yaml_data['preseed']['packages']:
        #    tasksel = yaml_data['preseed']['packages']['tasksel']
        #    tasksel_list = ', '.join(tasksel)
        #    preseed_cfg.append(f"tasksel tasksel/first multiselect {tasksel_list}")
        

        #if 'preseed' in yaml_data and 'localization' in yaml_data['preseed']:
        #    localization = yaml_data['preseed']['localization']
        #    if 'language' in localization and localization['language']:
        #        preseed_cfg.append(f"d-i debian-installer/language string {localization['language']}")
        #    else:
        #        preseed_cfg.append("d-i debian-installer/language string FAILED")
        #    if 'country' in localization and localization['country']:
        #        preseed_cfg.append(f"d-i debian-installer/country string {localization['country']}")
        #    else:
        #        preseed_cfg.append("d-i debian-installer/country string FAILED")
        #    if 'locale' in localization and localization['locale']:
        #        preseed_cfg.append(f"d-i debian-installer/locale string {localization['locale']}")
        #    else:
        #        preseed_cfg.append("d-i debian-installer/locale string FAILED")
        #    if 'keymap' in localization and localization['keymap']:
        #        preseed_cfg.append(f"d-i keyboard-configuration/xkb-keymap select {localization['keymap']}")
        #    else:
        #        preseed_cfg.append("d-i keyboard-configuration/xkb-keymap select FAILED")

        

        with open('/tmp/customiso/build_pressed', 'w') as preseed:
            preseed.write('\n'.join(preseed_cfg))

    def extract_iso(self):
        pass

    def import_presseed(self):
        pass

    def build_customiso_package(self):
        pass

    def import_packages(self):
        pass

    def pack_iso(self):
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
