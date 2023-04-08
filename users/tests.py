from django.test import TestCase
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
        response = self.client.post(reverse('register'), data=data)

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

        user = CustomUser.objects.get(email='testuser@example.com')

        # Test for stripe account registration
        self.assertIsNotNone(user.stripe_customer_id)
        self.assertEqual(user.email, 'testuser@example.com')


class UserLoginTestCase(TestCase):
    def setUp(self):
        # Arrange
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com', password='testpassword')

    def test_user_login(self):
        # Act
        response = self.client.post(
            reverse('login'), {'email': 'testuser@example.com', 'password': 'testpassword'})

        # Assert
        self.assertEqual(response.status_code, 200)
        #self.assertRedirects(response, reverse('dashboard'))

    def test_user_logout(self):
        # Arrange
        self.client.login(email='testuser@example.com',
                          password='testpassword')

        # Act
        response = self.client.post(reverse('logout'))

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
