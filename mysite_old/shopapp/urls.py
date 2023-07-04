from django.urls import path

from .views import (
    ShopIindexView,
    GroupsListView,
    create_order,
    ProductDetailsView,
    ProductListView,
    OrdersListView,
    OrderDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderUpdateView,
    OrderDeleteView,
)

app_name = 'shopapp'

urlpatterns = [
    path('', ShopIindexView.as_view(), name='index'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/confirm-delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-details'),
]
