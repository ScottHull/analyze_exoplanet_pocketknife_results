from src.mineralogy import Mineralogy
from src.composition import Inspect as InspectComposition
from src.buoyancy import Inspect as InspectBuoyancy, DEPTHS
from src.plots import Plots
from src.sort import Organize, Sort, Clean
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size': 14})

compositions = InspectComposition()
buoyancies = InspectBuoyancy()
b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)

oxide_x = 'MgO'
oxide_y = "FeO"
clean = True
crossover = True

bsp_compositions = {**compositions.get_composition(df=compositions.kepler_bsp),
                    **compositions.get_composition(df=compositions.adibekyan_bsp)}
f1400_compositions = {**compositions.get_composition(df=compositions.kepler_morb_f1400),
                      **compositions.get_composition(df=compositions.adibekyan_morb_f1400)}
f1600_compositions = {**compositions.get_composition(df=compositions.kepler_morb_f1600),
                      **compositions.get_composition(df=compositions.adibekyan_morb_f1600)}

if clean:
    bsp_compositions = Clean.remove_outliers_from_composition_dict(data=bsp_compositions, oxide=oxide_x.lower())
    f1400_compositions = Clean.remove_outliers_from_composition_dict(data=f1400_compositions, oxide=oxide_y.lower())
    f1600_compositions = Clean.remove_outliers_from_composition_dict(data=f1600_compositions, oxide=oxide_y.lower())

f1400_1200_buoyancies = {**b["kepler_f1400_1200_buoyancies"], **b["adibekyan_f1400_1200_buoyancies"]}
f1400_1400_buoyancies = {**b["kepler_f1400_1400_buoyancies"], **b["adibekyan_f1400_1400_buoyancies"]}
f1600_1200_buoyancies = {**b["kepler_f1600_1200_buoyancies"], **b["adibekyan_f1600_1200_buoyancies"]}
f1600_1400_buoyancies = {**b["kepler_f1600_1400_buoyancies"], **b["adibekyan_f1600_1400_buoyancies"]}
f1600_1600_buoyancies = {**b["kepler_f1600_1600_buoyancies"], **b["adibekyan_f1600_1600_buoyancies"]}

if crossover:
    f1400_1200_buoyancies = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=f1400_1200_buoyancies)
    f1400_1400_buoyancies = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=f1400_1400_buoyancies)
    f1600_1200_buoyancies = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=f1600_1200_buoyancies)
    f1600_1400_buoyancies = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=f1600_1400_buoyancies)
    f1600_1600_buoyancies = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=f1600_1600_buoyancies)

f1400_1200 = [bsp_compositions, f1400_compositions, f1400_1200_buoyancies, "F1400_1200"]
f1400_1400 = [bsp_compositions, f1400_compositions, f1400_1400_buoyancies, "F1400_1400"]
f1600_1200 = [bsp_compositions, f1600_compositions, f1600_1200_buoyancies, "F1600_1200"]
f1600_1400 = [bsp_compositions, f1600_compositions, f1600_1400_buoyancies, "F1600_1400"]
f1600_1600 = [bsp_compositions, f1600_compositions, f1600_1600_buoyancies, "F1600_1600"]

all_runs = [f1400_1200, f1400_1400, f1600_1200, f1600_1400, f1600_1600]

for i in all_runs:
    ax = plt.figure().add_subplot(111)
    x = []
    y = []
    c = []
    earth = ()
    for j in i[0].keys():
        if j in i[1].keys() and j in i[2].keys():
            x.append(i[1][j][oxide_x.lower()])
            y.append(i[1][j][oxide_y.lower()])
            if not crossover:
                c.append(i[2][j][-1])
            else:
                c.append(-1 * i[2][j])
        if j.lower() == "sun":
            earth = (i[1][j][oxide_x.lower()], i[1][j][oxide_y.lower()], i[2][j])
    sc = ax.scatter(x, y, c=c, marker="+")
    ax.scatter(earth[0], earth[1], c="red", marker="x", s=40, label="Sun")
    ax.set_xlabel(oxide_x + " wt%" + " (MORB)")
    ax.set_ylabel(oxide_y + " wt%" + " (MORB)")
    if not clean:
        ax.set_title(i[3])
    else:
        ax.set_title(i[3] + " (outliers removed outside 25th & 75th percentile)")
    ax.grid()
    cbar = plt.colorbar(sc, ax=ax)
    if not crossover:
        cbar.set_label('Net Buoyancy Force (N)')
    else:
        cbar.set_label('Positive to Negative Buoyancy Crossover Depth (km)')
    ax.legend()

plt.show()
