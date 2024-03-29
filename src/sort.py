import numpy as np
from scipy.stats import iqr
from src.atomic import Convert
from src.thickness import Thickness


class Sort:

    @classmethod
    def pair_composition_to_buoyancy(cls, buoyancy, composition, oxide):
        pairs = []
        for star in buoyancy.keys():
            final_buoyancy = buoyancy[star][-1]
            c = composition[star][oxide.lower()]
            pairs.append((c, final_buoyancy))
        return pairs

    @classmethod
    def pair_compositions_and_map_buoyancy(cls, buoyancy, composition, oxide_x, oxide_y, special_star=None):
        pairs = []
        c_keys = composition.keys()
        if special_star is None:
            for star in buoyancy.keys():
                if star in c_keys:
                    final_buoyancy = buoyancy[star][-1]
                    c_x = composition[star][oxide_x.lower()]
                    c_y = composition[star][oxide_y.lower()]
                    pairs.append((c_x, c_y, final_buoyancy))
        else:
            star = special_star
            final_buoyancy = buoyancy[star][-1]
            c_x = composition[star][oxide_x.lower()]
            c_y = composition[star][oxide_y.lower()]
            pairs.append((c_x, c_y, final_buoyancy))
        return pairs

    @classmethod
    def pair_compositions_and_map_buoyancy_relative_to_earth(cls, buoyancy, composition, oxide_x, oxide_y,
                                                             special_star=None):
        pairs = []
        c_keys = composition.keys()
        earth_buoyancy = buoyancy['Sun'][-1]
        if special_star is None:
            for star in buoyancy.keys():
                if star in c_keys:
                    final_buoyancy = buoyancy[star][-1]
                    buoyancy_relative = None
                    if final_buoyancy > earth_buoyancy:
                        buoyancy_relative = 1  # more buoyant than earth
                    else:
                        buoyancy_relative = 0  # less buoyant than earth
                    c_x = composition[star][oxide_x.lower()]
                    c_y = composition[star][oxide_y.lower()]
                    pairs.append((c_x, c_y, final_buoyancy, buoyancy_relative))
        else:
            star = special_star
            final_buoyancy = buoyancy[star][-1]
            buoyancy_relative = None
            if final_buoyancy > earth_buoyancy:
                buoyancy_relative = 1  # more buoyant than earth
            else:
                buoyancy_relative = 0  # less buoyant than earth
            c_x = composition[star][oxide_x.lower()]
            c_y = composition[star][oxide_y.lower()]
            pairs.append((c_x, c_y, final_buoyancy, buoyancy_relative))
        return pairs

    @classmethod
    def get_crossover_depth(cls, depths, buoyancies):
        cross_depths = {}
        for s in buoyancies.keys():
            b = buoyancies[s]
            for index, i in enumerate(b):
                if i < 0:
                    cross_depths.update({s: depths[index]})
                    break
                elif index == len(buoyancies) - 1:
                    cross_depths.update({s: np.nan})
                    break
        return cross_depths

    @classmethod
    def relate_appearance_temperature_to_composition(cls, star, appearance_temperatures, liquid_compositional_profile,
                                                     appearance_or_disappearance='appearance', fraction=False):
        d = {}
        for phase in appearance_temperatures.keys():
            if phase not in d.keys():
                d.update({phase: {}})
            t = appearance_temperatures[phase][appearance_or_disappearance]
            c_index = liquid_compositional_profile['temperature'].index(t)
            for oxide in liquid_compositional_profile.keys():
                if oxide != "temperature" and oxide != "mass":
                    if not fraction:
                        d[phase].update({oxide: liquid_compositional_profile[oxide][c_index]})
                    else:
                        d[phase].update({oxide: liquid_compositional_profile[oxide][c_index] /
                                                liquid_compositional_profile["mass"][c_index]})
                elif oxide == "mass":
                    d[phase].update({"mass": liquid_compositional_profile[oxide][c_index]})
        return d

    # @classmethod
    # def relate_morb_melt_fraction_and_temperature_bsp_composition_and_phase_appearances(cls, melt_fractions,
    #                                                                                     bsp_compositions, phases,
    #                                                                                     low_t_target_phase,
    #                                                                                     med_t_target_phase,
    #                                                                                     high_t_target_phase,
    #                                                                                     appearance_or_disappearance='appearance',):
    #     for star in melt_fractions.keys():
    #         if star in bsp_compositions.keys():
    #             if star in phases.keys():
    #                 f = melt_fractions[star]
    #                 c = bsp_compositions[star]
    #                 phases_appearances = phases[star][appearance_or_disappearance]


