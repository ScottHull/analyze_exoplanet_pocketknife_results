from src.mineralogy import Mineralogy
from src.composition import Inspect as InspectComposition
from src.buoyancy import Inspect as InspectBuoyancy, DEPTHS
from src.plots import Plots
from src.sort import Organize, Sort
import matplotlib.pyplot as plt

# # read in compositions
# compositions = InspectComposition()
# c = compositions.get_composition(df=compositions.kepler_morb_f1400)
#
# # read in densities and compositions
# buoyancies = InspectBuoyancy()
# b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)
# crossovers = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=b['kepler_f1600_1600_buoyancies'])
#
# # get all appearance/disappearance temperatures
# m = Mineralogy()
# all_appearance_and_disappearance_temperatures = m.get_appearance_and_disappearance_temperatures()
# all_minerals_found = m.get_all_unique_minerals_found()
# print(all_minerals_found)
#
# ax = Plots.plot_relative_cation_to_phase_appearance_at_map_crossover_depth(
#     appearances=all_appearance_and_disappearance_temperatures['kepler_morb_f1600'],
#     composition=c, crossover=crossovers,
#     target_cation="Si", normalizing_cation="Fe",
#     target_phase="clinopyroxene_0")
#
# plt.show()
compositions = InspectComposition()
buoyancies = InspectBuoyancy()
test = [
    ("kepler_f1400_1200_buoyancies", "kepler_morb_f1400", compositions.kepler_morb_f1400),
    ("kepler_f1400_1400_buoyancies", "kepler_morb_f1400", compositions.kepler_morb_f1400),
    ("kepler_f1600_1200_buoyancies", "kepler_morb_f1600", compositions.kepler_morb_f1600),
    ("kepler_f1600_1400_buoyancies", "kepler_morb_f1600", compositions.kepler_morb_f1600),
    ("kepler_f1600_1600_buoyancies", "kepler_morb_f1600", compositions.kepler_morb_f1600),
]

axs = []

for i in test:
    c = compositions.get_composition(df=i[2])

    b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)
    crossovers = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=b[i[0]])

    # get all appearance/disappearance temperatures
    m = Mineralogy()
    all_appearance_and_disappearance_temperatures = m.get_appearance_and_disappearance_temperatures()
    all_minerals_found = m.get_all_unique_minerals_found()
    print(all_minerals_found)

    ax = Plots.plot_relative_cation_to_phase_appearance_at_map_crossover_depth(
        appearances=all_appearance_and_disappearance_temperatures[i[1]],
        composition=c, crossover=crossovers,
        target_cation="Si", normalizing_cation="Fe",
        target_phase="clinopyroxene_0",
        title=i[0]
    )

    axs.append(ax)

plt.show()
