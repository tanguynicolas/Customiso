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

        self.step = 0

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
        self.end_make()

    def extract_iso(self):
        try:
            self.step += 1
            subprocess.call([f'{self.python_path}/scripts/extract.sh', '--iso', self.in_iso])
        except:
            print(f"[ ❌ ] {self.step}. Extraction du fichier ISO.\n")
            sys.exit(1)
        else:
            print(f"[ ✅ ] {self.step}. Extraction du fichier ISO.\n")

    def build_presseed(self):
        with open(self.conf_file, 'r') as f:
            try:
                yaml_data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(1)

        preseed_cfg = []
        preseed_cfg.append("# Customiso - 2023")

        # LOCALIZATION
        preseed_cfg.append("\n# LOCALIZATION")
        localization = yaml_data['preseed']['localization']

        if localization['language'] == "ask":
            pass
        elif localization['language']:
            preseed_cfg.append(f"d-i debian-installer/language string {localization['language']}")

        if localization['country'] == "ask":
            pass
        elif localization['country']:
            preseed_cfg.append(f"d-i debian-installer/country string {localization['country']}")

        if localization['locale'] == "ask":
            pass
        elif localization['locale']:
            preseed_cfg.append(f"d-i debian-installer/locale string {localization['locale']}")

        if localization['keymap'] == "ask":
            pass
        elif localization['keymap']:
            preseed_cfg.append(f"d-i keyboard-configuration/xkb-keymap select {localization['keymap']}")
        
        # CLOCK_TIME_ZONE
        preseed_cfg.append("\n# CLOCK_TIME_ZONE")
        clock_time_zone = yaml_data['preseed']['clock_time_zone']

        if clock_time_zone['timezone'] == "ask":
            pass
        elif clock_time_zone['timezone']:
            preseed_cfg.append(f"d-i time/zone string {clock_time_zone['timezone']}")

        # NETWORK
        preseed_cfg.append("\n# NETWORK")
        network = yaml_data['preseed']['network']

        if network['hostname'] == "ask":
            pass
        elif network['hostname']:
            preseed_cfg.append(f"d-i netcfg/get_hostname string {network['hostname']}")

        if network['domain'] == "ask":
            pass
        elif network['domain'] == "none":
            preseed_cfg.append(f"d-i netcfg/get_domain string")
        elif network['domain']:
            preseed_cfg.append(f"d-i netcfg/get_domain string {network['domain']}")

        if network['advanced']['ip_config'] == "ask":
            pass
        elif network['advanced']['ip_config'] == False:
            preseed_cfg.append("d-i netcfg/enable boolean false")
        elif network['advanced']['ip_config'] == True:
            preseed_cfg.append("d-i netcfg/enable boolean true")
            preseed_cfg.append("d-i netcfg/choose_interface select auto")
            preseed_cfg.append("d-i netcfg/dhcp_timeout string 8")
            preseed_cfg.append("d-i netcfg/dhcpv6_timeout string 8")

        # MIRROR
        preseed_cfg.append("\n# MIRROR")
        mirror = yaml_data['preseed']['mirror']

        if mirror['http_hostname'] == "ask":
            pass
        elif mirror['http_hostname']:
            preseed_cfg.append(f"d-i mirror/http/hostname string {mirror['http_hostname']}")

        if mirror['http_proxy'] == "ask":
            pass
        elif mirror['http_proxy'] == "none":
            preseed_cfg.append("d-i mirror/http/proxy string")
        elif mirror['http_proxy']:
            preseed_cfg.append(f"d-i mirror/http/proxy string {mirror['http_proxy']}")

        # ACCOUNTING
        preseed_cfg.append("\n# ACCOUNTING")
        accounting = yaml_data['preseed']['accounting']

        if accounting['root']['enable'] == True:
            preseed_cfg.append("d-i passwd/root-login boolean true")
            if accounting['root']['password'] == "ask":
                pass
            elif accounting['root']['password']:
                #preseed_cfg.append(f"d-i passwd/root-password password {accounting['root']['password']}")
                #preseed_cfg.append(f"d-i passwd/root-password-again password {accounting['root']['password']}")
                # Use: mkpasswd -m sha-512 <raw_password>
                preseed_cfg.append(f"d-i passwd/root-password-crypted password {accounting['root']['password']}")
        elif accounting['root']['enable'] == False:
            preseed_cfg.append("d-i passwd/root-login boolean false")

        if accounting['user']['fullname'] == "ask":
            pass
        elif accounting['user']['fullname']:
            preseed_cfg.append(f"d-i passwd/user-fullname string {accounting['user']['fullname']}")

        if accounting['user']['username'] == "ask":
            pass
        elif accounting['user']['username']:
            preseed_cfg.append(f"d-i passwd/username string {accounting['user']['username']}")

        if accounting['user']['password'] == "ask":
            pass
        elif accounting['user']['password']:
            #preseed_cfg.append(f"d-i passwd/user-password password {accounting['user']['password']}")
            #preseed_cfg.append(f"d-i passwd/user-password-again password {accounting['user']['password']}")
            # Use: mkpasswd -m sha-512 <raw_password>
            preseed_cfg.append(f"d-i passwd/user-password-crypted password {accounting['user']['password']}")

        # PARTITIONNING
        preseed_cfg.append("\n# PARTITIONNING")
        partitionning = yaml_data['preseed']['partitionning']

        if partitionning['predefined_mode'] == "ask" or partitionning['predefined_mode'] == 0:
            pass
        elif type(partitionning['predefined_mode']) == int:
            preseed_cfg.append("partman-auto partman-auto/disk string /dev/[sv]da")
            preseed_cfg.append("d-i partman-auto/method string regular")
            preseed_cfg.append("d-i partman-partitioning/confirm_write_new_label boolean true")
            preseed_cfg.append("d-i partman/choose_partition select finish")
            preseed_cfg.append("d-i partman/confirm boolean true")
            preseed_cfg.append("d-i partman/confirm_nooverwrite boolean true")

        if partitionning['predefined_mode'] == "ask" or partitionning['predefined_mode'] == 0:
            pass
        elif partitionning['predefined_mode'] == 1:
            # all files in one partition
            preseed_cfg.append("d-i partman-auto/choose_recipe select atomic")
        elif partitionning['predefined_mode'] == 2:
            # separate /home partition
            preseed_cfg.append("d-i partman-auto/choose_recipe select home")
        elif partitionning['predefined_mode'] == 3:
            # separate /home, /var, and /tmp partitions
            preseed_cfg.append("d-i partman-auto/choose_recipe select multi")

        # PACKAGES
        preseed_cfg.append("\n# PACKAGES")
        packages = yaml_data['preseed']['packages']

        if packages['tasksel'] == "ask":
            pass
        elif packages['tasksel']:
            tasksel_list = ', '.join(packages['tasksel'])
            preseed_cfg.append(f"tasksel tasksel/first multiselect {tasksel_list}")

        if packages['popularity_contest'] == "ask":
            pass
        elif packages['popularity_contest'] == True or packages['popularity_contest'] == False:
            preseed_cfg.append(f"popularity-contest popularity-contest/participate boolean {packages['popularity_contest']}")

        # FINISHING
        preseed_cfg.append("\n# FINISHING")
        
        customiso_pusher = False

        if yaml_data['post_install_script'] == "none" and yaml_data['additional_files'] == "none":
            pass
        elif yaml_data['post_install_script'] or yaml_data['additional_files']:
            customiso_pusher = True

            # Fabrication du paquet .deb
            os.makedirs('/tmp/customiso/customiso-pusher', exist_ok=True)
            shutil.copytree(f'{self.python_path}/templates/packages/customiso-pusher/DEBIAN', '/tmp/customiso/customiso-pusher/DEBIAN')
            os.chmod("/tmp/customiso/customiso-pusher/DEBIAN/postinst", 0o755)

            if yaml_data['post_install_script'] == "none":
                pass
            elif yaml_data['post_install_script']:
                try:
                    self.step += 1
                    os.makedirs('/tmp/customiso/customiso-pusher/opt', exist_ok=True)
                    shutil.copy(yaml_data['post_install_script'], '/tmp/customiso/customiso-pusher/opt/customiso-postinstall')
                except:
                    print(f"[ ❌ ] {self.step}. Préparation de l'ajout du script de post-installation.\n")
                else:
                    print(f"[ ✅ ] {self.step}. Préparation de l'ajout du script de post-installation.\n")

            if yaml_data['additional_files'] == "none":
                pass
            elif yaml_data['additional_files']:
                try:
                    self.step += 1
                    for p in yaml_data['additional_files']:
                        os.makedirs(os.path.dirname(f"/tmp/customiso/customiso-pusher/{p['to']}"), exist_ok=True)
                        shutil.copy(p['from'], f"/tmp/customiso/customiso-pusher/{p['to']}")
                except:
                    print(f"[ ❌ ] {self.step}. Préparation de l'ajout des fichiers personalisés.\n")
                else:
                    print(f"[ ✅ ] {self.step}. Préparation de l'ajout des fichiers personalisés.\n")

            # Ajout du paquet .deb
            os.makedirs('/tmp/customiso/cdrom/pool/main/c/customiso-pusher', exist_ok=True)
            subprocess.run("dpkg-deb --build '/tmp/customiso/customiso-pusher/' '/tmp/customiso/cdrom/pool/main/c/customiso-pusher/customiso-pusher.deb' > /dev/null 2>&1", shell=True)


        all_packages = []
        # On glisse le script customiso-pusher dans la liste s'il existe
        if customiso_pusher:
            try:
                self.step += 1
                all_packages.append('customiso-pusher')
                if yaml_data['post_install_script'] != "none":
                    preseed_cfg.append("d-i preseed/late_command string in-target /bin/bash /opt/customiso-postinstall")
            except:
                print(f"[ ❌ ] {self.step}. Ajout du script de post-installation et/ou des fichiers personalisés (étape 1/2).\n")
            else:
                print(f"[ ✅ ] {self.step}. Ajout du script de post-installation et/ou des fichiers personalisés (étape 1/2).\n")

        add_packages = False
        if yaml_data['additional_packages'] == "none":
            pass
        elif yaml_data['additional_packages']:
            try:
                self.step += 1
                add_packages = True
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
            except:
                print(f"[ ❌ ] {self.step}. Préparation de l'ajout des packages additionnels.\n")
            else:
                print(f"[ ✅ ] {self.step}. Préparation de l'ajout des packages additionnels.\n")
        
        if customiso_pusher or add_packages:
            try:
                self.step += 1
                package_list = ' '.join(all_packages)
                preseed_cfg.append(f"d-i pkgsel/include string {package_list}")
            except:
                print(f"[ ❌ ] {self.step}. Ajout du script de post-installation et/ou des fichiers personalisés (étape 2/2) et/ou des packages additionnels.\n")
            else:
                print(f"[ ✅ ] {self.step}. Ajout du script de post-installation et/ou des fichiers personalisés (étape 2/2) et/ou des packages additionnels.\n")

        finishing = yaml_data['preseed']['finishing']

        if finishing['reboot_message'] == False:
            preseed_cfg.append("d-i finish-install/reboot_in_progress note")
        
        if finishing['device_eject'] == True or finishing['device_eject'] == False:
            preseed_cfg.append(f"d-i cdrom-detect/eject boolean {finishing['device_eject']}")


        # MANDATORY / UNSUPPORTED
        preseed_cfg.append("\n# MANDATORY / UNSUPPORTED")
        preseed_cfg.append("d-i clock-setup/utc boolean true")
        preseed_cfg.append("d-i hw-detect/load_firmware boolean true")
        preseed_cfg.append("d-i mirror/country string manual")
        preseed_cfg.append("d-i mirror/http/directory string /debian")
        preseed_cfg.append("d-i apt-setup/use_mirror boolean false")
        preseed_cfg.append("d-i apt-setup/cdrom/set-first boolean false")
        #preseed_cfg.append("d-i apt-setup/non-free boolean true")
        #preseed_cfg.append("d-i apt-setup/contrib boolean true")
        preseed_cfg.append("d-i grub-installer/only_debian boolean true")
        preseed_cfg.append("d-i grub-installer/with_other_os boolean true")
        preseed_cfg.append("d-i grub-installer/bootdev string /dev/sda")
        preseed_cfg.append("d-i finish-install/keep-consoles boolean true")
        preseed_cfg.append("d-i pkgsel/upgrade select none")

        try:
            self.step += 1
            with open('/tmp/customiso/build_pressed', 'w') as preseed:
                preseed.write('\n'.join(preseed_cfg))
        except:
            print(f"[ ❌ ] {self.step}. Construction du fichier preseed.\n")
        else:
            print(f"[ ✅ ] {self.step}. Construction du fichier preseed.\n")

    def import_presseed(self):
        try:
            self.step += 1
            subprocess.call([f'{self.python_path}/scripts/preseed.sh'])
        except:
            print(f"[ ❌ ] {self.step}. Import du fichier preseed.\n")
            sys.exit(1)
        else:
            print(f"[ ✅ ] {self.step}. Import du fichier preseed.\n")

    def import_packages(self):
        try:
            self.step += 1
            subprocess.call([f'{self.python_path}/scripts/apply-packages.sh'])
        except:
            print(f"[ ❌ ] {self.step}. Intégration des nouveaux packages.\n")
            sys.exit(1)
        else:
            print(f"[ ✅ ] {self.step}. Intégration des nouveaux packages.\n")

    def pack_iso(self):
        try:
            self.step += 1
            subprocess.call([f'{self.python_path}/scripts/packing.sh', '--iso', f'{self.out_iso}'])
        except:
            print(f"[ ❌ ] {self.step}. Création de l'ISO personnalisé.\n")
            sys.exit(1)
        else:
            print(f"[ ✅ ] {self.step}. Création de l'ISO personnalisé.\n")

    def end_make(self):
        print(f"\nMerci d'avoir utilisé CustomISO !\nVotre image « {self.out_iso}.iso » est prête.\n")
