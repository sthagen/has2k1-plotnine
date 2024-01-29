from __future__ import annotations

import typing
from dataclasses import asdict, dataclass

from matplotlib.layout_engine import LayoutEngine
from matplotlib.text import Text

if typing.TYPE_CHECKING:
    from typing import Optional

    from matplotlib.backend_bases import RendererBase
    from matplotlib.offsetbox import AnchoredOffsetbox

    from plotnine import ggplot
    from plotnine.themes.targets import ThemeTargets
    from plotnine.typing import (
        Any,
        Axes,
        Facet,
        Figure,
        LegendPosition,
        Theme,
    )


@dataclass
class LayoutPack:
    """
    Objects required to compute the layout
    """

    axs: list[Axes]
    figure: Figure
    renderer: RendererBase
    theme: Theme
    facet: Facet
    axis_title_x: Optional[Text] = None
    axis_title_y: Optional[Text] = None
    # The legend references the legend_background. That is the
    # AnchoredOffsetbox that contains all the legends.
    legend: Optional[AnchoredOffsetbox] = None
    legend_position: Optional[LegendPosition] = None
    plot_caption: Optional[Text] = None
    plot_subtitle: Optional[Text] = None
    plot_title: Optional[Text] = None


class PlotnineLayoutEngine(LayoutEngine):
    """
    Implement geometry management for plotnine plots

    This layout manager automatically adjusts the location of
    objects placed around the plot panels and the subplot
    spacing parameters so that the plot fits cleanly within
    the figure area.
    """

    _adjust_compatible = True
    _colorbar_gridspec = False

    def __init__(self, plot: ggplot):
        self.plot = plot
        self.theme = plot.theme

    def execute(self, fig: Figure):
        from contextlib import nullcontext

        from ._plotnine_tight_layout import (
            get_plotnine_tight_layout,
            set_figure_artist_positions,
        )

        pack = self.setup()

        with getattr(pack.renderer, "_draw_disabled", nullcontext)():
            tparams = get_plotnine_tight_layout(pack)

        set_figure_artist_positions(pack, tparams)
        fig.subplots_adjust(**asdict(tparams.grid))

    def setup(self) -> LayoutPack:
        """
        Put together objects required to do the layout
        """
        targets = self.theme.targets

        def get_target(name: str) -> Any:
            """
            Return themeable target or None
            """
            if self.theme.T.is_blank(name):
                return None
            else:
                t = getattr(targets, name)
                if isinstance(t, Text) and t.get_text() == "":
                    return None
                return t

        legend_position = self.theme.getp("legend_position", None)
        return LayoutPack(
            axs=self.plot.axs,
            figure=self.plot.figure,
            renderer=self.plot.figure._get_renderer(),  # pyright: ignore
            theme=self.theme,
            facet=self.plot.facet,
            axis_title_x=get_target("axis_title_x"),
            axis_title_y=get_target("axis_title_y"),
            legend=get_target("legend_background"),
            legend_position=legend_position,
            plot_caption=get_target("plot_caption"),
            plot_subtitle=get_target("plot_subtitle"),
            plot_title=get_target("plot_title"),
        )
