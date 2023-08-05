import matplotlib.pyplot as plt
import pandas as pd

def stack_vertical_bar(data: pd.DataFrame, label: str, value: str, ax=None, fontsize=20):
    if ax is None:
        fig = plt.figure(figsize=(16, 2))
        ax = fig.add_subplot(1, 1, 1)

    labels = getattr(data, label)
    values = getattr(data, value)

    sum_ = values.sum()
    before_rate = 0

    for l, v in zip(labels, values):
        rate = v / sum_
        x = before_rate + rate

        ax.barh(0, x, left=before_rate)
        text_x = before_rate + rate / 2
        text = f"{l}\n{value} ({rate:.1%})"
        ax.text(text_x, 0, text, fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
        before_rate = x
    ax.grid(False)
    ax.set_xlim(0, 1)
    ax.tick_params(axis='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    [spine.set_visible(False) for spine in ax.spines.values()]

    return ax