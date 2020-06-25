import matplotlib.pyplot as plt
from sort import Sort, Organize, Clean
import numpy as np
from matplotlib.patches import Ellipse
from mpl_toolkits.axes_grid1 import make_axes_locatable


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
        ax.scatter(x_greater_than, y_greater_than, c='red', marker="+", label="Buoyancy > Earth ({})".format(len(x_greater_than)))
        ax.plot(xl_range, yl_greater_than, color='red', linestyle="--", label="Best Fit (> Earth)")
        coeffs_less_than = np.polyfit(x_less_than, y_less_than, 1)
        intercept_less_than = coeffs_less_than[-1]
        slope_less_than = coeffs_less_than[-2]
        yl_less_than = [(slope_less_than * xx) + intercept_less_than for xx in xl_range]
        ax.scatter(x_less_than, y_less_than, c='blue', marker="+", label="Buoyancy <= Earth ({})".format(len(x_less_than)))
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
            cleaned_depletions_oxide_x = Clean.remove_outliers_from_composition_dict(data=depletions, oxide=oxide_x.lower())
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
                                                                        undepleted_buoyancies, depleted_buoyancies,
                                                                                          depletions, title=""):
        buoyancy_differences = Organize.get_buoyancy_differences(parent_reservoir=depleted_buoyancies,
                                                                 daughter_reservoir=undepleted_buoyancies)
        return cls.plot_two_compositions_and_colormap_buoyancy_relative_to_earth(oxide_x=oxide_x, oxide_y=oxide_y,
                                                               buoyancies=buoyancy_differences,
                                                               depletions=depletions, title=title)
