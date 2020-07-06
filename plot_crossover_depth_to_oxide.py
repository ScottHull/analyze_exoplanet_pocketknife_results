from src.plots import Plots
from src.sort import Organize
from src.buoyancy import Inspect as InspectBuoyancy
from src.composition import Inspect as InspectComposition
import matplotlib.pyplot as plt


compositions = InspectComposition(path="exoplanets/Depleted_Lithosphere_Compositions")
# read in densities and compositions
buoyancies = InspectBuoyancy(reg_path="exoplanets/Densities/BSP_MORB",
                             depleted_path="exoplanets/Densities/Depleted_Lithosphere")

b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)
d = Organize.get_all_depletions(compositions=compositions)

# p = Plots.plot_crossover_depths(buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
#                                 compositions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
#                                 oxide="SiO2", title="f1400_1200_buoyancies")
p = Plots.plot_two_oxides_against_crossover_depth(buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
                                compositions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
                                oxide_x="SiO2", oxide_y="FeO", title="f1400_1200_buoyancies")

plt.show()
