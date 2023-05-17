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
generate.add_argument('-q', action='store_true') # Quiet (no explainations)
generate.add_argument('-c', type=str)            # Output conf file

# Commande enfant make
make = subparser.add_parser('make')
make.add_argument('-c', type=str, required=True) # Input conf file
make.add_argument('-i', type=str, required=True) # Input iso
make.add_argument('-o', type=str, required=True) # Output iso
make.add_argument('-v', action='store_true')     # Verbose

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
