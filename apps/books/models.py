from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title
