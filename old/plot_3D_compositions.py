from src.plots import Plots3D
from src.buoyancy import Inspect as InspectBuoyancy
from src.composition import Inspect as InspectComposition
from src.sort import Organize
import matplotlib.pyplot as plt

compositions = InspectComposition()
# read in densities and compositions
buoyancies = InspectBuoyancy(get_actual_mass_fractions=True)

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
                                                           buoyancies={**b[
                                                               'adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                                                                       **b[
                                                                           'kepler_depleted_f1400_1400_morb_1200_buoyancies']},
                                                           oxide_x="SiO2", oxide_y="MgO", oxide_z="FeO",
                                                           title="3D Test",
                                                           clean=True)

plt.show()
