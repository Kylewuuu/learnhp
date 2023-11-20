import hotpot as hp

# 读取hotpot/tutorial/tut3/input_files下的两个cif文件
mol1 = hp.Molecule.read_from("/home/kyle/learnhp/tut3/hotpot/tutorial/tut3/input_files/IRMOF-1.cif")
mol2 = hp.Molecule.read_from("/home/kyle/learnhp/tut3/hotpot/tutorial/tut3/input_files/MIL-101(Cr).cif")

# 查看对应文件记录的晶体结构信息，包括晶胞类型，晶胞参数，空间点群，晶胞体积和晶胞密度
cryst1 = mol1.crystal()  # Get the Crystal1 containing the Molecule
print('晶体IRMOF-1结构信息如下:')
print("晶胞类型：%s" %(cryst1.lattice_type))  # 晶体1的晶胞类型
print('晶胞参数：', cryst1.lattice_params)  # 晶体1的晶胞参数
print("空间点群：%s" %(cryst1.space_group))  # 晶体1的空间点群
print("晶胞体积：%.2e" %(cryst1.volume))  # 晶体1的晶胞体积
print('晶胞密度：%.2e' %(cryst1.density))  # 晶体1的晶胞密度

print('\n')

cryst2 = mol2.crystal()  # Get the Crystal2 containing the Molecule
print("晶体MIL-101(Cr)结构信息如下:")
print("晶胞类型：%s" %(cryst2.lattice_type))  # 晶体2的晶胞类型
print('晶胞参数：', cryst2.lattice_params)  # 晶体2的晶胞参数
print("空间点群：%s" %(cryst2.space_group))  # 晶体2的空间点群
print("晶胞体积：%.2e" %(cryst2.volume))  # 晶体2的晶胞体积
print('晶胞密度：%.2e' %(cryst2.density)) # 晶体2的晶胞密度

# 使得Molecule在晶胞内复制，按照对称元素填满整个晶胞
pack_mol1 = cryst1.pack_molecule
pack_mol2 = cryst2.pack_molecule

# 将填满晶胞后的分子结构pack_mol保存为cif文件，保存路径为hotpot/tutorial/tut3/output_files
pack_mol1.writefile('cif', '/home/kyle/learnhp/tut3/hotpot/tutorial/tut3/output_files/pack_IRMOF-1.cif')
pack_mol2.writefile('cif', '/home/kyle/learnhp/tut3/hotpot/tutorial/tut3/output_files/pack_MIL-101(Cr).cif')

# 遍历mol1 mol2中的原子，找到atomic_number为30 24的所有原子对象，并删除它们
atoms_to_remove1 = [atom for atom in pack_mol1.atoms if atom.atomic_number == 30]
for atom in atoms_to_remove1:
    pack_mol1.remove_atoms(atom)

atoms_to_remove2 = [atom for atom in pack_mol2.atoms if atom.atomic_number == 24]
for atom in atoms_to_remove2:
    pack_mol2.remove_atoms(atom)

'提取剩余晶体中的所有有机物，并以mol2文件保存到hotpot/tutorial/tut3/output_files文件底下'
org_mol1 = [c for c in pack_mol1.components if c.is_organic]
for i, mol in enumerate(org_mol1):
    mol.writefile('mol2', f'/home/kyle/learnhp/tut3/hotpot/tutorial/tut3/output_files/IRMOF_organic/IRMOF_org{i}.mol2')

org_mol2 = [d for d in pack_mol2.components if d.is_organic]
for j, mol in enumerate(org_mol2):
    mol.writefile('mol2', f'/home/kyle/learnhp/tut3/hotpot/tutorial/tut3/output_files/MIL-101(Cr)_organic/MIL-101(Cr)_org{j}.mol2')
