from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def analyze_keywords(low_rating_reviews, high_rating_reviews, top_n=20):
    # 한국어와 영어 모두를 다룰 수 있는 token_pattern 설정
    vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')

    low_rating_matrix = vectorizer.fit_transform(low_rating_reviews)
    low_rating_keywords = pd.DataFrame(low_rating_matrix.toarray(), columns=vectorizer.get_feature_names_out()).sum().sort_values(ascending=False)

    high_rating_matrix = vectorizer.fit_transform(high_rating_reviews)
    high_rating_keywords = pd.DataFrame(high_rating_matrix.toarray(), columns=vectorizer.get_feature_names_out()).sum().sort_values(ascending=False)

    low_rating_top_keywords = low_rating_keywords.head(top_n)
    high_rating_top_keywords = high_rating_keywords.head(top_n)

    return low_rating_top_keywords, high_rating_top_keywords
