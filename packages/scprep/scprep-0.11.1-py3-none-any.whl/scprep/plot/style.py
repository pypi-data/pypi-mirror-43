from .. import utils
from .tools import label_axis


@utils._with_pkg(pkg="matplotlib", min_version=3)
def style_phate(ax, label_prefix="PHATE"):
    """Removes ticks from `ax` and adds axis labels.

    Parameters
    ----------
    ax : matplotlib.Axes
        Axis to style
    label_prefix : str, optional (default: "PHATE")
        Prefix for numerically labeled axes
    """
    label_axis(ax.xaxis, ticks=False, label=label_prefix + '1')
    label_axis(ax.yaxis, ticks=False, label=label_prefix + '2')
    if hasattr(ax, 'get_zlim'):
        label_axis(ax.zaxis, ticks=False, label=label_prefix + '3')
    return ax
