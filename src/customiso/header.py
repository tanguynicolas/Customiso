from constants import *

def header(product: str):

    print(f"\n\
  {fC1}██████{fD1}╗{rB}██{fD1}╗{rB}   ██{fD1}╗{rB}███████{fD1}╗{rB}████████{fD1}╗{rB} ██████{fD1}╗{rB} ███{fD1}╗{rB}   ███{fD1}╗{rB}{fC2}██{fD2}╗{rB}███████{fD2}╗{rB} ██████{fD2}╗{rB}{rC}\n\
 {fC1}██{fD1}╔════╝{rB}██{fD1}║{rB}   ██{fD1}║{rB}██{fD1}╔════╝╚══{rB}██{fD1}╔══╝{rB}██{fD1}╔═══{rB}██{fD1}╗{rB}████{fD1}╗{rB} ████{fD1}║{rB}{fC2}██{fD2}║{rB}██{fD2}╔════╝{rB}██{fD2}╔═══{rB}██{fD2}╗{rC}\n\
 {fC1}██{fD1}║{rB}     ██{fD1}║{rB}   ██{fD1}║{rB}███████{fD1}╗{rB}   ██{fD1}║{rB}   ██{fD1}║{rB}   ██{fD1}║{rB}██{fD1}╔{rB}████{fD1}╔{rB}██{fD1}║{rB}{fC2}██{fD2}║{rB}███████{fD2}╗{rB}██{fD2}║{rB}   ██{fD2}║{rC}  {fB}{product}{rC}\n\
 {fC1}██{fD1}║{rB}     ██{fD1}║{rB}   ██{fD1}║╚════{rB}██{fD1}║{rB}   ██{fD1}║{rB}   ██{fD1}║{rB}   ██{fD1}║{rB}██{fD1}║╚{rB}██{fD1}╔╝{rB}██{fD1}║{rB}{fC2}██{fD2}║╚════{rB}██{fD2}║{rB}██{fD2}║{rB}   ██{fD2}║{rC}\n\
 {fC1}{fD1}╚{rB}██████{fD1}╗╚{rB}██████{fD1}╔╝{rB}███████{fD1}║{rB}   ██{fD1}║{rB}   {fD1}╚{rB}██████{fD1}╔╝{rB}██{fD1}║{rB} {fD1}╚═╝{rB} ██{fD1}║{rB}{fC2}██{fD2}║{rB}███████{fD2}║╚{rB}██████{fD2}╔╝{rC}\n\
  {fC1}{fD1}╚═════╝{rB} {fD1}╚═════╝{rB} {fD1}╚══════╝{rB}   {fD1}╚═╝{rB}    {fD1}╚═════╝{rB} {fD1}╚═╝{rB}     {fD1}╚═╝{rB}{fC2}{fD2}╚═╝╚══════╝{rB} {fD2}╚═════╝{rC}   {fI}par \033]8;;{linkedin}\aTanguy\033]8;;\a{rC}\n\
    ")

    print(f"=== Bienvenue sur Customiso {product} ! ===\n")
