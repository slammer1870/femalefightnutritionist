from django.test import Client, TestCase
from django.urls import reverse

from .models import CustomUser


class UserRegistrationTestCase(TestCase):
    def test_user_registration(self):
        # Arrange
        data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

        # Act
        response = self.client.post(reverse('users:register'), data=data)

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:dashboard'))

        user = CustomUser.objects.get(email='testuser@example.com')

        # Test for stripe account registration
        self.assertIsNotNone(user.stripe_customer_id)
        self.assertEqual(user.email, 'testuser@example.com')


class UserLoginTestCase(TestCase):
    def setUp(self):
        # Arrange
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com', password='testpassword')
        self.user.save()

    def test_user_login(self):

        logged_in = self.client.login(
            email='testuser@example.com', password='testpassword')

        self.assertEqual(logged_in, True)

    def test_user_logout(self):
        # Arrange
        self.client.login(email='testuser@example.com',
                          password='testpassword')

        # Act
        response = self.client.post(reverse('users:logout'))

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
