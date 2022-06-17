import math
from typing import Optional, Sequence

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def z_table(confidence):
    """Hand-coded Z-Table

    Parameters
    ----------
    confidence: float
        The confidence level for the z-value.

    Returns
    -------
        The z-value for the confidence level given.
    """
    return {
        0.99: 2.576,
        0.95: 1.96,
        0.90: 1.645
    }[confidence]


def confidence_interval(mean, n, confidence):
    """Computes the confidence interval of a sample.

    Parameters
    ----------
    mean: float
        The mean of the sample
    n: int
        The size of the sample
    confidence: float
        The confidence level for the z-value.

    Returns
    -------
        The confidence interval.
    """
    return z_table(confidence) * (mean / math.sqrt(n))


def standard_error(std_dev, n, confidence):
    """Computes the standard error of a sample.

    Parameters
    ----------
    std_dev: float
        The standard deviation of the sample
    n: int
        The size of the sample
    confidence: float
        The confidence level for the z-value.

    Returns
    -------
        The standard error.
    """
    return z_table(confidence) * (std_dev / math.sqrt(n))


def plot_confidence_bar(names, means, std_devs, N, title, x_label, y_label, confidence, show=False, filename=None, colors=None, yscale=None, flag=True):
    """Creates a bar plot for comparing different agents/teams.

    Parameters
    ----------

    names: Sequence[str]
        A sequence of names (representing either the agent names or the team names)
    means: Sequence[float]
        A sequence of means (one mean for each name)
    std_devs: Sequence[float]
        A sequence of standard deviations (one for each name)
    N: Sequence[int]
        A sequence of sample sizes (one for each name)
    title: str
        The title of the plot
    x_label: str
        The label for the x-axis (e.g. "Agents" or "Teams")
    y_label: str
        The label for the y-axis
    confidence: float
        The confidence level for the confidence interval
    show: bool
        Whether to show the plot
    filename: str
        If given, saves the plot to a file
    colors: Optional[Sequence[str]]
        A sequence of colors (one for each name)
    yscale: str
        The scale for the y-axis (default: linear)
    """
    if flag:
        errors = [standard_error(std_devs[i], N[i], confidence) for i in range(len(means))]
    else:
        errors = None
    fig, ax = plt.subplots()
    x_pos = np.arange(len(names))
    ax.bar(x_pos, means, yerr=errors, align='center', alpha=0.5, color=colors if colors is not None else "gray", ecolor='black', capsize=10, width = 0.6)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(names)
    ax.set_title(title)
    ax.yaxis.set_ticks([0,20,40,60,80,100])   
    ax.yaxis.grid(True)

    if flag:
        #sets 60 y-value red
        aux = ax.get_ygridlines()[3]
        aux.set_color("red")
        aux.set_linewidth(1)
    
    if yscale is not None:
        plt.yscale(yscale)
    plt.tight_layout()
    if filename is not None:
        dpi = 100
        fig = plt.gcf()
        fig.set_size_inches((1800/dpi),(600/dpi))
        fig.savefig(filename, dpi=dpi)
    if show:
        plt.show()
    plt.close()


def createAvgScorePlots(results, confidence=0.95, title="Agents Comparison", metric="Avg. Points Per Simulation", colors=None, filename = None, show=True):

    """Displays a bar plot comparing the performance of different agents/teams.

        Parameters
        ----------

        results: dict
            A dictionary where keys are the names and the values sequences of trials
        confidence: float
            The confidence level for the confidence interval
        title: str
            The title of the plot
        metric: str
            The name of the metric for comparison
        colors: Sequence[str]
            A sequence of colors (one for each agent/team)

        """

    names = list(results.keys())
    means = [result.mean() for result in results.values()]
    stds = [result.std() for result in results.values()]
    N = [result.size for result in results.values()]

    plot_confidence_bar(
        names=names,
        means=means,
        std_devs=stds,
        N=N,
        title=title,
        x_label="", y_label= metric,
        confidence=confidence, show=show, filename = filename, colors=colors
    )


def calculateWinPrct(values):
    prct =  ((values > 60).sum()) / (len(values)) 
    return prct * 100

def createWinPerctPlots(key,results, confidence=0.95, title="Agents Comparison", metric="Win %", colors=None, filename = None, show=True):

    """Displays a bar plot comparing the performance of different agents/teams.

        Parameters
        ----------

        results: dict
            A dictionary where keys are the names and the values sequences of trials
        confidence: float
            The confidence level for the confidence interval
        title: str
            The title of the plot
        metric: str
            The name of the metric for comparison
        colors: Sequence[str]
            A sequence of colors (one for each agent/team)

        """

    names = list(results.keys())
    winPrct = [calculateWinPrct(result) for result in results.values()]
    f = open("winPrct.txt", "a")
    f.write(key + " : " + str(winPrct) + "\n")
    stds = [result.std() for result in results.values()]
    N = [result.size for result in results.values()]

    plot_confidence_bar(
        names=names,
        means=winPrct,
        std_devs=stds,
        N=N,
        title=title,
        x_label="", y_label=metric,
        confidence=confidence, show=show, filename = filename, colors=colors, flag=False
    )


