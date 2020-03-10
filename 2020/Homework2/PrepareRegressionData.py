import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def readDF(path, precursor):
    tempDF = pd.read_csv(path + precursor + ".csv")
    tempDF.columns = precursor + "_" + tempDF.columns
    tempDF = tempDF.iloc[::-1]
    tempDF.set_index(precursor + "_Date", inplace=True)
    return tempDF

def add_bollingers(selDF, window, no_of_std, precursor):
    rolling_mean = selDF[precursor + "_Price"].rolling(window).mean()
    rolling_std = selDF[precursor + "_Price"].rolling(window).std()

    selDF[precursor + "_Bollinger High"] = rolling_mean + (rolling_std * no_of_std)
    selDF[precursor + "_Bollinger Low"] = rolling_mean - (rolling_std * no_of_std)


def add_fibonacci(selDF, precursor):
    fib100 = np.max(selDF[precursor + "_High"].tail(500))
    fib0 = np.min(selDF[precursor + "_Low"].tail(500))
    fib161 = (((fib100 - fib0) * 1.618034) + fib0)
    fib61 = (((fib100 - fib0) * 0.618034) + fib0)
    fib38 = (((fib100 - fib0) * 0.381966) + fib0)
    fib23 = (((fib100 - fib0) * 0.236068) + fib0)

    priceLen = len(selDF[precursor + "_Price"])
    selDF["Fib 100"] = np.ones(priceLen) * fib100
    selDF["Fib 0"] = np.ones(priceLen) * fib0
    selDF["Fib 161"] = np.ones(priceLen) * fib161
    selDF["Fib 61"] = np.ones(priceLen) * fib61
    selDF["Fib 38"] = np.ones(priceLen) * fib38
    selDF["Fib 23"] = np.ones(priceLen) * fib23


def add_moving_averages(selDF, precursor):
    selDF[precursor + "_ma50"] = selDF[precursor + "_Open"].rolling(50).mean()
    selDF[precursor + "_ma20"] = selDF[precursor + "_Open"].rolling(20).mean()


def plot_unregressed(selDF, precursor, prediction_delay):
    plt.plot(selDF[precursor + "_ma50"], linestyle="--", linewidth=1, label="MA 50")
    plt.plot(selDF[precursor + "_ma20"], linestyle="--", linewidth=1, label="MA 20")

    plt.plot(selDF.index, selDF[precursor + "_Price"], linestyle="-", color="blue", label="actual")
    # plt.plot(selDF.index, selDF[precursor + "_Bollinger High"], linestyle="dotted", color="green", linewidth=1,)
    # plt.plot(selDF.index, selDF[precursor + "_Bollinger Low"], linestyle="dotted", color="red", linewidth=1)
    plt.plot(selDF.index, selDF[precursor + "_High"], linestyle="dotted", color="green", linewidth=1, label="High")
    plt.plot(selDF.index, selDF[precursor + "_Low"], linestyle="dotted", color="red", linewidth=1, label="Low")
    plt.plot(selDF.index, selDF["Fib 100"], linestyle="-", color="green", linewidth=1, label="1.00")
    plt.plot(selDF.index, selDF["Fib 0"], linestyle="-", color="red", linewidth=1, label="0.00")
    plt.plot(selDF.index, selDF["Fib 161"], linestyle="dotted", color="purple", linewidth=1)
    plt.plot(selDF.index, selDF["Fib 61"], linestyle="dotted", color="purple", linewidth=1, label="Fibs")
    plt.plot(selDF.index, selDF["Fib 38"], linestyle="dotted", color="purple", linewidth=1)
    plt.plot(selDF.index, selDF["Fib 23"], linestyle="dotted", color="purple", linewidth=1)

    plt.gca().set_xticks(["2017-03-06", "2017-09-06", "2018-03-06", "2018-09-06", "2019-03-06", "2019-09-06", "2020-03-06"])
    # plt.xlim(left="2019-06-06", right="2019-09-06")
    # plt.ylim(top=13500,bottom=8000)
    plt.xticks(rotation=30)
    plt.gca().xaxis.grid(linestyle="--")
    # plt.gca().invert_xaxis()
    plt.xlabel("Dates")
    plt.ylabel("BTC/USD")
    plt.title("BTC/USD Real with detail, " + str(prediction_delay) + " Day(s) in Advance")
    plt.legend(loc="upper left", ncol=5)
    plt.show()


