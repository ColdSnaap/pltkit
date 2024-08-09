import os
import pandas as pd
import matplotlib.pyplot as plt


def struc_vs_energy_plot_old(
    directory,
    atom_number,
    figsize=(8, 6),
    fontsize = 15,
    title = "",
    write=False,
    ground_to_zero=True,
    e_ground=None
):
    file = directory
    if not os.path.isfile(file):
        raise NameError("file not exist")
    df = pd.read_csv(file, delim_whitespace=True, header=None, names=['Step', 'Energy'])

    #PSLi
    #31
    df = df.drop(df.index[199:220])
    df.reset_index(drop=True, inplace=True)

    #sym7
    # df = df.drop(df.index[290:300])
    # df.reset_index(drop=True, inplace=True)
    # df = df.drop(df.index[600:645])
    # df.reset_index(drop=True, inplace=True)
    # df = df.drop(df.index[399:600])
    # df.reset_index(drop=True, inplace=True) 
    #sym4
    # df = df.drop(df.index[399:417])
    # df.reset_index(drop=True, inplace=True)
    # sym1
    # df = df.drop(df.index[200:263])
    # df.reset_index(drop=True, inplace=True)
    #sym14
    # df = df.drop(df.index[399:400])
    # df.reset_index(drop=True, inplace=True)

    df["Energy/atom"] = df["Energy"] / float(atom_number)
    df['ID'] = range(1, len(df) + 1)

    print(df)

    # Lowest number column
    lowest_en = df["Energy/atom"][0]
    df["LowestE"] = lowest_en
    for i, item in enumerate(df["Energy/atom"]):
        if item < lowest_en:
            lowest_en = item
        df.loc[i, "LowestE"] = lowest_en
    
    # Ground to zero
    if e_ground is None:
        ground = df["LowestE"].min()
    else:
        ground = e_ground
    df["Ground"] = df["LowestE"] - ground
    df["E_ground"] = df["Energy/atom"] - ground
    print(ground)

    plt.figure(figsize=figsize)
    if ground_to_zero:
        plt.scatter(df["ID"], df["E_ground"]*1000, facecolors='none', edgecolors='black', alpha=0.5)
        plt.plot(df["ID"], df["Ground"]*1000, color='r', label='Lowest Energy')
        plt.ylabel('Energy/atom (meV)', fontsize=fontsize)
    else:
        plt.scatter(df["ID"], df["Energy/atom"], facecolors='none', edgecolors='black', alpha=0.5)
        plt.plot(df["ID"], df["LowestE"], color='r', label='Lowest Energy')
        plt.ylabel('Energy/atom (eV)', fontsize=fontsize)

    plt.title(title, fontsize=fontsize+1)
    plt.xlabel('Structure Number', fontsize=fontsize)
    plt.xlim(df["ID"].min(), df["ID"].max())
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(False)
    if write:
        plt.savefig('output.eps', format='eps')
        plt.savefig('output.png', format='png', dpi=600)
    plt.show()


def struc_vs_energy_plot_new(
    directory,
    atom_number,
    figsize=(8, 6),
    fontsize = 15,
    title = "",
    write=False,
    groud_to_zero=True,
    e_ground=None,
    y_lim=None
):
    # file = directory + "/Result/BestStrucsList"
    file = directory
    if not os.path.isfile(file):
        raise NameError("file not exist")
    df = pd.read_csv(file, skipinitialspace=True)
    
    # df = df.drop(df.index[399:402])
    # df.reset_index(drop=True, inplace=True) 
    
    df["Energy"] = df["Energy/Atom"] / float(atom_number)
    df['ID'] = range(1, len(df) + 1)

    # Lowest number column
    lowest_en = df["Energy"][0]
    df["LowestE"] = lowest_en
    for i, item in enumerate(df["Energy"]):
        if item < lowest_en:
            lowest_en = item
        df.loc[i, "LowestE"] = lowest_en

    # Ground to zero
    if e_ground is None:
        ground = df["LowestE"].min()
    else:
        ground = e_ground
    df["Ground"] = df["LowestE"] - ground
    df["E_ground"] = df["Energy"] - ground

    print(df)
    print(ground)
    plt.figure(figsize=figsize)
    if groud_to_zero:
        plt.scatter(df["ID"], df["E_ground"]*1000, facecolors='none', edgecolors='black', alpha=0.5)
        plt.plot(df["ID"], df["Ground"]*1000, color='r', label='Lowest Energy')
        plt.ylabel('Energy/atom (meV)', fontsize=fontsize)
    else:
        plt.scatter(df["ID"], df["Energy"], facecolors='none', edgecolors='black', alpha=0.5)
        plt.plot(df["ID"], df["LowestE"], color='r', label='Lowest Energy')
        plt.ylabel('Energy/atom (eV)', fontsize=fontsize)
    plt.title(title, fontsize=fontsize+1)
    plt.xlabel('Structure Number', fontsize=fontsize)
    plt.xlim(df["ID"].min(), df["ID"].max())
    if y_lim is not None:
        plt.ylim(y_lim[0], y_lim[1])
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(False)
    if write:
        plt.savefig('output.eps', format='eps')
        plt.savefig('output.png', format='png', dpi=600)
    plt.show()