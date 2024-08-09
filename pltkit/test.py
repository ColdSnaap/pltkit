from uspex import ReadIndividuals
from phonon import PhonopyInput
from structure import get_primitive
from structure import high_symm_k_path
from phonon import PhonopyResult
import os
import yaml
import math
import numpy as np
from collections import Counter
from structure import get_space_group
from sgrcsp import struc_vs_energy_plot_old
from sgrcsp import struc_vs_energy_plot_new
from structure import structure_converter
from tools import mlp_CHGNet
from tools import csv_plot
from tools import csv_plot2
from vasp import Dos, Band


# dir = "/Users/qizhang/Desktop/paper_new/USPEX_result/PSLi/31/results2"

# indi = ReadIndividuals(dir)

# en = indi.struc_vs_energy_plot(write=True)

# print(kpoints)
# print(kpath)
# # print("\n")
# structure = "/Users/qizhang/crystal_structure/paper3/structure/relaxed_structure/POSCAR_Zn_113"
# # # # # structure = os.getcwd() + "/POSCAR"
# # # ph = PhonopyInput(structure)
# # # print(ph.band_conf())
# # # # # result = ph.band_conf()
# get_space_group(structure, symprec=2)

# print(result)


# x = get_primitive(structure, sym=0.1, write=True)

# print(x)

# x_positions = [0.0000000, 0.0728471, 0.1428977, 0.1752815, 0.2849491, 0.3578022, 0.4313038, 0.5198936]
# y_positions = [0, 2, 4, 6, 8]
# tick_labels = ['$\Gamma$', '$X|Y$', '$\Gamma$', '$Z|R_2$', '$\Gamma$', '$T_2|U_2$', '$\Gamma$', '$V_2$']

# file = "/Users/qizhang/crystal_structure/paper3/phonon/Zn/phonon/82/phonon/"
# x = PhonopyResult(file)

# x.band_plot(write=True)



# file = "/Users/qizhang/Desktop/paper_new/For_Qi/Mn/Published_LiMnPS4-Srikanth.cif"
# prim = get_primitive(file, write=True)

# print(prim)


# file = "/Users/qizhang/Desktop/paper_new/PSLi/csp_data_new/group31/energy_relax"
# struc_vs_energy_plot_old(file, atom_number=16 ,write=True, title="$Li_3PS_4$ CSP in $Pmn2_1$(31)")

# file = "/Users/qizhang/crystal_structure/paper3/csp_result/Zn/sym1/BestStrucsList"
# struc_vs_energy_plot_new(file, atom_number=14, write=True, title="$LiZnPS_4$ CSP in $P1$(1)", groud_to_zero=True, y_lim=(-1,28))

# file = "/Users/qizhang/mill_backup/GeSe/148/elastic/POSCAR"
# x = structure_converter(file, "cif", write=True)

# file = "/Users/qizhang/Desktop/paper_new/GeSeNa/many_sym2/100.41792.cif"
# x = mlp_CHGNet(file)
# print(x)

file = os.getcwd()+"/Zn.csv"
csv_plot2(file, write_file=True)

# print("haha")

# vasp_file = "/Users/qizhang/mill_backup/GeSe/148/band"

# dos = Dos(vasp_file)
# dos.pdos(xlim=[-4,7], ylim=[0,30], label=True)

# band = Band(vasp_file)
# band.band()


# phonon_file = "/Users/qizhang/qqq/crystalproperties/GeSeNa_new/GeSeNa_properity_2/GeSeNa_phonon/ori/phonon"
# ph_result = PhonopyResult(phonon_file)
# ph_result.band_plot(write=True)