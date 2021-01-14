from django.urls import path

from app.views import *

urlpatterns = [
    # path("", views.index, name='index'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registerBuyer/', RegisterBuyerView.as_view(), name='registerBuyer'),
    path('registerSeller/', RegisterSellerView.as_view(), name='registerSeller'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('my_products/<int:pk>', MyProductListView.as_view(), name='my_product_list'),
    path('buyer_orders/<int:pk>', BuyerOrderListView.as_view(), name='buyer_order_list'),
    path('seller_orders/<int:pk>', SellerOrderListView.as_view(), name='seller_order_list'),
    path('add_product/', ProductAddView.as_view(), name='add_product'),
    path('my_products/<int:pk>/delete/<int:pk_product>', ProductDeleteView.as_view(), name='delete_product'),
    path('my_products/<int:pk>/edit/<int:pk_product>', ProductEditView.as_view(), name='edit_product'),
    path('order/<int:pk>/<int:pk_product>', OrderCreateView.as_view(), name='create_order'),
    path('seller_orders/<int:pk>/<int:pk_order>', OrderEditView.as_view(), name='edit_order'),
]
