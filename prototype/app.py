from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__, static_folder='static')

# Load the reviews data from separate files
google_play_reviews = pd.read_csv("../google_play_reviews.csv")
app_store_reviews = pd.read_csv("../app_store_reviews.csv")

# Standardize column names
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

# Replace NaN values with empty strings
google_play_reviews.fillna("", inplace=True)
app_store_reviews.fillna("", inplace=True)

# Ensure 'date' column is in proper datetime format and handle any inconsistencies
google_play_reviews['date'] = pd.to_datetime(google_play_reviews['date'], errors='coerce').fillna(pd.Timestamp('1970-01-01')).astype(str)
app_store_reviews['date'] = pd.to_datetime(app_store_reviews['date'], errors='coerce').fillna(pd.Timestamp('1970-01-01')).astype(str)

# Remove duplicates in app_store_reviews based on user_name and date
app_store_reviews = app_store_reviews.drop_duplicates(subset=['user_name', 'date'])

# Combine the reviews into a single DataFrame
all_reviews = pd.concat([google_play_reviews, app_store_reviews], ignore_index=True)

# Calculate the average rating for each bank
average_ratings = all_reviews.groupby('bank')['rating'].mean().reset_index()

@app.route('/')
def index():
    banks = pd.concat([google_play_reviews['bank'], app_store_reviews['bank']]).unique()
    bank_avg_ratings = average_ratings.to_dict(orient='records')
    return render_template('index.html', banks=banks, bank_avg_ratings=bank_avg_ratings)

@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    bank = request.args.get('bank')
    platform = request.args.get('platform')

    if platform == 'Google Play':
        filtered_reviews = google_play_reviews
    elif platform == 'App Store':
        filtered_reviews = app_store_reviews
    else:
        return jsonify([])  # In case of an invalid platform, return an empty list

    if bank:
        filtered_reviews = filtered_reviews[filtered_reviews['bank'] == bank]

    # Sort reviews by date in descending order before sending them to the client
    filtered_reviews = filtered_reviews.sort_values(by='date', ascending=False)

    reviews = filtered_reviews.to_dict('records')
    return jsonify(reviews)

if __name__ == "__main__":
    app.run(debug=True)
