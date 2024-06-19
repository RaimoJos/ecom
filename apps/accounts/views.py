from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, "accounts/register.html", {"form": form})


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        # Retrieve user information
        user = request.user
        context = {
            "user": user,
            # "favorites": user.favorites.all(),
            # "orders": user.orders.all(),
        }
        return render(request, "accounts/profile.html", context)
