import os
import pandas as pd
from src.atomic import _AtomicWeights, _OxideWeights

morb_f_temperatures = [
    1400,
    1600
]

run_name = "adibekyan"
base_path = "C:/Users/Scott/Desktop/3_26_2021/summary/"
bsp_composition_file = base_path + "{}_BSP_Compositions.csv".format(run_name)
morb_file_template = base_path + "{}_f{}_MORB_Compositions.csv"
morb_mgo_correction = 0.646022142

bsp_chem_df = pd.read_csv(bsp_composition_file, index_col="Star")
bsp_oxides = list(bsp_chem_df.keys())
for ftemp in morb_f_temperatures:
    depleted_bsp_fname = "{}_Depleted_BSP_f{}.csv".format(run_name, ftemp)
    if depleted_bsp_fname in os.listdir(base_path[:-1]):
        os.remove(base_path + depleted_bsp_fname)
    depleted_bsp_outfile = open(base_path + depleted_bsp_fname, 'w')
    header = "Star," + ",".join(str(i) for i in bsp_oxides) + "\n"
    depleted_bsp_outfile.write(header)
    morb_fname = morb_file_template.format(run_name, ftemp)
    morb_chem_df = pd.read_csv(morb_fname, index_col="Star")
    for star in bsp_chem_df.index:
        if star in morb_chem_df.index.tolist():
            bsp_oxide_mass = {}
            morb_oxide_wt_pct_no_mgo_corr = {}
            morb_oxide_mass = {}
            depleted_oxide_mass = {}
            depleted_bsp_oxide_wt_pct = {}
            for o in bsp_oxides:
                if o != "MgO":
                    morb_oxide_wt_pct_no_mgo_corr.update({o: morb_chem_df[o][star]})
                else:
                    morb_oxide_wt_pct_no_mgo_corr.update({o: morb_chem_df[o][star] / morb_mgo_correction})
            total = sum(morb_oxide_wt_pct_no_mgo_corr.values())
            for o in bsp_oxides:
                morb_oxide_wt_pct_no_mgo_corr[o] = (morb_oxide_wt_pct_no_mgo_corr[o] / total) * 100
            for o in bsp_oxides:
                bsp_oxide_mass.update({o: bsp_chem_df[o][star]})
                morb_oxide_mass.update(
                    {o: (morb_oxide_wt_pct_no_mgo_corr[o] / 100.0) * morb_chem_df['Mass'][star]})
                depleted_oxide_mass.update({o: bsp_oxide_mass[o] - morb_oxide_mass[o]})
            depleted_sum = sum(depleted_oxide_mass.values())
            for o in bsp_oxides:
                depleted_bsp_oxide_wt_pct.update({o: depleted_oxide_mass[o] / depleted_sum * 100})
            line = ",".join(str(depleted_bsp_oxide_wt_pct[o]) for o in bsp_oxides)
            depleted_bsp_outfile.write(star + "," + line + "\n")
    depleted_bsp_outfile.close()
