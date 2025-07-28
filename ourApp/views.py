from django.shortcuts import render
from .scraper import scrap
from django.contrib import messages
# Create your views here.
# landing page
def home(request):
    return render(request,"home.html")
def about(request):
    return render(request,"about.html")
# page after searching
def search_products(request):
    try:
        search_query = request.GET.get('q','hp laptop')
        products = scrap(search_query)
        request.session['initial_products'] = products
        request.session['search_query'] = search_query
        print("In views matched products: ",len(products))
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: Try searching again")
        return render(request,'products.html')
    return render(request, "products.html",{'products':products,'search_query':search_query})
def searchproducts(request):
    try:
        # Fetch selected brands as a list
        selected_brands = request.GET.getlist('brand', ['hp laptop'])
        request.session['selected_brands'] = selected_brands
        # Pass the list to the scraping function (or process it accordingly)
        products = []
        for brand in selected_brands:
            products += scrap(brand)  # Append results for each brand
        request.session['filtered_products'] = products
    except Exception as e:
        messages.error(request, "An unexpected error occurred: Try searching again.")
        return render(request, 'products.html', {'products':request.session.get('initial_products', []) , 'selected_brands': []})

    # Pass the selected brands to the template
    return render(request, "products.html", {'products': products, 'selected_brands': selected_brands})
def clearFilters(request):
    initial_products = request.session.get('initial_products', [])
    return render(request, "products.html", {'products': initial_products, 'selected_brands': []})
def sorting(request):
    # Retrieve the products from the session
    initial_products = request.session.get('initial_products', [])
    products = request.session.get('filtered_products', initial_products)
    brands = request.session.get('selected_brands',[])
    sort_option = request.GET.get('sortOption')  # Get the selected sort option

    if sort_option and products:
        # Sort products based on the selected option
        if sort_option == 'amazon':
            products = sorted(products, key=lambda x: x.get('aprice', float('inf')))
        elif sort_option == 'flipkart':
            products = sorted(products, key=lambda x: x.get('fprice', float('inf')))

    # Render the template with the sorted products
    return render(request, "products.html", {'products': products, 'selected_brands': brands})

def clearSorting(request):
    initial_products = request.session.get('initial_products', [])
    products = request.session.get('filtered_products', initial_products)
    brands = request.session.get('selected_brands',[])
    return render(request, "products.html", {'products': products, 'selected_brands': brands})