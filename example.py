from composition import Inspect as InspectComposition
from buoyancy import Inspect as InspectBuoyancy
from buoyancy import DEPTHS
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
                             depleted_path="exoplanets/Densities/Depleted_Lithosphere")

"""
Step 2: Collect and organize buoyancy forces.
"""

b = Organize.get_all_buoyancy_forces(buoyancies=buoyancies)
print(b.keys())  # shows the different dictionary keys available for use in the buoyancy return

"""
Step 2: Collect and organize compositional depletion (oxide weight percent).
        The formula for depletion is:
        [(daughter_reservoir - parent_reservoir) / parent_reservoir] * 100
"""

d = Organize.get_all_depletions(compositions=compositions)
print(d.keys())  # shows the different dictionary keys available for use in the compositional depletion percent return

"""
Step 3: Plot Example Results.
"""

# define the two available oxides that I want to plot
oxide_x = "SiO2"
oxide_y = "FeO"

# Produces a graph of depletion percent vs. buoyancy force
ax1 = Plots.plot_percent_depletion_vs_buoyancy_force(
    oxide=oxide_x,  # x-axis oxide
    buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},  # combine the Adibekyan and Kepler data
    depletions={**d['adibekyan_f1400_depletion'], **d['kepler_f1400_depletion']},  # combine the Adibekyan and Kepler data
    title="Example 1: Undepleted BSP w/ MORB F1400K (T_0=1200K)"  # title of the figure
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force
ax2 = Plots.plot_two_compositions_and_colormap_buoyancy(
    oxide_x=oxide_x,  # x-axis oxide
    oxide_y=oxide_y,  # y-axis oxide
    buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depletions={**d['adibekyan_f1400_depletion'], **d['kepler_f1400_depletion']},
    title="Example 2: Undepleted BSP w/ MORB F1400K (T_0=1200K)"
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force relative to the
# Earth value in the dataset
ax3 = Plots.plot_two_compositions_and_colormap_buoyancy_relative_to_earth(
    oxide_x=oxide_x,
    oxide_y=oxide_y,
    buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depletions={**d['adibekyan_f1400_depletion'], **d['kepler_f1400_depletion']},
    title="Example 3: Undepleted BSP w/ MORB F1400K (T_0=1200K) (Relative to Earth Model in This Dataset)"
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force difference between the
# depleted and undepleted BSP compositions
ax4 = Plots.plot_two_compositions_and_colormap_depleted_buoyancy_difference(
    oxide_x=oxide_x,
    oxide_y=oxide_y,
    undepleted_buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depleted_buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
    depletions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
    title="Example 4: Undepleted vs. Depleted BSP w/ MORB F1400K (T_0=1200K)"
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force difference between the
# depleted and undepleted BSP compositions relative to the Earth value in the dataset
ax5 = Plots.plot_two_compositions_and_colormap_depleted_buoyancy_difference_relative_to_earth(
    oxide_x=oxide_x,
    oxide_y=oxide_y,
    undepleted_buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depleted_buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
    depletions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
    title="Example 5: Undepleted vs. Depleted BSP w/ MORB F1400K (T_0=1200K) (Relative to Earth Model in This Dataset)"
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force difference between the
# depleted and undepleted BSP compositions where outliers outside the 25th and 75th percentile are removed
# This is the same figure as ax4 but with an additional argument in the function below.
ax6 = Plots.plot_two_compositions_and_colormap_depleted_buoyancy_difference(
    oxide_x=oxide_x,
    oxide_y=oxide_y,
    undepleted_buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depleted_buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
    depletions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
    title="Example 6: Undepleted vs. Depleted BSP w/ MORB F1400K (T_0=1200K) (Outliers Removed)",
    remove_outliers=True  # removes compositional outliers outside of the 25th and 75th percentile
)

# Produces a graph where two depletion percentages are plotted and colormapped to buoyancy force difference percentages
# between the depleted and undepleted BSP compositions where outliers outside the 25th and 75th percentile are removed
# This is the same figure as ax4 but with 2 additional arguments in the function below.
# Percent difference is defined as (depleted - undepleted) / undepleted * 100
# i.e. a positive percentage means the depleted BSP is more buoyant than the undepleted BSP
ax7 = Plots.plot_two_compositions_and_colormap_depleted_buoyancy_difference(
    oxide_x=oxide_x,
    oxide_y=oxide_y,
    undepleted_buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
    depleted_buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
    depletions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
    title="Example 7: Undepleted vs. Depleted BSP w/ MORB F1400K (T_0=1200K) (Outliers Removed)",
    remove_outliers=True,
    percentages=True  # returns the percent difference in buoyancy force between the depleted and undepleted BSP
)

ax8 = Plots.plot_buoyancy_force_as_function_of_depth(depth=DEPTHS,
                                                   buoyancies={**b['adibekyan_depleted_f1400_1400_morb_1200_buoyancies'],
                         **b['kepler_depleted_f1400_1400_morb_1200_buoyancies']},
                                                   title="Example 8: Net Buoyancy Force as a Function of Depth (MORB F1400K (T_0=1200K)")

ax9 = Plots.plot_crossover_depths(buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
                                compositions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
                                oxide=oxide_x, title="Example 9: BSP Oxide Depletion % vs. Positive-to-Negative-Buoyancy Crossover Depth (MORB F1400K (T_0=1200K)")

ax10 = Plots.plot_two_oxides_against_crossover_depth(buoyancies={**b['adibekyan_f1400_1200_buoyancies'], **b['kepler_f1400_1200_buoyancies']},
                                compositions={**d['adibekyan_depleted_f1400_depletion'], **d['kepler_depleted_f1400_depletion']},
                                oxide_x=oxide_x, oxide_y=oxide_y,
                                                     title="Example 10: BSP Oxide-Oxide Depletion % With Colormapped Crossover Depth (MORB F1400K (T_0=1200K)")

plt.show()
