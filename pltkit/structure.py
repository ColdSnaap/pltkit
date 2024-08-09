import ase.io
import seekpath
from pathlib import Path
from pymatgen.core import Structure
from pymatgen.io.vasp import Poscar
from pymatgen.io.cif import CifParser
from pymatgen.io.cif import CifWriter
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


def get_space_group(structure_file, symprec=0.1, write=False):
    # Load the structure from the POSCAR file
    structure = Structure.from_file(structure_file)

    # Create a SpacegroupAnalyzer object
    sga = SpacegroupAnalyzer(structure, symprec=symprec)

    # Get the space group number and symbol
    space_group_number = sga.get_space_group_number()
    space_group_symbol = sga.get_space_group_symbol()

    # Print the results
    print(f"Space Group Number: {space_group_number}")
    print(f"Space Group Symbol: {space_group_symbol}")

    if write:
        cif_writer = CifWriter(structure, symprec=0.1)
        cif_writer.write_file("output.cif")


def high_symm_k_path(structure_file, symprec=0.00001):
    # Load structure
    atoms = ase.io.read(structure_file)

    # Get the high symmetry path using Seekpath
    structure = (atoms.cell, atoms.get_scaled_positions(), atoms.get_atomic_numbers())
    path_data = seekpath.get_path(structure, symprec=symprec)

    # Extract k-points and labels
    kpoints = path_data['point_coords']
    labels = path_data['path']

    return kpoints, labels


def get_primitive(structure, sym=0.25, write=False):
    # Load the structure
    structure = Structure.from_file(structure)

    # Get the primitive cell
    primitive_structure = structure.get_primitive_structure(tolerance=sym)

    if write:
        primitive_structure.to(fmt="poscar", filename="POSCAR_primitive")
        print("Write POSCAR_primitive file")
    
    return primitive_structure


def structure_converter(structure, type: str = None, write=False):
    if isinstance(structure, str):
        # Create a Path object from the file path
        path = Path(structure)
        if path.exists():
            # Check if the file has an extension
            if path.suffix:
                # Return the extension without the dot
                file_type = path.suffix[1:]
            else:
                # Return the file name if there is no extension
                file_type = path.name
        else:
            raise NameError("File not exist")
        
        # Read structure file and store it as pymatgen structure
        if file_type == "cif":
            parser = CifParser(structure)
            structure = parser.get_structures()[0]
        elif file_type == "POSCAR" or "CONTCAR":
            poscar = Poscar.from_file(structure)
            structure = poscar.structure

    elif isinstance(structure, Structure):
        structure = structure
    else:
        raise NameError(f"Structure type: {type(structure)} not supported yet")
    
    if write:
        if type == "cif":
            cif_writer = CifWriter(structure, symprec=1)
            cif_writer.write_file("output.cif")
        
        elif type == "POSCAR":
            poscar = Poscar(structure)
            poscar.write_file("POSCAR_output")

    return structure