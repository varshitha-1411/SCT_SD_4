import requests
from bs4 import BeautifulSoup
import csv

def scrape_products(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.93 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve webpage: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    # Find all product containers
    product_cards = soup.find_all('article', class_='product_pod')

    for card in product_cards:
        # Get the product name
        name = card.h3.a['title']

        # Get the product price in GBP and convert to INR
        price_text = card.find('p', class_='price_color').text.strip()
        price_gbp = float(price_text.replace('£', ''))
        price_inr = round(price_gbp * 105, 2)

        # Get the product rating from the class attribute
        rating_tag = card.find('p', class_='star-rating')
        rating = rating_tag['class'][1] if rating_tag else 'N/A'

        product = {
            'Name': name,
            'Price (GBP)': f'£{price_gbp:.2f}',
            'Price (INR)': f'₹{price_inr:.2f}',
            'Rating': rating
        }
        products.append(product)

    return products

def save_to_csv(products, filename):
    keys = products[0].keys() if products else ['Name', 'Price (GBP)', 'Price (INR)', 'Rating']
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def main():
    url = 'https://books.toscrape.com/catalogue/page-1.html'
    products = scrape_products(url)
    if products:
        save_to_csv(products, 'products.csv')
        print(f"Successfully saved {len(products)} products to products.csv")
        
        # Print product info to the console
        print("\nProduct Information:")
        for product in products:
            print(f"Name: {product['Name']}")
            print(f"Price (GBP): {product['Price (GBP)']}")
            print(f"Price (INR): {product['Price (INR)']}")
            print(f"Rating: {product['Rating']}")
            print("-" * 30)
    else:
        print("No products found or failed to scrape.")

if __name__ == "__main__":
    main()
