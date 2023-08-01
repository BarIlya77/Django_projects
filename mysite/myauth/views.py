from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
# from django.shortcuts import reverse

from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.utils.translation import gettext_lazy as _, ngettext

from .models import Profile


class HelloView(View):
    message_text = _('welcome hello world!')

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.message_text}</h1>"
            f"\n<h2>{products_line}</h2>"
        )


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class PhotoUpdateView(UpdateView):
    model = Profile
    fields = ["avatar"]
    template_name = "myauth/photo-update.html"
    success_url = reverse_lazy("myauth:about-me")

    def get_object(self, queryset=None):
        user = self.request.user.profile
        # profile, created = Profile.objects.get_or_create(user=user)
        return user


class UserInfoView(DetailView):
    template_name = "myauth/user-info.html"
    model = User
    context_object_name = "user"


class UserUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.id == self.get_object().user.id
    model = Profile
    fields = "bio", "agreement_accepted", "agreement_accepted", "avatar"
    template_name_suffix = "_update_form"
    # template_name = "myauth/profile_update_form.html"

    def get_success_url(self):
        return reverse(
            "myauth:user-info",
            kwargs={"pk": self.object.user.pk},
        )


class UsersListView(ListView):
    template_name = "myauth/users_list.html"
    model = User
    context_object_name = "users"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
