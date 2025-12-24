import numpy as np
import pandas as pd
import argparse
import importlib.util
import os

# parse command line argument

parser = argparse.ArgumentParser(description="Generates ODEs")
parser.add_argument('--model', type=array required=True,
                    help='name all oligomers by monomer size eg monomers dimers trimers 1,2,3')
args = parser.parse_args()
model_path = args.model

# State the sizes of oligomers by monomer number
