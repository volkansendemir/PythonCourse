import pandas as pd
import random as rand


def pick_random(path, multiplier):
    df = pd.read_csv(f"{path}babacan_eksisozluk_clean.csv", encoding="utf-8-sig")
    bool_array = []
    print("Picking at random.")
    for index in range(df.shape[0]):
        treshold = 0.05 * multiplier
        if index < 2000:
            treshold = 0.01 * multiplier
        elif index < 4000:
            treshold = 0.02 * multiplier
        elif index < 6000:
            treshold = 0.03 * multiplier
        elif index < 8000:
            treshold = 0.04 * multiplier

        if (rand.random() < treshold):
            bool_array.append(True)
        else:
            bool_array.append(False)
    df = df[bool_array]
    if df.shape[0] > (250 * multiplier):
        df = df[-(250 * multiplier):]
    print("Random pick completed.")
    print("Writing to csv.")
    df.to_csv(f"{path}babacan_eksisozluk_random.csv", index=False, encoding="utf-8-sig")
    print("Writing to csv completed.")
