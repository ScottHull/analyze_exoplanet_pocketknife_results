from src.mineralogy import Mineralogy
from src.composition import Inspect as InspectComposition
from src.plots import Plots
import matplotlib.pyplot as plt

star = '2M18495813+4358487'
oxide = 'SiO2'
fraction = True
focus = "kepler_bsp"
keywords = ["Kepler", "BSP"]
appearance_or_disappearance = 'appearance'

c = InspectComposition()
m = Mineralogy()
all_appearance_and_disappearance_temperatures = m.get_appearance_and_disappearance_temperatures()

profiles = m.get_composition_at_appearance_or_disappearance(compositions=c,
                                                            appearance_and_disappearance_temperatures=
                                                            all_appearance_and_disappearance_temperatures[focus],
                                                            name_keywords=keywords,
                                                            appearance_or_disappearance=appearance_or_disappearance,
                                                            fraction=fraction)

ax = Plots.plot_appearance_or_disappearance_temperatures_against_composition(
    appearance_or_disappearance_temperatures=all_appearance_and_disappearance_temperatures[focus],
    compositions_at_temperature=profiles, oxide=oxide,
    appearance_or_disappearance=appearance_or_disappearance,
    fraction=fraction
)

plt.show()
