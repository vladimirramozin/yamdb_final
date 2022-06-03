from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_not_in_future_validator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.PositiveSmallIntegerField(
        validators=[year_not_in_future_validator]
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category, related_name='titles',
        on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, 'out of range'),
                    MaxValueValidator(10, 'out of range')])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('id', '-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title')
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    reviews = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['id']
