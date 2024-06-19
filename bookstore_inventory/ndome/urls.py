from django.urls import path
from .views import register_view, login_view, logout_view, home_view, admin_panel_view, user_panel_view
from .views import book_list_view, book_create_view, book_update_view, book_delete_view
from .views import author_create_view, author_list_view, author_update_view, author_delete_view, order_create_view, book_list_user_view
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView
from . import views

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin_panel/', admin_panel_view, name='admin_panel'),
    path('user_panel/', user_panel_view, name='user_panel'),
    path('admin_panel/books/', book_list_view, name='book_list'),
    path('admin_panel/books/create/', book_create_view, name='book_create'),
    path('admin_panel/books/update/<int:pk>/', book_update_view, name='book_update'),
    path('admin_panel/books/delete/<int:pk>/', book_delete_view, name='book_delete'),
    path('admin_panel/authors/create/', author_create_view, name='author_create'),
    path('admin_panel/authors/', author_list_view, name='author_list'),
    path('admin_panel/authors/update/<int:pk>/', author_update_view, name='author_update'),
    path('admin_panel/authors/delete/<int:pk>/', author_delete_view, name='author_delete'),
    path('user_panel/orders/create/', order_create_view, name='order_create'),
    path('user_panel/books/', book_list_user_view, name='book_list_user'),
    path('admin_panel/users/', UserListView.as_view(), name='user_list'),
    path('admin_panel/users/add/', UserCreateView.as_view(), name='user_create'),
    path('admin_panel/users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('admin_panel/users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    path('order-history/', views.order_history, name='order_history'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
