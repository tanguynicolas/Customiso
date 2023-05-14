"""
Programme secondaire qui récupère des données utilisateur et les serializes en YAML,
avec une structure bien définie.
"""

import subprocess
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

        # Récupération du chemin du script
        self.python_path = os.path.realpath(os.path.dirname(__file__))

        self.extract_iso()
        self.build_presseed()
        self.import_presseed()
        self.import_packages()
        self.pack_iso()

    def extract_iso(self):
        try:
            subprocess.call([f'{self.python_path}/scripts/extract.sh', '--iso', self.in_iso])
        except:
            print("[ ❌ ] Extraction du fichier ISO\n")
            sys.exit(1)
        else:
            print("[ ✅ ] Extraction du fichier ISO\n")

    def build_presseed(self):
        with open(self.conf_file, 'r') as f:
            try:
                yaml_data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)
                return False

        preseed_cfg = []
        preseed_cfg.append("# Customiso - 2023")

        # LOCALIZATION
        preseed_cfg.append("\n# LOCALIZATION")
        localization = yaml_data['preseed']['localization']

        if localization['language']:
            preseed_cfg.append(f"d-i debian-installer/language string {localization['language']}")
        else:
            preseed_cfg.append("d-i debian-installer/language string FAILED")

        if localization['country']:
            preseed_cfg.append(f"d-i debian-installer/country string {localization['country']}")
        else:
            preseed_cfg.append(" FAILED")

        if localization['locale']:
            preseed_cfg.append(f"d-i debian-installer/locale string {localization['locale']}")
        else:
            preseed_cfg.append(" FAILED")

        if localization['keymap']:
            preseed_cfg.append(f"d-i keyboard-configuration/xkb-keymap select {localization['keymap']}")
        else:
            preseed_cfg.append(" FAILED")
        
        # CLOCK_TIME_ZONE
        preseed_cfg.append("\n# CLOCK_TIME_ZONE")
        clock_time_zone = yaml_data['preseed']['clock_time_zone']

        if clock_time_zone['timezone']:
            preseed_cfg.append(f"d-i time/zone string {clock_time_zone['timezone']}")
        else:
            preseed_cfg.append(" FAILED")

        # NETWORK
        preseed_cfg.append("\n# NETWORK")
        network = yaml_data['preseed']['network']

        if network['hostname']:
            preseed_cfg.append(f"d-i netcfg/get_hostname string {network['hostname']}")
        else:
            preseed_cfg.append(" FAILED")

        if network['domain']:
            preseed_cfg.append(f"d-i netcfg/get_domain string {network['domain']}")
        else:
            preseed_cfg.append(" FAILED")

        if network['advanced']['ip_config']:
            preseed_cfg.append(f"d-i netcfg/enable boolean {network['advanced']['ip_config']}")
        else:
            preseed_cfg.append("d-i netcfg/choose_interface select auto")
            preseed_cfg.append("d-i netcfg/dhcp_timeout string 8")
            preseed_cfg.append("d-i netcfg/dhcpv6_timeout string 8")

        # MIRROR
        preseed_cfg.append("\n# MIRROR")
        mirror = yaml_data['preseed']['mirror']

        if mirror['http_hostname']:
            preseed_cfg.append(f"d-i mirror/http/hostname string {mirror['http_hostname']}")
        else:
            preseed_cfg.append(" FAILED")

        if mirror['http_proxy']:
            preseed_cfg.append(f"d-i mirror/http/proxy string {mirror['http_proxy']}")
        else:
            preseed_cfg.append("d-i mirror/http/proxy string")

        # ACCOUNTING
        preseed_cfg.append("\n# ACCOUNTING")
        accounting = yaml_data['preseed']['accounting']

        if accounting['root']['enable']:
            preseed_cfg.append(f"d-i passwd/root-login boolean {accounting['root']['enable']}")
        else:
            preseed_cfg.append(" FAILED")

        if accounting['root']['password']:
            preseed_cfg.append(f"d-i passwd/root-password password {accounting['root']['password']}")
            preseed_cfg.append(f"d-i passwd/root-password-again password {accounting['root']['password']}")
        else:
            preseed_cfg.append(" FAILED")

        if accounting['user']['fullname']:
            preseed_cfg.append(f"d-i passwd/user-fullname string {accounting['user']['fullname']}")
        else:
            preseed_cfg.append(" FAILED")

        if accounting['user']['username']:
            preseed_cfg.append(f"d-i passwd/username string {accounting['user']['username']}")
        else:
            preseed_cfg.append(" FAILED")

        if accounting['user']['password']:
            preseed_cfg.append(f"d-i passwd/user-password password {accounting['user']['password']}")
            preseed_cfg.append(f"d-i passwd/user-password-again password {accounting['user']['password']}")
        else:
            preseed_cfg.append(" FAILED")

        # PARTITIONNING
        preseed_cfg.append("\n# PARTITIONNING")
        partitionning = yaml_data['preseed']['partitionning']

        if partitionning['predefined_mode']:
            preseed_cfg.append(f" {partitionning['predefined_mode']}")
        else:
            preseed_cfg.append(" FAILED")

        # PACKAGES
        preseed_cfg.append("\n# PACKAGES")
        packages = yaml_data['preseed']['packages']

        if packages['tasksel']:
            tasksel_list = ', '.join(packages['tasksel'])
            preseed_cfg.append(f"tasksel tasksel/first multiselect {tasksel_list}")
        else:
            preseed_cfg.append(" FAILED")

        if packages['popularity_contest']:
            preseed_cfg.append(f"popularity-contest popularity-contest/participate boolean {packages['popularity_contest']}")
        else:
            preseed_cfg.append(" FAILED")

        # FINISHING
        preseed_cfg.append("\n# FINISHING")
        
        customiso_pusher = False
        if yaml_data['post_install_script'] or yaml_data['additional_files']:
            customiso_pusher = True

            # Fabrication du paquet .deb
            os.makedirs('/tmp/customiso/customiso-pusher', exist_ok=True)
            shutil.copytree(f'{self.python_path}/templates/packages/customiso-pusher/DEBIAN', '/tmp/customiso/customiso-pusher/DEBIAN')
            os.chmod("/tmp/customiso/customiso-pusher/DEBIAN/postinst", 0o755)

            if yaml_data['post_install_script']:
                os.makedirs('/tmp/customiso/customiso-pusher/opt', exist_ok=True)
                shutil.copy(yaml_data['post_install_script'], '/tmp/customiso/customiso-pusher/opt/customiso-postinstall')

            if yaml_data['additional_files']:
                for p in yaml_data['additional_files']:
                    os.makedirs(os.path.dirname(f"/tmp/customiso/customiso-pusher/{p['to']}"), exist_ok=True)
                    shutil.copy(p['from'], f"/tmp/customiso/customiso-pusher/{p['to']}")
            
            # Ajout du paquet .deb
            os.makedirs('/tmp/customiso/cdrom/pool/main/c/customiso-pusher', exist_ok=True)

        if yaml_data['additional_packages']:
            all_packages = []

            for package in yaml_data['additional_packages']:
                # Récupération du nom de chaque paquet dans une liste
                package_name = subprocess.run(f"dpkg --info {package} | grep 'Package:\s' | cut -d ' ' -f 3", shell=True, stdout=subprocess.PIPE)
                package_real_name = package_name.stdout.decode().strip()
                all_packages.append(package_real_name)
                
                # Copie de tous les paquets dans le bon endroit de l'ISO
                package_first_letter = package_real_name[0]
                package_path = f'/tmp/customiso/cdrom/pool/main/{package_first_letter}/{package_real_name}'
                os.makedirs(package_path, exist_ok=True)
                shutil.copy(package, package_path)

            # On glisse le script customiso-pusher dans la liste s'il existe
            if customiso_pusher:
                all_packages.append('customiso-pusher')
                preseed_cfg.append("d-i preseed/late_command string in-target /bin/bash /opt/customiso-postinstall")
                print("[ ✅ ] Ajout du script de post-installation et/ou des fichiers personalisés.\n")

            package_list = ', '.join(all_packages)
            preseed_cfg.append(f"d-i pkgsel/include string {package_list}")

            print("[ ✅ ] Ajout des nouveaux packages\n")
        else:
            preseed_cfg.append(" FAILED")

        finishing = yaml_data['preseed']['finishing']

        if finishing['reboot_message'] == True:
            preseed_cfg.append("d-i finish-install/reboot_in_progress note")
        else:
            preseed_cfg.append(" FAILED")
        
        if finishing['device_eject']:
            preseed_cfg.append(f"d-i cdrom-detect/eject boolean {finishing['device_eject']}")
        else:
            preseed_cfg.append(" FAILED")

        # MANDATORY / UNSUPPORTED
        preseed_cfg.append("\n# MANDATORY / UNSUPPORTED")
        preseed_cfg.append("d-i clock-setup/utc boolean true")
        preseed_cfg.append("d-i hw-detect/load_firmware boolean true")
        preseed_cfg.append("d-i mirror/country string manual")
        preseed_cfg.append("d-i mirror/http/directory string /debian")
        preseed_cfg.append("d-i apt-setup/cdrom/set-first boolean false")
        preseed_cfg.append("d-i apt-setup/use_mirror boolean false")
        preseed_cfg.append("d-i apt-setup/non-free boolean true")
        preseed_cfg.append("d-i apt-setup/contrib boolean true")
        preseed_cfg.append("d-i grub-installer/only_debian boolean true")
        preseed_cfg.append("d-i grub-installer/with_other_os boolean true")
        preseed_cfg.append("d-i grub-installer/bootdev string /dev/sda")
        preseed_cfg.append("d-i finish-install/keep-consoles boolean true")
        preseed_cfg.append("d-i pkgsel/upgrade select none")
        

        with open('/tmp/customiso/build_pressed', 'w') as preseed:
            preseed.write('\n'.join(preseed_cfg))

        print("[ ✅ ] Construction du fichier preseed\n")



    def import_presseed(self):
        try:
            subprocess.call([f'{self.python_path}/scripts/preseed.sh'])
        except:
            print("[ ❌ ] Import du fichier preseed\n")
            sys.exit(1)
        else:
            print("[ ✅ ] Import du fichier preseed\n")

    def import_packages(self):
        try:
            subprocess.call([f'{self.python_path}/scripts/apply-packages.sh'])
        except:
            print("[ ❌ ] Intégration des nouveaux packages\n")
            sys.exit(1)
        else:
            print("[ ✅ ] Intégration des nouveaux packages\n")

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
