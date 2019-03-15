#this method is a flexible method I devised both for this homework and some extracurricular stuff. It was designed to apply linear regression to data pairs
#in a sort of "moving" manner. It takes a specified amount of previous observations and predicts the next outcome based on their betas. For this homework
#limit = len(datax), forward is not effective and isTimeSeries is False.
def regress(datax, datay, limit, forward, isTimeSeries):
#datax -> random variable / covariant
#datay -> response variable / outcome
#limit -> range of data used for the regression. limit = len(datax) if we are using all data points. I was also working on a "moving regression calculator"
#forward -> makes predictions moving forward from the last observation point. Again, I was working with time series, if limit = len(datax) we wont be using this
#isTimeSeries -> this is false since we are not interested in the time aspect of the data for this example

#the regression formula -> b0 = ybar - xbar*b1  |   b1 = sum( (xi-xbar)*(yi-ybar) ) / sum( (xi-xbar)^2 )
        projections = []
        for i in range((limit - 1), (len(datay))):
            sumx = 0
            sumy = 0
            for j in range(0, limit):
                sumx += datax[i - limit + j]
                sumy += datay[i - limit + j]
            averagex = sumx / limit
            averagey = sumy / limit
            top = 0
            bot = 0
            for j in range(0, limit):
                top += ((datax[i - limit + j] - averagex) * (datay[i - limit + j] - averagey))
                bot += ((datax[i - limit + j] - averagex) * (datax[i - limit + j] - averagex))
            b1 = top / bot
            b0 = (averagey - (averagex * b1))
            projection = (b0 + (b1 * datax[i]))
            projections.append(round(projection, 2))
#the beta values are returned as an array where [0] is b0 and [1] is b1
            if (limit == len(datax)) and not isTimeSeries:
                return (b0, b1)
            
#the remainder of this method is never accessed in this example as betas are returned above
            if isTimeSeries and (i == (len(datay) - 1)):
                for j in range(0, forward):
                    sumx = 0
                    sumy = 0
                    for l in range(0, limit):
                        sumx += datax[len(datax) - 1 - l]
                        sumy += datay[len(datay) - 1 - l]
                    averagex = sumx / limit
                    averagey = sumy / limit
                    top = 0
                    bot = 0
                    for l in range(0, limit):
                        top += ((datax[len(datax) - 1 - l] - averagex) * (datay[len(datay) - 1 - l] - averagey))
                        bot += ((datax[len(datax) - 1 - l] - averagex) * (datax[len(datax) - 1 - l] - averagex))
                    b1 = top / bot
                    b0 = (averagey - (averagex * b1))
                    projection = (b0 + (b1 * (datax[len(datax) - 1] + j + 1)))
                    projections.append(round(projection, 2))
        return projections
