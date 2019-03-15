import numpy as np
import pandas as pd

#the following method first checks for type errors (it accepts only numpy ints or floats), then it sorts the data ascendingly first by datay, then by datax.
#the method then removes any NaNs first backward and then forward.
def sortData(datax, datay):
        if len(datax) != len(datay):
            raise Exception("Data lengths do not match!")

        for i in range(0, len(datax)):
            if 'numpy.int32' not in str(type(datax[i])) and 'numpy.int64' not in str(type(datax[i])) and 'numpy.float32' not in str(type(datax[i])) and 'numpy.float64' not in str(type(datax[i])):
                raise Exception("Data must contain only int or float!")
            if 'numpy.int32' not in str(type(datay[i])) and 'numpy.int64' not in str(type(datay[i])) and 'numpy.float32' not in str(type(datay[i])) and 'numpy.float64' not in str(type(datay[i])):
                raise Exception("Data must contain only int or float!"+str(type(datay[i])))
        temp = order(datay, datax)
        return order(temp[1], temp[0])

def order(datax, datay):
#because recursion failed as the data got too big for it, I had to resort to this type of a while loop construct.
#this is the method that sorts ascendingly.
        boolean = True
        while boolean:
            boolean = False
            for i in range(0, (len(datax) - 1)):
                if datax[i] > datax[i + 1]:
                    boolean = True
                    temp = datax[i]
                    datax[i] = datax[i + 1]
                    datax[i + 1] = temp
                    temp = datay[i]
                    datay[i] = datay[i + 1]
                    datay[i + 1] = temp
        moddatax = pd.array(datax).fillna(method='bfill').fillna(method='ffill')
        moddatay = pd.array(datay).fillna(method='bfill').fillna(method='ffill')
        return pd.DataFrame(np.array([moddatax, moddatay])).values

        #for i in range(0, (len(datax) - 1)):
        #    if datax[i] > datax[i + 1]:
        #        temp = datax[i]
        #        datax[i] = datax[i + 1]
        #        datax[i + 1] = temp
        #        temp = datay[i]
        #        datay[i] = datay[i + 1]
        #        datay[i + 1] = temp
        #        return order(datax, datay)
        #return pd.DataFrame(np.array([datax, datay])).fillna(method='bfill').fillna(method='ffill').values
