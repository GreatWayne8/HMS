# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Patient, Doctor, Appointment


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.url = reverse('register')  # URL for registration

    def test_registration_page_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Check if page is accessible

    def test_registration_form(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())  # Check user exists

    def test_registration_invalid_data(self):
        response = self.client.post(self.url, {
            'username': '',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword'  # Passwords do not match
        })
        self.assertEqual(response.status_code, 200)  # Should render registration page again
        self.assertFormError(response, 'form', 'username', 'This field is required.')  # Check error message

class UserLoginTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        self.url = reverse('login')  # URL for login

    def test_login_page_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.url, {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)  # User should be authenticated

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.url, {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should render login page again
        self.assertFalse(response.wsgi_request.user.is_authenticated)  # User should not be authenticated

class PatientViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')  # Log in the user
        self.url = reverse('add_patient')  # URL for adding patient

    def test_add_patient_page_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_add_patient(self):
        response = self.client.post(self.url, {
            'user': self.user.id,
            'phone': '123-456-7890'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after adding patient
        self.assertTrue(Patient.objects.filter(user=self.user).exists())  # Check if patient was added

    def test_add_patient_invalid_data(self):
        response = self.client.post(self.url, {
            'user': '',
            'phone': '123-456-7890'  # No user selected
        })
        self.assertEqual(response.status_code, 200)  # Should render page again
        self.assertFormError(response, 'form', 'user', 'This field is required.')  # Check error message
