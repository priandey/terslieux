from django.test import TestCase

from user.models import CustomUser

class TestUserViews(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="user@user.user", password="password")

    def test_sign_in_get(self):
        response = self.client.get('/user/signin/')
        self.assertTemplateUsed(response, 'user/signin.html')
        self.assertFalse(response.context['validForm'])

    def test_sign_in_post_valid_form(self):
        form_data = {
            'email': 'newUser@newUser.new',
            'password': 'password'
        }
        response = self.client.post('/user/signin/', data=form_data)
        self.assertRedirects(response, '/')

    def test_sign_in_post_invalid_form(self):
        form_data = {
            'email'   : 'user@user.user',
            'password': 'password'
        }
        response = self.client.post('/user/signin/', data=form_data)
        self.assertTrue(response.context['duplicate_email'])

    def test_log_in_get(self):
        response = self.client.get('/user/login/')
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])

    def test_log_in_post_valid(self):
        form_data = {
            'email': 'user@user.user',
            'password': 'password'
        }
        response = self.client.post('/user/login/', data=form_data)
        self.assertRedirects(response, '/private/')

    def test_log_in_post_invalid(self):
        form_data = {
            'email': 'youser@yuser.user',
            'password': 'password'
        }
        response = self.client.post('/user/login/', data=form_data)
        self.assertFalse(response.context['logged'])

    def test_profile(self):
        self.client.login(email='user@user.user', password='password')
        response = self.client.get('/user/profile/')
        self.assertTemplateUsed(response, 'user/userprofile.html')

    def test_edit_profile_get(self):
        self.client.login(email='user@user.user', password='password')
        response = self.client.get('/user/editprofile/')
        self.assertTemplateUsed(response, 'user/edit_profile.html')
        self.assertTrue(response.context['form'])

    def test_edit_profile_post_valid(self):
        self.client.login(email='user@user.user', password='password')
        form_data = {
            'password': 'anotherpassword'
        }
        response = self.client.post('/user/editprofile/', data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_invalid(self):
        self.client.login(email='user@user.user', password='password')
        form_data = {
            'password': ''
        }
        response = self.client.post('/user/editprofile/', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['error'])

    def test_delete_profile(self):
        self.client.login(email="user@user.user", password="password")
        response = self.client.post('/user/delprofile/')
        self.assertEqual(response.status_code, 301)
