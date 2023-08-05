import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def vertical_bar(data: pd.DataFrame, label: str, value: str, ax=None, ratio=True, fontsize=14):
    if ax is None:
        n = data.shape[0]
        fig = plt.figure(figsize=(16, 1 * n))
        ax = fig.add_subplot(1, 1, 1)

    labels = getattr(data, label)
    values = getattr(data, value)

    max_ = values.max()
    sum_ = values.sum()
    base = sum_ # TODO: max version for base

    sns.barplot(x=value, y=label, data=data.reset_index(), ax=ax, order=labels)
    margin = ax.get_xlim()[1]  / 100 

    for i, (l, v) in enumerate(zip(labels, values)):
        text = f'{v}'
        if ratio:
            v_ratio = v / base
            text = f'{text} ({v_ratio:.1%})'
        ax.text(v + margin, i, text, color='black', ha="left", va='center', fontsize=fontsize)

    [spine.set_visible(False) for spine in ax.spines.values()]
    ax.tick_params(bottom=False, left=False, labelbottom=False)
    ax.tick_params(axis='y', labelsize='x-large')

    return ax