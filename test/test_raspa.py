"""
python v3.9.0
@Project: hotpot
@File   : test_raspa
@Auther : Zhiyuan Zhang
@Data   : 2023/9/25
@Time   : 15:29
"""
import os
import logging
import unittest as ut

import test

import hotpot as hp
from hotpot.tasks.raspa import RASPA

raspa_root = hp.settings.get("paths", {}).get("raspa_root") or os.environ.get('RASPA_DIR')


logging.basicConfig(level=logging.INFO)


class TestRaspa(ut.TestCase):
    """ Test the hotpot.tasks.raspa subpackage """
    @classmethod
    def setUpClass(cls) -> None:
        print('Test', cls.__class__)

    def setUp(self) -> None:
        print('running test:', self._testMethodName)

    def tearDown(self) -> None:
        print('Normalize terminate test!', self._testMethodName)

    @ut.skipIf(not raspa_root, "the test need the Raspa software")
    def test_run(self):
        """"""
        mof_name = "IRMOF-1"
        path_mof = test.test_root.joinpath("inputs", "struct", f"{mof_name}.cif")


        mof = hp.Molecule.read_from(path_mof)

        raspa = RASPA(in_test=True)  # , parsed_output=False

        script = raspa.run(mof, "CO2", cycles=100)
        # json.dump(script, open(work_dir.joinpath("output.json"), 'w'), indent=True)

        # # work_dir.mkdir(parents=True, exist_ok=True)
        # with open(work_dir.joinpath("pure/pure_try1.txt"), 'w') as writer:
        #     writer.write(script)
        return script

    def test_guest_to_mol_file(self):
        """"""
        mof_name = "IRMOF-1"
        path_mof = test.test_root.joinpath("inputs", "struct", f"{mof_name}.cif")

        mof = hp.Molecule.read_from(path_mof)
        co2 = hp.Molecule.read_from("O=C=O", 'smi')
        co2.identifier = "CO2"

        raspa = RASPA(in_test=True)
        script = raspa.run(mof, co2, cycles=100)

        print(script)

    def test_input_critical_params(self):
        """ Test if the input critical params pass to the guest.def files """
        mof_name = "IRMOF-1"
        path_mof = test.test_root.joinpath("inputs", "struct", f"{mof_name}.cif")

        mof = hp.Molecule.read_from(path_mof)

        co2 = hp.Molecule.read_from("O=C=O", 'smi')
        co2.identifier = "test_CO2"

        raspa = RASPA(in_test=True)  # parsed_output=False

        Tc = 30.  # 304.1282
        Pc = 10654654.  # 7377300.0
        acentric_factor = 0.7  # 0.22394
        script = raspa.run(mof, co2, cycles=100, Tc=Tc, Pc=Pc, acentric_factor=acentric_factor, suffix="CO2")

        co2_file = raspa.raspa_root.joinpath("share", "raspa", "molecules", raspa.guest_dir_name, f"{co2.identifier}.def")
        with open(co2_file) as file:
            lines = file.readlines()

        # check whether the context about critical params is same as the input values
        self.assertEqual(float(lines[1].strip()), Tc, "the Tc is error!")
        self.assertEqual(float(lines[2].strip()), Pc, "the Pc is error!")
        self.assertEqual(float(lines[3].strip()), acentric_factor, "the acentric_factor is error!")

    def test_read_raspa_mol_file(self):
        """ Test if guest.def can convert to Molecule obj"""
        raspa_inputs_root = hp.data_root
        raspa_flexible_mol_path = os.path.join(raspa_inputs_root, "raspa_mol/2-methylbutane.def")
        raspa_rigid_mol_path = os.path.join(raspa_inputs_root, "raspa_mol/O2.def")

        self.assertRaises(TypeError, hp.Molecule.read_from, raspa_flexible_mol_path, 'raspa_mol')

        mol = hp.Molecule.read_from(raspa_rigid_mol_path, "raspa_mol")
        print(mol)
