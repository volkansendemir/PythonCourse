import pandas as pd
import re
import sys
from snowballstemmer import TurkishStemmer
from turkishnlp import detector

df = pd.DataFrame()


def _remove_bkz(job):
    global df
    regexp = re.compile(r"\(\s?bkz:\s?[^\)]{2,100}\)")
    df_str = df["clean"].astype(str)
    length = df.shape[0]
    for index in range(length):
        _print_progress_bar(index, length, job=job, prefix=f"{job} Progress:", length=50)
        entry = df_str[index]
        if bool(re.search(regexp, entry)):
            for x in re.finditer(regexp, entry):
                match = x.group()
                suggest = " " + match[5:-1].strip() + " "
                entry = entry.replace(match, suggest)
            entry = re.sub(regexp, " ", entry)
            df["clean"][index] = entry.strip()


def _remove_entry_links(job):
    global df
    regexp = re.compile(r"(\(bkz:\s?)?#\d{8,10}(\))?")
    df_str = df["clean"].astype(str)
    length = df.shape[0]
    for index in range(length):
        _print_progress_bar(index, length, job=job, prefix=f"{job} Progress:", length=50)
        entry = df_str[index]
        if bool(re.search(regexp, entry)):
            entry = re.sub(regexp, "", entry)
            df["clean"][index] = entry.strip()


def _remove_http_links(job):
    global df
    regexp = re.compile(r"http[^\s]*")
    df_str = df["clean"].astype(str)
    length = df.shape[0]
    for index in range(length):
        _print_progress_bar(index, length, job=job, prefix=f"{job} Progress:", length=50)
        entry = df_str[index]
        if bool(re.search(regexp, entry)):
            entry = re.sub(regexp, " ", entry)
            df["clean"][index] = entry.strip()


def _fix_punctuation(job):
    global df
    regexp = re.compile(r"\s[\.\,\;\:\?\!]{1,3}")
    regexpp = re.compile(r"[\.\,\;\:\?\!]{1,3}")
    regexppp = re.compile(r"\'[^\s\.]*")
    regexpppp = re.compile(r"[\"\’\.\,\;\:\?\!\'\/]{1,3}")
    regexppppp = re.compile(r"[-]{2,999}")
    df_str = df["clean"].astype(str)
    length = df.shape[0]
    for index in range(length):
        _print_progress_bar(index, length, job=job, prefix=f"{job} Progress:", length=50)
        entry = df_str[index]
        if bool(re.search(regexp, entry)):
            for x in re.finditer(regexp, entry):
                match = x.group()
                suggest = match[1:] + " "
                entry = entry.replace(match, suggest)
            entry = re.sub(" +", " ", entry)
            df["clean"][index] = entry.strip()
        if bool(re.search(regexpp, entry)):
            for x in re.finditer(regexpp, entry):
                match = x.group()
                suggest = match + " "
                entry = entry.replace(match, suggest)
            entry = re.sub(" +", " ", entry)
            entry = re.sub("\. \.", "..", entry)
            entry = re.sub("\. \.", "..", entry)
            df["clean"][index] = entry.strip()
        if bool(re.search(regexppp, entry)):
            for x in re.finditer(regexppp, entry):
                match = x.group()
                entry = entry.replace(match, " ")
            df["clean"][index] = entry.strip()
        if bool(re.search(regexpppp, entry)):
            for x in re.finditer(regexpppp, entry):
                match = x.group()
                entry = entry.replace(match, " ")
            df["clean"][index] = entry.strip()
        if bool(re.search(regexppppp, entry)):
            for x in re.finditer(regexppppp, entry):
                match = x.group()
                entry = entry.replace(match, " ")
            df["clean"][index] = entry.strip()



def _fix_double_space(job):
    global df
    df_str = df["clean"].astype(str)
    length = df.shape[0]
    for index in range(length):
        _print_progress_bar(index, length, job=job, prefix=f"{job} Progress:", length=50)
        entry = df_str[index]
        entry = re.sub(" +", " ", entry)
        df["clean"][index] = entry


def _fix_letters(job):
    global df
    df_str = df["clean"].astype(str)
    length = df.shape[0]
    for index in range(length):
        _print_progress_bar(index, length, job=job, prefix=f"{job} Progress:", length=50)
        entry = df_str[index]
        entry = entry.replace("ç", "c").replace("ı", "i").replace("ğ", "g")
        entry = entry.replace("ö", "o").replace("ş", "s").replace("ü", "u")
        df["clean"][index] = entry


def _make_stem(job):
    global df
    df_str = df["stem"].astype(str)
    turk_stemmer = TurkishStemmer()
    length = df.shape[0]
    for index in range(length):
        _print_progress_bar(index, length, job=job, prefix=f"{job} Progress:", length=50)
        words = df_str[index].split()
        words = " ".join(turk_stemmer.stemWords(words))
        df["stem"][index] = words


def _auto_correct(job):
    global df
    df_str = df["corrected"].astype(str)
    obj = detector.TurkishNLP()
    #obj.download()
    obj.create_word_set()
    length = df.shape[0]
    for index in range(length):
        _print_progress_bar(index, length, job=job, prefix=f"{job} Progress:", length=50)
        if " " in df_str[index]:
            words = df_str[index].split()
            words = obj.auto_correct(words)
            words = " ".join(words)
            df["corrected"][index] = words


def _print_progress_bar(iteration, total, job="", prefix="", suffix="", decimals=1, length=100, fill="█"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    #print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end=print_end, flush=True)
    sys.stdout.write("\r%s |%s| %s%% %s (%s:%s)" % (prefix, bar, percent, suffix, iteration, total))
    sys.stdout.flush()

    if (iteration + 1) == total:
        sys.stdout.write(f"\r{job} complete\n")
        sys.stdout.flush()


def clean_up(path):
    global df
    df = pd.read_csv(f"{path}babacan_eksisozluk.csv", encoding="utf-8-sig")
    df["clean"] = df["content"]
    _remove_entry_links("Removing entry links")
    _remove_bkz("Removing bkz")
    _remove_http_links("Removing http links")
    _fix_punctuation("Fixing punctuation")
    _fix_double_space("Fixing double spaces")
    #_fix_letters("Fixing Turkish letters")
    #df = df[df["clean"] != ""]
    df["corrected"] = df["clean"]
    #_auto_correct("Correcting typos")#Takes a long time, be warned
    df["stem"] = df["corrected"]
    _make_stem("Finding stems")
    df = df[df["clean"] != ""]
    sys.stdout.write("Writing to csv.\r")
    df.to_csv(f"{path}babacan_eksisozluk_clean.csv", index=False, encoding="utf-8-sig")
    print("Writing to csv completed.")
    print("Clean-up completed.\n\n")
