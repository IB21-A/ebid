from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import generics, serializers, viewsets
from rest_framework.response import Response
from rest_framework import status
from commerce.permissions import IsOwner, IsOwnerOrReadOnly

from commerce.serializers import WatchingSerializer
from commerce.models import Watching
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action, permission_classes
# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def watch_list(self, request, pk=None):
        """
        Returns a list of all the listing ids a user has in their watchlist
        """
        # TODO remove this if the authenticated only watchlist is completed
        user = self.get_object()
        watchlist = user.watching.all()
        return Response([auction.listing_id.id for auction in watchlist])


class UserWatchList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
 # TODO make this only available to the logged in user

    def list(self, request, *args, **kwargs):
        # queryset = Product.objects.prefetch_related(Prefetch(
        # 'likes',queryset=Like.objects.filter(like=True))
        # user_id = kwargs.get('pk')
        user = self.get_object()
        watchlist = user.watching.all()
        return Response([auction.listing_id.id for auction in watchlist])





class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom information to the payload
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
