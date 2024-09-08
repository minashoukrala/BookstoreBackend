from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product

class ProductViewTests(APITestCase):
    
    def setUp(self):
        # Set up initial data
        Product.objects.create(
            name="Test Product",
            category="Books",
            description="This is a test product.",
            price=9.99,
            image="test.jpg",
            available_quantity=10
        )

    def test_get_products(self):
        # Get the URL for the products endpoint
        url = reverse('get_products')  # Ensure this matches your URL name
        response = self.client.get(url)
        
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response contains the expected data
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Product")
