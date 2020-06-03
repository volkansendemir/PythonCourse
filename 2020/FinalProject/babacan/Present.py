import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def _chart_period(df, period):
    mean = df.set_index("date").groupby(pd.Grouper(freq=period)).mean()["predictions"]
    count = df.set_index("date").groupby(pd.Grouper(freq=period)).count()["content"]

    x = count.index
    y = count

    clist = [(0, "red"), (0.5, "yellow"), (1, "green")]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clist)
    width = 1
    if period == "Y":
        width = 100
    elif period == "M":
        width = 20
    ax = plt.subplot(111)
    ax.bar(x, y, width=width, color=rvb(mean / 2), log=True)
    ax.xaxis_date()

    plt.xticks(rotation=60)

    plt.show()


def present(path):
    df = pd.read_csv(f"{path}babacan_eksisozluk_predictions.csv", encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["date"])
    #_chart_period(df, "D")
    #_chart_period(df, "Y")
    _chart_period(df, "M")
