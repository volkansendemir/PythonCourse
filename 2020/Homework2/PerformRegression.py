import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

def print_regression_table(regStats, upper_anova, lower_anova):
    print("-------------------------------------------------------------------------------------")
    print(regStats)
    print("---------------ANOVA-----------------------------------------------------------------")
    print(upper_anova)
    print("-------------------------------------------------------------------------------------")
    print(lower_anova)


def regression_table(X, y, var_names, has_chart, dates, prediction_delay):
    betas = np.linalg.inv(X.T@X)@X.T@y
    yhat = X @ betas
    errors = y - yhat
    stdsq = (errors.T @ errors) / (len(errors) - len(betas))
    serrs = np.sqrt(np.diagonal(np.multiply(stdsq, np.linalg.inv(X.T @ X))))
    conf_level = 95
    t_coef = stats.t.ppf(1 - ((100 - conf_level) / 200), len(errors))
    conf_upper = betas + t_coef * serrs
    conf_lower = betas - t_coef * serrs
    my = np.mean(y)
    dfr = len(betas) - 1
    dfe = len(y) - len(betas)
    dft = dfe + dfr
    sse = np.sum(np.square(errors))
    mse = sse / dfe
    ssr = np.sum(np.square(yhat - my))
    msr = ssr / dfr
    sst = ssr + sse

    bigF = msr / mse
    sig_f = 1 - stats.f.cdf(bigF,dfr, dfe)

    r_sq = ssr / sst
    mr = np.sqrt(r_sq)
    adj_r_sq = 1 - (1 - r_sq) * ((len(errors) - 1) / (len(errors) - len(betas)))
    sterr = np.sqrt(mse)
    obs = len(y)

    t_stats = betas / serrs
    p_values = stats.t.sf(t_stats, len(errors) - 1) * 2

    pd.set_option("display.max_columns", 10)
    pd.set_option("display.width", 500)

    regStats = pd.DataFrame(data=[round(mr, 5),
                                  round(r_sq, 5),
                                  round(adj_r_sq, 5),
                                  round(sterr, 5),
                                  round(obs, 0)],
                            index=["Multiple R","R Square", "Adjusted R Square","Standard Error","Observations"],
                            columns=["Regression Statistics"])
    upper_anova = pd.DataFrame(data=np.array([[round(dfr, 0), round(dfe, 0), round(dft, 0)],
                                        [round(ssr, 0), round(sse, 0), round(sst, 0)],
                                        [round(msr, 0), round(mse, 0), ""],
                                        [round(bigF, 5), "", ""],
                                        [round(sig_f, 5), "", ""]]).T,
                            index=["Regression", "Residual", "Total"],
                            columns=["df", "SS", "MS", "F", "Significance F"])
    lower_anova = pd.DataFrame(data=np.array([betas,
                                        serrs,
                                        t_stats,
                                        p_values,
                                        conf_lower,
                                        conf_upper]).T,
                            index=var_names,
                            columns=["Coefficients", "Standard Error", "t Stat", "P-value", "Lower 95%", "Upper 95%"])

    #forward_predictions =

    if has_chart:
        plt.plot(dates, yhat, linestyle="-", color="green", linewidth=2, label="predicted")
        plt.plot(dates, y, linestyle="dotted", color="blue", linewidth=1, label="actual")
        plt.gca().set_xticks(
            ["2017-03-06", "2017-09-06", "2018-03-06", "2018-09-06", "2019-03-06", "2019-09-06", "2020-03-06"])
        # plt.xlim(left="2019-06-06", right="2019-09-06")
        # plt.ylim(top=13500,bottom=8000)
        plt.xticks(rotation=30)
        plt.gca().xaxis.grid(linestyle="--")
        # plt.gca().invert_xaxis()
        plt.xlabel("Dates")
        plt.ylabel("BTC/USD")
        plt.title("BTC/USD Real vs Predicted in " + str(prediction_delay) + " Day(s) in Advance")
        plt.legend(loc="upper left")
        plt.show()

    print_regression_table(regStats, upper_anova, lower_anova)


def hasMulticollinearity(bigX):
    for i in range(1, bigX.T.shape[0]):#I am checking for a linear relationship between columns.
        for j in range(i + 1, bigX.T.shape[0]):#If there is linearity, the ratio of each element would be the same.
            farr = bigX.T[i]
            sarr = bigX.T[j]
            divarr = (farr / sarr)#ratio of columns
            hasMC = True
            for k in range(2, len(divarr)):
                hasMC = hasMC & (round(divarr[0], 7) == round(divarr[k-1], 7))#Even if one is different, hasMC is false
            if hasMC:
                return True
    return False


def run_preset_regression(path, has_chart, prediction_delay):
    y_name = "btc_Price"
    bigX = pd.read_csv(path + "regression.csv")

    dates = bigX["Date"]
    bigX.pop("Date")

    bigX = bigX.ffill().bfill()

    smallY = np.array(bigX[y_name])

    bigX.pop(y_name)

    variable_names = np.array(bigX.columns)
    variable_names = np.insert(variable_names, 0, "Intercept", axis=0)

    bigX = np.array(bigX).T
    bigX = np.vstack([np.ones(len(smallY)), bigX]).T

    if hasMulticollinearity(bigX):
        print("Multicollinearity detected.")
    elif bigX.shape[0] == smallY.shape[0] and bigX.shape[1] == variable_names.shape[0]:
        regression_table(bigX, smallY, variable_names, has_chart, dates, prediction_delay)
    else:
        print("Dimensions do not fit.")


def run_custom_regression(file_location_and_name, y_column_name):
    bigX = pd.read_csv(file_location_and_name)
    bigX.reset_index()
    bigX.pop(bigX.columns[0])
    smallY = bigX[y_column_name]
    bigX.pop(y_column_name)
    if hasMulticollinearity(bigX):
        print("Multicollinearity detected.")
    elif bigX.shape[0] == smallY.shape[0] and bigX.shape[1] == bigX.columns.shape[0]:
        variable_names = bigX.columns
        variable_names = np.insert(variable_names, 0, "Intercept", axis=0)
        bigX = np.array(bigX).T
        bigX = pd.DataFrame(np.vstack([np.ones(len(smallY)), bigX]).T)
        bigX = bigX.bfill().ffill()
        smallY = pd.Series(smallY)
        smallY = smallY.bfill().ffill()
        smallY = np.array(smallY)
        regression_table(bigX, smallY, variable_names, False, np.empty(1), 0)
    else:
        print("Dimensions do not fit.")


your_path = "C:/Users/user/Desktop/" #should be the same path as in part-2 as that is where the files will be read from.
delay_in_days = 0
show_chart = False
run_preset_regression(your_path, show_chart, delay_in_days)
#run_custom_regression("C:/Users/user/Desktop/example.csv", "example")
