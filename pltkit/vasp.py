import os
import numpy as np
import matplotlib.pyplot as plt
from pymatgen.electronic_structure.core import Spin
from pymatgen.electronic_structure.plotter import BSDOSPlotter, BSPlotter, DosPlotter
from pymatgen.io.vasp.outputs import BSVasprun, Vasprun, Kpoints
from pymatgen.core.periodic_table import Element
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp import Poscar
from tools import SmoothFilter
from structure import high_symm_k_path
from phonon import PhonopyInput


class Dos:

    def __init__(self, file_path: str) -> None:
        self.path = file_path

        # Get element
        poscar_path = file_path + "/POSCAR"
        poscar = Poscar.from_file(poscar_path)
        elements = poscar.site_symbols
        self.elements = [Element[ele] for ele in elements]

        # Color mapping
        self.color = ["red", "green", "blue", "yellow"]

    def pdos(
        self,
        smooth=True,
        xlim=None, 
        ylim=None, 
        label=False,
        title=None
    ):
        vasprun_path = self.path + "/vasprun.xml"
        vasprun = Vasprun(vasprun_path)

        # Extract the total DOS
        dos_total = vasprun.complete_dos
        print(f"band gap:{dos_total.get_gap()}")
        print(f"cbm_vbm:{dos_total.get_cbm_vbm()}")
        print(dos_total.get)
        dos_element = dos_total.get_element_dos()
        energies = dos_total.energies - dos_total.efermi
        densities = dos_total.densities

        if smooth:
            for key in list(densities.keys()):
                sm = SmoothFilter(densities[key])
                densities[key] = sm.gaussian(2.0)
            
        # Plotting
        plt.figure(figsize=(8, 6))
        for spin in list(densities.keys()):
            density = densities[spin]
            if label:
                plt.plot(energies, density, label="Total", color="grey")
                plt.fill_between(energies, density, color='lightgrey', alpha=0.5)
            else:
                plt.plot(energies, density, color="grey")
                plt.fill_between(energies, density, color='lightgrey', alpha=0.5)
        
        for x, ele in enumerate(self.elements):            
            densities = dos_element[ele].densities
            if smooth:
                for key in list(densities.keys()):
                    sm = SmoothFilter(densities[key])
                    densities[key] = sm.gaussian(2.0)

            for spin in list(densities.keys()):
                density = densities[spin]
                color = self.color[x]
                if label:
                    plt.plot(energies, density, label=str(ele), color=color)
                else:
                    plt.plot(energies, density, color=color)
        
        if xlim is not None:
            plt.xlim(xlim[0], xlim[1])
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])
        
        if label:
            plt.legend(fontsize=15)
        if title is not None:
            plt.title(title)
        
        plt.tick_params(axis='both', labelsize=15)
        plt.xlabel("Energy (eV)", fontsize=15)
        plt.ylabel("DOS", fontsize=15)

        plt.show()
    
    def pdos_orbital(
        self,
        smooth=True,
        xlim=None, 
        ylim=None, 
        label=False,
        title=None
    ):
        pass


class Band:

    def __init__(self, file_path:str) -> None:
        self.path = file_path
        structure = self.path + "/POSCAR"
        kpoints, kpath = high_symm_k_path(structure, symprec=0.00001)

        path_list = []
        for i, segment in enumerate(kpath):
            if i == 0:
                for j in segment:
                    coor_list = ' '.join(map(str, kpoints[j]))
                    path_list.append(coor_list)
            else:
                left, right = segment
                right_before = kpath[i-1][1]
                if left == right_before:
                    coor_list = ' '.join(map(str, kpoints[right]))
                    path_list.append(coor_list)
                else:
                    path_list.append(",")
                    for j in segment:
                        coor_list = ' '.join(map(str, kpoints[j]))
                        path_list.append(coor_list)

        # Initialize an empty list to store the NumPy arrays
        arrays_list = []

        # Temporary list to hold individual sublists
        temp_list = []

        # Iterate through the original list and group elements into sublists separated by commas
        for item in path_list:
            if item == ',':
                # Convert the current sublist to a NumPy array and append to the arrays_list
                data_floats = [list(map(float, sub_item.split())) for sub_item in temp_list]
                data_array = np.array(data_floats)
                arrays_list.append(data_array)
                # Clear the temporary list for the next group
                temp_list = []
            else:
                # Add the item to the temporary list
                temp_list.append(item)

        # Convert the final sublist to a NumPy array and append to the arrays_list (if any remaining items)
        if temp_list:
            data_floats = [list(map(float, sub_item.split())) for sub_item in temp_list]
            data_array = np.array(data_floats)
            arrays_list.append(data_array)
        self.kpoint = arrays_list

        print(self.kpoint)

    # def euclidean_distance(self, a, b):
    #     return np.linalg.norm(a - b) 

    # def distance_list(self, kpoints_coor):
    #     dis_list = []
    #     k_coor = []
    #     count = 0
    #     for i in kpoints_coor:
    #         k_coor.append(i.frac_coords)
    #     for i, kpoint in enumerate(self.kpoint):
    #         dis_inter = [0.0]
    #         for index, coor in enumerate(k_coor):
    #             begin, end = kpoint[0], kpoint[-1]
    #             if index >= count:
    #                 while self.euclidean_distance(coor, end) < 0.0001:
    #                     self.euclidean_distance(coor, end)
    #                     dis_inter.append(0.0)


    def band(
        self,
        distance_list,
        labe_list,
        interval,
        drop=None,
    ):
        vasprun_path = self.path + "/vasprun.xml"
        kpoints_path = self.path + "/KPOINTS"
        vasprun = Vasprun(vasprun_path)

        efermi = vasprun.efermi
        band_structure = vasprun.get_band_structure( 
            kpoints_filename=None,
            efermi=efermi
        )

        
        # print(band_structure.kpoints[1].frac_coords)
        print(len(band_structure.kpoints))
        # print(band_structure.bands[Spin.up])
        # plotter = BSPlotter(band_structure)
        # plotter.get_plot().show()

# def band(file):
#     # Path to the vasprun.xml file
#     vasprun_path = file + "/vasprun.xml"  # Replace with the actual path

#     # Parse the vasprun.xml file
#     vasprun = Vasprun(vasprun_path)

#     # Extract the band structure
#     band_structure = vasprun.get_band_structure()

#     # Plot the band structure
#     plotter = BSPlotter(band_structure)
#     plot = plotter.get_plot()

#     # Show the plot
#     plotter.show()