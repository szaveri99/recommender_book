from flask import Flask, render_template, request, json
import pandas as pd

app = Flask(__name__)

# Load the book dataset
book_data = pd.read_csv('books_recommender.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the user's input book title
    
    input_book = request.form['book_title']

    # Implement your recommendation logic here (e.g., using a recommendation model)


    recommended_book = book_data[book_data['title'].str.contains(input_book, case=False)]
    recommended_book = pd.DataFrame(recommended_book['title'].iloc[0:len(recommended_book)])                                                            
    # recommended_book = pd.DataFrame(book_data.nlargest(5,input_book)['title'])
    # recommended_book = recommended_book[recommended_book['title']!=input_book]
    columns_to_merge = ['title','authors', 'publisher', 'isbn', 'language_code', 'ratings_count']
    # Merge the selected columns with the title
    merged_details = recommended_book.merge(book_data[columns_to_merge], on='title', how='inner')
    recommended_details = merged_details.to_dict(orient='records')
    titles = [item['title'] for item in recommended_details]
    # Get details for the recommended book
    # recommended_details = merged_details[merged_details['title'] == recommended_book].to_dict(orient='records')
    # print(recommended_details)
    return render_template('index.html', input_book=input_book, recommended_details=recommended_details, book_titles = titles)

if __name__ == '__main__':
    app.run(debug=True)
