from django.contrib.auth.views import LoginView
from django.urls import path


from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    # ProfileUpdateView,
    UsersListView,
    UserInfoView,
    UserUpdateView,
    PhotoUpdateView,
)

app_name = "myauth"

urlpatterns = [
    # path("login/", login_view, name="login"),
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    # path("logout/", logout_view, name="logout"),
    path("users/", UsersListView.as_view(), name="users_list"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    # path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    # path("about-me/<int:user_id>/", AboutMeView.as_view(), name="about-me"),
    # path("about-me/<str:name>/", AboutMeView.as_view(), name="about-me"),
    path("user-info/<int:pk>/", UserInfoView.as_view(), name="user-info"),
    path("user-info/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("about-me/update", PhotoUpdateView.as_view(), name="photo-update"),
    path("register/", RegisterView.as_view(), name="register"),
    # path("about-me/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile_update"),

    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),

    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]