class Organize:

    @classmethod
    def get_all_buoyancy_forces(cls, buoyancies):
        adibekyan_f1400_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1400_1200,
                                                                  morb_name="adibekyan_morb_f1400_1200")
        adibekyan_f1400_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1400_1400,
                                                                  morb_name="adibekyan_morb_f1400_1400")
        adibekyan_f1600_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1600_1200,
                                                                  morb_name="adibekyan_morb_f1400_1400")
        adibekyan_f1600_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1600_1400,
                                                                  morb_name="adibekyan_morb_f1600_1400")
        adibekyan_f1600_1600_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1600_1600,
                                                                  morb_name="adibekyan_morb_f1600_1600")

        kepler_f1400_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1400_1200,
                                                               morb_name="kepler_morb_f1400_1200")
        kepler_f1400_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1400_1400,
                                                               morb_name="kepler_morb_f1400_1400")
        kepler_f1600_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1600_1200,
                                                               morb_name="kepler_morb_f1600_1200")
        kepler_f1600_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1600_1400,
                                                               morb_name="kepler_morb_f1600_1400")
        kepler_f1600_1600_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1600_1600,
                                                               morb_name="kepler_morb_f1600_1600")

        adibekyan_depleted_f1400_1400_morb_1200_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1400_1400,
            morb_file=buoyancies.adibekyan_morb_f1400_1200, morb_name="adibekyan_morb_f1400_1200")
        adibekyan_depleted_f1400_1400_morb_1400_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1400_1400,
            morb_file=buoyancies.adibekyan_morb_f1400_1400, morb_name="adibekyan_morb_f1400_1400")
        adibekyan_depleted_f1600_1600_morb_1200_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1600_1600,
            morb_file=buoyancies.adibekyan_morb_f1600_1200, morb_name="adibekyan_morb_f1600_1200")
        adibekyan_depleted_f1600_1600_morb_1400_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1600_1600,
            morb_file=buoyancies.adibekyan_morb_f1600_1400, morb_name="adibekyan_morb_f1600_1400")
        adibekyan_depleted_f1600_1600_morb_1600_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1600_1600,
            morb_file=buoyancies.adibekyan_morb_f1600_1600, morb_name="adibekyan_morb_f1600_1600")

        kepler_depleted_f1400_1400_morb_1200_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1400_1400,
            morb_file=buoyancies.kepler_morb_f1400_1200, morb_name="kepler_morb_f1400_1200")
        kepler_depleted_f1400_1400_morb_1400_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1400_1400,
            morb_file=buoyancies.kepler_morb_f1400_1400, morb_name="kepler_morb_f1400_1400")
        kepler_depleted_f1600_1600_morb_1200_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1600_1600,
            morb_file=buoyancies.kepler_morb_f1600_1200, morb_name="kepler_morb_f1600_1200")
        kepler_depleted_f1600_1600_morb_1400_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1600_1600,
            morb_file=buoyancies.kepler_morb_f1600_1400, morb_name="kepler_morb_f1600_1400")
        kepler_depleted_f1600_1600_morb_1600_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1600_1600,
            morb_file=buoyancies.kepler_morb_f1600_1600, morb_name="kepler_morb_f1600_1600")

        return {
            'adibekyan_f1400_1200_buoyancies': adibekyan_f1400_1200_buoyancies,
            'adibekyan_f1400_1400_buoyancies': adibekyan_f1400_1400_buoyancies,
            'adibekyan_f1600_1200_buoyancies': adibekyan_f1600_1200_buoyancies,
            'adibekyan_f1600_1400_buoyancies': adibekyan_f1600_1400_buoyancies,
            'adibekyan_f1600_1600_buoyancies': adibekyan_f1600_1600_buoyancies,
            'kepler_f1400_1200_buoyancies': kepler_f1400_1200_buoyancies,
            'kepler_f1400_1400_buoyancies': kepler_f1400_1400_buoyancies,
            'kepler_f1600_1200_buoyancies': kepler_f1600_1200_buoyancies,
            'kepler_f1600_1400_buoyancies': kepler_f1600_1400_buoyancies,
            'kepler_f1600_1600_buoyancies': kepler_f1600_1600_buoyancies,
            'adibekyan_depleted_f1400_1400_morb_1200_buoyancies': adibekyan_depleted_f1400_1400_morb_1200_buoyancies,
            'adibekyan_depleted_f1400_1400_morb_1400_buoyancies': adibekyan_depleted_f1400_1400_morb_1400_buoyancies,
            'adibekyan_depleted_f1600_1600_morb_1200_buoyancies': adibekyan_depleted_f1600_1600_morb_1200_buoyancies,
            'adibekyan_depleted_f1600_1600_morb_1400_buoyancies': adibekyan_depleted_f1600_1600_morb_1400_buoyancies,
            'adibekyan_depleted_f1600_1600_morb_1600_buoyancies': adibekyan_depleted_f1600_1600_morb_1600_buoyancies,
            'kepler_depleted_f1400_1400_morb_1200_buoyancies': kepler_depleted_f1400_1400_morb_1200_buoyancies,
            'kepler_depleted_f1400_1400_morb_1400_buoyancies': kepler_depleted_f1400_1400_morb_1400_buoyancies,
            'kepler_depleted_f1600_1600_morb_1200_buoyancies': kepler_depleted_f1600_1600_morb_1200_buoyancies,
            'kepler_depleted_f1600_1600_morb_1400_buoyancies': kepler_depleted_f1600_1600_morb_1400_buoyancies,
            'kepler_depleted_f1600_1600_morb_1600_buoyancies': kepler_depleted_f1600_1600_morb_1600_buoyancies,
        }

    @classmethod
    def get_all_depletions(cls, compositions):
        adibekyan_f1400_depletion = compositions.get_depletion(parent_reservoir=compositions.adibekyan_bsp,
                                                               daughter_reservoir=compositions.adibekyan_morb_f1400)
        adibekyan_f1600_depletion = compositions.get_depletion(parent_reservoir=compositions.adibekyan_bsp,
                                                               daughter_reservoir=compositions.adibekyan_morb_f1600)

        kepler_f1400_depletion = compositions.get_depletion(parent_reservoir=compositions.kepler_bsp,
                                                            daughter_reservoir=compositions.kepler_morb_f1400)
        kepler_f1600_depletion = compositions.get_depletion(parent_reservoir=compositions.kepler_bsp,
                                                            daughter_reservoir=compositions.kepler_morb_f1600)

        adibekyan_depleted_f1400_depletion = compositions.get_depletion(
            parent_reservoir=compositions.adibekyan_depleted_bsp_f1400,
            daughter_reservoir=compositions.adibekyan_morb_f1400)
        adibekyan_depleted_f1600_depletion = compositions.get_depletion(
            parent_reservoir=compositions.adibekyan_depleted_bsp_f1600,
            daughter_reservoir=compositions.adibekyan_morb_f1600)
        kepler_depleted_f1400_depletion = compositions.get_depletion(
            parent_reservoir=compositions.kepler_depleted_bsp_f1400,
            daughter_reservoir=compositions.kepler_morb_f1400)
        kepler_depleted_f1600_depletion = compositions.get_depletion(
            parent_reservoir=compositions.kepler_depleted_bsp_f1600,
            daughter_reservoir=compositions.kepler_morb_f1600)

        adibekyan_bsp_depletion_f1400 = compositions.get_depletion(
            parent_reservoir=compositions.adibekyan_bsp,
            daughter_reservoir=compositions.adibekyan_depleted_bsp_f1400)
        adibekyan_bsp_depletion_f1600 = compositions.get_depletion(
            parent_reservoir=compositions.adibekyan_bsp,
            daughter_reservoir=compositions.adibekyan_depleted_bsp_f1600)
        kepler_bsp_depletion_f1400 = compositions.get_depletion(
            parent_reservoir=compositions.kepler_bsp,
            daughter_reservoir=compositions.kepler_depleted_bsp_f1400)
        kepler_bsp_depletion_f1600 = compositions.get_depletion(
            parent_reservoir=compositions.kepler_bsp,
            daughter_reservoir=compositions.kepler_depleted_bsp_f1600)

        return {
            'adibekyan_f1400_depletion': adibekyan_f1400_depletion,
            'adibekyan_f1600_depletion': adibekyan_f1600_depletion,
            'kepler_f1400_depletion': kepler_f1400_depletion,
            'kepler_f1600_depletion': kepler_f1600_depletion,
            'adibekyan_depleted_f1400_depletion': adibekyan_depleted_f1400_depletion,
            'adibekyan_depleted_f1600_depletion': adibekyan_depleted_f1600_depletion,
            'kepler_depleted_f1400_depletion': kepler_depleted_f1400_depletion,
            'kepler_depleted_f1600_depletion': kepler_depleted_f1600_depletion,
            'adibekyan_bsp_depletion_f1400': adibekyan_bsp_depletion_f1400,
            'adibekyan_bsp_depletion_f1600': adibekyan_bsp_depletion_f1600,
            'kepler_bsp_depletion_f1400': kepler_bsp_depletion_f1400,
            'kepler_bsp_depletion_f1600': kepler_bsp_depletion_f1600
        }

    @classmethod
    def get_all_compositions(cls, compositions):
        adibekyan_bsp = compositions.get_composition(compositions.adibekyan_bsp)
        adibekyan_morb_f1400 = compositions.get_composition(compositions.adibekyan_morb_f1400)
        adibekyan_morb_f1600 = compositions.get_composition(compositions.adibekyan_morb_f1600)
        adibekyan_depleted_bsp_f1400 = compositions.get_composition(compositions.adibekyan_depleted_bsp_f1400)
        adibekyan_depleted_bsp_f1600 = compositions.get_composition(compositions.adibekyan_depleted_bsp_f1600)
        kepler_bsp = compositions.get_composition(compositions.kepler_bsp)
        kepler_morb_f1400 = compositions.get_composition(compositions.kepler_morb_f1400)
        kepler_morb_f1600 = compositions.get_composition(compositions.kepler_morb_f1600)
        kepler_depleted_bsp_f1400 = compositions.get_composition(compositions.kepler_depleted_bsp_f1400)
        kepler_depleted_bsp_f1600 = compositions.get_composition(compositions.kepler_depleted_bsp_f1600)

        return {
            "adibekyan_bsp": adibekyan_bsp,
            "adibekyan_morb_f1400": adibekyan_morb_f1400,
            "adibekyan_morb_f1600": adibekyan_morb_f1600,
            "adibekyan_depleted_bsp_f1400": adibekyan_depleted_bsp_f1400,
            "adibekyan_depleted_bsp_f1600": adibekyan_depleted_bsp_f1600,
            "kepler_bsp": kepler_bsp,
            "kepler_morb_f1400": kepler_morb_f1400,
            "kepler_morb_f1600": kepler_morb_f1600,
            "kepler_depleted_bsp_f1400": kepler_depleted_bsp_f1400,
            "kepler_depleted_bsp_f1600": kepler_depleted_bsp_f1600
        }

    @classmethod
    def get_buoyancy_differences(cls, parent_reservoir, daughter_reservoir):
        buoyancy_differences = {}
        daughter_stars = daughter_reservoir.keys()
        for parent_star in parent_reservoir:
            parent_buoyancy = parent_reservoir[parent_star]
            if parent_star in daughter_stars:
                daughter_buoyancy = daughter_reservoir[parent_star]
                buoyancy_differences.update({parent_star: [x - y for x, y in zip(daughter_buoyancy, parent_buoyancy)]})
        return buoyancy_differences

    @classmethod
    def get_buoyancy_difference_percentages(cls, parent_reservoir, daughter_reservoir):
        buoyancy_differences = {}
        daughter_stars = daughter_reservoir.keys()
        for parent_star in parent_reservoir:
            parent_buoyancy = parent_reservoir[parent_star]
            if parent_star in daughter_stars:
                daughter_buoyancy = daughter_reservoir[parent_star]
                buoyancy_differences.update(
                    {parent_star: [((x - y) / y) * 100.0 for x, y in zip(daughter_buoyancy, parent_buoyancy)]})
        return buoyancy_differences

    @classmethod
    def pair_crossover_depth_to_oxide(cls, crossover_depths, compositions, oxide):
        pairs = {}
        for s in crossover_depths.keys():
            if s in compositions.keys():
                c = crossover_depths[s]
                o = compositions[s][oxide]
                pairs.update({s: [c, o]})
        return pairs

    @classmethod
    def pair_crossover_depth_to_two_oxides(cls, crossover_depths, compositions, oxide_x, oxide_y):
        pairs = {}
        for s in crossover_depths.keys():
            if s in compositions.keys():
                c = crossover_depths[s]
                o_x = compositions[s][oxide_x]
                o_y = compositions[s][oxide_y]
                pairs.update({s: [c, o_x, o_y]})
        return pairs

    @classmethod
    def get_three_oxides_and_buoyancy_force(cls, compositions, buoyancies, oxide_x, oxide_y, oxide_z):
        pairs = {}
        for s in buoyancies.keys():
            if s in compositions.keys():
                o_x = compositions[s][oxide_x]
                o_y = compositions[s][oxide_y]
                o_z = compositions[s][oxide_z]
                b = buoyancies[s][-1]
                pairs.update({s: [o_x, o_y, o_z, b]})
        return pairs

    @classmethod
    def pair_crossover_depth_to_three_oxides(cls, crossover_depths, compositions, oxide_x, oxide_y, oxide_z):
        pairs = {}
        for s in crossover_depths.keys():
            if s in compositions.keys():
                c = crossover_depths[s]
                o_x = compositions[s][oxide_x]
                o_y = compositions[s][oxide_y]
                o_z = compositions[s][oxide_z]
                pairs.update({s: [c, o_x, o_y, o_z]})
        return pairs


class Clean:

    @classmethod
    def remove_outliers_from_composition_dict(cls, data, oxide):
        prelim_data = {}
        cleaned_dict = {}
        stars = list(data.keys())
        for s in stars:
            if not np.isnan(data[s][oxide]):
                prelim_data.update({s: data[s]})
        stars = list(prelim_data.keys())
        uncleaned_data = [prelim_data[key][oxide] for key in stars]
        Q1 = np.quantile(uncleaned_data, 0.25)
        Q3 = np.quantile(uncleaned_data, 0.75)
        outlier_threshold = iqr(uncleaned_data, axis=0)
        first_quartile_threshold = Q1 - (1.5 * outlier_threshold)
        third_quartile_threshold = Q3 + (1.5 * outlier_threshold)
        for index, i in enumerate(stars):
            uc = uncleaned_data[index]
            if first_quartile_threshold < uc < third_quartile_threshold:
                cleaned_dict.update({i: data[i]})
                cleaned_dict[i][oxide] = uc
        return cleaned_dict
