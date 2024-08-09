# import matplotlib.pyplot as plt
# from pymatgen.io.vasp.outputs import Vasprun
# from pymatgen.electronic_structure.core import OrbitalType
# from pymatgen.electronic_structure.plotter import DosPlotter

# # path = "/Users/qizhang/mill_backup/GeSe/148/band"
# path = "/Users/qizhang/qqq/crystalproperties/GeSeNa_new/GeSeNa_properity/pre/dos_hybird"

# vasprun_path = path + "/vasprun.xml"

# # Load the vasprun.xml file
# vasprun = Vasprun(vasprun_path, parse_projected_eigen=True)
# complete_dos = vasprun.complete_dos
# print(type(complete_dos.get_element_dos()))
# # Initialize the plotter
# plotter = DosPlotter()

# # Get the elements in the structure
# elements = complete_dos.structure.composition.elements

# # Add projected DOS for each element and their orbitals
# # for element in elements:
# el_dos = complete_dos.get_element_spd_dos(elements[2])
# print(el_dos)
# for orbital, dos in el_dos.items():
#     print(dos.densities)
#     print(f"{elements[2]} {OrbitalType(orbital).name}")
#     plotter.add_dos(f"{elements[2]} {OrbitalType(orbital).name}", dos)

# # Plot the DOS
# plot = plotter.get_plot(xlim=(-4, 7), ylim=(0, 5))  # Adjust xlim and ylim as needed

# # Show the plot using Matplotlib's plt.show()
# plotter.save_plot("ori_Na.eps", xlim=(-4, 7), ylim=(0, 5))
# plt.show()

# import matplotlib.pyplot as plt
# from pymatgen.io.vasp.outputs import Vasprun
# from pymatgen.electronic_structure.core import OrbitalType
# from pymatgen.electronic_structure.plotter import DosPlotter
# from scipy.ndimage import gaussian_filter1d
# from pymatgen.electronic_structure.core import Spin

# path = "/Users/qizhang/mill_backup/GeSe/148/band"

# vasprun_path = path + "/vasprun.xml"

# # Function to smooth DOS data
# def smooth_dos(dos, sigma=0.1):
#     energies = dos.energies
#     densities = gaussian_filter1d(dos.densities[Spin.up], sigma=sigma)
#     return energies, densities

# # Load the vasprun.xml file
# vasprun = Vasprun(vasprun_path, parse_projected_eigen=True)
# complete_dos = vasprun.complete_dos

# # Initialize the plotter
# plotter = DosPlotter()

# # Get the elements in the structure
# elements = complete_dos.structure.composition.elements

# # Add projected DOS for each element and their orbitals
# # for element in elements:
# el_dos = complete_dos.get_element_spd_dos(elements[0])
# for orbital, dos in el_dos.items():
#     # Smooth the DOS data
#     energies, densities = smooth_dos(dos)
#     plotter.add_dos(f"{elements[0]} {OrbitalType(orbital).name}", dos)

# # Plot the DOS
# plot = plotter.get_plot(xlim=(-4, 7), ylim=(0, 5))  # Adjust xlim and ylim as needed

# # Show the plot using Matplotlib's plt.show()
# plt.show()