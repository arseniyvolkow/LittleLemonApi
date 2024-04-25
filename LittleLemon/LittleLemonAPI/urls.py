from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('categories-items',views.CategriesItems.as_view()),
    path('menuitems',views.MenuItemsList.as_view()),
    path('menuitems/<int:pk>',views.SingleMenuItemView.as_view()),
    path('groups/manager/users', views.ManagerListView.as_view()),
    path('groups/manager/users/<int:pk>', views.removeManagerRole),
    path('groups/delivery-crew/users', views.DeliveryCrewListView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.removeDeliveryCrewRole),
    path('cart/menu-items',views.ListCartItemsView.as_view()),
    path('orders',views.OrdersView.as_view()),
    path('orders/<int:pk>',views.SingleOrderView.as_view()),
]   
