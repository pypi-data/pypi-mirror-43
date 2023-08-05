"""
CleanPDB
========
"""

import argparse
import logging
import os
import os.path as op
import textwrap

from Bio import PDB
from tqdm import tqdm

import ssbio.utils
from ssbio.protein.structure.utils.structureio import StructureIO

log = logging.getLogger(__name__)


class CleanPDB(PDB.Select):

    """Selection rules to clean a PDB entry.

    These rules aim to:
    - Add missing chain identifiers to a PDB file
    - Select a single chain if noted
    - Remove alternate atom locations
    - Add atom occupancies
    - Add B (temperature) factors (default Biopython behavior)

    """

    def __init__(self, remove_atom_alt=True, keep_atom_alt_id='A', remove_atom_hydrogen=True, add_atom_occ=True,
                 remove_res_hetero=True, keep_chemicals=None, keep_res_only=None, add_chain_id_if_empty='X', keep_chains=None):
        """Initialize the parameters which indicate what cleaning will occur

        Args:
            remove_atom_alt (bool): Remove alternate positions
            keep_atom_alt_id (str): If removing alternate positions, which alternate ID to keep
            remove_atom_hydrogen (bool): Remove hydrogen atoms
            add_atom_occ (bool): Add atom occupancy fields if not present
            remove_res_hetero (bool): Remove all HETATMs
            keep_chemicals (str, list): If removing HETATMs, keep specified chemical names
            keep_res_only (str, list): Keep ONLY specified resnames, deletes everything else!
            add_chain_id_if_empty (str): Add a chain ID if not present
            keep_chains (str, list): Keep only these chains
            
        """
        self.remove_atom_alt = remove_atom_alt
        self.remove_atom_hydrogen = remove_atom_hydrogen
        self.keep_atom_alt_id = keep_atom_alt_id
        self.add_atom_occ = add_atom_occ
        self.remove_res_hetero = remove_res_hetero
        self.add_chain_id_if_empty = add_chain_id_if_empty
        if not keep_chains:
            self.keep_chains = []
        else:
            self.keep_chains = ssbio.utils.force_list(keep_chains)
        if not keep_chemicals:
            self.keep_chemicals = []
        else:
            self.keep_chemicals = ssbio.utils.force_list(keep_chemicals)
        if not keep_res_only:
            self.keep_res_only = []
        else:
            self.keep_res_only = ssbio.utils.force_list(keep_res_only)

    def accept_chain(self, chain):
        # If the chain does not have an ID, add one to it and keep it
        # http://comments.gmane.org/gmane.comp.python.bio.devel/10639
        if self.add_chain_id_if_empty and not chain.id.strip():
            chain.id = self.add_chain_id_if_empty
            return True
        # If a chain is specified and the current chain equals that specified chain, keep it
        elif self.keep_chains and chain.id in self.keep_chains:
            return True
        # If a chain is specified but the current chain does not equal that specified chain, remove it
        elif self.keep_chains and chain.id not in self.keep_chains:
            return False
        # If no chain is specified, keep all chains
        else:
            return True

    def accept_residue(self, residue):
        hetfield, resseq, icode = residue.get_id()
        if hetfield == '':
            hetfield = ' '
        if self.keep_res_only:
            if residue.resname.strip() in self.keep_res_only:
                return True
            else:
                return False
        # If you want to remove residues that are not normal, remove them
        if self.remove_res_hetero and hetfield[0] != ' ' and residue.resname.strip() not in self.keep_chemicals:
            return False
        else:
            return True

    def accept_atom(self, atom):
        # If the you want to remove hydrogens and the atom is a H, remove it
        if self.remove_atom_hydrogen and atom.element == 'H':
            return False
        # If you want to remove alternate locations, and the alt location isn't the one you want to keep, remove it
        elif self.remove_atom_alt and atom.is_disordered() and atom.get_altloc() != self.keep_atom_alt_id:
            return False
        else:
            # Add occupancies if there are none and you want to
            # http://comments.gmane.org/gmane.comp.python.bio.general/6289
            if self.add_atom_occ and atom.occupancy is None:
                atom.set_occupancy(1)
            if self.remove_atom_alt:
                atom.set_altloc(' ')
            return True

