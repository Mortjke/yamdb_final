from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, CustomUserViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, get_jwt_token,
                    sign_up)

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register('titles/(?P<title_id>[^/.]+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_jwt_token, name='get_jwt_token'),
    path('v1/', include(router.urls)),
]
