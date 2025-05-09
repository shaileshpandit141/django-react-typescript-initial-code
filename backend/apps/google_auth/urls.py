from django.urls import path

from .views import GoogleCallbackView, GoogleLoginView, GoogleTokenExchangeView

urlpatterns = [
    path("google/signin/", GoogleLoginView.as_view(), name="google-login"),
    path(
        "google/signin/token/exchange/",
        GoogleTokenExchangeView.as_view(),
        name="google-token-exchange",
    ),
    path("google/callback/", GoogleCallbackView.as_view(), name="google-callback"),
]
