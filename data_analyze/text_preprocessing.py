from konlpy.tag import Okt

def preprocess_text(all_reviews):
    stop_words = [
        '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다',
        '그리고', '하지만', '그러나', '그래서', '때문에', '따라서', '이후', '동안', '그런데', '게다가', '때문', '및', '또한',
        '사용', '은행', '너무', '하고', '에서', '있어서', '입니다', '해서', '다른', '사용', '계속', '하는'
        'the', 'and', 'is', 'to', 'it', 'in', 'this', 'of', 'for', 'with', 'that', 'on', 'are', 'as', 'at', 'by', 'an', "app", "not", "good"
    ]

    okt = Okt()

    low_rating_reviews = all_reviews[all_reviews['rating'] <= 3]['review']
    high_rating_reviews = all_reviews[all_reviews['rating'] >= 4]['review']

    def tokenize_and_remove_stopwords(text):
        tokens = okt.morphs(text)
        tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
        return ' '.join(tokens)

    low_rating_reviews = low_rating_reviews.apply(tokenize_and_remove_stopwords)
    high_rating_reviews = high_rating_reviews.apply(tokenize_and_remove_stopwords)

    return low_rating_reviews, high_rating_reviews
