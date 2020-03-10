import numpy as np
import pandas as pd
import wbdata
from homeworkOne import RegressionCalculator as rc
from homeworkOne import CleanData as cd

#gathers data from worldbank API
indicators = {'FP.CPI.TOTL.ZG': 'inflation', 'SL.UEM.TOTL.NE.ZS': 'unemployment'}
df = wbdata.get_dataframe(indicators, country='TUR')
df.to_csv('C:/Users/user/Desktop/regression data.csv')
#writes the data into a csv file at the defined location
inflationArray = df['inflation'].values
unemploymentArray = df['unemployment'].values
#data is split into numpy arrays as the CleanData class will check this data for type and will perform operations on numpy arrays

dataxy = cd.sortData(inflationArray, unemploymentArray)
#the return type of sortData is pandas.DataFrame, so the data is once again split into two to be passed on to the regression method
inflationArray = dataxy[0]
unemploymentArray = dataxy[1]

#Arguments: (independent variable, dependent variable, backward limit, forward projection, boolean isTimeSeries) -> read RegressionCalculator comments for more info
betas = rc.regress(inflationArray, unemploymentArray, len(inflationArray), 10, False)
#the regression method should take lim = len(independent variable), forward is not important, isTimeSeries need to be False
print('b0\t\t b1')
print(round(betas[0], 4),round(betas[1], 4))

beta0 = betas[0]
beta1 = betas[1]

predictions = (beta0 + (inflationArray*beta1))
np.set_printoptions(suppress=True)
errors = (predictions - unemploymentArray)
absErrors = np.abs(errors)
absPercErrors = (absErrors / unemploymentArray)
meanAbsPercError = np.average(absPercErrors)
print('MeanAbsolutePercentageError: ' + str(round(meanAbsPercError, 4)))

squaredErrors = np.square(errors)
rootMeanSquaredError = np.sqrt(np.average(squaredErrors))
#I used this formula for the prediction interval. yhat +- (2*rmse) for 95% interval.
upper95 = (predictions + 2*rootMeanSquaredError)
lower95 = (predictions - 2*rootMeanSquaredError)
outlier = ((unemploymentArray > upper95) | (unemploymentArray < lower95))

(np.array([inflationArray, unemploymentArray, upper95, predictions, lower95, errors]))
results = pd.DataFrame({'inflation': inflationArray, 'unemployment': unemploymentArray, 'upper': upper95, 'predictions': predictions, 'lower': lower95, 'outlier': outlier, 'error': errors})
print(results)
