import shutil
import urllib.request as request
from contextlib import closing
import gzip
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

    if (iteration + 1) == total:
        sys.stdout.write(f"\r{job} complete\n")
        sys.stdout.flush()


def _download_unzip_write(url_directory, path, year):
    #download
    with closing(request.urlopen(f"{url_directory}{year}.csv.gz")) as r:
        #unzip
        decompressed_file = gzip.GzipFile(fileobj=r)
        with open(f"{path}{year}.csv", "wb") as f:
            #write
            shutil.copyfileobj(decompressed_file, f)


url_directory = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/"
path = "C:/Users/vsendemir/Desktop/Koc/2020Spring/QMBU450/weather/"
years = range(1763, 1901)
#years = range(1901, 1951)
#years = range(1951, 2001)
#years = range(2000, 2021)
index = 1
length = len(years)
job = "Downloading "
for year in years:
    last_dl = datetime.datetime.now()
    _print_progress_bar(index, length, job=job, prefix=f"{job}{year} Progress:", suffix=last_dl, length=50)
    _download_unzip_write(url_directory, path, year)
    index += 1


