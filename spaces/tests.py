from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from django.test import TestCase


class TestSpaces(TestCase):
#   def test_post_list(self):
#       response = self.client.get(resolve_url('root'))
#       self.assertRedirects(response, resolve_url('spaces:index'))

    def test_post_new_without_login(self):
        data = {'message': 'hello world'}
        response = self.client.post(resolve_url('spaces:post_new'), data)
        redirect_url = resolve_url('login') + '?next=' + resolve_url('spaces:post_new')
        self.assertRedirects(response, redirect_url)

    def test_post_new_with_login(self):
        username, password = 'djangouser', '1234'
        get_user_model().objects.create_user(username, password=password)
        self.client.login(username=username, password=password)

        data = {'message': 'hello world'}
        response = self.client.post(resolve_url('spaces:post_new'), data)
        self.assertRedirects(response, resolve_url('spaces:index'))

