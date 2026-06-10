import datetime

import factory

from .models import Book


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=3)
    author = factory.Faker('name')
    summary = factory.Faker('paragraph')
    isbn = factory.Sequence(lambda n: f'{(9780000000000 + n):013d}')
    pages = factory.Faker('random_int', min=50, max=1200)
    published_date = factory.Faker(
        'date_between_dates',
        date_start=datetime.date(1950, 1, 1),
        date_end=datetime.date.today(),
    )
