import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc

# 한국어 폰트 설정
def set_korean_font():
    plt.rcParams['font.family'] = 'AppleGothic'
    plt.rcParams['axes.unicode_minus'] = False

def visualize_keywords(low_rating_top_keywords, high_rating_top_keywords):
    set_korean_font()  # 한국어 폰트 설정

    plt.figure(figsize=(14, 8))

    # 평점이 낮은 리뷰의 상위 키워드
    plt.subplot(1, 2, 1)
    # 붉은 계열의 color 추천 ->
    sns.barplot(x=low_rating_top_keywords.values, y=low_rating_top_keywords.index, color='lightcoral')
    plt.title('낮은 평점의 상위 키워드 (1-3)')
    plt.xlabel('빈도수')
    plt.ylabel('키워드')
    plt.xticks(rotation=45)

    # 평점이 높은 리뷰의 상위 키워드
    plt.subplot(1, 2, 2)
    sns.barplot(x=high_rating_top_keywords.values, y=high_rating_top_keywords.index, color='lightgreen')
    plt.title('높은 평점의 상위 키워드 (4-5)')
    plt.xlabel('빈도수')
    plt.ylabel('키워드')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
