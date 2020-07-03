from plots import Plots
from buoyancy import Inspect as InspectBuoyancy
from buoyancy import DEPTHS
from sort import Sort, Organize
import matplotlib.pyplot as plt

buoyancies = InspectBuoyancy(reg_path="exoplanets/Densities/BSP_MORB",
                             depleted_path="exoplanets/Densities/Depleted_Lithosphere")
b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)

p = Plots.plot_buoyancy_force_as_function_of_depth(depth=DEPTHS,
                                                   buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
                                                   title="depleted_f1400_1400_morb_1200_buoyancies")

plt.show()