def clean_pdb(pdb_file, out_suffix='_clean', outdir=None, force_rerun=False,
              remove_atom_alt=True, keep_atom_alt_id='A', remove_atom_hydrogen=True, add_atom_occ=True,
              remove_res_hetero=True, keep_chemicals=None, keep_res_only=None,
              add_chain_id_if_empty='X', keep_chains=None):
    """Clean a PDB file.

    Args:
        pdb_file (str): Path to input PDB file
        out_suffix (str): Suffix to append to original filename
        outdir (str): Path to output directory
        force_rerun (bool): If structure should be re-cleaned if a clean file exists already
        remove_atom_alt (bool): Remove alternate positions
        keep_atom_alt_id (str): If removing alternate positions, which alternate ID to keep
        remove_atom_hydrogen (bool): Remove hydrogen atoms
        add_atom_occ (bool): Add atom occupancy fields if not present
        remove_res_hetero (bool): Remove all HETATMs
        keep_chemicals (str, list): If removing HETATMs, keep specified chemical names
        keep_res_only (str, list): Keep ONLY specified resnames, deletes everything else!
        add_chain_id_if_empty (str): Add a chain ID if not present
        keep_chains (str, list): Keep only these chains

    Returns:
        str: Path to cleaned PDB file

    """
    outfile = ssbio.utils.outfile_maker(inname=pdb_file,
                                        append_to_name=out_suffix,
                                        outdir=outdir,
                                        outext='.pdb')

    if ssbio.utils.force_rerun(flag=force_rerun, outfile=outfile):
        my_pdb = StructureIO(pdb_file)
        my_cleaner = CleanPDB(remove_atom_alt=remove_atom_alt,
                              remove_atom_hydrogen=remove_atom_hydrogen,
                              keep_atom_alt_id=keep_atom_alt_id,
                              add_atom_occ=add_atom_occ,
                              remove_res_hetero=remove_res_hetero,
                              keep_res_only=keep_res_only,
                              add_chain_id_if_empty=add_chain_id_if_empty,
                              keep_chains=keep_chains,
                              keep_chemicals=keep_chemicals)

        my_clean_pdb = my_pdb.write_pdb(out_suffix=out_suffix,
                                        out_dir=outdir,
                                        custom_selection=my_cleaner,
                                        force_rerun=force_rerun)

        return my_clean_pdb
    else:
        return outfile


if __name__ == '__main__':
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                description=textwrap.dedent("""\
                                Clean PDB files - cleanpdb.py
                                -----------------------------
                                This script will automatically:

                                * Add missing chains to a PDB file
                                * Select a single chain or chains if noted
                                * Remove alternate atom locations
                                * Add atom occupancies
                                * Add B (temperature) factors (default Biopython behavior)

                                Cleaned PDBs will be in a clean_pdbs folder where the script is executed.
                                Example: script help
                                $ cleanpdb --help

                                Example: clean one PDB file
                                $ cleanpdb 1kf6.pdb

                                Example: clean one PDB file and keep only chains A and B
                                $ cleanpdb 1kf6.pdb --chain A,B

                                Example: clean multiple PDB files
                                $ cleanpdb *.pdb

                                Example: clean a whole directory of PDB
                                $ cleanpdb /path/to/pdb/files
                                """))
    p.add_argument('infile', help='PDB file or folder you want to clean', nargs='+', type=str)
    p.add_argument('--outsuffix', '-os', default='_clean', help='Suffix appended to PDB file')
    p.add_argument('--outdir', '-od', default='clean_pdbs', help='Directory to output clean PDBs')
    p.add_argument('--chain', '-c', default=None, help='Keep only specified chains')
    p.add_argument('--keephydro', '-hy', action='store_false', help='Keep hydrogen atoms (default is to remove)')
    p.add_argument('--keephetero', '-ht', action='store_false', help='Keep hetero atoms (default is to remove)')
    # TODO: if this flag is present, the alternate positions seem to switch line positions
    p.add_argument('--keepalt', '-ka', action='store_false', help='Keep alternate positions (default is to remove)')
    p.add_argument('--force', '-f', action='store_true', help='Force rerunning of cleaning even if the clean PDB exists')
    args = p.parse_args()

    if args.chain:
        args.chain = args.chain.split(',')

    if not op.isdir(args.outdir):
        os.mkdir(args.outdir)

    infiles = ssbio.utils.input_list_parser(args.infile)

    for pdb in tqdm(infiles):

        outfile = ssbio.utils.outfile_maker(inname=pdb,
                                            append_to_name=args.outsuffix,
                                            outdir=args.outdir,
                                            outext='.pdb')

        if ssbio.utils.force_rerun(flag=args.force, outfile=outfile):

            my_pdb = StructureIO(pdb)
            my_cleaner = CleanPDB(remove_atom_alt=args.keepalt,
                                  remove_atom_hydrogen=args.keephydro,
                                  keep_atom_alt_id='A',
                                  add_atom_occ=True,
                                  remove_res_hetero=args.keephetero,
                                  add_chain_id_if_empty='X',
                                  keep_chains=args.chain)

            my_clean_pdb = my_pdb.write_pdb(out_suffix=args.outsuffix,
                                            out_dir=args.outdir,
                                            custom_selection=my_cleaner,
                                            force_rerun=args.force)

    print('Clean PDBs at: {}'.format(args.outdir))
