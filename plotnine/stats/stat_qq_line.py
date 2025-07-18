import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError
from .stat import stat
from .stat_qq import theoretical_qq


@document
class stat_qq_line(stat):
    """
    Calculate line through quantile-quantile plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    distribution : str, default="norm"
        Distribution or distribution function name. The default is
        *norm* for a normal probability plot. Objects that look enough
        like a stats.distributions instance (i.e. they have a ppf
        method) are also accepted. See [scipy stats ](`scipy.stats`)
        for available distributions.
    dparams : dict, default=None
        Distribution-specific shape parameters (shape parameters plus
        location and scale).
    quantiles : array_like, default=None
        Probability points at which to calculate the theoretical
        quantile values. If provided, must be the same number as
        as the sample data points. The default is to use calculated
        theoretical points, use to `alpha_beta` control how
        these points are generated.
    alpha_beta : tuple, default=(3/8, 3/8)
        Parameter values to use when calculating the quantiles.
    line_p : tuple, default=(0.25, 0.75)
        Quantiles to use when fitting a Q-Q line. Must be 2 values.
    fullrange : bool, default=False
        If `True`{.py} the fit will span the full range of the plot.

    See Also
    --------
    plotnine.geom_qq_line : The default `geom` for this `stat`.
    scipy.stats.mstats.plotting_positions : Uses `alpha_beta`
        to calculate the quantiles.
    """

    REQUIRED_AES = {"sample"}
    DEFAULT_PARAMS = {
        "geom": "qq_line",
        "position": "identity",
        "na_rm": False,
        "distribution": "norm",
        "dparams": {},
        "quantiles": None,
        "alpha_beta": (3 / 8, 3 / 8),
        "line_p": (0.25, 0.75),
        "fullrange": False,
    }
    CREATES = {"x", "y"}

    def setup_params(self, data):
        if len(self.params["line_p"]) != 2:
            raise PlotnineError(
                "Cannot fit line quantiles. 'line_p' must be of length 2"
            )

    def compute_group(self, data, scales):
        from scipy.stats.mstats import mquantiles

        from .distributions import get_continuous_distribution

        line_p = self.params["line_p"]
        dparams = self.params["dparams"]

        # Compute theoretical values
        sample = data["sample"].sort_values().to_numpy()
        theoretical = theoretical_qq(
            sample,
            self.params["distribution"],
            alpha=self.params["alpha_beta"][0],
            beta=self.params["alpha_beta"][1],
            quantiles=self.params["quantiles"],
            distribution_params=dparams,
        )

        # Compute slope & intercept of the line through the quantiles
        cdist = get_continuous_distribution(self.params["distribution"])
        x_coords = cdist.ppf(line_p, **dparams)
        y_coords = mquantiles(sample, line_p)
        slope = (np.diff(y_coords) / np.diff(x_coords))[0]
        intercept = y_coords[0] - slope * x_coords[0]

        # Get x,y points that describe the line
        if self.params["fullrange"] and scales.x:
            x = scales.x.dimension()
        else:
            x = theoretical.min(), theoretical.max()

        x = np.asarray(x)
        y = slope * x + intercept
        data = pd.DataFrame({"x": x, "y": y})
        return data
