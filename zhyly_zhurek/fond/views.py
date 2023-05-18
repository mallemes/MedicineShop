from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView

from fond.forms import RegisterForm
from fond.models import Category, Patient, Fond, MyUser, Comment
from fond.utils import DataMixin


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>page not found</h1>')


class ElectronicaShowView(DataMixin, ListView):
    model = Patient
    template_name = "fond/all_cats.html"
    context_object_name = "patients"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title='patients')
        return dict(list(context.items()) + list(mixin.items()))


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

    def post(self, request, **kwargs):
        my_bln = request.POST.get("balance")
        if my_bln:
            request.user.balance = my_bln
            request.user.save()
        return redirect('profile')


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


class CategoryView(DataMixin, DetailView):
    model = Category
    template_name = "fond/detail_cat.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        activ = self.data()
        context['page_obj'] = activ
        mixin = self.get_user_context(title="category")
        return dict(list(context.items()) + list(mixin.items()))

    def data(self):
        queryset = self.object.patient_set.all()
        paginator = Paginator(queryset, 3)
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


class SingleElectronicaView(DataMixin, DetailView):
    model = Patient
    template_name = "fond/single_patient.html"
    context_object_name = "patient"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="patient")
        return dict(list(context.items()) + list(mixin.items()))

    def post(self, request, **kwargs):
        comment = request.POST.get("comment", None)
        my_data = request.POST
        user = request.user
        pat = Patient.objects.get(pk=my_data.get("patient_id", None))
        if comment:
            com = Comment()
            com.patient = pat
            com.user = user
            com.message = comment
            com.save()
        if not my_data.get("money"):
            messages.error(request, "qarazhat engiz.")
            return redirect(pat.get_absolute_url())
        if user.balance < int(my_data.get("money")):
            messages.error(request, "qarazhatynyz zhetkiliksiz.")
            return redirect('profile')

        fond = Fond.objects.filter(user=user, patient=pat)
        if not fond:
            user.balance = user.balance - int(my_data.get("money"))
            user.save()
            ff = Fond(user=user, patient=pat)
            ff.save()
        pat.jinalgany = pat.jinalgany + int(my_data.get("money"))
        pat.save()
        return redirect(pat.get_absolute_url())
