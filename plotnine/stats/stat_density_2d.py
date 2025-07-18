from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from .density import get_var_type, kde
from .stat import stat

if TYPE_CHECKING:
    from plotnine.typing import FloatArrayLike


class stat_density_2d(stat):
    """
    Compute 2D kernel density estimation

    {usage}

    Parameters
    ----------
    {common_parameters}
    contour : bool, default=True
        Whether to create contours of the 2d density estimate.
    n : int, default=64
        Number of equally spaced points at which the density is to
        be estimated. For efficient computation, it should be a power
        of two.
    levels : int | array_like, default=5
        Contour levels. If an integer, it specifies the maximum number
        of levels, if array_like it is the levels themselves.
    package : Literal["statsmodels", "scipy", "sklearn"], default="statsmodels"
        Package whose kernel density estimation to use.
    kde_params : dict
        Keyword arguments to pass on to the kde class.

    See Also
    --------
    plotnine.geom_density_2d : The default `geom` for this `stat`.
    statsmodels.nonparametric.kernel_density.KDEMultivariate
    scipy.stats.gaussian_kde
    sklearn.neighbors.KernelDensity
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "level"     # density level of a contour
    "density"   # Computed density at a point
    "piece"     # Numeric id of a contour in a given group
    ```

    `level` is only relevant when contours are computed. `density`
    is available only when no contours are computed. `piece` is
    largely irrelevant.
    """
    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "density_2d",
        "position": "identity",
        "na_rm": False,
        "contour": True,
        "package": "statsmodels",
        "kde_params": None,
        "n": 64,
        "levels": 5,
    }
    CREATES = {"y"}

    def setup_params(self, data):
        params = self.params
        if params["kde_params"] is None:
            params["kde_params"] = {}

        kde_params = params["kde_params"]
        if params["package"] == "statsmodels":
            params["package"] = "statsmodels-m"
            if "var_type" not in kde_params:
                x_type = get_var_type(data["x"])
                y_type = get_var_type(data["y"])
                kde_params["var_type"] = f"{x_type}{y_type}"

    def compute_group(self, data, scales):
        params = self.params
        package = params["package"]
        kde_params = params["kde_params"]

        group = data["group"].iloc[0]
        range_x = scales.x.dimension()
        range_y = scales.y.dimension()
        x = np.linspace(range_x[0], range_x[1], params["n"])
        y = np.linspace(range_y[0], range_y[1], params["n"])

        # The grid must have a "similar" shape (n, p) to the var_data
        X, Y = np.meshgrid(x, y)
        var_data = np.array([data["x"].to_numpy(), data["y"].to_numpy()]).T
        grid = np.array([X.flatten(), Y.flatten()]).T
        density = kde(var_data, grid, package, **kde_params)

        if params["contour"]:
            Z = density.reshape(len(x), len(y))
            data = contour_lines(X, Y, Z, params["levels"])
            # Each piece should have a distinct group
            groups = str(group) + "-00" + data["piece"].astype(str)
            data["group"] = groups
        else:
            data = pd.DataFrame(
                {
                    "x": X.flatten(),
                    "y": Y.flatten(),
                    "density": density.flatten(),
                    "group": group,
                    "level": 1,
                    "piece": 1,
                }
            )

        return data


def contour_lines(X, Y, Z, levels: int | FloatArrayLike):
    """
    Calculate contour lines
    """
    from contourpy import contour_generator

    # Preparation of values and the creating of contours is
    # adapted from MPL with some adjustments.
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Z = np.asarray(Z, dtype=np.float64)
    zmin, zmax = Z.min(), Z.max()
    cgen = contour_generator(
        X, Y, Z, name="mpl2014", corner_mask=False, chunk_size=0
    )

    if isinstance(levels, int):
        from mizani.breaks import breaks_extended

        levels = breaks_extended(n=levels)((zmin, zmax))

    # The counter_generator gives us a list of vertices that
    # represent all the contour lines at that level. There
    # may be 0, 1 or more vertices at a level. Each one of
    # these we call a piece, and it represented as an nx2 array.
    #
    # We want x-y values that describe *all* the contour lines
    # in tidy format. Therefore each x-y vertex has a
    # corresponding level and piece id.
    segments = []
    piece_ids = []
    level_values = []
    start_pid = 1
    for level in levels:
        vertices, *_ = cgen.create_contour(level)
        for pid, piece in enumerate(vertices, start=start_pid):
            n = len(piece)  # pyright: ignore
            segments.append(piece)
            piece_ids.append(np.repeat(pid, n))
            level_values.append(np.repeat(level, n))
            start_pid = pid + 1

    # Collapse the info and make it fit for dataframe columns
    if segments:
        x, y = np.vstack(segments).T
        piece = np.hstack(piece_ids)
        level = np.hstack(level_values)
    else:
        x, y = [], []
        piece = []
        level = []

    data = pd.DataFrame(
        {
            "x": x,
            "y": y,
            "level": level,
            "piece": piece,
        }
    )
    return data
