from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from .views import BlacklistTokenUpdateView, UserViewSet, RegisterView, MyTokenObtainPairView

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve', })

urlpatterns = [
    path('', user_list, name='user_list'),
    path('<int:pk>/', user_detail, name='user_list'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
