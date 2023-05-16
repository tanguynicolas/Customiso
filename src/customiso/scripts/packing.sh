#!/bin/bash
#
# Reconstitue un fichier ISO dont les composantes ont été extraites.

err() {
    echo "[$(date +'%Y-%m-%d')]: $*" >&2
    exit 1
}

usage() {
    echo -e "\nUse: ./$(basename "$0") --iso <iso_name>\n"
    echo -e "Type:\n   -h for help\n   --iso for specify ISO file name\n"
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
            iso_name="$2"
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

mkisofs -o "${iso_name}.iso" \
	-b isolinux/isolinux.bin \
	-c isolinux/boot.cat \
	-no-emul-boot \
	-boot-load-size 4 \
	-boot-info-table -J -R \
	-V "Generated by Customiso" \
	"${customiso_path}/${extract_dir}" > /dev/null 2>&1

# -o                Output file name
# -b                Boot image path
# -c                Boot catalog path
# -no-emul-boot     The system will load and execute this image without performing any disk emulation
# -boot-load-size   Specifies the number of "virtual" sectors to load in no-emulation mode
# -boot-info-table  Specifies that a 56-byte table with information of the CD-ROM layout will be patched in at offset 8 in the boot file
# -J                Generate Joliet directory records in addition to regular iso9660 file names
# -R                Generate SUSP and RR records using the Rock Ridge protocol to further describe the files on the iso9660 filesystem
# -V                Specifies the volume ID (volume name or label) to be written into the master block
# pathspec          The path of the directory tree to be copied into the iso9660 filesystem

