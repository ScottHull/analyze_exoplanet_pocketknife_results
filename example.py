from composition import Inspect as InspectComposition
from buoyancy import Inspect as InspectBuoyancy
from sort import Sort, Organize
from plots import Plots
import matplotlib.pyplot as plt

"""
Step 1: Calculate compositions (oxide wt%) and buoyancy forces.
"""

# read in compositions
compositions = InspectComposition(path="exoplanets/Depleted_Lithosphere_Compositions")
# read in densities and compositions
buoyancies = InspectBuoyancy(reg_path="exoplanets/Densities/BSP_MORB",
                             depleted_path="/Users/scotthull/Desktop/exoplanets/Densities/Depleted_Lithosphere")

"""
Step 2: Collect and organize buoyancy forces.
"""

b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)
print(b.keys())

"""
Step 2: Collect and organize compositional depletion (oxide weight percent).
        The formula for depletion is:
        [(daughter_reservoir - parent_reservoir) / parent_reservoir] * 100
"""

d = Organize.get_all_depletions(compositions=compositions)
print(d.keys())

"""
Step 3: Plot Results
"""

# define the two available oxides that I want to plot
oxide_x = "SiO2"
oxide_y = "FeO"

# Produces a graph of depletion percent vs. buoyancy force
ax1 = Plots.plot_percent_depletion_vs_buoyancy_force(
    oxide=oxide_x,
    buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depletions={**d['adibekyan_f1400_depletion'], **d['kepler_f1400_depletion']},
    title="Undepleted BSP w/ MORB F1400K (T_0=1200K)"
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force
ax2 = Plots.plot_two_compositions_and_colormap_buoyancy(
    oxide_x="SiO2",
    oxide_y='FeO',
    buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depletions={**d['adibekyan_f1400_depletion'], **d['kepler_f1400_depletion']},
    title="Undepleted BSP w/ MORB F1400K (T_0=1200K)"
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force relative to the
# Earth value in the dataset
ax3 = Plots.plot_two_compositions_and_colormap_buoyancy_relative_to_earth(
    oxide_x="SiO2",
    oxide_y='FeO',
    buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depletions={**d['adibekyan_f1400_depletion'], **d['kepler_f1400_depletion']},
    title="Undepleted BSP w/ MORB F1400K (T_0=1200K) (Relative to Earth Model in This Dataset)"
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force difference between the
# depleted and undepleted BSP compositions
ax4 = Plots.plot_two_compositions_and_colormap_depleted_buoyancy_difference(
    oxide_x="SiO2",
    oxide_y='FeO',
    undepleted_buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depleted_buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
    depletions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
    title="Undepleted vs. Depleted BSP w/ MORB F1400K (T_0=1200K)"
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force difference between the
# depleted and undepleted BSP compositions relative to the Earth value in the dataset
ax5 = Plots.plot_two_compositions_and_colormap_depleted_buoyancy_difference_relative_to_earth(
    oxide_x="SiO2",
    oxide_y='FeO',
    undepleted_buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depleted_buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
    depletions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
    title="Undepleted vs. Depleted BSP w/ MORB F1400K (T_0=1200K) (Relative to Earth Model in This Dataset)"
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force difference between the
# depleted and undepleted BSP compositions where outliers outside the 25th and 75th percentile are removed
ax6 = Plots.plot_two_compositions_and_colormap_depleted_buoyancy_difference(
    oxide_x="SiO2",
    oxide_y='FeO',
    undepleted_buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depleted_buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
    depletions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
    title="Undepleted vs. Depleted BSP w/ MORB F1400K (T_0=1200K) (Outliers Removed)",
    remove_outliers=True
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force difference percentages
# between the depleted and undepleted BSP compositions where outliers outside the 25th and 75th percentile are removed
ax7 = Plots.plot_two_compositions_and_colormap_depleted_buoyancy_difference(
    oxide_x="SiO2",
    oxide_y='FeO',
    undepleted_buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depleted_buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
    depletions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
    title="Undepleted vs. Depleted BSP w/ MORB F1400K (T_0=1200K) (Outliers Removed)",
    remove_outliers=True,
    percentages=True
)

plt.show()
