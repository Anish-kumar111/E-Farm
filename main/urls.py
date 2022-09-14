from django.urls import path
# from django.conf.urls import url
from . import views
from .views import (
    # MenuListView,
    AddressUpdateView,
    # SearchResultsView,
    SellerUpdateView,
    menuDetail,
    add_to_cart,
    get_cart_items,
    order_item,
    CartDeleteView,
    order_details,
    admin_view,
    item_list,
    pending_orders,
    accepted_orders,
    rejected_orders,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    subcategory,
    update_status,
    add_reviews,
    get_cart_item
    
)

app_name = "main"

urlpatterns = [
    path('', views.index, name='home'),
    # path('', MenuListView.as_view(), name='home'),
    path('product/<str:slug>', views.menuDetail, name='product'),    
    path('subcategories/<slug>', views.subCategory, name='subcategory'),
    path('categories/<slug>', views.category, name='category'),
    path('supcategories/<slug>', views.supcategory, name='supcategory'),
    path('search',views.search,name='search'),
    # path("search/", SearchResultsView.as_view(), name="search"),


    path('filter-data',views.filter_data,name='filter_data'),


    path('item_list/', views.item_list, name='item_list'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item-update/<slug>/', ItemUpdateView.as_view(), name='item-update'),
    path('item-delete/<slug>/', ItemDeleteView.as_view(), name='item-delete'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.get_cart_items, name='cart'),
    path('cart0/', views.get_cart_item, name='cart0'),
    path('remove-from-cart/<int:pk>/', CartDeleteView.as_view(), name='remove-from-cart'),
    path('address-from-cart/<int:pk>/', AddressUpdateView.as_view(), name='address-from-cart'),
    path('ordered/', views.order_item, name='ordered'),
    path('order_details/', views.order_details, name='order_details'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('rejected_orders/', views.rejected_orders, name='rejected_orders'),
    path('pending_orders/', views.pending_orders, name='pending_orders'),
    path('accepted_orders/', views.accepted_orders, name='accepted_orders'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard2/', views.admin_dashboard2, name='admin_dashboard2'),
    path('update_status/<int:pk>', views.update_status, name='update_status'),
    # path('update_seller/<int:pk>', views.update_seller, name='update_seller'),
    path('update_ready/<int:pk>', views.update_ready, name='update_ready'),
    # path(r'^update_ready/(?P<ready_id>\d+)/$', views.update_ready, name='update_ready'),
    path('postReview', views.add_reviews, name='add_reviews'),
    path('payment/', views.payment, name='payment'),
    path('seller-update/<int:pk>', SellerUpdateView.as_view(), name='seller-update'),
]
