from django.urls import path

from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('fav/', views.fav, name="fav"),
    path('plants/', views.plants, name="plants"),
    path('update_item/', views.updateItem, name="update_item"),

]
