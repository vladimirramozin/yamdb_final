import random

from api_yamdb.settings import ADMIN_EMAIL
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilterSet
from .mixins import CreateListRetrievDeletePatchViewSet, NoRetriveUpdateViewSet
from .permissions import (UserIsAdmin, UserIsAdminOrReadOnly,
                          UserIsAuthorOrAdminOrModerator)
from .serializers import (CategorySerializer, CheckConfirmationCodeSerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          SignupSerializer, TitleSerializer,
                          TitleWriteSerializer, UserOutSerializer,
                          UserSerializer)


@api_view(['POST'])
def signup(request):
    """
    Отправляем код на почту.
    6-ти значный код случайно генерируется из чисел от 0 до 9.

    """
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = ''.join(map(str, random.sample(range(10), 6)))
    email = serializer.validated_data['email']
    if User.objects.filter(email=email).exists():
        return Response('Email уже использован!',
                        status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=serializer.
                           validated_data['username']).exists():
        return Response('Username уже использован!',
                        status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(
        username=serializer.validated_data['username'],
        email=email)
    send_mail('registration', f'code: {confirmation_code}',
              f'Yamdb.ru {ADMIN_EMAIL}', [email])
    user_serializer = UserOutSerializer(user)
    return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    """
    Проверяем код.
    Если совпадает с тем, что лежит в data, то возвращаем статус ОК.
    """
    serializer = CheckConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [UserIsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(email=user.email, role=user.role)
        return Response(serializer.data)


class ReviewsViewSet(CreateListRetrievDeletePatchViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (UserIsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title_pk = self.kwargs['title_id']
        serializer.save(title_id=title_pk,
                        author=self.request.user)


class CommentViewSet(CreateListRetrievDeletePatchViewSet):
    serializer_class = CommentSerializer
    permission_classes = (UserIsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        reviews_instance = get_object_or_404(Review,
                                             id=self.kwargs['review_id'])
        return reviews_instance.comments.all()

    def perform_create(self, serializer):
        reviews_instance = get_object_or_404(Review,
                                             id=self.kwargs['review_id'])
        serializer.save(author=self.request.user,
                        reviews=reviews_instance)


class CategoryViewSet(NoRetriveUpdateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (UserIsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(NoRetriveUpdateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (UserIsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id').all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (UserIsAdminOrReadOnly,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitleWriteSerializer
        return TitleSerializer
