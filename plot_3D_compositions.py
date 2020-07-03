from plots import Plots3D
from buoyancy import Inspect as InspectBuoyancy
from composition import Inspect as InspectComposition
from buoyancy import DEPTHS
from sort import Sort, Organize
import matplotlib.pyplot as plt

compositions = InspectComposition(path="exoplanets/Depleted_Lithosphere_Compositions")
# read in densities and compositions
buoyancies = InspectBuoyancy(reg_path="exoplanets/Densities/BSP_MORB",
                             depleted_path="exoplanets/Densities/Depleted_Lithosphere")

b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)
d = Organize.get_all_depletions(compositions=compositions)

# p = Plots3D.plot_three_oxides_and_colormap_buoyancy(compositions={**d['adibekyan_depleted_f1400_depletion'],
#                                                                   **d['kepler_depleted_f1400_depletion']},
#                                                     buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
#                                                                 **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
#                                                     oxide_x="SiO2", oxide_y="MgO", oxide_z="FeO", title="3D Test",
#                                                     clean=True)

p = Plots3D.plot_three_oxides_and_colormap_crossover_depth(compositions={**d['adibekyan_depleted_f1400_depletion'],
                                                                  **d['kepler_depleted_f1400_depletion']},
                                                    buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                                                                **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
                                                    oxide_x="SiO2", oxide_y="MgO", oxide_z="FeO", title="3D Test",
                                                    clean=True)

plt.show()
