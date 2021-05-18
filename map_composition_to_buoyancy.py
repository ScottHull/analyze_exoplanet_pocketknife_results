import pandas as pd
import matplotlib.pyplot as plt
from src.atomic import Convert

# BSP temperature, MORB F temperature, MORB temperature
runs = [
    (1600, 1600, 1600),
    (1600, 1600, 1400),
    (1600, 1400, 1400),
    (1400, 1400, 1400),
]


def get_cation_pct(star, composition):
    given_feo = composition['FeO'][star]
    given_mgo = composition['MgO'][star]
    given_sio2 = composition['SiO2'][star]
    given_cao = composition['CaO'][star]
    given_al2o3 = composition['Al2O3'][star]
    given_tio2 = composition['TiO2'][star]
    given_na2o = composition['Na2O'][star]
    oxides = {
        "feo": given_feo,
        "mgo": given_mgo,
        "sio2": given_sio2,
        "cao": given_cao,
        "al2o3": given_al2o3,
        "tio2": given_tio2,
        "na2o": given_na2o
    }
    atomic_pct = Convert().convert_oxide_pct_to_cation_pct(oxides=oxides)
    return atomic_pct


def get_composition_file(path_to_folder, material, F_temperature, runs=None):
    df = None
    if runs is None:
        runs = ["kepler", "adibekyan"]
    for index, run in enumerate(runs):
        bsp_template = path_to_folder + "/{}_{}_Compositions.csv".format(run.lower(), material.upper())
        morb_template = path_to_folder + "/{}_f{}_{}_Compositions.csv".format(run.lower(), F_temperature,
                                                                              material.upper())
        selected = None
        if material.lower() == "bsp":
            selected = bsp_template
        else:
            selected = morb_template
        if index == 0:
            df = pd.read_csv(selected)
            df['run'] = ['kepler' for i in range(0, len(list(df['Star'])))]
            df.set_index('Star', inplace=True)
        else:
            df2 = pd.read_csv(selected)
            df2['run'] = ['adibekyan' for i in range(0, len(list(df2['Star'])))]
            df2.set_index('Star', inplace=True)
            df2 = df2.drop("Sun")
            df = df.append(df2)
    return df


def get_density_file(path_to_folder, bsp_temperature, morb_F_temperature, morb_temperature, runs=None):
    df = None
    if runs is None:
        runs = ["kepler", "adibekyan"]
    for index, run in enumerate(runs):
        template = path_to_folder + "/{}_BSP_{}_MORB_F{}_{}.csv".format(run.capitalize(), bsp_temperature,
                                                                        morb_F_temperature, morb_temperature)
        if index == 0:
            df = pd.read_csv(template)
            df.set_index('star', inplace=True)
        else:
            df2 = pd.read_csv(template)
            df2.set_index('star', inplace=True)
            df2 = df2.drop("Sun")
            df = df.append(df2)
    return df


def get_data(element_1, element_2, composition, density):
    data = []
    for star in composition.index:
        if star in density.index.values.tolist():
            run = composition['run'][star]
            element_1 = element_1[0:2].lower()
            element_2 = element_2[0:2].lower()
            cation_pct = get_cation_pct(star=star, composition=composition)
            element_1_val = cation_pct[element_1]
            element_2_val = cation_pct[element_2]
            s = sum(list(cation_pct.values()))
            try:
                final_density = density["573.68"][star].values[0]
            except:
                final_density = density["573.68"][star]
            data.append((star, run, element_1_val, element_2_val, final_density))
    return data


def plot(fig, ax, index, data, bsp_temp, morb_f_temp, morb_temp, element_1, element_2, compostion_relative_to):
    fname = "bsp_{}_morb_f{}_{}_{}_relative.png".format(bsp_temp, morb_f_temp, morb_temp, compostion_relative_to)
    ax = ax.ravel()
    ax[index].scatter(
        [i[2] / i[3] for i in data if i[1] == "adibekyan"],
        [i[4] for i in data if i[1] == "adibekyan"],
        marker="+",
        color='red',
        label='adibekyan'
    )
    ax[index].scatter(
        [i[2] / i[3] for i in data if i[1] == "kepler"],
        [i[4] for i in data if i[1] == "kepler"],
        marker="+",
        color='blue',
        label='kepler'
    )
    ax[index].axvline([i[2] / i[3] for i in data if i[0] == "Sun"], linestyle="--", color='black')
    ax[index].axhline([i[4] for i in data if i[0] == "Sun"], linestyle="--", color='black', label="Sun")
    element_1 = element_1[0:2].capitalize()
    element_2 = element_2[0:2].capitalize()
    # ax[index].set_xlabel("{}/{} ({})".format(element_1, element_2, compostion_relative_to))
    # ax[index].set_ylabel("Specific Buoyancy @ 573.68 km")
    ax[index].set_title("BSP {} K, MORB F{} K @ {} K".format(bsp_temp, morb_f_temp, morb_temp))
    ax[index].grid()
    fig.supxlabel("{}/{} ({})".format(element_1, element_2, compostion_relative_to))
    fig.supylabel("Specific Buoyancy @ 573.68 km")
    if index == len(ax) - 1:
        ax[index].legend()


composition_path = "C:/Users/Scott/Desktop/3_26_2021/summary"
density_path = composition_path + "/specific_buoyancy"
element_1 = "MgO"
element_2 = "FeO"

fig_bsp, axs_bsp = plt.subplots(2, 2, figsize=(16, 9), facecolor='w', edgecolor='k')
fig_morb, axs_morb = plt.subplots(2, 2, figsize=(16, 9), facecolor='w', edgecolor='k')

c_bsp = get_composition_file(path_to_folder=composition_path, material="bsp", F_temperature="")
for index, r in enumerate(runs):
    bsp_temp, morb_f_temp, morb_temp = r[0], r[1], r[2]
    c_morb = get_composition_file(path_to_folder=composition_path, material="morb", F_temperature=morb_f_temp)
    d = get_density_file(path_to_folder=density_path, bsp_temperature=bsp_temp,
                         morb_F_temperature=morb_f_temp, morb_temperature=morb_temp)
    data_bsp = get_data(element_1=element_1, element_2=element_2, composition=c_bsp, density=d)
    data_morb = get_data(element_1=element_1, element_2=element_2, composition=c_morb, density=d)
    plot(data=data_bsp, bsp_temp=bsp_temp, morb_f_temp=morb_f_temp, morb_temp=morb_temp,
         element_1=element_1, element_2=element_2, compostion_relative_to="BSP", fig=fig_bsp, ax=axs_bsp, index=index)
    plot(data=data_morb, bsp_temp=bsp_temp, morb_f_temp=morb_f_temp, morb_temp=morb_temp,
         element_1=element_1, element_2=element_2, compostion_relative_to="MORB", fig=fig_morb, ax=axs_morb,
         index=index)

plt.show()
