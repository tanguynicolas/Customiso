"""
Programme principal qui analyse les options et dirige l'utilsateur sur la suite du programme.
"""

import argparse
import sys

from constants import *
from header import header
from generate import Generator

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

# Commande enfant generate
generate = subparser.add_parser('generate')
generate.add_argument('-q', action='store_true') # Quiet (no explainations)
generate.add_argument('-o', type=str)            # Output file

# Commande enfant make
make = subparser.add_parser('make')
make.add_argument('-f', type=str)                # Input file
make.add_argument('-v', action='store_true')     # Verbose

# Traitement des options et arguments
args = parser.parse_args()

if args.command == 'generate':
    header(args.command.capitalize())

    generator = Generator(args.q, args.o)
    generator.start_generate()


elif args.command == 'make':
    header(args.command.capitalize())
    print(f"Options {args.f} {args.v}")

elif len(sys.argv)==1:
    eprint(f"{fCwarning}No arguments supplied...{rC}\n")
    parser.print_help(sys.stderr)
    sys.exit(1)
