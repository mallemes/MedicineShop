from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from fond.forms import RegisterForm
from fond.utils import DataMixin


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>page not found</h1>')


class IndexView(DataMixin, TemplateView):
    template_name = "fond/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="index")
        return dict(list(context.items()) + list(mixin.items()))


class AboutView(DataMixin, TemplateView):
    template_name = "fond/about.html"

    def get_context_data(self, **kwargs):
        return self.get_user_context(title="about page")


class ContactView(DataMixin, TemplateView):
    template_name = "fond/contacts.html"

    def get_context_data(self, **kwargs):
        return self.get_user_context(title="contacts")


class ProfileView(DataMixin, TemplateView):
    template_name = "fond/profile.html"

    # def post(self, request, **kwargs):
    #     my_bln = request.POST.get("balance")
    #     if my_bln:
    #         request.user.balance = my_bln
    #         request.user.save()
    #     return redirect('profile')


class Register(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = "fond/register.html"
    success_url = reverse_lazy('costumerLogin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="registration")
        return dict(list(context.items()) + list(mixin.items()))


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'fond/login.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="login")
        return dict(list(context.items()) + list(mixin.items()))


@login_required
def costumerLogout(request):
    logout(request)
    messages.error(request, "success log out")
    return redirect("/")
