import random
from django.core.management.base import BaseCommand, CommandError
from blog.models import Article, Author


class Command(BaseCommand):
    help = 'set in parameter count of add cities'

    def add_arguments(self, parser):
        parser.add_argument('article', nargs='+', type=int)

    def handle(self, *args, **options):
        len_insert = options['article'][0]

        if len_insert < 1:
            raise CommandError(f'argument = {len_insert} not in diapason: more then 1')
        else:
            auther_queryset = Author.objects.all()
            # print(len(auther_queryset))
            # print(auther_queryset[1])
            ps = self.authors(len_insert)
            l = len(auther_queryset)
            for p_in in ps:
                r_l = random.randint(0, l - 1)
                p = Article(title=p_in[0], body=p_in[1], author=auther_queryset[r_l])
                p.save(force_insert=True)
                self.stdout.write(self.style.SUCCESS(f'article: {p} '))

            self.stdout.write(self.style.SUCCESS(f'Success insert {len_insert} Article'))

    @staticmethod
    def authors(ln):
        return_arr: list = list()
        for i in range(ln):
            r_l = random.randint(5, 18)
            un = ''
            fn = ''
            for j in range(r_l):
                un += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            for j in range(r_l):
                fn += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

            return_arr.append((un, fn))
        return return_arr
