```bash
cd
```

```bash
customiso generate -c /tmp/demonstration.yaml
```

```yaml
additional_packages:
  - /home/tn/Desktop/Customiso/Customiso/src/customiso/samples/deb_packages/ponysay_3.0.3+20210327-1_all.deb
  - /home/tn/Desktop/Customiso/Customiso/src/customiso/samples/deb_packages/lsd_0.23.1_amd64.deb

additional_files:
  - from: /home/tn/Desktop/Customiso/Customiso/src/customiso/samples/afile.xml
    to: /etc/config
  - from: /home/tn/Desktop/Customiso/Customiso/src/customiso/samples/somefile.yaml
    to: /var/data
  - from: /home/tn/Desktop/Customiso/Customiso/src/customiso/samples/thefile.json
    to: /bin/program

post_install_script: /home/tn/Desktop/Customiso/Customiso/src/customiso/samples/test_script.sh
```

```bash
customiso make -c "/tmp/demonstration.yaml" -i "kvm/isos/debian-11.7.0-amd64-DVD-1.iso" -o "demonstration"
```

Démarrage de la VM.

Si additional_packages :
- lsd -l /
- ponysay Démo

Si additional_files :
- cat /etc/config
- cat /var/data
- cat /bin/program

Si post_install_script :
- cat /opt/demo
- cat /var/demo
- cat /etc/demo

