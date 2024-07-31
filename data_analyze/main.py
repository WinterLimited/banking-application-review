import matplotlib
matplotlib.use('TkAgg')  # 백엔드 설정

from data_loader import load_and_preprocess_data
from text_preprocessing import preprocess_text
from keyword_analysis import analyze_keywords
from visualization import visualize_keywords

def main():
    # 데이터 로드 및 전처리
    all_reviews = load_and_preprocess_data()

    # 텍스트 전처리 및 키워드 분석
    low_rating_reviews, high_rating_reviews = preprocess_text(all_reviews)

    # 키워드 분석
    low_rating_top_keywords, high_rating_top_keywords = analyze_keywords(low_rating_reviews, high_rating_reviews)

    # 시각화
    visualize_keywords(low_rating_top_keywords, high_rating_top_keywords)

if __name__ == "__main__":
    main()
