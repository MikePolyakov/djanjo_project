from django.core.management.base import BaseCommand
from mixer.backend.django import mixer

from situation_report_app.models import Post
from users_app.models import AppUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        AppUser.objects.filter(is_superuser=False).delete()

        count = 500
        for i in range(count):
            p = (i/count)*100
            print(f'{i}) {p} %')
            new_post = mixer.blend(Post)
            print(new_post)
            mixer.blend(Post)

        print('end')
