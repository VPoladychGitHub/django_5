import random
from django.core.management.base import BaseCommand, CommandError
from blog.models import Comment, Article


class Command(BaseCommand):
    help = 'set in parameter count of add cities'

    def add_arguments(self, parser):
        parser.add_argument('comment', nargs='+', type=int)

    def handle(self, *args, **options):
        len_insert = options['comment'][0]

        if len_insert < 1:
            raise CommandError(f'argument = {len_insert} not in diapason: more then 1')
        else:
            article_queryset = Article.objects.all()
            # print(len(auther_queryset))
            # print(auther_queryset[1])
            # ps = self.comments(len_insert)
          # r_l = random.randint(0, len(article_queryset) - 1)


            l = len(article_queryset)
            ps = self.comments(len_insert)
            for p_in in ps:
                r_l  = random.randint(0, l - 1)
                print(r_l)
                p = Comment(username=p_in[0], comment_text=p_in[1], article=article_queryset[r_l])
                p.save(force_insert=True)
                self.stdout.write(self.style.SUCCESS(f'comment: {p} '))

            self.stdout.write(self.style.SUCCESS(f'Success insert {len_insert} Comment'))

    @staticmethod
    def comments(ln):
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
