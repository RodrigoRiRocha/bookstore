from django.test import TestCase

from apps.books.factories import BookFactory


class BookFactoryTests(TestCase):
    def test_book_factory_creates_book(self):
        book = BookFactory()

        self.assertIsNotNone(book.id)
        self.assertEqual(len(book.isbn), 13)
        self.assertGreater(book.pages, 0)