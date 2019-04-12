import os
from scripts import *

for file in os.listdir('geometry'):
    if file.endswith(".xyz"):
        geometry_filename = 'geometry/' + file

dummies = []
for file in os.listdir('dummies'):
    if file.endswith(".xyz"):
        dummies.append('dummies/' + file)

for file in dummies:
    create_protonopts(geometry_filename, file)