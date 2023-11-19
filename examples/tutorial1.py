import hotpot as hp

mol = hp.Molecule.read_from('c1ccccc1', 'smi')  # Load a benzene molecule
print(mol.has_3d)  # the molcule is a 2D molcule now, whose all coordinates are (0, 0, 0)

mol.build_3d(force_field='UFF')  # build the molecule to 3D, by univeral force field
print(mol.has_3d)  # Now, the molecule is a 3D molecule, all of atoms have their coordinate

# check the atoms coordinates:
mol.normalize_labels()  # reorder the atom's labels
for atom in mol.atoms:
    print(atom.label, atom.symbol, atom.coordinates)  # get the label, symbol, coordinates of the atom

print(mol.atoms)  # get all atoms in the molecule
print(mol.bonds)  # get all bonds in the molecule

atom = mol.atoms[0]
bond = mol.bonds[0]

print(atom.neighbours)  # get all neigh atoms of this atoms
print(bond.atom1, bond.atom2)  # get the begin and end atom of this bond
print(bond.type)  # get the bond type