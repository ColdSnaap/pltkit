import yaml
import os
import math
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from structure import high_symm_k_path


def are_lists_approximately_equal(list1, list2, rel_tol=1e-5, abs_tol=1e-5):
    if len(list1) != len(list2):
        return False
    
    return all(math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol) for a, b in zip(list1, list2))


class PhonopyInput:

    def __init__(self, structure) -> None:
        self.structure = structure   

    def band_conf(self, symprec=0.00001):
        kpoints, kpath = high_symm_k_path(self.structure, symprec=symprec)
        # print(kpoints)
        # print(kpath)
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
        
        # Construct the string with two spaces between items, no space before commas, and one space after commas
        result = ""
        for i, item in enumerate(path_list):
            if item == ',':
                result = result.rstrip() + item + ' '  # Remove space before comma, add comma and one space after
            else:
                result += item  # Add item without trailing space
                if i < len(path_list) - 1 and path_list[i + 1] != ',':
                    result += "  "  # Add two spaces after the item if the next item is not a comma

        return result


class PhonopyResult:

    def __init__(self, result_dir) -> None:
        self.result = result_dir
        if not os.path.isdir(self.result):
            raise NameError("Directory not exist")


    def band_plot(self, write=False):
        structure = self.result + "/POSCAR"
        if not os.path.isfile(structure):
            raise NameError("Structure file (POSCAR) not found")
        
        kpoints, kpath = high_symm_k_path(structure)

        # Set x tick labels
        tick_labels = []
        new_kpath = [[] for i in range(len(kpath))]
        for i, segment in enumerate(kpath):
            for j, point in enumerate(segment):
                if point == "GAMMA":
                    new_kpath[i].append(f"$\Gamma$")
                elif point == "DELTA_0":
                    new_kpath[i].append(f"$\Delta_0$")
                elif point == "SIGMA_0":
                    new_kpath[i].append(f"$\Sigma_0$")
                else:
                    new_kpath[i].append(f"${point}$")

        for i, segment in enumerate(new_kpath):
            if i == 0:
                tick_labels.append(segment[0])
            else:
                left, right = segment
                right_before = new_kpath[i-1][1]
                if left == right_before:
                    tick_labels.append(right_before)
                else:
                    string = f"{right_before}|{left}"
                    new_string = string.replace('$|$', '|').replace('$|', '|').replace('|$', '|')
                    tick_labels.append(new_string)
        tick_labels.append(new_kpath[len(new_kpath)-1][1])
        # print(tick_labels)
        # print("\n")

        # Set x positions
        band_file = self.result + "/band.yaml"
        with open(band_file, 'r') as file:
            band_data = yaml.safe_load(file)

        # Get a simple label list
        lable_list = []
        for i, segment in enumerate(kpath):
            left, right = segment
            if i == 0:
                lable_list.append(left)
            else:
                right_before = kpath[i-1][1]
                lable_list.append(right_before)
        lable_list.append(kpath[len(kpath)-1][1])

        # print(f'lable_list:{lable_list}')
        # print(f"kpoints:{kpoints}")
        distance_dict = {}
        # for lable in lable_list:

        label_uniq = list(set(lable_list))

        for lable in label_uniq:
            app_list = []
            for i in band_data['phonon']:
                if are_lists_approximately_equal(i['q-position'], kpoints[lable]):
                # if abs(float(i['q-position']) - float(kpoints[lable])) < 10e-5:
                    app_list.append(float(i['distance']))
            distance_dict[lable] = sorted(list(set(app_list)))
            # distance_dict[lable] = app_list

        label_count  = Counter(lable_list)
        # print(f'distance_dict:{distance_dict}')

        # Counter directory
        count_dict = {}
        for i in label_uniq:
            count_dict[i] = 0

        # print(f'label_count:{label_count}')
        # Distance list
        distance_list = []
        print(os.getcwd())
        print(lable_list)
        print(label_count)
        print(distance_dict)
        print("-----------------------------")
        for label in lable_list:
            print(label)
            print(distance_list)
            if label_count[label] == 1:
                distance_list.append(distance_dict[label][0])
            else:
                distance_list.append(distance_dict[label][count_dict[label]])
                count_dict[label] += 1

        # Check if list is sorted
        is_sorted = distance_list == sorted(distance_list)
        if not is_sorted:
            raise ValueError("Distance list (x positions) is not sorted")

        # Band frequency
        q_points = [q['distance'] for q in band_data['phonon']]
        bands = [[] for _ in range(len(band_data['phonon'][0]['band']))]
        
        for q in band_data['phonon']:
            for i, freq in enumerate(q['band']):
                bands[i].append(freq['frequency'])
        
        # Set ylim xlim and y tick positions
        xmin, xmax = min(q_points), max(q_points)
        ymin, ymax = float('inf'), float('-inf')

        for i in bands:
            ymin_inter = min(i)
            ymax_inter = max(i)
            if ymin_inter < ymin:
                ymin = ymin_inter
            if ymax_inter > ymax:
                ymax = ymax_inter
                
        # Generate integer list
        # Calculate the start and end values
        start_value = int(np.floor(ymin))
        end_value = int(np.ceil(ymax))

        # Ensure 0 is within the range
        if start_value > 0:
            start_value = 0
        if end_value < 0:
            end_value = 0

        # Calculate the number of points to ensure 0 is included
        range_span = abs(end_value - start_value) + 1
        evenly_spaced = np.linspace(start_value, end_value, range_span, endpoint=True)

        # Convert to integers and remove duplicates
        integer_list = list(map(int, np.unique(np.round(evenly_spaced))))
        
        x_positions = distance_list
        y_positions = integer_list
        tick_labels = tick_labels

        print(x_positions)
        print(tick_labels)

        # 3. Plot the phonon band structure
        fig, ax = plt.subplots(figsize=(6, 5))
        
        indices_with_pipe = [index for index, item in enumerate(tick_labels) if '|' in item]
        
        if len(indices_with_pipe) != 0:
            for index in indices_with_pipe:
                pip_x_position = [x_positions[index] for index in indices_with_pipe]
            
            pip_index = [q_points.index(i) for i in pip_x_position]

            for position in pip_index:
                q_points[position] = np.nan
            
            for band in bands:
                for position in pip_index:
                    band[position] = np.nan
                ax.plot(q_points, band, color='black')
        
        else:
            for band in bands:
                ax.plot(q_points, band, color='black')
        
        for xpos in x_positions:
            ax.axvline(x=xpos, color='grey', linestyle='dashed', alpha=0.2)
        
        # for ypos in y_positions:
        #     ax.axhline(y=ypos, color='grey', linestyle='dashed', alpha=0.2)
        ax.axhline(y=0, color='grey', linestyle='dashed', alpha=0.2)

        # Use the axes object to set ticks and labels
        ax.set_xticks(x_positions)
        ax.set_xticklabels(tick_labels)
        ax.tick_params(axis='both', labelsize=15)
        ax.set_xlim([xmin, xmax])
        # ax.set_ylim([0, max([max(band) for band in bands])])
        ax.set_ylim([0, 9])
        # ax.set_xlabel('Wavevector', fontsize=15)  # Set x-axis label size
        ax.set_ylabel('Frequency (THz)', fontsize=15)  # Set y-axis label size
        # ax.grid(axis='y')
        # y_min, y_max = ax.get_ylim()
        # ax.set_yticks(np.arange(y_min, y_max, 2))
        ax.set_yticks(y_positions)
        plt.tight_layout()
        if write:
            plt.savefig('band.eps', format='eps')
            plt.savefig('band.png', format='png', dpi=600)
        plt.show()
    
    def dos_plot(self):
        pass