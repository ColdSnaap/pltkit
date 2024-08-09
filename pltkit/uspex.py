import os
import pandas as pd
import matplotlib.pyplot as plt


class ReadIndividuals:
    
    def __init__(self, uspex_result) -> None:
        individuals_file = uspex_result + "/Individuals"
        individuals_csv_file = uspex_result+"/Individuals.csv"
        # Check if Individuals file exists
        if not os.path.isfile(individuals_file):
            raise NameError("Individuals not exist")
        else:
            # Modify the Individuals file
            with open(individuals_file, 'r') as file:
                lines = file.readlines()
            # Extract the header and data lines
            header = lines[0]
            data_lines = lines[2:]
            # ID: 1, Enthalpy: 4, Volume: 5, Density: 6, Fitness: 7, SYMM: 9
            indices = [1, 8, 9, 10, 11, 16]
            # Write to a new CSV file
            with open(individuals_csv_file, 'w') as file:
                # Write the header
                file.write("ID,Enthalpy,Volume,Density,Fitness,SYMM,AtomNo\n")
                # Write the data
                for line in data_lines:
                    # Split the line into columns
                    columns = line.split()
                    
                    # Get how many atoms in the structure
                    inside_brackets = False
                    numbers_to_sum = []
                    found_first_pair = False

                    # Iterate through the list
                    for item in columns:
                        if item == '[' and not found_first_pair:
                            inside_brackets = True
                            found_first_pair = True
                            continue
                        if ']' in item and inside_brackets:
                            inside_brackets = False
                            # Handle the case where the closing bracket is attached to a number
                            number_part = item.replace(']', '')
                            if number_part.isdigit():
                                numbers_to_sum.append(int(number_part))
                            continue
                        if inside_brackets:
                            if item.isdigit():
                                numbers_to_sum.append(int(item))

                    # Sum the collected numbers
                    sum_of_numbers = sum(numbers_to_sum)
                    # Extract the required columns
                    selected_columns = [columns[i] for i in indices]
                    # Write the selected columns to the CSV file
                    file.write(','.join(selected_columns) + f',{sum_of_numbers}\n')

            # Read the file into a DataFrame
            self.df = pd.read_csv(individuals_csv_file)
            self.df["Energy/atom"] = self.df["Enthalpy"] / self.df["AtomNo"]


    def struc_vs_energy_plot(
        self,
        figsize=(8, 6),
        fontsize = 15,
        title = "",
        write=False,
    ):
        df = self.df.copy()
        # Lowest number column
        lowest_en = df["Energy/atom"][0]
        df["LowestE"] = lowest_en
        for i, item in enumerate(df["Energy/atom"]):
            if item < lowest_en:
                lowest_en = item
            df.loc[i, "LowestE"] = lowest_en

        plt.figure(figsize=figsize)
        plt.scatter(self.df["ID"], self.df["Energy/atom"], facecolors='none', edgecolors='black', alpha=0.5)
        plt.plot(df["ID"], df["LowestE"], color='r', label='Lowest Energy')
        plt.title(title)
        plt.xlabel('Structure Number', fontsize=fontsize)
        plt.ylabel('Energy/atom (eV)', fontsize=fontsize)
        plt.xlim(df["ID"].min(), df["ID"].max())
        plt.grid(False)
        plt.tick_params(axis='both', which='major', labelsize=12)

        if write:
            plt.savefig('output.eps', format='eps')
            plt.savefig('output.png', format='png', dpi=600)

        plt.show()
