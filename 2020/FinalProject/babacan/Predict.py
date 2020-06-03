import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def predict(path):
    labeled_df = pd.read_csv(f"{path}babacan_eksisozluk_labeled.csv")
    full_df = pd.read_csv(f"{path}babacan_eksisozluk_clean.csv")

    tfidf_vectorizer = TfidfVectorizer()

    labeled_df_str = labeled_df["stem"].astype(str)

    vectorized_tfidf = tfidf_vectorizer.fit_transform(labeled_df_str)

    lrc = LogisticRegression(max_iter=10000, tol=1e-8)

    lrc = lrc.fit(vectorized_tfidf, labeled_df["label"])

    labeled_df_str = full_df["stem"].astype(str)

    tfidf_vectorizer = TfidfVectorizer(vocabulary=tfidf_vectorizer.vocabulary_)
    vectorized_tfidf = tfidf_vectorizer.fit_transform(labeled_df_str)

    predictions = lrc.predict(vectorized_tfidf)

    full_df["predictions"] = predictions

    full_df = full_df[["date", "content", "predictions"]]

    full_df.to_csv(f"{path}babacan_eksisozluk_predictions.csv", index=False, encoding="utf-8-sig")
