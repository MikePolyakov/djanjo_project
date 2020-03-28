from django.test import TestCase
from .models import Post, Article, Source, Place
from users_app.models import AppUser
# faker - простые данные, например случайное имя
from faker import Faker
# mixer - полностью создать fake модель
from mixer.backend.django import mixer


# Create your tests here.
class PostTestCase(TestCase):

    def setUp(self):
        user = AppUser.objects.create_user(username='test_user',
                                           email='test@test.test',
                                           password='user4321')
        self.post = Post.objects.create(name='test_post',
                                        text='test_text',
                                        user=user)
        self.post_str = Post.objects.create(name='test_post_str',
                                            text='test_text',
                                            user=user)

    def test_has_image(self):
        print('test_has_image #1')
        self.assertFalse(self.post.has_image())

    def test_str(self):
        print('test_str #2')
        self.assertEqual(str(self.post_str), 'test_post_str')


class PostTestCaseFaker(TestCase):

    def setUp(self):
        faker = Faker()
        user = AppUser.objects.create_user(username=faker.name(),
                                           email='test@test.test',
                                           password='user4321')
        self.post = Post.objects.create(name=faker.name(),
                                        text=faker.name(),
                                        user=user)
        self.post_str = Post.objects.create(name='test_post_str',
                                            text=faker.name(),
                                            user=user)
        # print(self.post.name)

    def test_has_image(self):
        print('test_has_image #3')
        self.assertFalse(self.post.has_image())

    def test_str(self):
        print('test_str #4')
        self.assertEqual(str(self.post_str), 'test_post_str')


class PostTestCaseMixer(TestCase):

    def setUp(self):
        self.post = mixer.blend(Post)
        self.post_str = mixer.blend(Post, name='test_post_str')

    def test_has_image(self):
        print('test_has_image #5')
        self.assertFalse(self.post.has_image())

    def test_str(self):
        print('test_str #6')
        self.assertEqual(str(self.post_str), 'test_post_str')


class ArticleTestCaseMixer(TestCase):

    def setUp(self):
        self.article_str = mixer.blend(Article, name='test_article')

    def test_str(self):
        print('test_str #7')
        self.assertEqual(str(self.article_str), 'test_article')


class SourceTestCaseMixer(TestCase):

    def setUp(self):
        self.source_str = mixer.blend(Source, name='test_source')

    def test_str(self):
        print('test_str #8')
        self.assertEqual(str(self.source_str), 'test_source')


class PlaceTestCaseMixer(TestCase):

    def setUp(self):
        self.place_str = mixer.blend(Place, place_name='test_place')

    def test_str(self):
        print('test_str #9')
        self.assertEqual(str(self.place_str), 'test_place')
