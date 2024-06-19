from django.contrib import admin
from .models import Author, Book, Order, OrderItem

admin.site.site_header = "Bookstore Inventory Administration"

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'ISBN', 'price', 'stock_quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date')
    search_fields = ('user__username',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity')
    search_fields = ('order__id', 'book__title')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
