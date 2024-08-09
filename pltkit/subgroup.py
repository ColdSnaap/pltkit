from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure
from pymatgen.symmetry.groups import sg_symbol_from_int_number

# Example crystal structure for space group P21 (4)
lattice = Lattice.monoclinic(5.431, 5.431, 5.431, 90, 90, 120)
species = ["Si"] * 2
coords = [[0, 0, 0], [0.333, 0.667, 0.333]]
structure = Structure(lattice, species, coords)
analyzer = SpacegroupAnalyzer(structure, symprec=0.01)
original_sym_ops = analyzer.get_symmetry_operations()

# Function to check if all symmetry operations of sg1 are in sg2
def is_supergroup(sg_number, original_sym_ops):
    sg_symbol = sg_symbol_from_int_number(sg_number)
    try:
        # Create a dummy structure with the desired space group symmetry
        dummy_analyzer = SpacegroupAnalyzer(structure.copy(), symprec=0.01)
        dummy_analyzer.get_symmetry_operations()
        dummy_analyzer.get_space_group_operations(sg_number)
        candidate_sym_ops = dummy_analyzer.get_symmetry_operations()
        
        # Check if all original symmetry operations are in the candidate's operations
        for op in original_sym_ops:
            if op not in candidate_sym_ops:
                return False
        return True
    except:
        return False

# List of all 230 space group numbers
all_space_groups = list(range(1, 231))

# Identify supergroups
supergroups = [sg for sg in all_space_groups if sg > 4 and is_supergroup(sg, original_sym_ops)]

# Print the supergroups
print("Supergroups of space group 4 (P21):", supergroups)