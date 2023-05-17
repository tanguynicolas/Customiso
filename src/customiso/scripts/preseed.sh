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

options=$(getopt -a -o hv -l help -- "$@") || usage

eval set -- "$options" # eval for remove simple quote

while true; do
    case "$1" in
        -h|--help)
            usage
	        shift;;
        -v)
            verbose=true
	        shift;;
        --)
            shift; break;;
        *)
            err "Unexpected option: '$1' - pas d'argument attendu ici.";
    esac 
done


### Coeur du script

LOCAL_DIR=$(cd "$( dirname "${BASH_SOURCE[0]}")" && pwd)
. $LOCAL_DIR/constants.sh

cp ${verbose:+-v} ${customiso_path}/build_pressed                   ${customiso_path}/${extract_dir}/preseed.cfg
cp ${verbose:+-v} $LOCAL_DIR/../templates/preseed/isolinux/menu.cfg ${customiso_path}/${extract_dir}/isolinux/
cp ${verbose:+-v} $LOCAL_DIR/../templates/preseed/isolinux/txt.cfg  ${customiso_path}/${extract_dir}/isolinux/
