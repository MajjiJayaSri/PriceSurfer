from fuzzywuzzy import fuzz
from .flipkart import scrap_Flipkart
from .amazon import ScrapAmazon
def scrap(search_key):
    flipkart_details = scrap_Flipkart(search_key)
    flipkart_prod_details = [
        {'name': name, 'price': price, 'image': image, 'link': link}
        for name, price, image, link in flipkart_details
    ]

    amazon_details = ScrapAmazon(search_key)
    amazon_prod_details= [
        {'name': name, 'price': price, 'image': image, 'link': link}
        for name, price, image, link in amazon_details
    ]


    flipkart_products = [product['name'] for product in flipkart_prod_details]

    amazon_products = [product['name'] for product in amazon_prod_details]


    threshold = 50

    matching_products = set()

    for flipkart_product in flipkart_products:
        for amazon_product in amazon_products:
            similarity_score = fuzz.ratio(flipkart_product.lower(), amazon_product.lower())

            if similarity_score > threshold:
                matching_products.add((flipkart_product, amazon_product))
    matched_products = []
    if matching_products:
        for flipkart_product, amazon_product in matching_products:
            #print(f"Flipkart: {flipkart_product} <=> Amazon: {amazon_product}")
            d = dict()
            for fdict in flipkart_prod_details:
                if fdict['name'] == flipkart_product:
                    d['name'] = fdict['name']
                    d['image'] = fdict['image']
                    d['fprice'] = fdict['price']
                    d['flink'] = fdict['link']
                    break
            for adict in amazon_prod_details:
                if adict['name'] == amazon_product:
                    d['aprice'] = adict['price']
                    d['alink'] = adict['link']
                    break
            matched_products.append(d)
            
    else:
        print("No matching products found.")
    return matched_products
