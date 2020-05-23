import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, RBF


def get_vectorizer_score(vectorizer, regressor):
    vectorized = vectorizer.fit_transform(participant_responses)

    participant_train, participant_test, comparable_train, comparable_test = train_test_split(vectorized,
                                                                                              comparable_values)
    regressor.fit(participant_train.toarray(), comparable_train)

    participant_results = regressor.predict(participant_test.toarray())
    regressor_score = np.corrcoef(participant_results, comparable_test)
    return regressor_score[0,1]
    #The above line extracts the accuracy from the correlation matrix. It is a 2-by-2 and I ignore the identities.


def run_analysis():
    #For each vectorizer, I will take the average of scores based on number of reps decided by the user.
    for i in range(num_rep):
        for j in range(len_vectorizers):
            print("Processing", ((i * len_vectorizers) + j + 1), "in", (num_rep * len_vectorizers))
            vectorizer_results[j] = vectorizer_results[j] * i
            res = get_vectorizer_score(vectorizers[j], regressor)
            vectorizer_results[j] = vectorizer_results[j] + res
            vectorizer_results[j] = vectorizer_results[j] / (i + 1)
            # print(vectorizer_results[j])
        # print("----------")


def report_analysis():
    for i in range(len_vectorizers):
        print(vectorizer_names[i], ":", vectorizer_results[i])
    top_score = np.max(vectorizer_results)
    worst_score = np.min(vectorizer_results)
    top_vectorizer = vectorizer_names[vectorizer_results == top_score]
    worst_vectorizer = vectorizer_names[vectorizer_results == worst_score]
    print(f"Based on {num_rep} repetition(s), %s outperfroms with {top_score} accuracy." %top_vectorizer)
    print(f"%s, on the other hand, underperformed with {worst_score} accuracy." %worst_vectorizer)


#I read the data and place the relevant parts into separate Series. Please adjust file location.
hw_data = pd.read_csv('C:/Users/vsendemir/Desktop/Koc/2020Spring/QMBU450/immSurvey.csv')

participant_responses = hw_data["textToSend"]
comparable_values = hw_data["stanMeansNewSysPooled"]

#I will use the same regressor on all vectorizers, so I initialize it here.
rbf = ConstantKernel(1.0) * RBF(length_scale=1.0)
regressor = GaussianProcessRegressor(kernel=rbf, alpha=1e-7)
#I keep getting a convergence warning so I changed the alpha but I can't seem to get rid of the error.
#It doesn't stop the execution so I ignored the error after a point.

#I initialize vectorizers here
count_vectorizer = CountVectorizer()
tfid_vectorizer = TfidfVectorizer()
bigram_vectorizer = CountVectorizer(ngram_range=(2, 2), token_pattern=r'\b\w+\b', min_df=1)

#I place vectorizers and their names in numpy arrays. I initialize their scores as zeros.
vectorizers = np.array([count_vectorizer, tfid_vectorizer, bigram_vectorizer])
vectorizer_names = np.array(["count", "tfid", "bigram"])
vectorizer_results = np.zeros(len(vectorizers))

#I want to repeat the fitting a number of times as this process is random and I want to see a pattern.
num_rep = 5  #the greater the number of repetitions, the longer it takes...
len_vectorizers = len(vectorizers)

run_analysis()
report_analysis()

#I have run this with 20 reps and found count as best performing, yet it switches between count and tfid so I can't say
#anything conclusive about the best performing. However, the bigram does perform worst in all cases.
#I also fooled around with nltk but I didn't add it in here.
