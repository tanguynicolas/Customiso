#!/bin/bash

# ASCII art   : https://patorjk.com/software/taag/#p=display&h=2&f=ANSI%20Shadow&t=CustomIso
# Color guide : https://misc.flogisoft.com/bash/tip_colors_and_formatting
# Color name  : https://www.ditig.com/256-colors-cheat-sheet
# Emojis      : https://unicode.org/emoji/charts/full-emoji-list.html

fC1='\e[38;5;031m' # DeepSkyBlue3
fC2='\e[38;5;003m' # Olive
fC3='\e[38;5;015m' # White
fD1='\e[2m'        # Dim
fD2='\e[2m'        # Dim
fB='\e[1m'         # Bold
fI='\e[3m'         # Italic
_C='\e[0m'         # Reset all
_B='\e[22m'        # Reset dim

to_end_of_term() {
    for i in $(seq 1 $(stty size | cut -d' ' -f2)); do 
        echo -n "$1" 
    done
}

clear

echo -e "
  ${fC1}██████${fD1}╗${_B}██${fD1}╗${_B}   ██${fD1}╗${_B}███████${fD1}╗${_B}████████${fD1}╗${_B} ██████${fD1}╗${_B} ███${fD1}╗${_B}   ███${fD1}╗${_B}${fC2}██${fD2}╗${_B}███████${fD2}╗${_B} ██████${fD2}╗${_B}${_C}
 ${fC1}██${fD1}╔════╝${_B}██${fD1}║${_B}   ██${fD1}║${_B}██${fD1}╔════╝╚══${_B}██${fD1}╔══╝${_B}██${fD1}╔═══${_B}██${fD1}╗${_B}████${fD1}╗${_B} ████${fD1}║${_B}${fC2}██${fD2}║${_B}██${fD2}╔════╝${_B}██${fD2}╔═══${_B}██${fD2}╗${_C}
 ${fC1}██${fD1}║${_B}     ██${fD1}║${_B}   ██${fD1}║${_B}███████${fD1}╗${_B}   ██${fD1}║${_B}   ██${fD1}║${_B}   ██${fD1}║${_B}██${fD1}╔${_B}████${fD1}╔${_B}██${fD1}║${_B}${fC2}██${fD2}║${_B}███████${fD2}╗${_B}██${fD2}║${_B}   ██${fD2}║${_C}  ${fB}Generate${_C}
 ${fC1}██${fD1}║${_B}     ██${fD1}║${_B}   ██${fD1}║╚════${_B}██${fD1}║${_B}   ██${fD1}║${_B}   ██${fD1}║${_B}   ██${fD1}║${_B}██${fD1}║╚${_B}██${fD1}╔╝${_B}██${fD1}║${_B}${fC2}██${fD2}║╚════${_B}██${fD2}║${_B}██${fD2}║${_B}   ██${fD2}║${_C}
 ${fC1}${fD1}╚${_B}██████${fD1}╗╚${_B}██████${fD1}╔╝${_B}███████${fD1}║${_B}   ██${fD1}║${_B}   ${fD1}╚${_B}██████${fD1}╔╝${_B}██${fD1}║${_B} ${fD1}╚═╝${_B} ██${fD1}║${_B}${fC2}██${fD2}║${_B}███████${fD2}║╚${_B}██████${fD2}╔╝${_C}
  ${fC1}${fD1}╚═════╝${_B} ${fD1}╚═════╝${_B} ${fD1}╚══════╝${_B}   ${fD1}╚═╝${_B}    ${fD1}╚═════╝${_B} ${fD1}╚═╝${_B}     ${fD1}╚═╝${_B}${fC2}${fD2}╚═╝╚══════╝${_B} ${fD2}╚═════╝${_C}   ${fI}par \e]8;;http://linkedin.tanguynicolas.fr\aTanguy\e]8;;\a${_C}
"

echo "=== Bienvenue sur Customiso Generate ! ==="
echo ""
echo "⛽ Souaitez-vous générer un fichier de configuration pour Customiso Make ?"
read -p "[O/n] : " choice
echo ""
echo "🚀 C'est parti."
echo ""
to_end_of_term "="
echo ""
echo ""
echo "Quel sera le nom d'hôte de votre machine ?"
read -p ": " choice
echo ""
echo "Souhaitez-vous créer un compte root ?"
read -p "[o/N] : " choice
echo ""
echo "Quel sera le nom complet de votre utilisateur ?"
read -p ": " choice
echo ""
echo "Quel sera l'identifiant de votre utilisateur ?"
read -p "[tanguy] : " choice
echo ""
echo "Quel sera le mot de passe de votre utilisateur ?"
read -p ": " choice
echo ""



echo -e "
${fC1}████████████████████${fC2} ██${_B}
${fC2}██████████████████████${_B}
${fC2}████${fC3}██${fC2}████████${fC3}██${fC2}█████${_B}
${fC2}██████████████████████${_B}
${fC1}████████████████████${fC2} ██${_B}
${fC1}██${fC1}█${fC1}██████████████${fC1}█${fC1}██${_B}
${fC1}███${fC3}█${fC1}████████████${fC3}█${fC1}███${_B}
${fC1}████${fC3}████████████${fC1}████${_B}
${fC1}████████████████████${_B}
"

