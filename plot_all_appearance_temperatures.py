from src.mineralogy import Mineralogy
from src.composition import Inspect as InspectComposition
from src.plots import Plots
import matplotlib.pyplot as plt

oxide = 'SiO2'
fraction = True
appearance_or_disappearance = 'appearance'

focus_keywords = ["BSP", ""]
focus = "{}{}".format(focus_keywords[0].lower(), focus_keywords[1].lower())
kepler_focus = "kepler_{}".format(focus)
kepler_keywords = ["Kepler"] + focus_keywords
adibekyan_focus = "adibekyan_{}".format(focus)
adibekyan_keywords = ["Adibekyan"] + focus_keywords

c = InspectComposition()
m = Mineralogy()
all_appearance_and_disappearance_temperatures = m.get_appearance_and_disappearance_temperatures()

adibekyan_profiles = m.get_composition_at_appearance_or_disappearance(compositions=c,
                                                            appearance_and_disappearance_temperatures=
                                                            all_appearance_and_disappearance_temperatures[adibekyan_focus],
                                                            name_keywords=adibekyan_keywords,
                                                            appearance_or_disappearance=appearance_or_disappearance,
                                                            fraction=fraction)
kepler_profiles = m.get_composition_at_appearance_or_disappearance(compositions=c,
                                                            appearance_and_disappearance_temperatures=
                                                            all_appearance_and_disappearance_temperatures[kepler_focus],
                                                            name_keywords=kepler_keywords,
                                                            appearance_or_disappearance=appearance_or_disappearance,
                                                            fraction=fraction)

ax = Plots.plot_appearance_or_disappearance_temperatures_against_composition(
    appearance_or_disappearance_temperatures={**all_appearance_and_disappearance_temperatures[adibekyan_focus],
                                              **all_appearance_and_disappearance_temperatures[kepler_focus]},
    compositions_at_temperature={**adibekyan_profiles, **kepler_profiles}, oxide=oxide,
    appearance_or_disappearance=appearance_or_disappearance,
    fraction=fraction,
    title="Adibekyan + Kepler {} {}".format(focus_keywords[0].upper(), focus_keywords[1].upper())
)

plt.show()
