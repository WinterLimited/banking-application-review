from google_play_scraper import Sort, reviews_all
import pandas as pd

class GooglePlayCrawler:
    def __init__(self, app_id):
        self.app_id = app_id

    # 200개의 리뷰를 가져옴
    def get_reviews(self, how_many=200):
        reviews = reviews_all(
            self.app_id,
            sleep_milliseconds=0,
            lang='en',
            country='us',
            sort=Sort.NEWEST
        )
        return pd.DataFrame(reviews[:how_many])
