import matplotlib.pyplot as plt
from src.sort import Sort, Organize, Clean
import numpy as np
from src.buoyancy import DEPTHS
from mpl_toolkits.mplot3d import Axes3D


class Plots:

    @classmethod
    def plot_percent_depletion_vs_buoyancy_force(cls, oxide, buoyancies, depletions, title=""):
        mapped = Sort.pair_composition_to_buoyancy(
            buoyancy=buoyancies, composition=depletions, oxide=oxide.lower())

        ax = plt.figure().add_subplot(111)
        x = [i[0] for i in mapped]
        y = [i[1] for i in mapped]
        # determine best fit line
        coeffs = np.polyfit(x, y, 1)
        intercept = coeffs[-1]
        slope = coeffs[-2]
        xl = [min(x), max(x)]
        yl = [(slope * xx) + intercept for xx in xl]
        ax.scatter(x, y, marker="+")
        ax.plot(xl, yl, color='red', linestyle="--", label="Best Fit")

        ax.set_xlabel("{} Depletion (%)".format(oxide))
        ax.set_ylabel("Buoyancy Force (N)")
        ax.set_title(title)
        ax.grid()

        return ax

    @classmethod
    def plot_two_compositions_and_colormap_buoyancy(cls, oxide_x, oxide_y, buoyancies, depletions, title=""):
        mapped = Sort.pair_compositions_and_map_buoyancy(
            buoyancy=buoyancies,
            composition=depletions, oxide_x=oxide_x.lower(), oxide_y=oxide_y.lower())
        earth_mapped = Sort.pair_compositions_and_map_buoyancy(
            buoyancy=buoyancies,
            composition=depletions, oxide_x=oxide_x.lower(), oxide_y=oxide_y.lower(), special_star="Sun")

        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = [i[0] for i in mapped]
        y = [i[1] for i in mapped]
        b = [i[2] for i in mapped]
        # undepleted_ellipse = Ellipse(xy=(((max(x) - min(x)) / 2.0), (max(y) - min(y)) / 2.0),
        #                              width=abs(max(x) - min(x)),
        #                              height=abs(max(y) - min(y)), edgecolor='blue', lw=4, facecolor='none',
        #                              label="Undepleted BSP Sample")
        # determine best fit line
        coeffs = np.polyfit(x, y, 1)
        intercept = coeffs[-1]
        slope = coeffs[-2]
        xl = [min(x), max(x)]
        yl = [(slope * xx) + intercept for xx in xl]
        sc = ax.scatter(x, y, c=b, marker="+", cmap='viridis')
        ax.scatter(earth_mapped[0][0],
                   earth_mapped[0][1],
                   marker='x', color='black', s=50, label='Sun-Derived Model')
        ax.plot(xl, yl, color='red', linestyle="--", label="Best Fit")
        # ax.add_patch(undepleted_ellipse)
        cbar = plt.colorbar(sc, ax=ax)
        cbar.set_label('Buoyancy Force')
        ax.set_xlabel("{} Depletion (%)".format(oxide_x))
        ax.set_ylabel("{} Depletion (%)".format(oxide_y))
        ax.set_title(title)
        ax.legend()
        ax.grid()

        return ax

    @classmethod
    def plot_two_compositions_and_colormap_buoyancy_relative_to_earth(cls, oxide_x, oxide_y, buoyancies,
                                                                      depletions, title=""):
        mapped = Sort.pair_compositions_and_map_buoyancy_relative_to_earth(
            buoyancy=buoyancies, composition=depletions, oxide_x=oxide_x.lower(), oxide_y=oxide_y.lower())
        earth_mapped = Sort.pair_compositions_and_map_buoyancy_relative_to_earth(
            buoyancy=buoyancies, composition=depletions, oxide_x=oxide_x.lower(), oxide_y=oxide_y.lower(),
            special_star="Sun")

        fig = plt.figure()
        ax = fig.add_subplot(111)
        x_greater_than = [i[0] for i in mapped if i[3] == 1]
        y_greater_than = [i[1] for i in mapped if i[3] == 1]
        x_less_than = [i[0] for i in mapped if i[3] == 0]
        y_less_than = [i[1] for i in mapped if i[3] == 0]
        # determine best fit line
        coeffs_greater_than = np.polyfit(x_greater_than, y_greater_than, 1)
        intercept_greater_than = coeffs_greater_than[-1]
        slope_greater_than = coeffs_greater_than[-2]
        xl_range = [min(x_greater_than + x_less_than), max(x_greater_than + x_less_than)]
        yl_greater_than = [(slope_greater_than * xx) + intercept_greater_than for xx in xl_range]
        ax.scatter(x_greater_than, y_greater_than, c='red', marker="+",
                   label="Buoyancy > Earth ({})".format(len(x_greater_than)))
        ax.plot(xl_range, yl_greater_than, color='red', linestyle="--", label="Best Fit (> Earth)")
        coeffs_less_than = np.polyfit(x_less_than, y_less_than, 1)
        intercept_less_than = coeffs_less_than[-1]
        slope_less_than = coeffs_less_than[-2]
        yl_less_than = [(slope_less_than * xx) + intercept_less_than for xx in xl_range]
        ax.scatter(x_less_than, y_less_than, c='blue', marker="+",
                   label="Buoyancy <= Earth ({})".format(len(x_less_than)))
        ax.scatter(earth_mapped[0][0], earth_mapped[0][1],
                   marker='x', color='black', s=50, label='Sun-Derived Model')
        ax.plot(xl_range, yl_less_than, color='blue', linestyle="--", label="Best Fit (<= Earth)")
        ax.set_xlabel("{} Depletion (%)".format(oxide_x))
        ax.set_ylabel("{} Depletion (%)".format(oxide_y))
        ax.set_title(title)
        ax.legend()
        ax.grid()

        return ax

    @classmethod
    def plot_two_compositions_and_colormap_depleted_buoyancy_difference(cls, oxide_x, oxide_y, undepleted_buoyancies,
                                                                        depleted_buoyancies, depletions, title="",
                                                                        remove_outliers=False, percentages=False):
        if percentages:
            buoyancy_differences = Organize.get_buoyancy_difference_percentages(parent_reservoir=depleted_buoyancies,
                                                                                daughter_reservoir=undepleted_buoyancies)
        else:
            buoyancy_differences = Organize.get_buoyancy_differences(parent_reservoir=depleted_buoyancies,
                                                                     daughter_reservoir=undepleted_buoyancies)
        if remove_outliers:
            cleaned_depletions_oxide_x = Clean.remove_outliers_from_composition_dict(data=depletions,
                                                                                     oxide=oxide_x.lower())
            cleaned_depletions_oxide_y = Clean.remove_outliers_from_composition_dict(data=cleaned_depletions_oxide_x,
                                                                                     oxide=oxide_y.lower())
            return cls.plot_two_compositions_and_colormap_buoyancy(oxide_x=oxide_x, oxide_y=oxide_y,
                                                                   buoyancies=buoyancy_differences,
                                                                   depletions=cleaned_depletions_oxide_y, title=title)
        else:
            return cls.plot_two_compositions_and_colormap_buoyancy(oxide_x=oxide_x, oxide_y=oxide_y,
                                                                   buoyancies=buoyancy_differences,
                                                                   depletions=depletions, title=title)

    @classmethod
    def plot_two_compositions_and_colormap_depleted_buoyancy_difference_relative_to_earth(cls, oxide_x, oxide_y,
                                                                                          undepleted_buoyancies,
                                                                                          depleted_buoyancies,
                                                                                          depletions, title=""):
        buoyancy_differences = Organize.get_buoyancy_differences(parent_reservoir=depleted_buoyancies,
                                                                 daughter_reservoir=undepleted_buoyancies)
        return cls.plot_two_compositions_and_colormap_buoyancy_relative_to_earth(oxide_x=oxide_x, oxide_y=oxide_y,
                                                                                 buoyancies=buoyancy_differences,
                                                                                 depletions=depletions, title=title)

    @classmethod
    def plot_buoyancy_force_as_function_of_depth(cls, depth, buoyancies, title):
        ax = plt.figure().add_subplot(111)
        earth_buoyancy = buoyancies['Sun']
        FOUND_GOOD = False
        FOUND_BAD = False
        depth = [-1 * i for i in depth]
        for s in buoyancies.keys():
            b = buoyancies[s]
            if b[-1] <= earth_buoyancy[-1]:
                if not FOUND_GOOD:
                    ax.plot(depth, b, color='blue', label="Buoyancy <= Earth (Good!)")
                    FOUND_GOOD = True
                else:
                    ax.plot(depth, b, color='blue')
            else:
                if not FOUND_BAD:
                    ax.plot(depth, b, color='red', label="Buoyancy > Earth (Bad!)")
                    FOUND_BAD = True
                else:
                    ax.plot(depth, b, color='red')
        ax.plot(depth, earth_buoyancy, color='green', linewidth=2, label="Earth")
        ax.set_xlabel("Depth (km)")
        ax.set_ylabel("Buoyancy Force (N)")
        ax.set_title(title)
        ax.legend()
        ax.grid()

        return ax

    @classmethod
    def plot_crossover_depths(cls, buoyancies, compositions, oxide, title):
        crossover_depths = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=buoyancies)
        paired_crossover_to_oxide = Organize.pair_crossover_depth_to_oxide(crossover_depths=crossover_depths,
                                                                           oxide=oxide.lower(),
                                                                           compositions=compositions)
        crossovers = [paired_crossover_to_oxide[i][0] for i in paired_crossover_to_oxide.keys()]
        comps = [paired_crossover_to_oxide[i][1] for i in paired_crossover_to_oxide.keys()]
        ax = plt.figure().add_subplot(111)
        ax.scatter(comps, crossovers, color='black', marker="+")
        ax.set_xlabel("Negative to Positive Net Buoyancy Crossover Depth (km)")
        ax.set_ylabel("{} Depletion %".format(oxide))
        ax.set_title(title)
        ax.grid()

        return ax

    @classmethod
    def plot_two_oxides_against_crossover_depth(cls, buoyancies, compositions, oxide_x, oxide_y, title):
        crossover_depths = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=buoyancies)
        paired_crossover_to_oxide = Organize.pair_crossover_depth_to_two_oxides(crossover_depths=crossover_depths,
                                                                                oxide_x=oxide_x.lower(),
                                                                                oxide_y=oxide_y.lower(),
                                                                                compositions=compositions)
        o_x = [paired_crossover_to_oxide[i][0] for i in paired_crossover_to_oxide.keys()]
        o_y = [paired_crossover_to_oxide[i][1] for i in paired_crossover_to_oxide.keys()]
        c_d = [paired_crossover_to_oxide[i][2] for i in paired_crossover_to_oxide.keys()]
        ax = plt.figure().add_subplot(111)
        sc = ax.scatter(o_x, o_y, c=c_d, marker="+", cmap='viridis')
        cbar = plt.colorbar(sc, ax=ax)
        cbar.set_label('Crossover Depth (km)')
        ax.set_xlabel("{} Depletion %".format(oxide_x))
        ax.set_ylabel("{} Depletion %".format(oxide_y))
        ax.set_title(title)
        ax.grid()

        return ax

    @classmethod
    def plot_compositional_profile_and_disappearances(cls, profile, mineral_temps, title="", appearance_or_disappearance='appearance'):
        oxide_map = {
            "feo": "FeO",
            "na2o": "Na2O",
            "mgo": "MgO",
            "al2o3": "Al2O3",
            "sio2": "SiO2",
            "cao": "CaO",
            "tio2": "TiO2"
        }
        max_y_for_text = []
        for i in profile.keys():
            if i != "temperature" and i != "mass":
                max_y_for_text += profile[i]
        max_y_for_text = max(max_y_for_text)
        ax = plt.figure().add_subplot(111)
        for i in mineral_temps.keys():
            ax.axvline(mineral_temps[i][appearance_or_disappearance], linewidth=2.0, color="black", linestyle="--")
            ax.text(mineral_temps[i][appearance_or_disappearance] + 2, max_y_for_text - 18, i,
                    rotation=270, fontsize=10)
        for i in profile.keys():
            if i != "temperature":
                ax.plot(profile['temperature'], profile[i], linewidth=2.0, label=oxide_map[i])
        ax.set_xlabel("Temperature (C)")
        ax.set_ylabel("Oxide wt%")
        ax.set_title(title)
        ax.legend()
        ax.grid()

        return ax

    @classmethod
    def plot_compositional_mass_fraction_profile_and_disappearances(cls, profile, mineral_temps, title="",
                                                      appearance_or_disappearance='appearance'):
        oxide_map = {
            "feo": "FeO",
            "na2o": "Na2O",
            "mgo": "MgO",
            "al2o3": "Al2O3",
            "sio2": "SiO2",
            "cao": "CaO",
            "tio2": "TiO2"
        }
        max_y_for_text = []
        for i in profile.keys():
            if i != "temperature" and i != "mass":
                max_y_for_text += profile[i]
        max_y_for_text = max(max_y_for_text)
        print(max_y_for_text)
        ax = plt.figure().add_subplot(111)
        for i in mineral_temps.keys():
            ax.axvline(mineral_temps[i][appearance_or_disappearance], linewidth=2.0, color="black", linestyle="--")
            ax.text(mineral_temps[i][appearance_or_disappearance] + 2, max_y_for_text - 18, i,
                    rotation=270, fontsize=10)
        for i in profile.keys():
            if i != "temperature" and i != "mass":
                ax.plot(profile['temperature'], profile[i], linewidth=2.0, label=oxide_map[i])
        ax.set_xlabel("Temperature (C)")
        ax.set_ylabel("Oxide Mass (g)")
        ax.set_title(title)
        ax.legend()
        ax.grid()

        return ax

    @classmethod
    def plot_appearance_or_disappearance_temperatures_against_composition(cls, appearance_or_disappearance_temperatures,
                                                                          compositions_at_temperature, oxide,
                                                                          appearance_or_disappearance='appearance',
                                                                          fraction=False):

        oxide = oxide.lower()
        phases = {}
        for star in appearance_or_disappearance_temperatures.keys():
            for phase in appearance_or_disappearance_temperatures[star].keys():
                if phase not in phases.keys():
                    phases.update({phase: {
                        oxide: [],
                        "temperature": []
                    }})
                t = appearance_or_disappearance_temperatures[star][phase][appearance_or_disappearance]
                c = compositions_at_temperature[star][phase][oxide]
                phases[phase][oxide].append(c)
                phases[phase]['temperature'].append(t)
        ax = plt.figure().add_subplot(111)
        for phase in phases.keys():
            ax.scatter(phases[phase][oxide], phases[phase]['temperature'], linewidth=2.0, marker="+", label=phase)
        if not fraction:
            ax.set_xlabel("Oxide Mass (g)")
        else:
            ax.set_xlabel("Oxide Mass Fraction")
        ax.set_ylabel("Temperature (C)")
        ax.grid()
        ax.legend()

        return ax


