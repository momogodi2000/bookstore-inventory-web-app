import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Author, Order, OrderItem

class BookstoreInventoryTests(TestCase):

    def setUp(self):
        # Set up the test client
        self.client = Client()
        
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='admin', password='adminpassword')

        # Create test authors
        self.author1 = Author.objects.create(name="Author One", biography="Bio of author one.")
        self.author2 = Author.objects.create(name="Author Two", biography="Bio of author two.")
        
        # Create test books
        self.book1 = Book.objects.create(title="Book One", author=self.author1, isbn="1111111111111", price=10.00, stock_quantity=5)
        self.book2 = Book.objects.create(title="Book Two", author=self.author2, isbn="2222222222222", price=15.00, stock_quantity=3)

    def test_register_user(self):
        response = self.client.post(reverse('register'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects on success

    def test_login_user(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(response.url.startswith('/user_panel/'))  # Redirects to user panel

    def test_login_admin(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'adminpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(response.url.startswith('/admin_panel/'))  # Redirects to admin panel

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects on success

    def test_book_creation(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('book_create'), {
            'title': 'New Book',
            'author': self.author1.id,
            'isbn': '3333333333333',
            'price': 20.00,
            'stock_quantity': 10
        })
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_book_update(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('book_update', args=[self.book1.id]), {
            'title': 'Updated Book One',
            'author': self.author1.id,
            'isbn': '1111111111111',
            'price': 12.00,
            'stock_quantity': 7
        })
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')
        self.assertEqual(self.book1.price, 12.00)

    def test_book_delete(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('book_delete', args=[self.book2.id]))
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    def test_order_placement(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('place_order'), {
            'books': json.dumps([
                {'book_id': self.book1.id, 'quantity': 2},
                {'book_id': self.book2.id, 'quantity': 1}
            ])
        })
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.items.count(), 2)

    def test_author_creation(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('author_create'), {
            'name': 'New Author',
            'biography': 'Biography of new author.'
        })
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(Author.objects.filter(name='New Author').exists())

    def test_author_update(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('author_update', args=[self.author1.id]), {
            'name': 'Updated Author One',
            'biography': 'Updated bio of author one.'
        })
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.name, 'Updated Author One')
        self.assertEqual(self.author1.biography, 'Updated bio of author one.')

    def test_author_delete(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('author_delete', args=[self.author2.id]))
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertFalse(Author.objects.filter(id=self.author2.id).exists())

    def test_order_history_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)  # Check if the view returns a successful response
        self.assertTemplateUsed(response, 'order/order_history.html')  # Check if the correct template is used

if __name__ == "__main__":
    unittest.main()

