#!/bin/bash
#
# Envoi les fichiers nécessaires à l'installation silencieuse dans l'ISO préalablement extraite.

err() {
    echo "[$(date +'%Y-%m-%d')]: $*" >&2
    exit 1
}

usage() {
    echo -e "\nUse: ./$(basename "$0")\n"
    echo -e "Type:\n   -h for help\n"
    exit 0
}


### Gestion des paramètres

#[[ $# -lt 1 ]] && err 'Missing arguments, type -h' && exit 1

options=$(getopt -a -o h -l help -- "$@") || usage

eval set -- "$options" # eval for remove simple quote

while true; do
    case "$1" in
        -h|--help)
            usage
	    shift;;
        --)
            shift; break;;
        *)
            err "Unexpected option: '$1' - pas d'argument attendu ici.";
    esac 
done

[[ $# -gt 0 ]] && err 'Too many arguments, type -h' && exit 1

### Coeur du script

LOCAL_DIR=$(cd "$( dirname "${BASH_SOURCE[0]}")" && pwd)
. $LOCAL_DIR/constants.sh

echo "# A config-deb file.

# Points to where the unpacked DVD-1 is.
Dir {
    ArchiveDir \"${customiso_path}/${extract_dir}\";
};

# Sets the top of the .deb directory tree.
TreeDefault {
   Directory \"pool/\";
};

# The location for a Packages file.                
BinDirectory \"pool/main\" {
   Packages \"dists/bullseye/main/binary-amd64/Packages\";
};

# We are only interested in .deb files (.udeb for udeb files).                                
Default {
   Packages {
       Extensions \".deb\";
    };
};" > ${customiso_path}/config-deb

apt-ftparchive --quiet generate ${customiso_path}/config-deb  > /dev/null 2>&1

sed -i '/MD5Sum:/,$d' ${customiso_path}/${extract_dir}/dists/bullseye/Release
apt-ftparchive release ${customiso_path}/${extract_dir}/dists/bullseye \
        >> ${customiso_path}/${extract_dir}/dists/bullseye/Release

cd "${customiso_path}/${extract_dir}"
md5sum $(find ! -name "md5sum.txt" ! -path "./isolinux/*" -follow -type f 2>/dev/null) \
        > "${customiso_path}/${extract_dir}/md5sum.txt";
