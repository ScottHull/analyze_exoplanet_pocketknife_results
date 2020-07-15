from src.mineralogy import Mineralogy
from src.composition import Inspect as InspectComposition
from src.buoyancy import Inspect as InspectBuoyancy, DEPTHS
from src.plots import Plots
from src.sort import Organize, Sort
import matplotlib.pyplot as plt

compositions = InspectComposition()
buoyancies = InspectBuoyancy()
m = Mineralogy()

oxide = 'SiO2'
fraction = True
appearance_or_disappearance = 'appearance'

focus_keywords = ["BSP", ""]
focus = "{}{}".format(focus_keywords[0].lower(), focus_keywords[1].lower())
kepler_focus = "kepler_{}".format(focus)
kepler_keywords = ["Kepler"] + focus_keywords
adibekyan_focus = "adibekyan_{}".format(focus)
adibekyan_keywords = ["Adibekyan"] + focus_keywords

kepler = [
    ("kepler_f1400_1200_buoyancies", "kepler_morb_f1400", compositions.kepler_morb_f1400, 1400 - 273.15),
    ("kepler_f1400_1400_buoyancies", "kepler_morb_f1400", compositions.kepler_morb_f1400, 1400 - 273.15),
    ("kepler_f1600_1200_buoyancies", "kepler_morb_f1600", compositions.kepler_morb_f1600, 1600 - 273.15),
    ("kepler_f1600_1400_buoyancies", "kepler_morb_f1600", compositions.kepler_morb_f1600, 1600 - 273.15),
    ("kepler_f1600_1600_buoyancies", "kepler_morb_f1600", compositions.kepler_morb_f1600, 1600 - 273.15),
]

adibekyan = [
    ("adibekyan_f1400_1200_buoyancies", "adibekyan_morb_f1400", compositions.adibekyan_morb_f1400, 1400 - 273.15),
    ("adibekyan_f1400_1400_buoyancies", "adibekyan_morb_f1400", compositions.adibekyan_morb_f1400, 1400 - 273.15),
    ("adibekyan_f1600_1200_buoyancies", "adibekyan_morb_f1600", compositions.adibekyan_morb_f1600, 1600 - 273.15),
    ("adibekyan_f1600_1400_buoyancies", "adibekyan_morb_f1600", compositions.adibekyan_morb_f1600, 1600 - 273.15),
    ("adibekyan_f1600_1600_buoyancies", "adibekyan_morb_f1600", compositions.adibekyan_morb_f1600, 1600 - 273.15),
]

axs = []

all_appearance_and_disappearance_temperatures = m.get_appearance_and_disappearance_temperatures()

adibekyan_profiles = m.get_composition_at_appearance_or_disappearance(compositions=compositions,
                                                                      appearance_and_disappearance_temperatures=
                                                                      all_appearance_and_disappearance_temperatures[
                                                                          adibekyan_focus],
                                                                      name_keywords=adibekyan_keywords,
                                                                      appearance_or_disappearance=appearance_or_disappearance,
                                                                      fraction=fraction)
kepler_profiles = m.get_composition_at_appearance_or_disappearance(compositions=compositions,
                                                                   appearance_and_disappearance_temperatures=
                                                                   all_appearance_and_disappearance_temperatures[
                                                                       kepler_focus],
                                                                   name_keywords=kepler_keywords,
                                                                   appearance_or_disappearance=appearance_or_disappearance,
                                                                   fraction=fraction)


