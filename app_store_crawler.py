from app_store_scraper import AppStore
import pandas as pd
import time

class AppStoreCrawler:
    def __init__(self, app_id, country='kr'):
        self.app_id = app_id
        self.country = country
        self.app = AppStore(country=self.country, app_name='', app_id=self.app_id)

    def get_reviews(self, how_many=200):
        all_reviews = []
        fetched_reviews_ids = set()
        remaining_reviews = how_many

        while remaining_reviews > 0:
            count = min(20, remaining_reviews)
            self.app.review(how_many=count)
            new_reviews = [review for review in self.app.reviews if (review['userName'], review['date']) not in fetched_reviews_ids]

            # 고유 식별자로 (userName, date) 조합을 사용하여 중복 제거
            for review in new_reviews:
                fetched_reviews_ids.add((review['userName'], review['date']))

            all_reviews.extend(new_reviews)
            remaining_reviews -= len(new_reviews)

            time.sleep(1)

            if len(new_reviews) < count:
                break

        # DataFrame으로 변환하고 날짜로 정렬
        reviews_df = pd.DataFrame(all_reviews)
        reviews_df['date'] = pd.to_datetime(reviews_df['date'])
        reviews_df = reviews_df.sort_values(by='date', ascending=False).head(how_many)

        return reviews_df
