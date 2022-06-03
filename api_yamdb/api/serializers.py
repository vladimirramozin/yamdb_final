from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("User 'me' not allowed")
        return value


class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class SendCodeSerializer(serializers.Serializer):
    """
    Отправка кода подтверждения на почту.
    """
    email = serializers.EmailField(required=True)


class CheckConfirmationCodeSerializer(serializers.Serializer):
    """
    Проверка кода подтверждения.
    """
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role',)
        model = User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review
        read_only_fields = ('author', 'pub_date')

    def validate(self, data):
        if self.context['view'].request.method == 'PATCH':
            return data
        title = get_object_or_404(Title,
                                  id=self.context['view'].kwargs['title_id'])
        if Review.objects.filter(title=title,
                                 author=self.context['view']
                                 .request.user).exists():
            raise serializers.ValidationError('Review not Unique')
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('genre', 'category')


class TitleWriteSerializer(TitleSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
