from django.test import Client, TestCase
from faker import Faker
from users_app.models import AppUser


# tests without login
class OpenViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fake = Faker()

    # get запрос
    def test_statuses_index(self):
        response = self.client.get('/')
        print('test_statuses')
        self.assertEqual(response.status_code, 200)

    def test_statuses_news(self):
        response = self.client.get('/news/')
        print('test_statuses')
        self.assertEqual(response.status_code, 200)

    def test_statuses_news_last_page(self):
        response = self.client.get('/news/?page=last')
        print('test_statuses')
        self.assertEqual(response.status_code, 200)

    def test_statuses_news_first_page(self):
        response = self.client.get('/news/?page=1')
        print('test_statuses')
        self.assertEqual(response.status_code, 200)

    def test_statuses_posts(self):
        response = self.client.get('/posts/')
        print('test_statuses')
        self.assertEqual(response.status_code, 200)

    def test_statuses_sources(self):
        response = self.client.get('/sources/')
        print('test_statuses')
        self.assertEqual(response.status_code, 200)

    def test_statuses_sources_last_page(self):
        response = self.client.get('/sources/?page=last')
        print('test_statuses')
        self.assertEqual(response.status_code, 200)

    def test_statuses_sources_first_page(self):
        response = self.client.get('/sources/?page=1')
        print('test_statuses')
        self.assertEqual(response.status_code, 200)

    def test_statuses_contact(self):
        response = self.client.get('/contact/')
        print('test_statuses')
        self.assertEqual(response.status_code, 200)

    # post запрос
    def test_statuses_post_request(self):
        response = self.client.post('/contact/',
                                    {'name': self.fake.name(),
                                     'email': self.fake.email(),
                                     'message': self.fake.text()
                                     })
        print('post request')
        self.assertEqual(response.status_code, 302)


# tests with login
class ViewsTest(TestCase):

    def test_create_post_without_login(self):
        print('test_create_post_without_login')
        AppUser.objects.create_user(username='test_user1', email='test1@test.com', password='test1234567')
        # create_post without login
        response = self.client.get('/create_post/')
        self.assertEqual(response.status_code, 302)

    def test_create_post_with_login(self):
        print('test_create_post_with_login')
        AppUser.objects.create_user(username='test_user2', email='test2@test.com', password='test1234567')
        # create_post with login
        self.client.login(username='test_user2', password='test1234567')
        response = self.client.get('/create_post/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        print('test_login')
        AppUser.objects.create_user(username='test_user3', email='test3@test.com', password='test1234567')
        response = self.client.login(username='test_user3', password='test1234567')
        self.assertEqual(response, True)

    def test_logout_after_login(self):
        print('test_logout_after_login')
        AppUser.objects.create_user(username='test_user4', email='test4@test.com', password='test1234567')
        self.client.login(username='test_user4', password='test1234567')
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)

    def test_go_to_pass_change(self):
        print('test_go_to_pass_change')
        AppUser.objects.create_user(username='test_user5', email='test5@test.com', password='test1234567')
        self.client.login(username='test_user5', password='test1234567')
        response = self.client.get('/users/pass_change/')
        self.assertEqual(response.status_code, 200)


# API tests without login
class ApiOpenViewsTest(TestCase):

    # get запрос
    def test_places_api_statuses(self):
        response = self.client.get('/api/v0/places/')
        print('places_api_statuses')
        self.assertEqual(response.status_code, 200)

    def test_sources_api_statuses(self):
        response = self.client.get('/api/v0/sources/')
        print('sources_api_statuses')
        self.assertEqual(response.status_code, 200)

    def test_articles_api_statuses(self):
        response = self.client.get('/api/v0/articles/')
        print('articles_api_statuses')
        self.assertEqual(response.status_code, 403)
