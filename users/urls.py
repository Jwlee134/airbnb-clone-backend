from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


# me path가 str:username의 아래쪽에 있으면 me가 username으로 인식되게 된다.
# @를 붙여서 me란 username을 가진 user를 me path와 중복되지 않게 한다. 아니면 me라는 username을 사용하지 못하게 하던가.
urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("sign-up", views.SignUp.as_view()),
    path("token-login", obtain_auth_token),
    path("jwt-login", views.JWTLogin.as_view()),
    path("github", views.GithubLogin.as_view()),
    path("kakao", views.KakaoLogin.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
    path("@<str:username>/rooms", views.PublicUserRooms.as_view()),
    path("@<str:username>/reviews", views.PublicUserReviews.as_view()),
]
