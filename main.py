import pandas as pd
from google_play_crawler import GooglePlayCrawler
from app_store_crawler import AppStoreCrawler


def main():
    apps = {
        "신한은행": {"app_store_id": "357484932", "google_play_id": "com.shinhan.sbanking"},
        "국민은행": {"app_store_id": "373742138", "google_play_id": "com.kbstar.kbbank"},
        "하나은행": {"app_store_id": "1362508015", "google_play_id": "com.kebhana.hanapush"},
        "우리은행": {"app_store_id": "1470181651", "google_play_id": "com.wooribank.smart.npib"},
        "농협은행": {"app_store_id": "1444712671", "google_play_id": "nh.smart.banking"},
        "카카오뱅크": {"app_store_id": "1258016944", "google_play_id": "com.kakaobank.channel"},
        "토스": {"app_store_id": "839333328", "google_play_id": "viva.republica.toss"},
        "케이뱅크": {"app_store_id": "1178872627", "google_play_id": "com.kbankwith.smartbank"}
    }

    google_play_reviews = []
    app_store_reviews = []

    for bank, ids in apps.items():
        print(f"Fetching reviews for {bank}...")

        # Google Play reviews
        google_crawler = GooglePlayCrawler(ids["google_play_id"])
        google_reviews = google_crawler.get_reviews(200)
        google_reviews["platform"] = "Google Play"
        google_reviews["bank"] = bank
        google_play_reviews.append(google_reviews)

        # App Store reviews
        app_store_crawler = AppStoreCrawler(ids["app_store_id"])
        app_store_reviews_data = app_store_crawler.get_reviews(200)
        app_store_reviews_data["platform"] = "App Store"
        app_store_reviews_data["bank"] = bank
        app_store_reviews.append(app_store_reviews_data)

    # Concatenate all reviews into separate DataFrames
    google_play_reviews_df = pd.concat(google_play_reviews, ignore_index=True)
    app_store_reviews_df = pd.concat(app_store_reviews, ignore_index=True)

    google_play_reviews_df.to_csv("google_play_reviews.csv", index=False)
    app_store_reviews_df.to_csv("app_store_reviews.csv", index=False)

    print("Google Play reviews have been saved to google_play_reviews.csv")
    print("App Store reviews have been saved to app_store_reviews.csv")

if __name__ == "__main__":
    main()
