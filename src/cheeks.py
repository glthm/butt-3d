import dataclasses as dc

import matplotlib.colors as mc
from matplotlib.axes import Axes
from matplotlib import pyplot as plt
from scipy.stats import lognorm
import numpy as np
import typing as tp


def constant_cmap(name: str, color: str):
    return mc.LinearSegmentedColormap.from_list(name, [color, color], N=256)

@dc.dataclass
class Cheeks3D:
    cutoff: float = 0.3
    spread: float = 0.3
    width: float = 0.8
    rounding: float = 0.7
    mu: float = 1
    sigma: float = 1

    # X/Y grid params
    resolution: dc.InitVar[int] = 200
    x_min: dc.InitVar[float] = -2
    x_max: dc.InitVar[float] = 2
    y_min: dc.InitVar[float] = -5
    y_max: dc.InitVar[float] = 5

    # acceptable bounds for shape parameters
    cutoff_bounds: tp.ClassVar[tuple[float, float]] = (0, 1)
    spread_bounds: tp.ClassVar[tuple[float, float]] = (0, 1)
    width_bounds: tp.ClassVar[tuple[float, float]] = (0, 1)
    rounding_bounds: tp.ClassVar[tuple[float, float]] = (0, 1)
    mu_bounds: tp.ClassVar[tuple[float, float]] = (0, 3)
    sigma_bounds: tp.ClassVar[tuple[float, float]] = (0, 3)



    def __post_init__(self, resolution, x_min, x_max, y_min, y_max):
        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(y_min, y_max, resolution)
        self.X, self.Y = np.meshgrid(x, y)
        self.update_Z()


    def update_Z(self):
        """
        Sets and returns the array of Z values using the set attributes of `self`.
        Based on https://mathematica.stackexchange.com/questions/66538/how-do-i-draw-a-pair-of-buttocks
        """
        Z1 = -lognorm.pdf(
            (self.Y + self.width) ** 2 + self.X ** 2,
            s=self.sigma, scale=np.exp(self.mu)
        ) * np.exp(self.spread * (self.Y + self.rounding) ** 2)
        Z2 = -lognorm.pdf(
            (self.Y - self.width) ** 2 + self.X ** 2,
            s=self.sigma, scale=np.exp(self.mu)
        ) * np.exp(self.spread * (self.Y - self.rounding) ** 2)
        self.Z = np.max([Z1, Z2, -self.cutoff * np.ones_like(Z1)], axis=0)

    def draw(self, ax: Axes, **kwargs):
        kwargs = kwargs or {
             #"'cmap':constant_cmap('my_cmap', 'black'),
            'cmap': "Reds",
            'linewidth':0.5,
            'antialiased':True,
            #'shade':True
        } # defaults
        ax.clear()
        ax.set_axis_off()
        # colors = mc.LightSource().shade(self.Z, cmap=plt.get_cmap(kwargs['cmap']))
        ax.plot_surface(self.X, self.Y, self.Z, **kwargs)