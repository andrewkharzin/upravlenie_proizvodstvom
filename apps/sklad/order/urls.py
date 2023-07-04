from django.urls import path
from .views_base import generate_qr_code,  CustomerDeleteView
from .views.customer_views import CustomerOrdersView, customer_list, customer_create, customer_update
from .views.order_views import order_detail, order_list, search_orders, create_order, update_order, delete_order, get_stock_quantity
from .views.order_views import generate_pdf_report as grp
from .views.invoice_view import invoice_list

app_name = "order"

urlpatterns = [
    # другие URL-маршруты
    path('orders/active/qr-code/<int:order_id>/', generate_qr_code, name='generate_qr_code'),
    path('customers/', customer_list, name='customer_list'),
    path('customers/<int:customer_id>/', CustomerOrdersView.as_view(), name='customer_detail'),
    path('customers/create/', customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    # path('customers/<int:customer_id>/orders/', CustomerOrdersView.as_view(), name='customer_orders'),

    # Order path
    # path('orders/<int:order_id>/<int:invoice_id>/<int:pay_address_id>/', order_detail, name='order_detail')
    path('orders/', order_list, name='order_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('orders/<int:order_id>/generate_report/', grp, name='generate_pdf_report'),
    path('search_orders/', search_orders, name='search_orders'),
    #CRUD
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('orders/create/', create_order, name='order_create'),
    path('orders/<int:pk>/update/', update_order, name='order_update'),
    path('orders/<int:pk>/delete/', delete_order, name='order_delete'),


    # Invoice path
    path('invoices/', invoice_list, name='invoice_list'),
    path('get_stock_quantity/', get_stock_quantity, name='get_stock_quantity'),


]
