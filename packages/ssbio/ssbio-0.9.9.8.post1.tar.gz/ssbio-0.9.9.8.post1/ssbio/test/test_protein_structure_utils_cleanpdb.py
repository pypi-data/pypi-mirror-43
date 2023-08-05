import os.path as op
import unittest

from ssbio.protein.structure.utils.cleanpdb import CleanPDB
from ssbio.protein.structure.utils.structureio import StructureIO


class TestCleanPDB(unittest.TestCase):
    """Unit tests for CleanPDB
    """

    def test_clean_pdb(self):
        files = [('1kf6.pdb', '1kf6_clean_tester.pdb'), ('PHOE_ECOLI_model1.pdb', 'PHOE_ECOLI_model1_clean_tester.pdb'),
                 ('E04142.pdb', 'E04142_clean_tester.pdb'), ('1cbn.pdb', '1cbn_clean_tester.pdb')]

        outdir = op.join('test_files', 'out')
        working_dir = 'test_structures'
        out_suffix = '_clean'
        custom_clean = CleanPDB()

        for infile,outfile in files:
            outfile_new = '{}{}.pdb'.format(op.splitext(infile)[0], out_suffix)
            infile_path = op.join(working_dir, infile)

            my_pdb = StructureIO(infile_path)
            default_cleaned_pdb = my_pdb.write_pdb(custom_selection=custom_clean, out_suffix=out_suffix,
                                                   out_dir=outdir, force_rerun=True)
            default_cleaned_pdb_basename = op.basename(default_cleaned_pdb)

            # test if the filename is correct
            self.assertEqual(default_cleaned_pdb_basename, outfile_new)

            # test if the file contents are equal
            self.assertEqual(open(default_cleaned_pdb,'r').read(),
                             open(op.join(working_dir, outfile), 'r').read())

            # test that the file does not equal the original file
            self.assertNotEqual(open(default_cleaned_pdb,'r').read(),
                                open(infile_path, 'r').read())

    def test_clean_pdb_and_get_chain(self):
        files = [('1kf6.pdb', '1kf6_clean_chainA_tester.pdb')]
        outdir = op.join('test_files', 'out')
        working_dir = 'test_structures'
        out_suffix = '_clean_chainA'
        custom_clean = CleanPDB(keep_chains='A')

        for infile, outfile in files:
            outfile_new = '{}{}.pdb'.format(op.splitext(infile)[0], out_suffix)
            infile_path = op.join(working_dir, infile)

            my_pdb = StructureIO(infile_path)
            default_cleaned_pdb = my_pdb.write_pdb(custom_selection=custom_clean, out_suffix=out_suffix,
                                                   out_dir=outdir, force_rerun=True)
            default_cleaned_pdb_basename = op.basename(default_cleaned_pdb)

            # test if the filename is correct
            # print(default_cleaned_pdb_basename, outfile_new)
            self.assertEqual(default_cleaned_pdb_basename, outfile_new)

            # test if the file contents are equal
            self.assertEqual(open(default_cleaned_pdb, 'r').read(),
                             open(op.join(working_dir, outfile), 'r').read())

            # test that the file does not equal the original file
            self.assertNotEqual(open(default_cleaned_pdb, 'r').read(),
                                open(infile_path, 'r').read())