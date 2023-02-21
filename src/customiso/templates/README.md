```bash
docker run --name debian-dl --workdir /root -d --rm -v /home/tn/Desktop/Customiso/Customiso/resources/packages:/root debian sleep infinity
docker exec debian-dl apt update && apt download -y neofetch*
```

