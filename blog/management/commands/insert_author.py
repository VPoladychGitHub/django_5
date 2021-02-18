import random
from django.core.management.base import BaseCommand, CommandError
from blog.models import Author


class Command(BaseCommand):
    help = 'set in parameter count of add cities'

    def add_arguments(self, parser):
        parser.add_argument('author', nargs='+', type=int)

    def handle(self, *args, **options):
        len_insert = options['author'][0]

        if len_insert < 1:
            raise CommandError(f'argument = {len_insert} not in diapason: more then 1')
        else:
            ps = self.authors(len_insert)
            for p_in in ps:
                p = Author(username=p_in[0], first_name=p_in[1], last_name=p_in[2], mail=p_in[3])
                p.save(force_insert=True)
                self.stdout.write(self.style.SUCCESS(f'author: {p} '))

            self.stdout.write(self.style.SUCCESS(f'Success insert {len_insert} Author'))

    @staticmethod
    def authors(ln):
        return_arr: list = list()
        for i in range(ln):
            r_l = random.randint(5, 8)
            un = ''
            fn = ''
            ln = ''
            em = '@test.com'
            for j in range(r_l):
                un += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            for j in range(r_l):
                fn += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            for j in range(r_l):
                ln += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            for j in range(r_l):
                em += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            return_arr.append((un, fn, ln, em))
        return return_arr
