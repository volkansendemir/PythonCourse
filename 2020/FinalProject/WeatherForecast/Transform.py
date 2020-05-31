import pandas as pd
import numpy as np
import sys
import datetime


def _print_progress_bar(iteration, total, job="", prefix="", suffix="", decimals=1, length=100, fill="█"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    #print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end=print_end, flush=True)
    sys.stdout.write("\r%s |%s| %s%% (%s:%s) %s" % (prefix, bar, percent, iteration, total, suffix))
    sys.stdout.flush()


def _create_pivot(path, year):
    df = pd.read_csv(f"{path}Raw/{year}.csv", header=None, usecols=[0, 1, 2, 3])
    df.columns = ["loc", "day", "prop", "value"]
    df = df.pivot_table(index=["loc", "day"],
                        columns="prop",
                        values="value",
                        aggfunc="first")
    df.reset_index().rename_axis(None, axis=1)
    df.to_csv(f"{path}Pivot/{year}_pivot.csv")


path = "C:/Users/vsendemir/Desktop/Koc/2020Spring/QMBU450/weather/"
#years = range(1763, 1901)
#years = range(1901, 1951)
years = range(1947, 1951)
#years = range(1951, 2001)
#years = range(2001, 2021)
iteration = 1
total = len(years)
job = "Transforming "
times = []
average_time = 0
for year in years:
    init_time = datetime.datetime.now().timestamp()
    _print_progress_bar(iteration, total, job=job, prefix=f"{job}{year} Progress:", suffix=average_time, length=50)
    _create_pivot(path, year)
    done_time = datetime.datetime.now().timestamp()
    passed_time = done_time - init_time
    times.append(passed_time)
    average_time = datetime.datetime.utcfromtimestamp(np.average(times))
    iteration += 1
    if iteration == total:
        job = "Transformation "
        sys.stdout.write(f"\r{job} complete\n")
        sys.stdout.flush()
