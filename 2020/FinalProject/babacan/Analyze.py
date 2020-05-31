import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from snowballstemmer import TurkishStemmer

labeled_df = pd.DataFrame()
full_df = pd.DataFrame()

vectorized_count = None
vectorized_tfidf = None


def analyze(path):
    global labeled_df, full_df
    labeled_df = pd.read_csv(f"{path}babacan_eksisozluk_labeled.csv")
    full_df = pd.read_csv(f"{path}babacan_eksisozluk_clean.csv")

    _vectorize()

    _test_classifiers(vectorized_tfidf)


def _make_stem(labeled_df_str):
    turk_stemmer = TurkishStemmer()
    for i in range(labeled_df_str.shape[0]):
        words = labeled_df_str[i].split()
        words = " ".join(turk_stemmer.stemWords(words))
        labeled_df_str[i] = words
    return labeled_df_str


def _vectorize():
    global vectorized_count, vectorized_tfidf
    count_vectorizer = CountVectorizer()
    tfidf_vectorizer = TfidfVectorizer()

    labeled_df_str = labeled_df["stem"].astype(str)

    labeled_df_str = _make_stem(labeled_df_str)

    vectorized_count = count_vectorizer.fit_transform(labeled_df_str)
    vectorized_tfidf = tfidf_vectorizer.fit_transform(labeled_df_str)


def _train_classifier(vectorized, classifier, is_dense):
    global labeled_df
    x_train, x_test, y_train, y_test = train_test_split(vectorized, labeled_df["label"], test_size=0.5)
    a, b, c, d = train_test_split(labeled_df.index, labeled_df.index, test_size=0.5)
    x_train = vectorized[a]
    x_test = vectorized[b]
    y_train = labeled_df["label"][c]
    y_test = labeled_df["label"][d]

    #if is_dense:
        #print(x_train)
        #classifier = classifier.fit(np.array(x_train), np.array(y_train))
    #else:
    classifier = classifier.fit(x_train, y_train)
    test_prediction = classifier.predict(x_test)
    train_prediction = classifier.predict(x_train)





    score = accuracy_score(test_prediction, y_test)
    return score, classifier


def _train_classifiers(vectorized, classifiers, is_dense):
    global labeled_df
    x_train, x_test, y_train, y_test = train_test_split(vectorized, labeled_df["label"], test_size=0.5)
    a, b, c, d = train_test_split(labeled_df.index, labeled_df.index, test_size=0.5)
    x_train = vectorized[a]
    x_test = vectorized[b]
    y_train = labeled_df["label"][c]
    y_test = labeled_df["label"][d]

    #if is_dense:
        #print(x_train)
        #classifier = classifier.fit(np.array(x_train), np.array(y_train))
    #else:
    cumu_prediction = np.zeros(y_test.shape[0])
    for classifier in classifiers:
        classifier = classifiers[classifier].fit(x_train, y_train)
        test_prediction = classifier.predict(x_test)
        train_prediction = classifier.predict(x_train)
        cumu_prediction += test_prediction

    cumu_prediction = cumu_prediction / len(classifiers)
    for i in range(len(cumu_prediction)):
        if cumu_prediction[i] < (2/3):
            cumu_prediction[i] = 0
        elif cumu_prediction[i] < (4/3):
            cumu_prediction[i] = 1
        else:
            cumu_prediction[i] = 2
    score = accuracy_score(cumu_prediction, y_test)
    for i in range(len(a)):
        content = labeled_df["content"][a[i]]
        supposed_label = labeled_df["label"][a[i]]
        predicted_label = cumu_prediction[i]
        print(supposed_label, predicted_label, content)

    return score, classifier


def _test_classifiers(vectorized):
    knn = KNeighborsClassifier(n_neighbors=2)
    gnb = GaussianNB()
    abc = AdaBoostClassifier(n_estimators=100)
    rfc = RandomForestClassifier(max_depth=50)
    sgdc = SGDClassifier(max_iter=10000, tol=1e-8)
    nnc = MLPClassifier(solver='lbfgs', alpha=1e-8, max_iter=10000, hidden_layer_sizes=(8, 8, 8))
    svm = SVC(gamma='auto')
    lrc = LogisticRegression(max_iter=10000, tol=1e-8)
    dtc = DecisionTreeClassifier(max_depth=50)
    classifiers = {"KNN": knn,
                  #"GNB": gnb,
                  "ABC": abc,
                  "RFC": rfc,
                  "SGDC": sgdc,
                  "NNC": nnc,
                  "SVM": svm,
                  "LRC": lrc,
                  "DTC": dtc}

    rep_count = 25

    score, c = _train_classifiers(vectorized, classifiers, False)
    print(score)

    return
    scores = {}
    for classifier in classifiers:
        scores_array = []
        for i in range(rep_count):
            scores_array.append([0, classifiers[classifier]])
        scores[classifier] = scores_array

    for i in range(rep_count):
        for classifier in classifiers:
            print("Training:", classifier, f"{(i + 1)} in {rep_count}")
            score, c = _train_classifier(vectorized, classifiers[classifier], (classifier == "GNB"))
            scores[classifier][i] = [score, c]
            print(scores[classifier][i][0])



path = "C:/Users/vsendemir/Desktop/Koc/2020Spring/QMBU450/babacan/"
analyze(path)


