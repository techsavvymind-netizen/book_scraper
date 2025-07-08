import requests
from bs4 import BeautifulSoup
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='S1@houK92!8%',
    database='books'
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        rating INT,
        price VARCHAR(20),
        availability VARCHAR(255)
    )
''')

# Web scraping
url = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

ratings_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

books = soup.find_all('article', class_='product_pod')

for book in books:
    title = book.h3.a['title']
    rating_text = book.p.get('class')[1] if len(book.p.get('class')) > 1 else 'No rating'
    rating = ratings_map.get(rating_text, 0)
    price = book.find('p', class_='price_color').text.strip()
    availability = book.find('p', class_='instock availability').text.strip()

    cursor.execute('''
        INSERT INTO books (title, rating, price, availability)
        VALUES (%s, %s, %s, %s)
    ''', (title, rating, price, availability))

# Commit and close
conn.commit()
cursor.close()
conn.close()