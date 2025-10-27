import dataclasses as dc
import tkinter as tk
from tkinter import ttk

import typing as tp

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import cheeks


class CheeksGuiCore(cheeks.Cheeks3Dcore):
    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        if tp.TYPE_CHECKING:
            assert dc.is_dataclass(self),\
                f"CheeksGUI inherits from {super()} which must be a dataclass"
        print(*dc.fields(self), sep='\n')
        self.root = self.tk_init()
        self.fig, self.ax = self.mpl_init()

        self.sliders = [
            self.slider_init(attr)
            for attr in dc.fields(self)
        ]
        self.canvas = self.canvas_init()  # needed to display sliders
        self.root.mainloop()

    def update_cheek_attr(self, attr_name: str, value: float, redraw: bool = True):
        if tp.TYPE_CHECKING:
            assert dc.is_dataclass(self),\
                f"CheeksGUI inherits from {super()} which must be a dataclass"
        if attr_name not in [f.name for f in dc.fields(self)]:
            raise ValueError(f"{attr_name} is not an attribute of Cheeks3D instances that you can edit")
        self.__setattr__(attr_name, value)
        self.update_Z()
        if redraw:
            self.draw(self.ax)
            try:
                self.canvas.draw_idle()
            except AttributeError:
                # we can ignore this because it only happens at slider init
                print("todo add a check that we are in slider_init")
                pass

    def tk_init(self):
        """
        Initializes and returns root, a Tkinter GUI
        """
        root = tk.Tk()
        root.title("Butt3D-gui")
        root.geometry("800x600")
        return root

    def mpl_init(self):
        """
        Initializes and returns fig, ax, Matplotlib Figure and 3D Axes
        """
        fig = Figure(figsize=(9, 9), dpi=100)
        ax = fig.add_subplot(111, projection="3d")
        ax.set_title("A pair of buttcheeks in dimension n=3")
        return fig, ax

    def canvas_init(self):
        """
        Returns the canvas object that embeds the Matplotlib figure `fig` in the Tkinter instance `root`
        """
        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        return canvas

    def slider_init(self, attr: dc.Field):
        slider_frame = ttk.Frame(self.root)
        slider_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        attr_bounds = getattr(self, f"{attr.name}_bounds")
        ttk.Label(slider_frame, text=f"{attr.name.title()}:").pack(side=tk.LEFT)
        slider = ttk.Scale(
            slider_frame,
            from_=attr_bounds[0],
            to=attr_bounds[1],
            orient=tk.HORIZONTAL,
            command=lambda val: self.update_cheek_attr(attr.name, float(val), redraw=True)
        )
        slider.set(attr.default)
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        return slider


def make_gui_class(cheeks_class):
    return type(f"CheeksGui_{cheeks_class.__name__.removeprefix("Cheeks3D_")}", (CheeksGuiCore, cheeks_class), {})

def run_gui_class(cheeks_class):
    return make_gui_class(cheeks_class)()

def run_gui(cheeks_model: str):
    key = f"Cheeks3D_{cheeks_model.lower()}"
    if key not in (vc := vars(cheeks)):
        raise KeyError(
            f"{key} was not found in the declared variables of the `cheeks.py` file. Available parameters for this "
            f"function are: {', '.join([k.removeprefix("Cheeks3D_") for k in vc if k.startswith("Cheeks3D_")])}"
        )
    return run_gui_class(vc[key])


if __name__ == "__main__":
    run_gui('gpap')