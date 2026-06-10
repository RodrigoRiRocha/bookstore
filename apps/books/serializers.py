from rest_framework import serializers

from .models import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
        ]


class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=32)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'summary',
            'isbn',
            'pages',
            'published_date',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise serializers.ValidationError('Title must contain at least 3 characters.')
        return cleaned

    def validate_isbn(self, value: str) -> str:
        digits_only = ''.join(char for char in value if char.isdigit())
        if len(digits_only) != 13:
            raise serializers.ValidationError('ISBN must contain exactly 13 digits.')
        return digits_only

    def validate_pages(self, value: int | None) -> int | None:
        if value is not None and value < 1:
            raise serializers.ValidationError('Pages must be greater than zero.')
        return value
