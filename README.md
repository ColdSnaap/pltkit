<!-- [![DOI](https://zenodo.org/badge/805911060.svg)](https://zenodo.org/doi/10.5281/zenodo.11838813) -->

<h1 align="center">Pltkit</h1>

</h4>
Pltkit is a data processing and visualization tool under development, designed for computational material science. Its functions include preparing input files for VASP, generating high-symmetry paths from POSCAR/cif files, and plotting electronic DOS/band structures as well as phonon DOS/band structures from Phonopy results, among other tasks.

## Prerequisites

### Python Version
Python 3.9+

### Required Packages
- `pymatgen`
- `ase`
- `matplotlib`
- `pandas`

<!-- The `pyxtal` package will automatically install ASE version 3.18.0 and Pymatgen 2024.3.1 when you run:
```sh
pip install pyxtal
```
However, since the ASE package on PyPI has not been updated for two years, you need to install the latest ASE version from their GitLab repository to ensure compatibility with chgnet. You can do this by running:
```sh
pip install git+https://gitlab.com/ase/ase
``` -->

<!-- ### PyXtal modification
SGRCSP uses PyXtal to generate symmetry-restricted structures. However, some modifications and bug fixes are required for the PyXtal package to support our desired functionality. Please copy the Python scripts from the pyxtal_modify folder to the corresponding PyXtal package directory.

### Bond configuration
To generate molecular crystal structures, you need to set the bond lengths between atoms within the molecules. This configuration should be defined in the bonds.json file located in the database folder of the PyXtal package. Only approximate bond lengths are necessary. -->


## Usage
<!-- [Documentation](https://sgrcsp.readthedocs.io/en/latest/) is under development. -->

### High-symmetry path within the first Brillouin zone.

**Example Python Script:**
```python
from structure import high_symm_k_path

structure = "POSCAR file path"
print(high_symm_k_path(structure))
```
**Output:**
```python
({'GAMMA': [0.0, 0.0, 0.0], 'Z': [0.0, 0.0, 0.5], 'M': [0.5, 0.5, 0.0], 'A': [0.5, 0.5, 0.5], 'R': [0.0, 0.5, 0.5], 'X': [0.0, 0.5, 0.0]}, [('GAMMA', 'X'), ('X', 'M'), ('M', 'GAMMA'), ('GAMMA', 'Z'), ('Z', 'R'), ('R', 'A'), ('A', 'Z'), ('X', 'R'), ('M', 'A')])
```

### Phonon band structure.

**Example Python Script:**
```python
from phonon import PhonopyResult

file = "phonon calculation result folder"
x = PhonopyResult(file)
x.band_plot(write=True)
```
**Example Output:**

![GeSe_phonon](https://github.com/user-attachments/assets/a76dfec2-b4f6-44d9-a28a-ac5633c1e9ce)

