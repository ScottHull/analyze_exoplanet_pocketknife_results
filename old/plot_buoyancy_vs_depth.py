from src.plots import Plots
from src.buoyancy import Inspect as InspectBuoyancy
from src.buoyancy import DEPTHS
from src.sort import Organize
import matplotlib.pyplot as plt

buoyancies = InspectBuoyancy()
b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)

p = Plots.plot_buoyancy_force_as_function_of_depth(depth=DEPTHS,
                                                   buoyancies={
                                                       **b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                                                       **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
                                                   title="depleted_f1400_1400_morb_1200_buoyancies")

plt.show()
