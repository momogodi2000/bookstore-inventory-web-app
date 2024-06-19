from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Book, Author, Order, OrderItem
from .forms import BookForm, AuthorForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User
from .forms import UserForm
from .models import Order

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_panel')
                else:
                    return redirect('user_panel')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def admin_panel_view(request):
    if not request.user.is_superuser:
        return redirect('login')
    
    # Pass the user information to the template
    context = {
        'user': request.user
    }
    return render(request, 'panels/admin_panel.html', context)

@login_required
def user_panel_view(request):
    if request.user.is_superuser:
        return redirect('admin_panel')
    return render(request, 'panels/user_panel.html')



# CRUD Views for Book
@login_required
def book_list_view(request):
    if not request.user.is_superuser:
        return redirect('login')
    books = Book.objects.all()
    return render(request, 'book_manage/book_list.html', {'books': books})

@login_required
def book_create_view(request):
    if not request.user.is_superuser:
        return redirect('login')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_manage/book_form.html', {'form': form, 'action': 'Create'})

@login_required
def book_update_view(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_manage/book_form.html', {'form': form, 'action': 'Update'})

@login_required
def book_delete_view(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_manage/book_confirm_delete.html', {'book': book})




# Author Views
def author_create_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'author_book/author_create.html', {'form': form})

def author_list_view(request):
    authors = Author.objects.all()
    return render(request, 'author_book/author_list.html', {'authors': authors})

def author_update_view(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'author_book/author_update.html', {'form': form})

def author_delete_view(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        return redirect('author_list')
    return render(request, 'author_book/author_delete.html', {'author': author})


    ##order


@login_required
def order_create_view(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        quantity = int(request.POST.get('quantity'))
        book = get_object_or_404(Book, id=book_id)
        
        if quantity > book.stock_quantity:
            # Handle the case where requested quantity is more than available stock
            return render(request, 'order/order_create.html', {
                'books': Book.objects.all(),
                'error': 'Requested quantity is more than available stock.'
            })
        
        # Reduce stock quantity
        book.stock_quantity -= quantity
        book.save()
        
        # Create Order and OrderItem
        order = Order.objects.create(user=request.user)
        OrderItem.objects.create(order=order, book=book, quantity=quantity)
        
        return redirect('user_panel')
    
    books = Book.objects.all()
    return render(request, 'order/order_create.html', {'books': books})



@login_required
def book_list_user_view(request):
    books = Book.objects.all()
    return render(request, 'order/book_list_user.html', {'books': books})


@login_required
def user_panel_view(request):
    return render(request, 'panels/user_panel.html')



##users

class UserListView(ListView):
    model = User
    template_name = 'crud_user/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'crud_user/user_create.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'crud_user/user_update.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'crud_user/user_delete.html'
    success_url = reverse_lazy('user_list')



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/order_detail.html', {'order': order})
