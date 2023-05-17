from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse


# class MyUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = models.ImageField(null=True, blank=True, upload_to="user/avatars/")
#     balance = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     patients = models.ManyToManyField(User, through="Fond")
#
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             profile, created = MyUser.objects.get_or_create(user=instance)
#
#     post_save.connect(create_user_profile, sender=User)
#
#     def __str__(self):
#         return self.user

class MyUser(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, upload_to="user/avatars/")
    balance = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, null=True, blank=True)
    poster = models.ImageField(null=True, blank=True, upload_to="category/photos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Patient(models.Model):
    fullName = models.CharField(max_length=250)
    photo = models.ImageField(null=True, blank=True, upload_to="patient/photos/")
    description = models.TextField()
    address = models.CharField(max_length=250)
    moneySum = models.IntegerField(default=579000)
    jinalgany = models.IntegerField(default=123870)
    age = models.IntegerField(null=True, blank=True)
    disease = models.CharField(max_length=250)  # болезнь
    isInvalid = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(MyUser, through="Fond")

    def get_absolute_url(self):
        return reverse('single_patient', kwargs={"cat_slug": self.category.slug, "pk": self.pk})

    def __str__(self):
        return self.fullName


class Fond(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
