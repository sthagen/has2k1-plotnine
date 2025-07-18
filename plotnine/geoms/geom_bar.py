from __future__ import annotations

import typing

from .._utils import resolution
from ..doctools import document
from .geom_rect import geom_rect

if typing.TYPE_CHECKING:
    import pandas as pd


@document
class geom_bar(geom_rect):
    """
    Bar plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    just : float, default=0.5
        How to align the column with respect to the axis breaks. The default
        `0.5` aligns the center of the column with the break. `0` aligns the
        left of the of the column with the break and `1` aligns the right of
        the column with the break.
    width : float, default=None
        Bar width. If `None`{.py}, the width is set to
        `90%` of the resolution of the data.

    See Also
    --------
    plotnine.geom_histogram
    plotnine.stat_count : The default `stat` for this `geom`.
    """

    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"xmin", "xmax", "ymin", "ymax"}
    DEFAULT_PARAMS = {
        "stat": "count",
        "position": "stack",
        "na_rm": False,
        "just": 0.5,
        "width": None,
    }

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if "width" not in data:
            if self.params["width"]:
                data["width"] = self.params["width"]
            else:
                data["width"] = resolution(data["x"], False) * 0.9

        just = self.params.get("just", 0.5)

        bool_idx = data["y"] < 0

        data["ymin"] = 0.0
        data.loc[bool_idx, "ymin"] = data.loc[bool_idx, "y"]

        data["ymax"] = data["y"]
        data.loc[bool_idx, "ymax"] = 0.0

        data["xmin"] = data["x"] - data["width"] * just
        data["xmax"] = data["x"] + data["width"] * (1 - just)
        del data["width"]
        return data
