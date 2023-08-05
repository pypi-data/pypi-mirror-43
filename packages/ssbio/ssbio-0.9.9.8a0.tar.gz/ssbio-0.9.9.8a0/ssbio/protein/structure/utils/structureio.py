from Bio import PDB
from Bio.PDB.PDBIO import PDBIO
from Bio.PDB.PDBIO import Select
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.mmtf import MMTFParser
from Bio.PDB.PDBExceptions import PDBConstructionWarning
import os.path as op
import logging
import warnings
import ssbio.utils
from ssbio.biopython.bp_mmcifparser import MMCIFParserFix

log = logging.getLogger(__name__)

cifp = MMCIFParserFix(QUIET=True)
pdbp = PDBParser(PERMISSIVE=True, QUIET=True)
mmtfp = MMTFParser()


def as_protein(structure, filter_residues=True):
    """ Exposes methods in the Bio.Struct.Protein module.
        Parameters:
            - filter_residues boolean; removes non-aa residues through Bio.PDB.Polypeptide is_aa function
              [Default: True]
        Returns a new structure object.
    """

    from ssbio.biopython.Bio.Struct.Protein import Protein
    return Protein.from_structure(structure, filter_residues)


class StructureIO(PDBIO):
    """Extended class to load any structure file into a Biopython Structure object

    Loads the first model when there are multiple available.
    Also adds some logging methods.
    """

    # XTODO: need to revamp this module to be clearer on what files are supported, how file path is parsed
    # (should explicitly define it)
    def __init__(self, structure_file, file_type=None):
        PDBIO.__init__(self)

        dirname, filename_without_extension, file_type2 = ssbio.utils.split_folder_and_path(structure_file)
        self.structure_file = structure_file

        # Unzip the file if it is zipped
        if file_type == '.gz':
            unzipped = ssbio.utils.gunzip_file(structure_file, outdir=dirname)
            dirname, filename_without_extension, file_type2 = ssbio.utils.split_folder_and_path(unzipped)

        if not file_type:
            file_type = file_type2
        else:
            if '.' not in file_type:
                file_type = '.{}'.format(file_type)

        if file_type.lower() in ['.pdb', '.ent', '.mmcif', '.cif', '.mmtf']:
            # Load the structure
            if file_type.lower() == '.pdb' or file_type.lower() == '.ent':
                structure = pdbp.get_structure(id='ssbio_pdb', file=structure_file)
            if file_type.lower() == '.mmcif' or file_type.lower() == '.cif':
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', PDBConstructionWarning)
                    structure = cifp.get_structure(structure_id='ssbio_cif', filename=structure_file)
            if file_type.lower() == '.mmtf':
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', PDBConstructionWarning)
                    structure = mmtfp.get_structure(file_path=structure_file)
            log.debug('{}: parsed 3D coordinates of structure'.format(op.basename(structure_file)))
        else:
            raise ValueError('{}: unsupported file type'.format(file_type))

        self.set_structure(structure)
        try:
            self.first_model = structure[0]
        except KeyError:
            raise KeyError('{}: no models contained in structure! Please check structure file contents.'.format(structure_file))

    def write_pdb(self, custom_name='', out_suffix='', out_dir=None, custom_selection=None, force_rerun=False):
        """Write a new PDB file for the Structure's FIRST MODEL.

        Set custom_selection to a PDB.Select class for custom SMCRA selections.

        Args:
            custom_name: Filename of the new file (without extension)
            out_suffix: Optional string to append to new PDB file
            out_dir: Optional directory to output the file
            custom_selection: Optional custom selection class
            force_rerun: If existing file should be overwritten

        Returns:
            out_file: filepath of new PDB file

        """
        if not custom_selection:
            custom_selection = ModelSelection([0])

        # If no output directory, custom name, or suffix is specified, add a suffix "_new"
        if not out_dir or not custom_name:
            if not out_suffix:
                out_suffix = '_new'

        # Prepare the output file path
        outfile = ssbio.utils.outfile_maker(inname=self.structure_file,
                                            outname=custom_name,
                                            append_to_name=out_suffix,
                                            outdir=out_dir,
                                            outext='.pdb')
        try:
            if ssbio.utils.force_rerun(flag=force_rerun, outfile=outfile):
                self.save(outfile, custom_selection)
        except TypeError as e:
            # If trying to save something that can't be saved as a PDB (example: 5iqr.cif), log an error and return None
            # The error thrown by PDBIO.py is "TypeError: %c requires int or char"
            log.error('{}: unable to save structure in PDB file format'.format(self.structure_file))
            raise TypeError(e)

        return outfile


class ModelSelection(PDB.Select):
    """Selection rule to keep only a specified model of a PDB file."""

    def __init__(self, models_to_keep):
        self.models_to_keep = models_to_keep

    def accept_model(self, model):
        if model.id == model:
            return True
        elif model.id in self.models_to_keep:
            return True
        else:
            return False