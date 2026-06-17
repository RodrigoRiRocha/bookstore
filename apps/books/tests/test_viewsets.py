from django.test import TestCase

from apps.books.serializers import BookListSerializer, BookSerializer
from apps.books.views import BookViewSet


class BookViewSetTests(TestCase):
    def test_get_serializer_class_returns_list_serializer_for_list_action(self):
        viewset = BookViewSet()
        viewset.action = 'list'

        serializer_class = viewset.get_serializer_class()

        self.assertIs(serializer_class, BookListSerializer)

    def test_get_serializer_class_returns_default_serializer_for_other_actions(self):
        viewset = BookViewSet()
        viewset.action = 'retrieve'

        serializer_class = viewset.get_serializer_class()

        self.assertIs(serializer_class, BookSerializer)