import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import sys

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import PolynomialFeatures

labeled_df = pd.DataFrame()
full_df = pd.DataFrame()

vectorized_count = None
vectorized_tfidf = None


def _poly_fit(vectorized):
    poly = PolynomialFeatures(degree=2, include_bias=False)
    polorized = poly.fit_transform(vectorized)
    return polorized


def _vectorize():
    global vectorized_count, vectorized_tfidf
    count_vectorizer = CountVectorizer()
    tfidf_vectorizer = TfidfVectorizer()

    labeled_df_str = labeled_df["stem"].astype(str)

    vectorized_count = count_vectorizer.fit_transform(labeled_df_str)
    vectorized_tfidf = tfidf_vectorizer.fit_transform(labeled_df_str)

    #vectorized_count = _poly_fit(vectorized_count) #The dataset has over 70k words, a polyfeatures matrix
    #vectorized_tfidf = _poly_fit(vectorized_tfidf) #is too large to compute even with degree=2


def _train_classifier(vectorized, classifier):
    global labeled_df
    #x_train, x_test, y_train, y_test = train_test_split(vectorized, labeled_df["label"], test_size=0.5)
    a, b, c, d = train_test_split(labeled_df.index, labeled_df.index, test_size=0.4)
    x_train = vectorized[a]
    x_test = vectorized[b]
    y_train = labeled_df["label"][c]
    y_test = labeled_df["label"][d]

    classifier = classifier.fit(x_train, y_train)
    test_prediction = classifier.predict(x_test)
    #train_prediction = classifier.predict(x_train)

    score = accuracy_score(test_prediction, y_test)
    return score, classifier


def _test_classifiers(vectorized, num_rep):
    knn = KNeighborsClassifier(n_neighbors=2)
    abc = AdaBoostClassifier(n_estimators=100)
    rfc = RandomForestClassifier(max_depth=50)
    sgdc = SGDClassifier(max_iter=10000, tol=1e-8)
    nnc = MLPClassifier(solver='lbfgs', alpha=1e-8, max_iter=10000, hidden_layer_sizes=(8, 8, 8))
    svm = SVC(gamma='auto')
    lrc = LogisticRegression(max_iter=10000, tol=1e-8)
    dtc = DecisionTreeClassifier(max_depth=50)
    classifiers = {"KNN": knn,
                  "ABC": abc,
                  "RFC": rfc,
                  "SGDC": sgdc,
                  "NNC": nnc,
                  "SVM": svm,
                  "LRC": lrc,
                  "DTC": dtc}

    scores = {}
    for classifier in classifiers:
        scores_array = []
        for i in range(num_rep):
            scores_array.append(0)
        scores[classifier] = scores_array

    for i in range(num_rep):
        for classifier in classifiers:
            sys.stdout.write(f"\rTraining: {classifier} {(i + 1)} in {num_rep}")
            sys.stdout.flush()
            score, c = _train_classifier(vectorized, classifiers[classifier])
            scores[classifier][i] = score
        if i == (num_rep - 1):
            sys.stdout.write("\r")
            sys.stdout.flush()

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(scores)
    print(df)


def analyze(path, num_rep=10):
    global labeled_df, full_df

    labeled_df = pd.read_csv(f"{path}babacan_eksisozluk_labeled.csv")
    full_df = pd.read_csv(f"{path}babacan_eksisozluk_clean.csv")

    _vectorize()

    print("Count")
    _test_classifiers(vectorized_count, num_rep)
    print("Tfidf")
    _test_classifiers(vectorized_tfidf, num_rep)
