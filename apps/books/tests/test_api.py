from rest_framework import status
from rest_framework.test import APITestCase

from apps.books.factories import BookFactory
from apps.books.models import Book


class BookApiTests(APITestCase):
    def test_list_endpoint_returns_compact_payload(self):
        BookFactory(
            title='Refactoring',
            author='Martin Fowler',
            summary='Long summary should not be in list payload.',
            isbn='9780201485677',
            pages=448,
        )

        response = self.client.get('/api/books/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            set(response.data[0].keys()),
            {'id', 'title', 'author', 'isbn'},
        )

    def test_create_endpoint_persists_book(self):
        payload = {
            'title': '  The Pragmatic Programmer  ',
            'author': 'Andrew Hunt',
            'summary': 'Classic engineering book.',
            'isbn': '978-0201616224',
            'pages': 352,
            'published_date': '1999-10-30',
        }

        response = self.client.post('/api/books/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

        created = Book.objects.first()
        self.assertEqual(created.title, 'The Pragmatic Programmer')
        self.assertEqual(created.isbn, '9780201616224')
