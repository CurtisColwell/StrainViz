import os
from scripts import *

dummies = []
for file in os.listdir('dummies'):
    if file.endswith("protonopt.out"):
        dummies.append('dummies/' + file)

for file in dummies:
    create_input(file)