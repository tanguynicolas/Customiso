"""
Fichier qui contient toutes les constantes.

ASCII art   : https://patorjk.com/software/taag/#p=display&h=2&f=ANSI%20Shadow&t=CustomIso
Color guide : https://misc.flogisoft.com/bash/tip_colors_and_formatting
Color name  : https://www.ditig.com/256-colors-cheat-sheet
Emojis      : https://unicode.org/emoji/charts/full-emoji-list.html
"""

import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

linkedin = 'http://linkedin.tanguynicolas.fr'
fCsuccess = '\033[38;5;006m' # Cyan
fCinfo = '\033[38;5;028m'    # Green
fCwarning = '\033[38;5;214m' # Orange
fCerror = '\033[91m'         # Red
fC1 = '\033[38;5;031m' # DeepSkyBlue3
fC2 = '\033[38;5;003m' # Olive
fC3 = '\033[38;5;015m' # White
fD1 = '\033[2m'        # Dim
fD2 = '\033[2m'        # Dim
fB = '\033[1m'         # Bold
fI = '\033[3m'         # Italic
rC = '\033[0m'         # Reset all
rB = '\033[22m'        # Reset dim

distribution = "Debian"
