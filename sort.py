import numpy as np
from scipy.stats import iqr

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


class Organize:

    @classmethod
    def get_all_buoyancy_forces(cls, buoyancies):
        adibekyan_f1400_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1400_1200)
        adibekyan_f1400_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1400_1400)
        adibekyan_f1600_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1600_1200)
        adibekyan_f1600_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1600_1400)
        adibekyan_f1600_1600_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                                  morb_file=buoyancies.adibekyan_morb_f1600_1600)

        kepler_f1400_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1400_1200)
        kepler_f1400_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1400_1400)
        kepler_f1600_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1600_1200)
        kepler_f1600_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1600_1400)
        kepler_f1600_1600_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                               morb_file=buoyancies.kepler_morb_f1600_1600)

        adibekyan_depleted_f1400_1400_morb_1200_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1400_1400,
            morb_file=buoyancies.adibekyan_morb_f1400_1200)
        adibekyan_depleted_f1400_1400_morb_1400_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1400_1400,
            morb_file=buoyancies.adibekyan_morb_f1400_1400)
        adibekyan_depleted_f1600_1600_morb_1200_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1600_1600,
            morb_file=buoyancies.adibekyan_morb_f1600_1200)
        adibekyan_depleted_f1600_1600_morb_1400_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1600_1600,
            morb_file=buoyancies.adibekyan_morb_f1600_1400)
        adibekyan_depleted_f1600_1600_morb_1600_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.adibekyan_depleted_bsp_f1600_1600,
            morb_file=buoyancies.adibekyan_morb_f1600_1600)

        kepler_depleted_f1400_1400_morb_1200_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1400_1400,
            morb_file=buoyancies.kepler_morb_f1400_1200)
        kepler_depleted_f1400_1400_morb_1400_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1400_1400,
            morb_file=buoyancies.kepler_morb_f1400_1400)
        kepler_depleted_f1600_1600_morb_1200_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1600_1600,
            morb_file=buoyancies.kepler_morb_f1600_1200)
        kepler_depleted_f1600_1600_morb_1400_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1600_1600,
            morb_file=buoyancies.kepler_morb_f1600_1400)
        kepler_depleted_f1600_1600_morb_1600_buoyancies = buoyancies.get_buoyancy(
            bsp_file=buoyancies.kepler_depleted_bsp_f1600_1600,
            morb_file=buoyancies.kepler_morb_f1600_1600)

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
                buoyancy_differences.update({parent_star: [((x - y) / y) * 100.0 for x, y in zip(daughter_buoyancy, parent_buoyancy)]})
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
