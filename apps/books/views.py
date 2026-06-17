from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookListSerializer, BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_action_classes = {
        'list': BookListSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, BookSerializer)
