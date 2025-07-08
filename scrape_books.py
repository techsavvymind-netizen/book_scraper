import requests
from bs4 import BeautifulSoup
import csv


    

url = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Mapping rating text to numeric values
ratings_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

books = soup.find_all('article', class_='product_pod')


with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    # writer = csv.writer(file)
    fieldnames = ['Title', 'rating_class', 'Price','availability']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()


    for book in books:
        # Title
        title = book.h3.a['title']
    
        # Rating
        rating_class = book.p.get('class')
        rating_text = rating_class[1] if len(rating_class) > 1 else 'No rating'
        rating = ratings_map.get(rating_text, 0)
    
        # Price
        price = book.find('p', class_='price_color').text.strip()
    
        # Availability
        availability = book.find('p', class_='instock availability').text.strip()
    
        print(f'Title: {title}')
        print(f'Rating: {rating} stars')
        print(f'Price: {price}')
        print(f'Availability: {availability}')
        print('---')
    
        writer.writerow({'Title': title ,'rating_class':rating,'Price':price ,'availability':availability})
    
    
    