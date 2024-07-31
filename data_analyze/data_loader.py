import pandas as pd

def load_and_preprocess_data():
    # 데이터 로드
    google_play_reviews = pd.read_csv("../google_play_reviews.csv")
    app_store_reviews = pd.read_csv("../app_store_reviews.csv")

    # 열 이름 표준화
    google_play_reviews = google_play_reviews.rename(columns={
        'reviewId': 'review_id',
        'userName': 'user_name',
        'userImage': 'user_image',
        'content': 'review',
        'score': 'rating',
        'thumbsUpCount': 'thumbs_up_count',
        'reviewCreatedVersion': 'review_created_version',
        'at': 'date',
        'replyContent': 'developer_response',
        'repliedAt': 'replied_at',
        'appVersion': 'app_version'
    })

    app_store_reviews = app_store_reviews.rename(columns={
        'date': 'date',
        'developerResponse': 'developer_response',
        'review': 'review',
        'rating': 'rating',
        'isEdited': 'is_edited',
        'title': 'title',
        'userName': 'user_name'
    })

    # 결측치 처리
    google_play_reviews.fillna("", inplace=True)
    app_store_reviews.fillna("", inplace=True)

    # 날짜 형식 변환
    google_play_reviews['date'] = pd.to_datetime(google_play_reviews['date'], errors='coerce').fillna(pd.Timestamp('1970-01-01')).astype(str)
    app_store_reviews['date'] = pd.to_datetime(app_store_reviews['date'], errors='coerce').fillna(pd.Timestamp('1970-01-01')).astype(str)

    # 중복 제거
    app_store_reviews = app_store_reviews.drop_duplicates(subset=['user_name', 'date'])

    # 데이터 병합
    all_reviews = pd.concat([google_play_reviews, app_store_reviews], ignore_index=True)

    return all_reviews
