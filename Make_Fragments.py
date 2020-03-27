# -*- coding: utf-8 -*-
"""
@author: Hiromasa Kaneko
"""

from rdkit import Chem
from rdkit.Chem import BRICS

number_of_free_bonds = 1  # The number of free bond(s) restricted. If 0, all fragments are saved

max_of_minFragmentSize = 10
# load molecules
# from Smiles
molecules = [molecule for molecule in Chem.SmilesMolSupplier('sample_main_fragments.smi',
                                                             delimiter='\t', titleLine=False)
             if molecule is not None]

# from sdf file
# molecules = [molecule for molecule in Chem.SDMolSupplier('logSdataset1290_2d.sdf') if molecule is not None]

print('number of molecules :', len(molecules))

# generate fragments
fragments = set()
for i in range(1, max_of_minFragmentSize + 1):
    print(i, '/', max_of_minFragmentSize)
    for molecule in molecules:
        fragment = BRICS.BRICSDecompose(molecule, minFragmentSize=i)
        fragments.update(fragment)

# select and arange fragments
new_fragments = []
number_of_generated_structures = 0
for fragment in fragments:
    free_bond = []
    free_bond = [index for index, atom in enumerate(fragment) if atom == '*']
    flag = False
    if number_of_free_bonds == 0:
        if len(free_bond):
            flag = True
    else:
        if len(free_bond) == number_of_free_bonds:
            flag = True
    if flag:
        slip_index = []
        for i in range(len(free_bond)):
            if fragment[free_bond[i] - 2] == '[':
                slip_index.append(free_bond[i] - 2)
                slip_index.append(free_bond[i] - 1)
                slip_index.append(free_bond[i] + 1)
            else:
                slip_index.append(free_bond[i] - 3)
                slip_index.append(free_bond[i] - 2)
                slip_index.append(free_bond[i] - 1)
                slip_index.append(free_bond[i] + 1)
        new_fragment = ''
        for index, char_in_fragment in enumerate(fragment):
            if not index in slip_index:
                new_fragment += char_in_fragment
        new_fragments.append(new_fragment)
print('number of selected fragments :', len(new_fragments))

# delete duplications of fragments
new_fragments = list(set(new_fragments))
print('number of selected fragments without duplications :', len(new_fragments))

print(new_fragments)

# save fragments
str_ = '\n'.join(new_fragments)
with open('generated_fragments.smi', 'wt') as writer:
    writer.write(str_)
writer.close()
