from SentimentAnalysisBabacan.Download import download
from SentimentAnalysisBabacan.CleanUp import clean_up
from SentimentAnalysisBabacan.RandomPick import pick_random
from SentimentAnalysisBabacan.Analyze import analyze
from SentimentAnalysisBabacan.Predict import predict
from SentimentAnalysisBabacan.Present import present

path = "C:/Users/vsendemir/Desktop/Koc/2020Spring/QMBU450/babacan/"

#download(path)
#clean_up(path)
#pick_random(path=path, multiplier=3) #sample size = multiplier * 250
#the labeling process is manual
analyze(path, num_rep=10)#LRC and tfidf performed somewhat better
predict(path)
present(path)
