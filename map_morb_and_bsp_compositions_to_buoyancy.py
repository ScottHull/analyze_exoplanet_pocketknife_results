from src.mineralogy import Mineralogy
from src.composition import Inspect as InspectComposition
from src.buoyancy import Inspect as InspectBuoyancy, DEPTHS
from src.plots import Plots
from src.sort import Organize, Sort
import matplotlib.pyplot as plt

compositions = InspectComposition()
buoyancies = InspectBuoyancy()

oxide = 'SiO2'

kepler = [
    ("kepler_bsp_buoyancies", "kepler_bsp", compositions.kepler_bsp, 1400 - 273.15),
    ("kepler_f1400_1200_buoyancies", "kepler_morb_f1400", compositions.kepler_morb_f1400, 1400 - 273.15),
    ("kepler_f1400_1400_buoyancies", "kepler_morb_f1400", compositions.kepler_morb_f1400, 1400 - 273.15),
    ("kepler_f1600_1200_buoyancies", "kepler_morb_f1600", compositions.kepler_morb_f1600, 1600 - 273.15),
    ("kepler_f1600_1400_buoyancies", "kepler_morb_f1600", compositions.kepler_morb_f1600, 1600 - 273.15),
    ("kepler_f1600_1600_buoyancies", "kepler_morb_f1600", compositions.kepler_morb_f1600, 1600 - 273.15),
]

adibekyan = [
    ("adibekyan_bsp_buoyancies", "adibekyan_bsp", compositions.adibekyan_bsp, 1400 - 273.15),
    ("adibekyan_f1400_1200_buoyancies", "adibekyan_morb_f1400", compositions.adibekyan_morb_f1400, 1400 - 273.15),
    ("adibekyan_f1400_1400_buoyancies", "adibekyan_morb_f1400", compositions.adibekyan_morb_f1400, 1400 - 273.15),
    ("adibekyan_f1600_1200_buoyancies", "adibekyan_morb_f1600", compositions.adibekyan_morb_f1600, 1600 - 273.15),
    ("adibekyan_f1600_1400_buoyancies", "adibekyan_morb_f1600", compositions.adibekyan_morb_f1600, 1600 - 273.15),
    ("adibekyan_f1600_1600_buoyancies", "adibekyan_morb_f1600", compositions.adibekyan_morb_f1600, 1600 - 273.15),
]

bsp_compositions = {**kepler[0], **adibekyan[0]}
f1400_compositions = {**compositions.kepler_morb_f1400, **compositions.adibekyan_morb_f1400}
f1600_compositions = {**compositions.kepler_morb_f1600, **compositions.adibekyan_morb_f1600}
f1400_1200_buoyancies = {**buoyancies.get}

