from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet, UserViewSet, get_jwt_token,
                    signup)

app_name = 'api'
router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router.register(
    (r'titles/(?P<title_id>\d+)/'
     r'reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)'),
    CommentViewSet,
    basename='comments')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet,
                basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
                ReviewsViewSet,
                basename='reviews')
router.register('users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_jwt_token, name='send_confirmation_code'),
    path('v1/', include(router.urls)),
]
