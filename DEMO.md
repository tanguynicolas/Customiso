```bash
cd
```

```bash
customiso generate -c /tmp/demonstration.yaml
```

```yaml
vim Desktop/Customiso/Customiso/src/customiso/samples/config.yaml
```

```bash
customiso make -c "Desktop/Customiso/Customiso/src/customiso/samples/config.yaml" -i "kvm/isos/debian-11.7.0-amd64-DVD-1.iso" -o "demonstration"
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

