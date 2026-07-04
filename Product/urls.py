from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Product Home
    path('home/', views.ProductListView.as_view(), name='Product_product_list'),

    # Product Details
    path('product/detail/<slug:slug>/', views.ProductDetailView.as_view(), name='Product_product_detail'),

    # Orders
    path('orders/', views.OrderListView.as_view(), name='Product_order_list'),
    path('order/conformed/', views.order_conform, name='Product_order_conform'),
    path('order/create/<slug:slug>/', views.OrderCreateView.as_view(), name='Product_order_create'),
    path('order/detail/<slug:slug>/', views.OrderDetailView.as_view(), name='Product_order_detail'),

]