import requests
from bs4 import BeautifulSoup


def html_to_text(html: str) -> str:
    # Step 1: Convert literal '\n' to actual newlines
    html = html.replace('\\n', '\n')

    # Step 2: Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Step 3: Handle <ul> and <li> tags
    for ul in soup.find_all('ul'):
        bullet_items = []
        for li in ul.find_all('li'):
            bullet_items.append(f"- {li.get_text(strip=True)}")
        ul.replace_with('\n'.join(bullet_items))

    # Step 4: Handle <br> and block-level elements to insert line breaks
    for br in soup.find_all('br'):
        br.replace_with('\n')

    for tag in soup.find_all(['p', 'div']):
        tag.insert_after('\n')

    # Step 5: Get cleaned text
    text = soup.get_text()

    # Step 6: Normalize multiple newlines
    lines = [line.strip() for line in text.splitlines()]
    return '\n'.join([line for line in lines if line])


def get_products_shopify_store_one_page(shopify_domain: str, results_limit: int = 20, page_index: int = 1):
    api_url = f"{shopify_domain}/products.json?limit={results_limit}&page={page_index}"
    response = requests.get(api_url)
    response.raise_for_status()

    raw_products_list = response.json()['products']

    products_list = []

    for product in raw_products_list:
        for variant in product['variants']:
            clean_data = {
                "name": f"{product['title']} - {variant['title']}",
                "category": product['product_type'],
                "price": variant['price'],
                "weight": variant['grams'],
                "tags": product['tags'],
                "description": html_to_text(product['body_html']),
            }

            products_list.append(clean_data)

    return products_list


def get_products_shopify_store_all_pages(shopify_domain: str, results_limit: int = 20):
    curent_page = 1
    products_list = []

    fetched_products = get_products_shopify_store_one_page(shopify_domain, results_limit, curent_page)

    while len(fetched_products) > 0:
        # Add the last fetched products to the products list
        products_list.extend(fetched_products)

        # Increment the current page counter to fetch data from the next page
        curent_page += 1
        fetched_products = get_products_shopify_store_one_page(shopify_domain, results_limit, curent_page)

    return products_list
