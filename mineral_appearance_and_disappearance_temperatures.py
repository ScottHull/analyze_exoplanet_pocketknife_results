from src.mineralogy import Mineralogy
from src.composition import Inspect as InspectComposition
from src.plots import Plots
import matplotlib.pyplot as plt

star = '2M18495813+4358487'
oxide = 'SiO2'

# compositions = InspectComposition(path="exoplanets/Depleted_Lithosphere_Compositions")
# c = Organize.get_all_compositions(compositions=compositions)
c_star = InspectComposition().get_liquid_compositional_profile_of_star(star=star,
                                                                                                  name_keywords=[
                                                                                                      "Kepler", "BSP"])
c_star_massfrac = InspectComposition().get_liquid_compositional_mass_fraction_profile_of_star(
    star=star,
    name_keywords=[
        "Kepler", "BSP"])

m = Mineralogy()
all_appearance_and_disappearance_temperatures = m.get_appearance_and_disappearance_temperatures()
all_minerals_found = m.get_all_unique_minerals_found()
# print(all_minerals_found)
# print(all_appearance_and_disappearance_temperatures['kepler_bsp'][star])

p = Plots.plot_compositional_profile_and_disappearances(profile=c_star, mineral_temps=
all_appearance_and_disappearance_temperatures['kepler_bsp'][star], title=star)
p_massfrac = Plots.plot_compositional_mass_fraction_profile_and_disappearances(profile=c_star_massfrac, mineral_temps=
all_appearance_and_disappearance_temperatures['kepler_bsp'][star], title=star)

plt.show()
