from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from assignment.Uauth.serializer import UserRegistrationSerializer

User = get_user_model()

class UserRegistrationSerializerTest(APITestCase):
    def test_valid_data(self):
        data = {'username': 'testuser', 'password': 'strongpassword'}
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, data['username'])

    def test_missing_username(self):
        data = {'password': 'strongpassword'}
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {'username': ['This field is required.']})

    def test_missing_password(self):
        data = {'username': 'testuser'}
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {'password': ['This field is required.']})

    def test_optional_email(self):
        data = {'username': 'testuser', 'password': 'strongpassword', 'email': 'test@example.com'}
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, data['email'])
        data = {'username': 'testuser2', 'password': 'anotherpassword'}
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, None)
