from pymatgen.io.vasp import Poscar
from chgnet.model.model import CHGNet
from chgnet.model.dynamics import StructOptimizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter
from structure import structure_converter


def mlp_CHGNet(structure, fmax: float = 0.1, relax: bool = False) -> list:
    structure = structure_converter(structure)
    relax_structure = False
    chgnet = CHGNet.load()
    if relax==False:
        # print(self.structure)
        prediction = chgnet.predict_structure(structure)
        energy = round(prediction['e'] * len(structure), 5)
        energy_per_atom = round(float(prediction['e']), 5)
    elif relax==True:
        relaxer = StructOptimizer()
        result = relaxer.relax(structure, fmax=fmax)
        energy = round(result['trajectory'].energies[-1], 5)
        relax_structure = Poscar(result['final_structure'])
        energy_per_atom = round(result['trajectory'].energies[-1] / len(structure), 5)

    return relax_structure, energy, energy_per_atom


def csv_plot(csv_file, title=None, write_file=False):

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    print(df)

    # Check if necessary columns exist in the DataFrame
    if 'structure' not in df.columns or 'vasp' not in df.columns or 'mlpotential' not in df.columns:
        raise ValueError("CSV file must contain 'structure', 'vasp', and 'mlpotential' columns")

    # Create the plot
    plt.figure(figsize=(8, 5))
    
    # Scatter plots for 'vasp' and 'mlpotential'
    plt.scatter(df['structure'], df['vasp'], marker='o')
    # plt.scatter(df['structure'], df['mlpotential'], label='CHGnet', marker='x')

    # Set labels and title
    plt.xlabel('Structure Number', fontsize=14)
    plt.ylabel('Energy (meV)', fontsize=14)
    if title:
        plt.title(title, fontsize=16)

    # Add legend and grid
    plt.legend()
    plt.grid(False)

    # Optionally write the plot to a file
    if write_file:
        plt.savefig("output.png", dpi=600)

    # Show the plot
    plt.show()


def csv_plot2(csv_file, title=None, write_file=False):

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    print(df)

    # Create the plot
    plt.figure(figsize=(4, 6))
    
    # Scatter plots for 'vasp' and 'mlpotential'
    plt.scatter(df['structure'], df['vasp1'], marker='o')
    # plt.scatter(df['structure'], df['mlpotential'], label='CHGnet', marker='x')

    # Set labels and title
    plt.xlabel('Structure Number', fontsize=14)
    # plt.ylabel('Energy (meV)', fontsize=14)
    if title:
        plt.title(title, fontsize=16)
    # plt.gca().axes.xaxis.set_ticks([])
    # plt.gca().axes.yaxis.set_ticks([])
    # Add legend and grid
    plt.legend()
    plt.grid(False)
    plt.ylim(-1, 28)
    plt.xticks([1, 2, 3])

    # Optionally write the plot to a file
    if write_file:
        plt.savefig("output.png", dpi=600)

    # Show the plot
    plt.show()

class SmoothFilter:
    
    def __init__(self, data) -> None:
        self.data = data

    def moving_average(self, window_size):
        cumsum = np.cumsum(np.insert(self.data, 0, 0))
        moving_averages = (cumsum[window_size:] - cumsum[:-window_size]) / window_size
        return moving_averages
    
    def savgol(self, window_size, poly_order):
        smoothed_data = savgol_filter(self.data, window_size, poly_order)
        return smoothed_data
    
    def gaussian(self, sigma):
        smoothed_data = gaussian_filter(self.data, sigma)
        return smoothed_data