def add_x_variables(selDF1, selDF2, precursor, prediction_delay):
    fibs = ["Fib 100", "Fib 0", "Fib 161", "Fib 61", "Fib 38", "Fib 23"]
    fib_pull_factor = np.zeros(len(selDF1[precursor + "_Price"]))
    for fib in fibs:
        temp_factor = (selDF1[precursor + "_High"] - selDF1[fib])
        temp_factor = temp_factor * (selDF1[fib] < selDF1[precursor + "_High"])
        fib_pull_factor = fib_pull_factor + temp_factor
    fib_pull_factor = fib_pull_factor * fib_pull_factor
    fib_push_factor = np.zeros(len(selDF1[precursor + "_Price"]))
    for fib in fibs:
        temp_factor = (selDF1[fib] - selDF1[precursor + "_Low"])
        temp_factor = temp_factor * (selDF1[fib] > selDF1[precursor + "_Low"])
        fib_push_factor = fib_push_factor + temp_factor
    fib_push_factor = fib_push_factor * fib_push_factor
    bollinger_pull_factor = np.zeros(len(selDF1[precursor + "_Price"]))
    bollinger_pull_factor = (selDF1[precursor + "_Bollinger High"] - selDF1[precursor + "_Price"])
    bollinger_pull_factor = bollinger_pull_factor * (selDF1[precursor + "_Bollinger High"] > selDF1[precursor + "_Price"])
    bollinger_pull_factor = bollinger_pull_factor * bollinger_pull_factor
    bollinger_push_factor = np.zeros(len(selDF1[precursor + "_Price"]))
    bollinger_push_factor = (selDF1[precursor + "_Price"] - selDF1[precursor + "_Bollinger Low"])
    bollinger_push_factor = bollinger_push_factor * (selDF1[precursor + "_Bollinger Low"] < selDF1[precursor + "_Price"])
    bollinger_push_factor = bollinger_push_factor * bollinger_push_factor

    fin_DF = pd.DataFrame()
    ma_pull = (selDF1[precursor + "_ma20"] - selDF1[precursor + "_ma50"])
    data_length = len(selDF1[precursor + "_Price"])
    nan_array = np.empty(prediction_delay)
    nan_array[:] = np.nan
    fin_DF["ma_trend"] = np.insert(np.array(ma_pull[0:(data_length - prediction_delay):]), 0, nan_array, axis=0)
    fin_DF["bollinger_pull"] = np.insert(np.array(bollinger_pull_factor[0:(data_length - prediction_delay):]), 0,
                                         nan_array, axis=0)
    fin_DF["bollinger_push"] = np.insert(np.array(bollinger_push_factor[0:(data_length - prediction_delay):]), 0, nan_array, axis=0)
    fin_DF["fib_pull"] = np.insert(np.array(fib_pull_factor[0:(data_length - prediction_delay):]), 0, nan_array, axis=0)
    fin_DF["fib_push"] = np.insert(np.array(fib_push_factor[0:(data_length - prediction_delay):]), 0, nan_array, axis=0)
    vol = selDF1[precursor + "_Vol."]
    fin_DF["Volume"] = np.insert(np.array(vol[0:(data_length - prediction_delay):]), 0, nan_array, axis=0)
    fin_DF["Date"] = selDF1.index
    fin_DF.set_index("Date", inplace=True)
    selDF1["xau_Price"] = selDF2["xau_Price"]
    selDF1.ffill().bfill()
    fin_DF["xau_Price"] = np.insert(np.array(selDF1["xau_Price"][0:(data_length - prediction_delay):]), 0, nan_array, axis=0)
    return fin_DF


def prepare_data(path, show_chart):
    print("Data preparation started.")

    btc_df = readDF(path, "btc")
    xau_df = readDF(path, "xau")

    add_bollingers(btc_df, 20, 3, "btc")
    add_fibonacci(btc_df, "btc")
    add_moving_averages(btc_df, "btc")

    btc_df = btc_df.ffill().bfill()

    final_DF = add_x_variables(btc_df, xau_df, "btc", delay_in_days)
    final_DF["btc_Price"] = btc_df["btc_Price"]
    final_DF = final_DF.ffill().bfill()
    final_DF.to_csv(your_path + "regression.csv")

    print("Data preparation completed.")

    if show_chart:
        plot_unregressed(btc_df, "btc", delay_in_days)


your_path = "C:/Users/user/Desktop/"
show_chart = False
delay_in_days = 0
prepare_data(your_path, show_chart)
