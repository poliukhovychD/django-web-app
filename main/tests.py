from django.test import RequestFactory, TestCase
from django.urls import reverse

import json
from .models import Category, Brand, Color, Size, Product
from .views import filter_data, delete_cart_item, signup
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignupForm



class FilterDataViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(title='Category 1')
        self.brand = Brand.objects.create(title='Brand 1')
        self.color = Color.objects.create(title='Color 1', color_code='#FFFFFF')
        self.size = Size.objects.create(title='Size 1')
        self.product = Product.objects.create(
            title='Product 1',
            slug='product-1',
            detail='Product 1 detail',
            specs='Product 1 specs',
            category=self.category,
            brand=self.brand,
            color=self.color,
            size=self.size,
        )

    def test_filter_data(self):
        url = reverse('filter_data')  # Assuming you have a URL pattern named 'filter_data'

        # Set up the request data
        data = {
            'color[]': [self.color.id],
            'category[]': [self.category.id],
            'brand[]': [self.brand.id],
            'size[]': [self.size.id],
            'minPrice': '10',
            'maxPrice': '100',
        }
        request = self.factory.get(url, data)

        # Call the view function
        response = filter_data(request)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')




class AddToCartViewTest(TestCase):
    def test_add_to_cart(self):
        client = Client()
        url = reverse('add_to_cart')  # Assuming you have a URL pattern named 'add_to_cart'

        # Set up the request data
        data = {
            'id': '1',
            'image': 'product.jpg',
            'title': 'Product 1',
            'qty': '2',
            'price': '10.99',
        }

        # Call the view function
        response = client.get(url, data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertContains(response, 'data')
        self.assertContains(response, 'totalitems')

        # Additional assertions based on your implementation
        # Example: Assert that the cart data and total items are as expected
        self.assertEqual(response.json()['data'], {
            '1': {
                'image': 'product.jpg',
                'title': 'Product 1',
                'qty': '2',
                'price': '10.99',
            }
        })
        self.assertEqual(response.json()['totalitems'], 1)


class DeleteCartItemViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_delete_cart_item(self):
        url = reverse('delete-from-cart')

        # Set up the request data
        data = {
            'id': '1',
        }
        request = self.factory.get(url, data)

        # Set up the session data with the item to be deleted
        session_data = {
            'cartdata': {
                '1': {
                    'image': 'product.jpg',
                    'title': 'Product 1',
                    'qty': '2',
                    'price': '10.99',
                }
            }
        }
        request.session = session_data

        # Call the view function
        response = delete_cart_item(request)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertContains(response, 'data')
        self.assertContains(response, 'totalitems')

        # Parse the JSON data
        content = response.content.decode('utf-8')
        data = json.loads(content)
# Verify item deletion
        self.assertNotIn('1', data['data'])
        self.assertEqual(data['totalitems'], 0)

class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_search(self):
        url = reverse('search')
        search_query = 'shirt'

        # Create some test data
        category = Category.objects.create(title='Clothing', image='clothing.jpg')
        brand = Brand.objects.create(title='Brand X', image='brandx.jpg')
        color = Color.objects.create(title='Red', color_code='#FF0000')
        size = Size.objects.create(title='Medium')
        product1 = Product.objects.create(title='T-Shirt', slug='t-shirt', detail='Test T-Shirt', specs='Test Specs',
                                          category=category, brand=brand, color=color, size=size)
        product2 = Product.objects.create(title='Jeans', slug='jeans', detail='Test Jeans', specs='Test Specs',
                                          category=category, brand=brand, color=color, size=size)
        product3 = Product.objects.create(title='Shirt', slug='shirt', detail='Test Shirt', specs='Test Specs',
                                          category=category, brand=brand, color=color, size=size)

        # Make a GET request to the search view
        response = self.client.get(url, {'q': search_query})

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

        # Verify the response context
        data = response.context['data']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], product3)
        self.assertEqual(data[1], product1)


class SignupTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.valid_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

    def test_signup_with_valid_data(self):
        response = self.client.post(self.signup_url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirects to home page
        self.assertEqual(response.url, reverse('home'))
        # Verify that the user is created
        self.assertTrue(User.objects.filter(username='testuser').exists())
        # Verify that the user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signup_with_invalid_data(self):
        invalid_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'differentpassword'  # Invalid password confirmation
        }
        response = self.client.post(self.signup_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Renders signup page
        self.assertTemplateUsed(response, 'registration/signup.html')
        # Verify that the user is not created
        self.assertFalse(User.objects.filter(username='testuser').exists())
        # Verify that the user is not logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)