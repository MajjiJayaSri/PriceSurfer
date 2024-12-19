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
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: Try searching again")
        return render(request,'product.html')
    return render(request, "products.html",{'products':products,'search_query':search_query})