class Plots3D:

    @classmethod
    def plot_three_oxides_and_colormap_buoyancy(cls, compositions, buoyancies, oxide_x, oxide_y, oxide_z, title,
                                                clean=False):
        ax = Axes3D(plt.figure())
        if clean:
            c1 = Clean.remove_outliers_from_composition_dict(data=compositions, oxide=oxide_x.lower())
            c2 = Clean.remove_outliers_from_composition_dict(data=c1, oxide=oxide_y.lower())
            c3 = Clean.remove_outliers_from_composition_dict(data=c2, oxide=oxide_z.lower())
            p = Organize.get_three_oxides_and_buoyancy_force(compositions=c3, buoyancies=buoyancies,
                                                             oxide_x=oxide_x.lower(), oxide_y=oxide_y.lower(),
                                                             oxide_z=oxide_z.lower())
        else:
            p = Organize.get_three_oxides_and_buoyancy_force(compositions=compositions, buoyancies=buoyancies,
                                                             oxide_x=oxide_x.lower(), oxide_y=oxide_y.lower(),
                                                             oxide_z=oxide_z.lower())
        o_x = [p[i][0] for i in p.keys()]
        o_y = [p[i][1] for i in p.keys()]
        o_z = [p[i][2] for i in p.keys()]
        b = [p[i][3] for i in p.keys()]
        sc = ax.scatter(o_x, o_y, o_z, c=b, marker="+")
        ax.set_xlabel("{} Depletion %".format(oxide_x))
        ax.set_ylabel("{} Depletion %".format(oxide_y))
        ax.set_zlabel("{} Depletion %".format(oxide_z))
        ax.set_title(title)
        cbar = plt.colorbar(sc, ax=ax)
        cbar.set_label('Net Buoyancy Force (N)')

        return ax


    @classmethod
    def plot_three_oxides_and_colormap_crossover_depth(cls, compositions, buoyancies, oxide_x, oxide_y, oxide_z, title,
                                                clean=False):
        ax = Axes3D(plt.figure())
        crossover_depths = Sort.get_crossover_depth(depths=DEPTHS, buoyancies=buoyancies)
        if clean:
            c1 = Clean.remove_outliers_from_composition_dict(data=compositions, oxide=oxide_x.lower())
            c2 = Clean.remove_outliers_from_composition_dict(data=c1, oxide=oxide_y.lower())
            c3 = Clean.remove_outliers_from_composition_dict(data=c2, oxide=oxide_z.lower())
            p = Organize.pair_crossover_depth_to_three_oxides(compositions=c3, crossover_depths=crossover_depths,
                                                             oxide_x=oxide_x.lower(), oxide_y=oxide_y.lower(),
                                                             oxide_z=oxide_z.lower())
        else:
            p = Organize.pair_crossover_depth_to_three_oxides(compositions=compositions, crossover_depths=crossover_depths,
                                                             oxide_x=oxide_x.lower(), oxide_y=oxide_y.lower(),
                                                             oxide_z=oxide_z.lower())
        o_x = [p[i][0] for i in p.keys()]
        o_y = [p[i][1] for i in p.keys()]
        o_z = [p[i][2] for i in p.keys()]
        b = [p[i][3] for i in p.keys()]
        sc = ax.scatter(o_x, o_y, o_z, c=b, marker="+")
        ax.set_xlabel("{} Depletion %".format(oxide_x))
        ax.set_ylabel("{} Depletion %".format(oxide_y))
        ax.set_zlabel("{} Depletion %".format(oxide_z))
        ax.set_title(title)
        cbar = plt.colorbar(sc, ax=ax)
        cbar.set_label('Crossover Depth (km)')

        return ax