from django.test import TestCase

from apps.books.factories import BookFactory
from apps.books.models import Book


class BookModelTests(TestCase):
    def test_string_representation_returns_title(self):
        book = BookFactory(title='Domain-Driven Design')

        self.assertEqual(str(book), 'Domain-Driven Design')

    def test_default_ordering_is_by_title(self):
        BookFactory(title='Z title')
        BookFactory(title='A title')

        ordered_titles = list(Book.objects.values_list('title', flat=True))
        self.assertEqual(ordered_titles, ['A title', 'Z title'])
