from src.mineralogy import Mineralogy
from src.composition import Inspect as InspectComposition
from src.buoyancy import Inspect as InspectBuoyancy, DEPTHS
from src.plots import Plots
from src.sort import Organize, Sort
import matplotlib.pyplot as plt

# read in compositions
compositions = InspectComposition()
c = compositions.get_composition(df=compositions.kepler_bsp)

# read in densities and compositions
buoyancies = InspectBuoyancy()
b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)
crossovers = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=b['kepler_f1400_1200_buoyancies'])

# get all appearance/disappearance temperatures
m = Mineralogy()
all_appearance_and_disappearance_temperatures = m.get_appearance_and_disappearance_temperatures()
all_minerals_found = m.get_all_unique_minerals_found()
print(all_minerals_found)

ax = Plots.plot_relative_cation_to_phase_appearance_at_map_crossover_depth(
    appearances=all_appearance_and_disappearance_temperatures['kepler_bsp'],
    composition=c, crossover=crossovers,
    target_cation="Si", normalizing_cation="Mg",
    target_phase="clinopyroxene_0")

plt.show()