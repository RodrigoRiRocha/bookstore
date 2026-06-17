from django.test import TestCase

from apps.books.serializers import BookSerializer


class BookSerializerTests(TestCase):
    def test_valid_data_passes_and_normalizes_fields(self):
        serializer = BookSerializer(
            data={
                'title': '  Clean Architecture  ',
                'author': 'Robert C. Martin',
                'summary': 'Practical software architecture guidance.',
                'isbn': '978-0134494166',
                'pages': 432,
                'published_date': '2017-09-20',
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['title'], 'Clean Architecture')
        self.assertEqual(serializer.validated_data['isbn'], '9780134494166')

    def test_title_shorter_than_three_characters_is_invalid(self):
        serializer = BookSerializer(
            data={
                'title': 'ab',
                'author': 'Author',
                'isbn': '9780134494167',
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_isbn_with_wrong_length_is_invalid(self):
        serializer = BookSerializer(
            data={
                'title': 'Valid title',
                'author': 'Author',
                'isbn': '1234567890',
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('isbn', serializer.errors)

    def test_pages_must_be_greater_than_zero(self):
        serializer = BookSerializer(
            data={
                'title': 'Valid title',
                'author': 'Author',
                'isbn': '9780134494168',
                'pages': 0,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('pages', serializer.errors)

    def test_pages_can_be_null(self):
        serializer = BookSerializer(
            data={
                'title': 'Domain-Driven Design',
                'author': 'Eric Evans',
                'isbn': '9780321125217',
                'pages': None,
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIsNone(serializer.validated_data['pages'])
