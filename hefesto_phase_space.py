import pandas as pd
import matplotlib.pyplot as plt

path_fort58 = "/Users/scotthull/Desktop/Sun_fort58.csv"
path_fort66 = "/Users/scotthull/Desktop/Sun_fort66.csv"

df_fort58 = pd.read_csv(path_fort58)
df_fort66 = pd.read_csv(path_fort66)

phases = df_fort66.keys().tolist()[3:]
selected_phases = ['gt', 'qtz', 'coes']

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
ax.set_xlabel("Depth (km)")
ax.set_ylabel("Phase Fraction")
for p in selected_phases:
    ax.plot(
        df_fort66['depth'],
        df_fort66[p],
        linewidth=2.0,
        label=p
    )
# ax.invert_yaxis()
# ax.invert_xaxis()
ax.grid()
ax.legend()

plt.show()