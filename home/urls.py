# home


from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    
    # path('order/<int:perfume_id>/', views.create_order, name='create'),

 
    path('create_order/<int:perfume_id>/', views.create_order, name='create_order'),

    path('cart/', views.cart_view, name='cart'),

    path('update-cart-quantity/', views.update_cart_quantity, name='update_cart_quantity'),    
    
    
    path('remove-cart-item/', views.remove_cart_item, name='remove_cart_item'),
    
    path('booking/', views.booking, name='booking'),
    
    path('search/', views.search_perfumes, name='search_perfumes'),



]
