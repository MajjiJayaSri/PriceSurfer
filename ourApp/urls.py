from django.urls import path
from . import views

urlpatterns = [
    path('search_products/',views.search_products,name='search_products'),
    path('',views.home, name="home"),
    path('home/',views.home, name="home"),
    path('about/',views.about, name="about"),

]