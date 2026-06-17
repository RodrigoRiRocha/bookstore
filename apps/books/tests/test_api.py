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
        self.assertEqual(response.data['count'], 1)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(
            set(response.data['results'][0].keys()),
            {'id', 'title', 'author', 'isbn'},
        )

    def test_list_endpoint_is_paginated(self):
        BookFactory.create_batch(3)

        response = self.client.get('/api/books/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIsNotNone(response.data['next'])

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

    def test_retrieve_endpoint_returns_full_payload(self):
        book = BookFactory(
            title='Design Patterns',
            author='Erich Gamma',
            summary='Classic object-oriented design catalog.',
            isbn='9780201633610',
            pages=395,
        )

        response = self.client.get(f'/api/books/{book.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data.keys()),
            {
                'id',
                'title',
                'author',
                'summary',
                'isbn',
                'pages',
                'published_date',
                'created_at',
            },
        )

    def test_partial_update_allows_nullable_pages(self):
        book = BookFactory(pages=240)

        response = self.client.patch(
            f'/api/books/{book.id}/',
            {'pages': None},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book.refresh_from_db()
        self.assertIsNone(book.pages)
