import pandas as pd
import matplotlib.pyplot as plt

run = "adibekyan"
material = 'morb'
# selected_phases = ['cpx', 'opx']
# selected_phases = ['ol', 'wa', 'ri', 'pv', 'ppv']
selected_phases = ['qtz', 'coes', 'gt']
temperatures = [1200, 1400, 1600]
morb_f_temperature = 1400

fig, axs = plt.subplots(2, 2, figsize=(16, 9), facecolor='w', edgecolor='k')

for index, temperature in enumerate(temperatures):
    ax = axs.ravel()
    if material == 'bsp':
        path_fort58 = "C:/Users/Scott/Desktop/3_26_2021/adibekyan/hefesto_output_files/csv/{}/{}/fort.58/Sun.csv".format(
            material, temperature)
        path_fort66 = "C:/Users/Scott/Desktop/3_26_2021/adibekyan/hefesto_output_files/csv/{}/{}/fort.66/Sun.csv".format(
            material, temperature)
    else:
        path_fort58 = "C:/Users/Scott/Desktop/3_26_2021/adibekyan/hefesto_output_files/csv/{}/f{}/{}/fort.58/Sun.csv".format(
            material, morb_f_temperature, temperature)
        path_fort66 = "C:/Users/Scott/Desktop/3_26_2021/adibekyan/hefesto_output_files/csv/{}/f{}/{}/fort.66/Sun.csv".format(
            material, morb_f_temperature, temperature)

    df_fort58 = pd.read_csv(path_fort58)
    df_fort66 = pd.read_csv(path_fort66)

    phases = df_fort66.keys().tolist()[3:]

    for p in selected_phases:
        ax[index].plot(
            df_fort66['depth'],
            df_fort66[p],
            linewidth=2.0,
            label=p
        )
    # ax.invert_yaxis()
    # ax.invert_xaxis()
    ax[index].grid()
    ax[index].set_title("{}: {} K".format(material.upper(), temperature))
    if index == len(temperatures) - 1:
        ax[index].legend()

fig.supxlabel("Depth (km)")
fig.supylabel("Phase Fraction")
if material == 'bsp':
    fig.suptitle("Sun")
else:
    fig.suptitle("Sun (MORB @ F{})".format(morb_f_temperature))

plt.show()
