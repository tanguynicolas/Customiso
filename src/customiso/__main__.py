'''
Programme principal qui analyse les options et dirige l'utilsateur sur la suite du programme.
'''

import argparse
import sys

from constants import *
from header import header
from generate import Generator
from make import Maker

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

# Commande enfant generate
generate = subparser.add_parser('generate')
generate.add_argument('-q', action='store_true', # Quiet (no explainations)
                      help='Si vous ne souhaitez pas avoir de message d\'explication complémentaires (utilisateurs avertit).')
generate.add_argument('-c', type=str,            # Output conf file
                      metavar='output_conf_file', help='Le chemin où vous souaitez entreposer le fichier de configuration une fois créé.')

# Commande enfant make
make = subparser.add_parser('make')
make.add_argument('-c', type=str, required=True, # Input conf file
                  metavar='input_conf_file', help='Le chemin vers le fichier de configuration à charger.')
make.add_argument('-i', type=str, required=True, # Input iso
                  metavar='input_iso', help='Le chemin vers l\'image ISO Debian de base.')
make.add_argument('-o', type=str, required=True, # Output iso
                  metavar='output_iso', help='Le chemin où vous souaitez entreposer l\'image ISO Debian personnalisée une fois créé.')
make.add_argument('-v', action='store_true',     # Verbose
                  help='Si vous souhaitez augmenter la verbosité (= déboguage).')

# Traitement des options et arguments
args = parser.parse_args()

if args.command == 'generate':
    header(args.command.capitalize())

    generator = Generator(args.q, args.c)
    generator.start_generate()

elif args.command == 'make':
    header(args.command.capitalize())
    
    maker = Maker(args.c, args.i, args.o, args.v)
    maker.start_make()

elif len(sys.argv)==1:
    eprint(f"{fCwarning}No arguments supplied...{rC}\n")
    parser.print_help(sys.stderr)
    sys.exit(1)
