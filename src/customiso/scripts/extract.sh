#!/bin/bash
#
# Extrait l'intégralité d'un fichier ISO.

err() {
    echo "[$(date +'%Y-%m-%d')]: $*" >&2
    exit 1
}

usage() {
    echo -e "\nUse: ./$(basename "$0") --iso <iso_file>\n"
    echo -e "Type:\n   -h for help\n   --iso for specify ISO file\n"
    exit 0
}


### Gestion des paramètres

[[ $# -lt 1 ]] && err 'Missing arguments, type -h' && exit 1

options=$(getopt -a -o hi: -l help,iso: -- "$@") || usage

eval set -- "$options" # eval for remove simple quote

while true; do
    case "$1" in
        -h|--help)
            usage
	        shift;;
        -i|--iso)
            iso_path="$2"
	    shift 2;;
        --)
            shift; break;;
        *)
            err "Unexpected option: '$1' - pas d'argument attendu ici.";
    esac 
done


### Coeur du script

LOCAL_DIR=$(cd "$( dirname "${BASH_SOURCE[0]}")" && pwd)
. $LOCAL_DIR/constants.sh

mkdir -p "${customiso_path}/${extract_dir}"
bsdtar -C "${customiso_path}/${extract_dir}" -xf "$iso_path"
chmod -R +w "${customiso_path}/${extract_dir}"
