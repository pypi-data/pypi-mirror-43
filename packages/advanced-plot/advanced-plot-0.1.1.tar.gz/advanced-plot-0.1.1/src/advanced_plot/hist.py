import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def hist(data: pd.Series, ax=None, ratio=True, fontsize=20, distplot_opt={}):
    if ax is None:
        n = data.shape[0]
        fig = plt.figure(figsize=(16, 5))
        ax = fig.add_subplot(1, 1, 1)

    all_ = data.shape[0]
    mean = data.mean().round(1)
    median = data.median().round(1)
    mode = data.mode().values[0].round(1)

    sns.distplot(data, ax=ax, **distplot_opt)

    text = f"""All: {all_}
Mean: {mean}
Median: {median}
Mode: {mode}"""

    ax.text( 0.99, 0.99, text, ha='right', va='top', transform=ax.transAxes, fontsize=fontsize)